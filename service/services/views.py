from django.shortcuts import render
from django.db.models import Prefetch, F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet

from . import models
from .serializers import SubscriptionSerializer

class SubscriptionView(ReadOnlyModelViewSet):
    # queryset = models.Subscription.objects.all().prefetch_related(
    #     'plan',
    #     Prefetch('client', queryset=models.Client.objects.all().select_related('user').only('company_name', 'user__email'))
    # ).annotate(price=F('service__full_price') - F('service__full_price') * F('plan__discount_percent') / 100.00)

    queryset = models.Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=models.Client.objects.all().select_related('user').only('company_name', 'user__email'))
    )

    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        response_data = {
            'result':response.data,
        }
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        response.data = response_data
        return response