
import requests, json
from django.http import HttpResponse
from django.conf import settings


test_api_url = 'https://api.hubapi.com/deals/v1/deal/paged?includeAssociations=true&properties=dealname&properties=dealstage&properties=closedate&properties=amount&properties=dealtype'


def oauth_callback(request):

    authorization_code = request.GET.get('code')
    token = get_token(authorization_code)

    try:
        # try using token
        headers = {
            'Authorization': 'Bearer {}'.format(token['access_token']),
            'Content-Type': 'application/json'
        }
        response = requests.get(test_api_url, headers=headers, verify=False)
    except Exception as ex:
        return HttpResponse("Response" + str(ex))

    return HttpResponse("Response" + response.text)


def get_token(authorization_code):

    token_url = "https://api.hubapi.com/oauth/v1/token"

    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': settings.HUBSPOT_CALLBACK_URI,
        'client_id': settings.HUBSPOT_CLIENT_ID,
        'client_secret': settings.HUBSPOT_CLIENT_SECRET
    }

    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False)
    tokens = json.loads(access_token_response.text)
    return tokens
