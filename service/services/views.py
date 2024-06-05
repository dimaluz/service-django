from django.shortcuts import render
from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from . import models
from .serializers import SubscriptionSerializer

class SubscriptionView(ReadOnlyModelViewSet):
    queryset = models.Subscription.objects.all().prefetch_related(
        Prefetch('client', queryset=models.Client.objects.all().select_related('user').only('company_name', 'user__email'))
    )

    serializer_class = SubscriptionSerializer