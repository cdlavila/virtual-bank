import unittest
from accounts.utils.hasher import hash_password, verify_password
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestHashPassword(unittest.TestCase):
    #  Verify correct password returns True
    def test_correct_password_returns_true(self):
        password = "password123"
        hashed_password = hash_password(password)
        result = pwd_context.verify(password, hashed_password)
        self.assertTrue(result)

    #  Verify incorrect password returns False
    def test_incorrect_password_returns_false(self):
        password = "password123"
        incorrect_password = "wrongpassword"
        hashed_password = hash_password(password)
        result = pwd_context.verify(incorrect_password, hashed_password)
        self.assertFalse(result)


class TestVerifyPassword(unittest.TestCase):
    #  Verify correct password returns True
    def test_correct_password_returns_true(self):
        password = "password123"
        hashed_password = pwd_context.hash(password)
        result = verify_password(password, hashed_password)
        self.assertTrue(result)

    #  Verify incorrect password returns False
    def test_incorrect_password_returns_false(self):
        password = "password123"
        incorrect_password = "wrongpassword"
        hashed_password = pwd_context.hash(password)
        result = verify_password(incorrect_password, hashed_password)
        self.assertFalse(result)
