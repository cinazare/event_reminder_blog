"""
serializes the requests
"""
from rest_framework import serializers
from account.models import User


class UserLoginSerializer(serializers.ModelSerializer):
    """serializer for the user login page"""

    class Meta:
        model = User
        fields = ['username', 'password']
        # extra_kwargs = {
        #     'password': {
        #         'write_only': True,
        #     }
        # }