from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import viewsets, status
from wallet.models import *
from wallet.serializers import TransactionsSerializer 
from account.models import User



# class FinancialCreditViewSet(viewsets.ViewSet):
#     """a get query set to see the financial credeit"""

#     def get(self, request):
        