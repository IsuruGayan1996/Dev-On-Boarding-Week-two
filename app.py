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
from flask_cors import CORS
import time
from datetime import datetime
from decouple import config
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Set a secret key for your Flask app
app.config["SECRET_KEY"] = config("SECRET_KEY")

# Database configuration
MYSQL_HOST = config("MYSQL_HOST")
MYSQL_USER = config("MYSQL_USER")
MYSQL_PASSWORD = config("MYSQL_PASSWORD")
MYSQL_DB = config("MYSQL_DB")
MYSQL_PORT = config("MYSQL_PORT", cast=int)


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
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = await check_user_exist(id=data["user_id"])
        except:
            return jsonify({"error": "Token is invalid"}), 401
        return await f(current_user, *args, **kwargs)

    return decorated_function


# Get All Users
@app.get("/users")
async def get_users():
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT user_id, user_name, email FROM users")
            users = await cur.fetchall()
            await cur.close()
            pool.close()
            users_dict_list = [dict(zip(("user_id", "user_name", "email", "password"), row)) for row in users]
            return {"users": users_dict_list}, 200


# Get User using Id
@app.get("/users/<int:user_id>")
async def get_user(user_id):
    user = await check_user_exist(id=user_id)
    if user:
        user_dict = dict(zip(("user_id", "user_name", "email"), user))
        return {"user": user_dict}, 200
    else:
        return jsonify({"Error": "User not exists"}), 404


# Add User
@app.post("/users")
async def add_user():
    if request.is_json:
        user = request.get_json()
        required_fields = ["user_name", "email", "password"]
        for field in required_fields:
            if field not in user:
                return {"error": f"{field} field is required"}, 400
            elif not user.get(field):
                return {"error": f"{field} field is empty"}, 400
        if await check_user_exist(name=user["user_name"]):
            return {"error": "User already exists"}, 400
        pool = await create_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                user["password"] = generate_password_hash(user["password"], method="sha256")
                await cur.execute("INSERT INTO users (user_name, email, password) VALUES (%s, %s, %s)",
                                  (user["user_name"], user["email"], user["password"]))
                last_insert_id = cur.lastrowid
                await cur.close()
                pool.close()
                return jsonify({"message": "User created successfully!", "last_insert_id": last_insert_id}), 201
    return {"error": "Request must be JSON"}, 415


# Check if user exists and return user
async def check_user_exist(id=None, name=None):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            if not id:
                await cur.execute("SELECT * FROM users WHERE user_name = %s", (name,))
            else:
                await cur.execute("SELECT user_id, user_name, email FROM users WHERE user_id = %s", (id,))
            user = await cur.fetchone()
            await cur.close()
            pool.close()
            return user


# Update User
@app.put("/users/<int:user_id>")
async def update_user(user_id):
    if not await check_user_exist(id=user_id):
        return {"error": "User not found"}, 404
    else:
        if request.is_json:
            update_user = request.get_json()
            required_fields = ["user_name", "email", "password"]
            for field in required_fields:
                if field not in update_user:
                    return {"error": f"{field} field is required"}, 400
                elif not update_user.get(field):
                    return {"error": f"{field} field is empty"}, 400
            else:
                pool = await create_pool()
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("UPDATE users SET user_name=%s, email=%s, password=%s WHERE user_id=%s",
                                          (update_user["user_name"], update_user["email"], update_user["password"],
                                           user_id))
                        await cur.close()
                        pool.close()
                        return {"message": "User updated successfully!"}, 200
        else:
            return {"error": "Request must be JSON"}, 415


# Delete User
@app.delete("/users/<int:user_id>")
async def delete_user(user_id):
    if not await check_user_exist(id=user_id):
        return {"error": "User not found"}, 404
    else:
        pool = await create_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                await cur.close()
                pool.close()
                return jsonify({"message": "User deleted successfully!"}), 200


# Obtain token access and refresh pairs endpoint
@app.post("/login")
async def login():
    user_name = request.json["user_name"]
    password = request.json["password"]
    user = await check_user_exist(name=user_name)
    user_dict = dict(zip(("user_id", "user_name", "email", "password"), user))
    if not user or not check_password_hash(user_dict["password"], password):
        return jsonify({"error": "Invalid username or password."}), 401
    return create_and_return_token(user_dict["user_id"])


