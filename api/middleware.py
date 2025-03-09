from rest_framework import status
from rest_framework.response import Response
from itsdangerous import SignatureExpired, BadSignature, URLSafeSerializer

Secret_key = "I am a good boy"
class MiddleWare:
    def fetchuser(self,request):
        token = request.headers.get('auth-token')
        serializer = URLSafeSerializer(Secret_key, salt="activate")
        try:
            data = serializer.loads(token)
            print(data)
        except SignatureExpired:
            return Response({"detail": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except BadSignature:
            return Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"detail":True})