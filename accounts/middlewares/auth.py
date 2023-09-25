from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from accounts.utils import jwt


def check_authentication(func):
    @wraps(func)  # This is used to preserve the original function's metadata
    def wrapper(self, request, *args, **kwargs):
        authorization_header = request.META.get('HTTP_AUTHORIZATION', None)
        if not authorization_header:
            return Response({'error': 'Authorization header not found'}, status=status.HTTP_401_UNAUTHORIZED)

        bearer = authorization_header.split(' ')[0]
        if not bearer:
            return Response({'error': 'Token structure is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        token = authorization_header.split(' ')[1]

        try:
            payload = jwt.verify_token(token)
        except Exception:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        request.user = payload
        return func(self, request, *args, **kwargs)

    return wrapper
