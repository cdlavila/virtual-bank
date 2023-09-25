import os
import unittest
from unittest import mock
from accounts.utils.jwt import create_token, verify_token
from jwt import encode, decode


class TestCreateToken(unittest.TestCase):
    #  Returns a JWT token for valid input data
    @mock.patch.dict(os.environ, {'JWT_SECRET_KEY': 'dummy_secret_key'})
    def test_returns_jwt_token_for_valid_input_data(self):
        # Define the input data
        data = {'user_id': 12345}

        # Call the create_token function
        token = create_token(data=data)

        # Assert that the token is not None
        self.assertIsNotNone(token)

        # Assert that the token is a string
        self.assertIsInstance(token, str)

        # Assert that the token is a valid JWT token by decoding it
        decoded_token = decode(token, 'dummy_secret_key', algorithms=['HS256'])
        self.assertEqual(decoded_token['user_id'], 12345)


class TestVerifyToken(unittest.TestCase):
    #  Verify a valid token with a valid JWT_SECRET_KEY
    @mock.patch.dict(os.environ, {'JWT_SECRET_KEY': 'dummy_secret_key'})
    def test_valid_token_with_valid_key(self):
        # Define the input data
        data = {'user_id': 12345}

        # Call the create_token function
        token = encode(payload=data, key='dummy_secret_key', algorithm='HS256')

        # Call the verify_token function
        decoded_token = verify_token(token=token)

        # Assert that the decoded token is not None
        self.assertIsNotNone(decoded_token)

        # Assert that the decoded token is a dictionary
        self.assertIsInstance(decoded_token, dict)

        # Assert that the decoded token has the correct user_id
        self.assertEqual(decoded_token['user_id'], 12345)
