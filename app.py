# Import necessary modules
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import jwt
import datetime
from datetime import date
from functools import wraps
import os
from tenacity import retry, stop_after_attempt, wait_fixed
import aiomysql

# Initialize Flask application
app = Flask(__name__)

# Set a secret key for your Flask app
app.config['SECRET_KEY'] = 'thisissecretkey'

# Database configuration
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "toweek2one"
MYSQL_PORT = 3306


# Function to create database connection pool
@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def create_pool():
    pool = await aiomysql.create_pool(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        autocommit=True
    )
    return pool


def token_required(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return jsonify({"error": "Token is missing"}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = await check_user_exist(id=data["user_id"])
        except:
            return jsonify({"error": "Token is invalid"}), 401
        return await f(current_user, *args, **kwargs)

    return decorated_function


# Get All Users
@app.get('/users')
async def get_users():
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM users")
            users = await cur.fetchall()
            return jsonify({'users': users}), 200


# Get User using Id
@app.get('/users/<int:user_id>')
async def get_user(user_id):
    user = await check_user_exist(id=user_id)
    if user:
        return jsonify({"user": user}), 200
    else:
        return jsonify({"Error": "User not exists"}), 404


# Add User
@app.post('/users')
async def add_user():
    if request.is_json:
        user = request.get_json()
        if user['user_name'] == '' or user['email'] == '' or user['password'] == '':
            return {"error": "Feild is empty"}, 400
        if await check_user_exist(name=user["user_name"]) is not None:
            return {"error": "User already exists"}, 400
        pool = await create_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                user["password"] = generate_password_hash(user["password"], method="sha256")
                await cur.execute("INSERT INTO users (user_name, email, password) VALUES (%s, %s, %s)",
                                  (user["user_name"], user["email"], user["password"]))
                last_insert_id = cur.lastrowid
                return jsonify({'message': 'User created successfully!', 'last_insert_id': last_insert_id}), 201
    return {"error": "Request must be JSON"}, 415


# Check if user exists and return user
async def check_user_exist(id="", name=""):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            if id == "":
                await cur.execute("SELECT * FROM users WHERE user_name = %s", (name,))
            else:
                await cur.execute("SELECT * FROM users WHERE user_id = %s", (id,))
            user = await cur.fetchone()
            return user;


# Update User
@app.put('/users/<int:user_id>')
async def update_user(user_id):
    if await check_user_exist(id=user_id) is None:
        return {"error": "User not found"}, 404
    else:
        if request.is_json:
            update_user = request.get_json()
            update_user["password"] = generate_password_hash(update_user["password"], method="sha256")
            if update_user['user_name'] == '' or update_user['email'] == '' or update_user['password'] == '':
                return {"error": "Feild is empty"}, 400
            else:
                pool = await create_pool()
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("UPDATE users SET user_name=%s, email=%s, password=%s WHERE user_id=%s",
                                          (update_user['user_name'], update_user['email'], update_user['password'],
                                           user_id))
                        return {"message": "User updated successfully!"}, 200
        else:
            return {"error": "Request must be JSON"}, 415


# Delete User
@app.delete('/users/<int:user_id>')
async def delete_user(user_id):
    if await check_user_exist(id=user_id) is None:
        return {"error": "User not found"}, 404
    else:
        pool = await create_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                return jsonify({'message': 'User deleted successfully!'}), 200


# Obtain token access and refresh pairs endpoint
@app.post('/login')
async def login():
    user_name = request.json['user_name']
    password = request.json['password']
    user = await check_user_exist(name=user_name)
    if not user or not check_password_hash(user[3], password):
        return jsonify({'error': 'Invalid username or password.'}), 401
    access_token = jwt.encode({'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                              app.config['SECRET_KEY'],
                              algorithm='HS256')
    refresh_token = jwt.encode({'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)},
                               app.config['SECRET_KEY'], algorithm='HS256')
    access_expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    refresh_expire = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute('INSERT INTO refresh_tokens (user_id, refresh_token) VALUES (%s, %s)',
                              (user[0], refresh_token))
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'access_expire': access_expire,
                    'refresh_expire': refresh_expire}), 200


# Obtain new access token from refresh token endpoint
@app.route('/refresh', methods=['POST'])
async def refresh():
    refresh_token = request.json['refresh_token']
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute('SELECT * FROM refresh_tokens WHERE refresh_token = %s', (refresh_token,))
            token = await cur.fetchone()
    if not token:
        return jsonify({'error': 'Invalid refresh token.'}), 401
    try:
        jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Refresh token has expired.'}), 401
    access_token = jwt.encode({'user_id': token[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                              app.config['SECRET_KEY'],
                              algorithm='HS256')
    refresh_token = jwt.encode({'user_id': token[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)},
                               app.config['SECRET_KEY'], algorithm='HS256')
    access_expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    refresh_expire = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'access_expire': access_expire,
                    'refresh_expire': refresh_expire}), 200


# Add pin
@app.post('/pins')
@token_required
async def add_pin(current_user):
    title = request.form['title']
    body = request.form['body']
    f = request.files.get('image')
    if title == '' or body == '' or f is None:
        return jsonify({'error': 'Field is empty'}), 400
    filename = secure_filename(f.filename)
    f.save(filename)
    image = filename
    added_date = date.today().strftime("%Y-%m-%d")
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO pins (title, body, image, user_id, added_date) VALUES (%s, %s, %s, %s, %s)",
                              (title, body, image, current_user[0], added_date))
            last_insert_id = cur.lastrowid
            return jsonify({'message': 'Pin created successfully!', 'last_insert_id': last_insert_id}), 201


# Get All pins
@app.get('/pins')
async def get_pins():
    created_by = request.args.get('created_by')
    order_by_field = request.args.get('order_by_field')
    order_by = request.args.get('order_by')
    if created_by:
        user = await check_user_exist(name=created_by)
        user_id = user[0]
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            query = "SELECT * FROM pins"
            params = []
            if created_by:
                query += " WHERE user_id = %s"
                params.append(user_id)
            if order_by_field and order_by:
                query += f" ORDER BY {order_by_field} {order_by}"
            await cur.execute(query, params)
            pins = await cur.fetchall()
            return jsonify({'pins': pins}), 200


# Get Pin By ID
@app.get('/pins/<int:pin_id>')
async def get_pin(pin_id):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM pins where pin_id =%s", (pin_id,))
            pin = await cur.fetchone()
            return jsonify({'pin': pin}), 200


# Check if pin exists and return pin
async def check_pin_exists(user_id, pin_id):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM pins where pin_id =%s and user_id =%s", (pin_id, user_id))
            pin = await cur.fetchone()
            return pin


# Update pin
@app.put('/pins/<int:pin_id>')
@token_required
async def update_pin(current_user, pin_id):
    if await check_pin_exists(current_user[0], pin_id) is None:
        return {"error": "Pin not found"}, 404
    title = request.form['title']
    body = request.form['body']
    f = request.files.get('image')
    filename = secure_filename(f.filename)
    image = filename
    old_pin = await check_pin_exists(current_user[0], pin_id)
    old_image = old_pin[3]
    if old_image != image and image != "":
        os.remove(old_image)
        f.save(image)
    added_date = date.today().strftime("%Y-%m-%d")
    update_title = old_pin[1] if title == "" else title
    update_body = old_pin[2] if body == "" else body
    update_image = old_pin[3] if image == "" else image

    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE pins SET title=%s, body=%s, image=%s, added_date=%s WHERE pin_id=%s and user_id=%s",
                (update_title, update_body, update_image, added_date, pin_id, current_user[0]))
            updated_pin = await check_pin_exists(current_user[0], pin_id)
            return jsonify({'message': 'Pin updated successfully!', "Updated Pin": updated_pin}), 200


# Delete Pin
@app.delete('/pins/<int:pin_id>')
@token_required
async def delete_pin(current_user, pin_id):
    if await check_pin_exists(current_user[0], pin_id) is None:
        return {"error": "Pin not found"}, 404
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM pins WHERE pin_id = %s and user_id = %s", (pin_id, current_user[0]))
            return jsonify({'message': 'Pin deleted successfully!'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8001)
