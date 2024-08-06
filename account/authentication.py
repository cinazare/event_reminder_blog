"""
custom jwt authorization
"""
import datetime
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError
User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    """authentication class with jwt"""

    def authenticate(self, request):
        """extract the jwt from the authorization header"""
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None
        
        jwt_token = jwt_token.split()[1]

        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('invalid signature')
        except:
            raise ParseError()

        user_id = payload.get('id')
        if user_id is None:
            raise AuthenticationFailed('user has not been found in jwt')

        user = User.objects.filter(id=user_id).first()

        if user is None:
            raise AuthenticationFailed('user not found')

        return user, payload
    

    def authenticate_header(self, request):
        return 'bearer'


    @classmethod
    def create_access(cls, refresh):
        """create access token with refresh token"""
        
        try:
            payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('invalid signature')
        except:
            raise ParseError()
        
        

        user_id = payload.get('id')
        if user_id is None:
            AuthenticationFailed('user has not been found in token')

        
        payload = {
            'id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.now().timestamp(),
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token


    @classmethod
    def create_refresh(cls, id):
        """create refresh token with id"""
        payload = {
            'id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now().timestamp(),
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token


    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')
        return token


