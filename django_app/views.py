from rest_framework.views import APIView
from rest_framework.response import Response


class ServerWelcomeView(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to the banking server'})


class APIWelcomeView(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to the banking API'})
