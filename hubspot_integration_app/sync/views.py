from datetime import datetime
from decimal import Decimal
from django.shortcuts import redirect
from django.http import HttpResponse
from sync.models import Token
from sync.exceptions import TokenException
from sync.hubspot_apis import get_all_deals, generate_token, refresh_token
from deals.models import Deal


def oauth_callback(request):
    authorization_code = request.GET.get('code')
    error_code = request.GET.get('error')
    error_description = request.GET.get('error_description')

    if not authorization_code:
        return HttpResponse('Authorization error: {} - {}'.format(error_code, error_description))

    try:
        token_data = generate_token(authorization_code)
    except TokenException as exception:
        return HttpResponse('Token exception: '.format(exception))

    Token.objects.create(**token_data)

    try:
        sync_data()
    except Exception as exception:
        return HttpResponse('Could not sync up data: '.format(exception))

    return redirect('/deals/home')


def get_valid_token():
    """
    Get and return a valid token that can be used to hit Hubspot APIs.
    If token is expired, call refresh token to get a new valid one.
    :return: string
    """
    token = Token.objects.order_by('-id').first()
    if not token:
        return

    if not token.is_expired():
        return token.access_token

    try:
        new_token = refresh_token(token.refresh_token)
    except TokenException:
        return

    Token.objects.create(user=token.user, access_token=new_token['access_token'],
                         refresh_token=new_token['refresh_token'], expires_in=new_token['expires_in'])

    return new_token['access_token']


def sync_data():
    """
    Hit Hubspot APIs to get data and create it in our database.
    """
    token = get_valid_token()
    if not token:
        raise TokenException('Could not get a valid token')

    deals_data = get_all_deals(token)
    deals = deals_data.get('deals')
    Deal.objects.delete()

    for deal_data in deals:
        properties = deal_data.get('properties')
        Deal.objects.create(deal_id=deal_data.get('dealId'),
                            name=properties.get('dealname').get('value'),
                            stage=properties.get('dealstage').get('value'),
                            close_date=datetime.fromtimestamp(int(properties.get('closedate').get('value')) / 1000),
                            deal_type=properties.get('dealtype').get('value'),
                            amount=Decimal(properties.get('amount').get('value')))
