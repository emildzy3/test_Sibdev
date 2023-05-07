from rest_framework import serializers
from . import models


class AnalyticsSerializer(serializers.Serializer):
    deals = serializers.FileField()

    class Meta:
        fields = ['deals']


class UserListSerializer(serializers.ModelSerializer):
    spent_money = serializers.IntegerField()
    gems = serializers.CharField(allow_blank=True)

    class Meta:
        model = models.Deal
        fields = [
            'username',
            'spent_money',
            'gems',
        ]
