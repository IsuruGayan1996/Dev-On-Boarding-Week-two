import unittest
from app import app
import json
import datetime


class TestAPI(unittest.TestCase):
    def test_get_users(self):
        with app.test_client() as client:
            response = client.get('/users')
            # Test that the function returns a 200 status code when the request is successful.
            self.assertEqual(response.status_code, 200)
            # Test length of the function returns a JSON object.
            self.assertEqual(len(response.json), 1)
            # Test that the function returns a JSON object with a key of users.
            self.assertIn('users', response.get_json())
            # Test that the function returns a JSON object with a key of users and a value of a list.
            self.assertIsInstance(response.get_json()['users'], list)
            print("Test 1 completed")

    def test_get_user(self):
        with app.test_client() as client:
            response1 = client.get('/users/16')
            # Test that the function returns a 200 status code when the request is successful.
            self.assertEqual(response1.status_code, 200)
            # Test that the function returns a JSON object with a key of user.
            self.assertIn('user', response1.get_json())
            # Test that the correct content type header is returned with the response
            self.assertEqual(response1.headers['Content-Type'], 'application/json')

            response2 = client.get('/users/1')
            # Test that the function returns a 404 status code when the request is unsuccessful.
            self.assertEqual(response2.status_code, 404)
            print("Test 2 completed")

    def test_add_user(self):
        with app.test_client() as client:
            response1 = client.post('/users',
                                    json={'user_name': 'example_user10', 'email': "johndoe@example.com",
                                          'password': "12345"})
            # Test that the function returns a 201 status code when the request is successful
            # self.assertEqual(response1.status_code, 201)
            # Test if user_name already exists return a 400.
            self.assertEqual(response1.status_code, 400)
            # Test that the correct content type header is returned with the response
            self.assertEqual(response1.headers['Content-Type'], 'application/json')

            response2 = client.post('/users',
                                    json={'user_name': 'example23', 'email': "johndoe@example.com", 'password': ""})
            # Test that an error message is returned with a 400 status code when a required field is empty.
            self.assertEqual(response2.status_code, 400)

            response3 = client.post('/users', data="notjson")
            # Test that an error message is returned with a 400 status code when the request is not JSON.
            self.assertEqual(response3.status_code, 415)

            print("Test 3 completed")

    def test_update_user(self):
        with app.test_client() as client:
            # response1 = client.put('/users/28', json={'user_name': 'example234', 'email': "johndoe@example.com",
            #                                           'password': "12345"})
            # Test that the function returns a 200 status code when the request is successful.
            # self.assertEqual(response1.status_code, 200)
            # Test that the correct content type header is returned with the response
            # self.assertEqual(response1.headers['Content-Type'], 'application/json')

            response2 = client.put('/users/280', json={'user_name': 'example234', 'email': "johndoe@example.com",
                                                       'password': "12345"})
            # Test that the function returns a 404 status code when the request is user not exists.
            self.assertEqual(response2.status_code, 404)

            # response3 = client.put('/users/28', json={'user_name': '', 'email': "johndoe@example.com",
            #                                            'password': "12345"})
            # # Test that the function returns a 200 status code when the request is successful.
            # self.assertEqual(response3.status_code, 400)

            response4 = client.put('/users/28', data="notjson")
            # Test that an error message is returned with a 400 status code when the request is not JSON.
            self.assertEqual(response4.status_code, 415)

            print("Test 4 completed")

    def test_delete_user(self):
        with app.test_client() as client:
            response1 = client.delete('/users/31')
            # Test that the function returns a 200 status code when the request is successful.
            # self.assertEqual(response1.status_code, 200)

            response2 = client.delete('/users/31')
            # Test that the function returns a 404 status code when the request is user not exists.
            self.assertEqual(response2.status_code, 404)

            print("Test 5 completed")

    def test_login(self):
        with app.test_client() as client:
            response1 = client.post('/login', json={'user_name': 'example_user1',
                                                    'password': "12345"})
            # Test that the function returns a 200 status code when the request is successful.
            self.assertEqual(response1.status_code, 200)

            response2 = client.post('/login', json={'user_name': 'example_user1',
                                                    'password': "123456"})
            # Test that the function returns a 401 status code when the username or password invalid.
            self.assertEqual(response2.status_code, 401)

            # Test that the access token and refresh token have the correct expiration time
            response2 = client.post('/login', json={'user_name': 'example_user1',
                                                    'password': "12345"})
            response_data = json.loads(response2.get_data())
            access_expire = datetime.datetime.strptime(response_data['access_expire'], '%a, %d %b %Y %H:%M:%S %Z')
            refresh_expire = datetime.datetime.strptime(response_data['refresh_expire'], '%a, %d %b %Y %H:%M:%S %Z')
            # print(access_expire, refresh_expire)

            access_expected_expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
            refresh_expected_expire = datetime.datetime.utcnow() + datetime.timedelta(days=7)

            # print(access_expected_expire, refresh_expected_expire)
            self.assertAlmostEqual(access_expire, access_expected_expire, delta=datetime.timedelta(seconds=1))
            self.assertAlmostEqual(refresh_expire, refresh_expected_expire, delta=datetime.timedelta(seconds=1))

            print("Test 6 completed")


if __name__ == "__main__":
    tester = TestAPI()
