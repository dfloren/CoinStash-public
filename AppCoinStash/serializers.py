from rest_framework import serializers
from .models import CoinList


class CoinListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CoinList
        fields = ('coin_id', 'coin_symbol', 'coin_name')
