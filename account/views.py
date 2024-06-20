"""
views for the accounts
 """
from rest_framework.views import APIView
from rest_framework import status
from account.models import User
from rest_framework.response import Response
from account.authentication import JWTAuthentication
from account.serializers import UserLoginSerializer
from rest_framework import permissions
from django.http import HttpResponseRedirect


class LogInApiView(APIView):
    """loging users with jwt"""
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        """loging in user"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        username = serializer.data['username']
        password = serializer.data['password']

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token = JWTAuthentication.create_jwt(user)
        response = HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/events/user')
        response.set_cookie(key='jwt_token', value=token, httponly=True)
        response.data = {
            'jwt_token': token
        }

        return response

# class LogInApiView(APIView):
#     """loging users with jwt"""
#     serializer_class = UserLoginSerializer
#
#     def post(self, request):
#         """do users authorization"""
#         username = request.data['username']
#         password = request.data['password']
#
#         user = User.objects.filter(username=username).first()
#         if user is None:
#             raise AuthenticationFailed('user not found')
#
#         if not user.check_password(password):
#             raise AuthenticationFailed('incorrect password')
#
#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()
#         }
#
#         token = jwt.encode(payload, 'secret', algorithm='HS256')
#
#         response = Response()
#         response.set_cookie(key='jwt', value=token, httponly=True)
#         response.data = {
#             'jwt': token
#         }
#         return response





