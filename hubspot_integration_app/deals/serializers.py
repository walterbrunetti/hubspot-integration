from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from deals.models import Deal


class DealSerializer(DocumentSerializer):
    deal_id = serializers.IntegerField()
    name = serializers.CharField()
    stage = serializers.CharField()
    close_date = serializers.DateTimeField()
    deal_type = serializers.CharField()
    amount = serializers.DecimalField(decimal_places=2, max_digits=256)

    class Meta:
        model = Deal
        fields = [
            'deal_id',
            'name',
            'stage',
            'close_date',
            'deal_type',
            'amount'
        ]
