from rest_framework import serializers
from . import models


class AnalyticsSerializer(serializers.Serializer):
    deals = serializers.FileField()

    class Meta:
        fields = ['deals']


class UserListSerializer(serializers.ModelSerializer):
    spent_money = serializers.IntegerField()
    gems = serializers.CharField()

    class Meta:
        model = models.Customer
        fields = [
            'login',
            'spent_money',
            'gems',
        ]
