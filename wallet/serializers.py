from rest_framework import serializers
from wallet.models import Transaction


class TransactionsSerializer(serializers.ModelSerializer):
    """a serializer for transactions"""

    class Meta:
        model = Transaction
        fields = (
            'user',
            'date',
            'mode',
            'mount'
        )
        extra_kwargs = {
            'date': {'read_only': True},
            'user': {'read_only': True},
            'mode': {'read_only': True}
        }
