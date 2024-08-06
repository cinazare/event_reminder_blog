"""
views for the accounts
 """
from rest_framework.views import APIView
from rest_framework import status, exceptions
from account.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from event.serializers import EditEventSerializer, JoinOnAnEventSerializer
from event.models import Participants, Events
from .serializers import UserLoginSerializer, UserRefreshTokenSerializer
from .authentication import JWTAuthentication



class LoginApiView(APIView):
    """login api view"""
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid()

        username = serializer.data['username']
        password = serializer.data['password']

        print(username)
        print(password)
        
        user = User.objects.filter(username=username).first()
        print(user)
        if not user:
            return Response({'message':'username doesnt exist'})
        
        if not user.check_password(password):
            return Response({'message':'password is wrong'})
        
        
        refresh = JWTAuthentication.create_refresh(user.id)
        access = JWTAuthentication.create_access(refresh)

        return Response(
            {
                'message': 'successful authentication',
                'access': access,
                'refresh': refresh
                }
            )



class RefreshAPIView(APIView):
    """getting refresh and build access"""
    serializer_class = UserRefreshTokenSerializer
    permission_classes = [AllowAny, ]


    def post(self, request, *args, **kwargs):
        serializer = UserRefreshTokenSerializer(data=request.data)
        serializer.is_valid()
        
        access = JWTAuthentication.create_access(serializer.data['refresh'])

        return Response({'access': access, 'refresh': serializer.data['refresh']})
    



# class LogInApiView(APIView):
#     """loging users with jwt"""
#     serializer_class = UserLoginSerializer
#     permission_classes = [permissions.AllowAny,]
#
#     def post(self, request):
#         """loging in user"""
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid()
#
#         username = serializer.data['username']
#         password = serializer.data['password']
#
#         user = User.objects.filter(username=username).first()
#         if user is None or not user.check_password(password):
#             return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
#
#         token = JWTAuthentication.create_jwt(user)
#         response = HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/events/user')
#         response.set_cookie(key='jwt_token', value=token, httponly=True)
#         response.data = {
#             'jwt_token': token
#         }
#
#         return response


class ParticipantsJoin(APIView):
    """participants joining on events"""
    permission_classes = [AllowAny]
    serializer_class = JoinOnAnEventSerializer

    def get(self, request, pk):
        """retrieving event with pk as id"""
        if not pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        event = Events.objects.filter(id=pk).first()
        serializer = EditEventSerializer(event)
        return Response(serializer.data)

    def post(self, request, pk):
        """join on the selected event"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        event = Events.objects.filter(id=pk).first()
        if not event:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event.duplicate(serializer.data['phone_number']):
            return Response({'message': 'y;ou have already installed'})

        Participants.objects.create(
            phone_number=serializer.data['phone_number'],
            full_name=serializer.data['full_name'],
            student_number=serializer.data['student_number'],
            event=event
        )

        return Response({"message": 'user created successfully'}, status=status.HTTP_201_CREATED)