# Obtain new access token from refresh token endpoint
@app.post("/refresh")
async def refresh():
    refresh_token = request.json["refresh_token"]
    try:
        token_payload = jwt.decode(refresh_token, app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token has expired."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid refresh token."}), 401
    return create_and_return_token(token_payload["user_id"])


def create_and_return_token(user_id):
    access_expire = int(time.time()) + 3600
    refresh_expire = int(time.time()) + 604800
    access_token = jwt.encode({"user_id": user_id, "exp": access_expire},
                              app.config["SECRET_KEY"],
                              algorithm="HS256")
    refresh_token = jwt.encode({"user_id": user_id, "exp": refresh_expire},
                               app.config["SECRET_KEY"], algorithm="HS256")
    return jsonify({"access_token": access_token, "refresh_token": refresh_token,
                    "access_expire": datetime.fromtimestamp(access_expire),
                    "refresh_expire": datetime.fromtimestamp(refresh_expire)}), 200


# Add pin
@app.post("/pins")
@token_required
async def add_pin(current_user):
    required_fields = {"title": request.form.get("title"), "body": request.form.get("body"),
                       "image": request.files.get("image")}
    for field, value in required_fields.items():
        if not value:
            return jsonify({"error": f"{field} is required."}), 400
    filename = secure_filename(required_fields["image"].filename)
    required_fields["image"].save(filename)
    image = filename
    added_date = date.today().strftime("%Y-%m-%d")
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO pins (title, body, image, user_id, added_date) VALUES (%s, %s, %s, %s, %s)",
                              (required_fields["title"], required_fields["body"], image, current_user[0], added_date))
            last_insert_id = cur.lastrowid
            await cur.close()
            pool.close()
            return jsonify({"message": "Pin created successfully!", "last_insert_id": last_insert_id}), 201


# Get All pins
@app.get("/pins")
async def get_pins():
    created_by = request.args.get("created_by")
    order_by_field = request.args.get("order_by_field")
    order_by = request.args.get("order_by")
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
            await cur.close()
            pool.close()
            pins_dict_list = [dict(zip(("pin_id", "title", "body", "image", "user_id", "added_date"), row)) for row in
                              pins]
            return jsonify({"pins": pins_dict_list}), 200


# Get Pin By ID
@app.get("/pins/<int:pin_id>")
async def get_pin(pin_id):
    pin = await check_pin_exists(pin_id=pin_id)
    if not pin:
        return jsonify({"error": "Pin does not exist"}), 404
    pin_dict = dict(zip(("pin_id", "title", "body", "image", "user_id", "added_date"), pin))
    return jsonify({"pin": pin_dict}), 200


# Check if pin exists and return pin
async def check_pin_exists(user_id=None, pin_id=None):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            if not user_id:
                await cur.execute("SELECT * FROM pins where pin_id =%s", (pin_id))
            else:
                await cur.execute("SELECT * FROM pins where pin_id =%s and user_id =%s", (pin_id, user_id))
            pin = await cur.fetchone()
            await cur.close()
            pool.close()
            return pin


# Update pin
@app.put("/pins/<int:pin_id>")
@token_required
async def update_pin(current_user, pin_id):
    if not await check_pin_exists(user_id=current_user[0], pin_id=pin_id):
        return {"error": "Pin not found"}, 404
    title = request.form["title"]
    body = request.form["body"]
    f = request.files.get("image")
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
            await cur.close()
            pool.close()
            pin_dict = dict(zip(("pin_id", "title", "body", "image", "user_id", "added_date"), updated_pin))
            return jsonify({"message": "Pin updated successfully!", "Updated Pin": pin_dict}), 200


# Delete Pin
@app.delete("/pins/<int:pin_id>")
@token_required
async def delete_pin(current_user, pin_id):
    if not await check_pin_exists(current_user[0], pin_id):
        return {"error": "Pin not found"}, 404
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM pins WHERE pin_id = %s and user_id = %s", (pin_id, current_user[0]))
            return jsonify({"message": "Pin deleted successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=8001)
