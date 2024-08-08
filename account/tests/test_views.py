from django.test import TestCase, Client
from django.urls import reverse
from account.models import User
from rest_framework import status
from account.views import LoginApiView 
import jwt
from account.authentication import ALGORITHM
from django.conf import settings



def jwt_parse(token):
    """decoding token to get testuser id"""
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    return payload['id']



class UserLoginTest(TestCase):


    def setUp(self):
        """creating setups before user login"""
        self.login_url = reverse('account:login')
        self.client = Client()
        self.user = User.objects.create_user(username='test_name', password='123456')

        
    def test_login_failing_with_wrong_username(self):
        """if user enter a wrong username shouldnt be able to login"""
        payload = {
            'username': 'mohammad', 
            'password': '123456'
        }

        res = self.client.post(self.login_url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['message'], 'username doesnt exist')

    
    def test_login_failing_with_wrong_password(self):
        """with wrong password user shouldnt be able to login"""
        payload = {
            'username': 'test_name', 
            'password': '1234567'
        }

        res = self.client.post(self.login_url, payload)

        self.assertEqual(res.data['message'], 'password is wrong')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_login_succesfuly_with_user(self):
        """login with our test user"""
        payload = {
            'username': 'test_name',
            'password': '123456'
        }

        res = self.client.post(self.login_url, payload)

        self.assertEqual(self.user.id, jwt_parse(res.data['access']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        


    






