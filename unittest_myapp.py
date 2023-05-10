import unittest
from app import app
import json
import datetime
import time


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
            response1 = client.put('/users/16', json={'user_name': 'example234', 'email': "johndoe@example.com",
                                                      'password': "12345"})
            # Test that the function returns a 200 status code when the request is successful.
            self.assertEqual(response1.status_code, 200)
            # Test that the correct content type header is returned with the response
            self.assertEqual(response1.headers['Content-Type'], 'application/json')

            response2 = client.put('/users/280', json={'user_name': 'example234', 'email': "johndoe@example.com",
                                                       'password': "12345"})
            # Test that the function returns a 404 status code when the request is user not exists.
            self.assertEqual(response2.status_code, 404)

            response3 = client.put('/users/16', json={'user_name': '', 'email': "johndoe@example.com",
                                                      'password': "12345"})
            # Test that the function returns a 200 status code when the request is successful.
            self.assertEqual(response3.status_code, 400)

            response4 = client.put('/users/16', data="notjson")
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
            response1 = client.post('/login', json={'user_name': 'example_user2',
                                                    'password': "12345"})
            # Test that the function returns a 200 status code when the request is successful.
            self.assertEqual(response1.status_code, 200)

            response2 = client.post('/login', json={'user_name': 'example_user2',
                                                    'password': "123456"})
            # Test that the function returns a 401 status code when the username or password invalid.
            self.assertEqual(response2.status_code, 401)

            # Test that the access token and refresh token have the correct expiration time
            response2 = client.post('/login', json={'user_name': 'example_user2',
                                                    'password': "12345"})
            response_data = json.loads(response2.get_data())

            access_expire = response_data['access_expire']
            refresh_expire = response_data['refresh_expire']
            access_expected_expire = int(time.time()) + 3600
            refresh_expected_expire = int(time.time()) + 604800

            # Convert access_expire,refresh_expire to a datetime object
            access_expire_datetime = datetime.datetime.strptime(access_expire, '%a, %d %b %Y %H:%M:%S %Z')
            refresh_expire_datetime = datetime.datetime.strptime(refresh_expire, '%a, %d %b %Y %H:%M:%S %Z')

            # Convert access_expire_datetime,refresh_expire_datetime to a Unix timestamp
            access_expire_timestamp = int(access_expire_datetime.timestamp())
            refresh_expire_timestamp = int(refresh_expire_datetime.timestamp())

            assert access_expire_timestamp == access_expected_expire
            assert refresh_expire_timestamp == refresh_expected_expire

            # print(access_expected_expire, refresh_expected_expire)
            self.assertEqual(access_expire_timestamp, access_expected_expire)
            self.assertEqual(refresh_expire_timestamp, refresh_expected_expire)

            print("Test 6 completed")

    def test_refresh(self):
        with app.test_client() as client:
            # Test that a new access token is generated when a valid refresh token is provided
            response1 = client.post('/refresh', json={
                'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNSwiZXhwIjoxNjg0MzUxMzk3fQ.BSQSE3u8Rrpm_9B8KouVpVZA0TxY19BKHoXuqXcfO1I'})
            self.assertEqual(response1.status_code, 200)

            # Test that the new access token and refresh token have the correct expiration time
            response_data = json.loads(response1.get_data())
            access_expire = response_data['access_expire']
            refresh_expire = response_data['refresh_expire']
            access_expected_expire = int(time.time()) + 3600
            refresh_expected_expire = int(time.time()) + 604800

            # Convert access_expire,refresh_expire to a datetime object
            access_expire_datetime = datetime.datetime.strptime(access_expire, '%a, %d %b %Y %H:%M:%S %Z')
            refresh_expire_datetime = datetime.datetime.strptime(refresh_expire, '%a, %d %b %Y %H:%M:%S %Z')

            # Convert access_expire_datetime,refresh_expire_datetime to a Unix timestamp
            access_expire_timestamp = int(access_expire_datetime.timestamp())
            refresh_expire_timestamp = int(refresh_expire_datetime.timestamp())

            assert access_expire_timestamp == access_expected_expire
            assert refresh_expire_timestamp == refresh_expected_expire

            # print(access_expected_expire, refresh_expected_expire)
            self.assertEqual(access_expire_timestamp, access_expected_expire)
            self.assertEqual(refresh_expire_timestamp, refresh_expected_expire)

            # Test that an error message is returned when an invalid refresh token is provided or the refresh token has expired
            response2 = client.post('/refresh', json={
                'refresh_token': 'yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNjgzMTAzMjMzfQ.vqqhJzwYUTqWglZFZoUh_SjfvDPuX1L0izm321O9fBM'})
            self.assertEqual(response2.status_code, 401)

            print("Test 7 completed")

    def test_add_pin(self):
        with app.test_client() as client:
            # Test that the function returns a 201 status code when the request is successful.
            # login_payload = {'user_name': 'example_user1', 'password': '12345'}
            # login_response = client.post('/login', json=login_payload)
            # token = json.loads(login_response.data.decode('utf-8'))['access_token']
            #
            # data = {
            #     'title': 'test title',
            #     'body': 'test body'
            # }
            # with open('testing_image1.png', 'rb') as f:
            #     files = {
            #         'image': f
            #     }
            #     headers = {
            #         'Authorization': token
            #     }
            #     response = client.post('/pins', data=data, files=files,
            #                            headers=headers,
            #                            content_type='multipart/form-data')
            #     self.assertEqual(response.status_code, 201)

            # Test that an error message is returned with a 400 status code when the request attributes is empty.
            login_payload = {'user_name': 'example_user1', 'password': '12345'}
            login_response = client.post('/login', json=login_payload)
            token = json.loads(login_response.data.decode('utf-8'))['access_token']

            data = {
                'title': 'test title',
                'body': 'test body'
            }
            headers = {
                'Authorization': token
            }
            response = client.post('/pins', data=data,
                                   headers=headers,
                                   content_type='multipart/form-data')
            self.assertEqual(response.status_code, 400)

            print("Test 8 completed")

    def test_get_pins(self):
        with app.test_client() as client:
            # Test that the endpoint returns all pins when no query parameters are provided.
            response = client.get('/pins')
            self.assertEqual(response.status_code, 200)

            # Test that the endpoint returns the correct pins when a "created_by" query parameter is provided.
            response = client.get('/pins?created_by=example_user2')
            self.assertEqual(response.status_code, 200)
            #
            # Test that the endpoint returns the pins in the correct order when "order_by_field" and "order_by" query parameters are provided.
            response = client.get('/pins?order_by_field=added_date&order_by=desc')
            self.assertEqual(response.status_code, 200)

            print("Test 9 completed")

    def test_get_pin(self):
        with app.test_client() as client:
            # Test that the endpoint returns the correct pin when a valid pin_id is provided.
            response = client.get('/pins/37')
            self.assertEqual(response.status_code, 200)

            # Test that the endpoint returns an error message when an invalid pin_id is provided.
            response = client.get('/pins/100')
            self.assertEqual(response.status_code, 404)

            print("Test 10 completed")

    def test_update_pin(self):
        with app.test_client() as client:
            # Test that the endpoint returns a 400 status code when the request pin is not exists.
            login_payload = {'user_name': 'example234', 'password': '12345'}
            login_response = client.post('/login', json=login_payload)
            token = json.loads(login_response.data.decode('utf-8'))['access_token']

            # print(token)
            data = {
                'title': 'test title',
                'body': 'test body'
            }
            headers = {
                'Authorization': token
            }
            response = client.put('/pins/32', data=data,
                                  headers=headers,
                                  content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)

            response = client.put('/pins/320', data=data,
                                  headers=headers,
                                  content_type='multipart/form-data')
            self.assertEqual(response.status_code, 404)

            print("Test 11 completed")

    def test_delete_pin(self):
        with app.test_client() as client:
            # Test that the endpoint returns a 200 status code when the request is successful.
            login_payload = {'user_name': 'example234', 'password': '12345'}
            login_response = client.post('/login', json=login_payload)
            token = json.loads(login_response.data.decode('utf-8'))['access_token']

            # response = client.delete('/pins/36', headers={'Authorization': token})
            # self.assertEqual(response.status_code, 200)

            # Test that the endpoint returns a 404 status code when the request pin is not exists.
            response = client.delete('/pins/36', headers={'Authorization': token})
            self.assertEqual(response.status_code, 404)

            print("Test 12 completed")


if __name__ == "__main__":
    tester = TestAPI()
