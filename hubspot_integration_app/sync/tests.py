import unittest
from unittest import mock
from sync.models import Token
from sync.views import get_valid_token, sync_data
from deals.models import Deal


class ViewsTests(unittest.TestCase):

    def tearDown(self):
        Token.objects.all().delete()
        Deal.objects.all().delete()

    def test_get_valid_token_returns_existing_token_if_its_not_expired(self):
        token_obj = Token.objects.create(user='test', access_token='some_token',
                                         refresh_token='refresh_token', expires_in=21600)

        token = get_valid_token()
        self.assertEqual(token, token_obj.access_token)

    @mock.patch('sync.views.refresh_token')
    def test_refresh_token_is_created_if_existing_token_is_expired(self, mock_refresh_token):
        token_obj = Token.objects.create(user='test', access_token='some_token',
                                         refresh_token='refresh_token', expires_in=0)
        self.assertTrue(token_obj.is_expired())

        mock_refresh_token.return_value = {'access_token': 'new_token',
                                           'refresh_token': token_obj.refresh_token,
                                           'expires_in': 21600}

        token = get_valid_token()
        mock_refresh_token.assert_called_once()
        self.assertEqual(token, 'new_token')
        self.assertTrue(Token.objects.all().count(), 2)

    @mock.patch('sync.views.get_all_deals')
    def test_sync_data_creates_deals_returned_by_api(self, mock_get_all_deals):
        token_obj = Token.objects.create(user='test', access_token='some_token',
                                         refresh_token='refresh_token', expires_in=21600)

        self.assertEqual(Deal.objects.all().count(), 0)

        mock_get_all_deals.return_value = {
            "deals": [
                {
                    "dealId": 1,
                    "properties": {
                        "dealname": {"value": "Test deal 1"},
                        "amount": {"value": "100"},
                        "closedate": {"value": "1610134510962"},
                        "dealstage": {"value": "contractsent"},
                        "dealtype": {"value": "newbusiness"}
                    }
                },
                {
                    "dealId": 2,
                    "properties": {
                        "dealname": {"value": "Test deal 2"},
                        "amount": {"value": "200"},
                        "closedate": {"value": "1610134510962"},
                        "dealstage": {"value": "contractsent"},
                        "dealtype": {"value": "newbusiness"}
                    }
                }
            ]
        }

        sync_data()
        self.assertEqual(Deal.objects.all().count(), 2)
