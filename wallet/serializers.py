from rest_framework import serializers
from wallet.models import Transaction

class TransactionsSerializer(serializers.ModelSerializer):
    """a serilizer for transactions"""

    class Meta:
        model = Transaction
        fields = (
            'wallet', 
            'date',
            'mode',
            'mount'
        )
        extra_kwargs = {
            'date': {'read_only': True}
        }
