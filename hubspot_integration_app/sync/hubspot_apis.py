import requests
from requests import exceptions
from django.conf import settings
from sync.exceptions import TokenException


def generate_token(authorization_code):
    token_url = "https://api.hubapi.com/oauth/v1/token"
    info_url = 'https://api.hubapi.com/oauth/v1/access-tokens/{}'

    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': settings.HUBSPOT_CALLBACK_URI,
        'client_id': settings.HUBSPOT_CLIENT_ID,
        'client_secret': settings.HUBSPOT_CLIENT_SECRET
    }
    try:
        response = requests.post(token_url, data=data, verify=False, allow_redirects=False)
        response.raise_for_status()
        token = response.json()

        token_info_response = requests.get(info_url.format(token['access_token']), verify=False)
        user = token_info_response.json().get('user', '')
        token['user'] = user
    except (exceptions.HTTPError, exceptions.RequestException) as exception:
        raise TokenException('Error trying to generate token: {}'.format(exception))
    return token


def refresh_token(refresh_token):
    token_url = "https://api.hubapi.com/oauth/v1/token"
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': settings.HUBSPOT_CLIENT_ID,
        'client_secret': settings.HUBSPOT_CLIENT_SECRET
    }
    try:
        response = requests.post(token_url, data=data, verify=False, allow_redirects=False)
        response.raise_for_status()
    except (exceptions.HTTPError, exceptions.RequestException) as exception:
        raise TokenException('Error trying to refresh token: {}'.format(exception))

    return response.json()


def get_all_deals(token):
    deals_api_url = 'https://api.hubapi.com/deals/v1/deal/paged?properties=dealname&properties=dealstage&properties=closedate&properties=amount&properties=dealtype'

    try:
        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json'
        }
        response = requests.get(deals_api_url, headers=headers, verify=False)
        response.raise_for_status()
    except (exceptions.HTTPError, exceptions.RequestException):
        raise

    return response.json()
