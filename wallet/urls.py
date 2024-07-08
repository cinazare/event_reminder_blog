"""
this file will manage urls for transactions and wallet functionality
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wallet.views import TransactionsViewSet

router = DefaultRouter()
router.register('transactions', TransactionsViewSet, basename='transactions-history')
urlpatterns = router.urls

