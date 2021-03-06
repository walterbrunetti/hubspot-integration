from django.views.generic import TemplateView
from django.conf import settings
from rest_framework_mongoengine import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from deals.models import Deal
from deals.serializers import DealSerializer
from sync.views import sync_data
from sync.exceptions import TokenException


class HomeView(TemplateView):
    template_name = "deal/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['auth_uri'] = settings.HUBSPOT_AUTH_URI
        return context


class DealListAPIView(generics.ListAPIView):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class SyncDealsData(APIView):

    def post(self, request, format=None):
        try:
            sync_data()
            return Response({'success': True})
        except TokenException:
            return Response({'success': False, 'token_exception': True})
        except Exception as exception:
            return Response({'success': False, 'error_massage': exception})
