from django.test import TestCase, Client
from django.urls import reverse
from account.models import User
from rest_framework import status
import jwt
from account.authentication import ALGORITHM
from django.conf import settings
from event.models import Events, Participants

def jwt_parse(token):
    """decoding token to get testuser id"""
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    return payload['id']



class UserLoginTest(TestCase):
    """testing user login functionality"""

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
        self.assertEqual(self.user.id, jwt_parse(res.data['refresh']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)



class RefreshTest(TestCase):
    """testing the refresh token works"""

    def setUp(self):
        self.refresh_url = reverse('account:refresh')
        self.login_url = reverse('account:login')
        
        self.client = Client()        
        self.user = User.objects.create_user(username='test_user', password='123456')
    

    def test_if_refresh_token_works_correctly(self):
        """testing refresh token works properly"""
        payload = {
            'username': 'test_user',
            'password': '123456'
        }

        token = self.client.post(self.login_url, payload)
        
        self.assertEqual(self.user.id, jwt_parse(token.data['access']))
        self.assertEqual(self.user.id, jwt_parse(token.data['refresh']))
        self.assertEqual(token.status_code, status.HTTP_200_OK)

        refresh_payload = {
            'refresh': token.data['refresh']
        }
        res = self.client.post(self.refresh_url, refresh_payload)

        self.assertEqual(self.user.id, jwt_parse(res.data['access']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)



class ParticipantsJoinOnEventsTest(TestCase):
    """tesing the joining users on events"""

    def setUp(self):
        
        self.client = Client()

        self.user = User.objects.create_user(username='test_user', password='123456')
        self.event = Events.objects.create(
            provider=self.user,
            course_name='test_course',
            teacher_name='test_teacher',
            number_of_sessions='10',
        )
        self.join_url = reverse('account:join-events', kwargs={'pk':self.event.id})


    def test_if_events_information_get_successfuly(self):
        """getting the information of the test"""
        res = self.client.get(self.join_url)

        event = Events.objects.filter(id=res.data['id']).first()

        self.assertEqual(self.event, event)
        self.assertEqual(status.HTTP_200_OK, res.status_code)

    def test_if_joining_on_event_works_propperly(self):
        """joining a test user on our event"""
        payload = {
            'phone_number': '11111111111',
            'full_name': 'test_participant',
            'student_number':'4012023304'
        }
        Events.objects.create(
            provider=self.user,
            course_name='test_course_2',
            teacher_name='test_teacher_2',
            number_of_sessions='10',
        )
        
        res = self.client.post(self.join_url, payload)

        participant = self.event.participants.filter(phone_number=payload['phone_number'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(participant.exists())
        self.assertEqual(participant.first().event.id, self.event.id)
        self.assertEqual(res.data, payload)





