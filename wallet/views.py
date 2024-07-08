"""
views for transactions
"""
from rest_framework.views import APIView
from wallet.models import Transaction
from account.models import User
from rest_framework import viewsets, status
from wallet.serializers import TransactionsSerializer
from rest_framework.response import Response


class TransactionsViewSet(viewsets.ViewSet):
    """getting and posting view-sets for users"""

    serializer_class = TransactionsSerializer

    def list(self, request):
        """showing all users transactions"""
        queryset = Transaction.objects.filter(user=request.user)
        financial_credit = request.user.get_credit()

        serializer = TransactionsSerializer(queryset, many=True)
        return Response(
            {'financial credit': financial_credit, 'transaction': serializer.data}
        )

    def create(self, request):
        """charging or consumpting users financial_credit"""
        serializer = TransactionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = {'user': request.user}
        serializer.save(**payload)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



