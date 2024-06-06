from rest_framework import serializers
from . import models


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        fields = ('__all__')


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    price = serializers.SerializerMethodField()

    def get_price(self, subscription):
        return subscription.price

    class Meta:
        model = models.Subscription
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')