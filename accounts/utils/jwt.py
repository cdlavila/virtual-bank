from jwt import encode, decode
import os
from dotenv import load_dotenv


def create_token(data):
    return encode(payload=data, key=os.getenv('JWT_SECRET_KEY'), algorithm='HS256')


def verify_token(token):
    return decode(jwt=token, key=os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
