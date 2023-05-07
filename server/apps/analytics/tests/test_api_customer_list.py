from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from .. import serializers

EXAMPLE_RESPONSE = {
    "response": [
        {
            "username": "resplendent",
            "spent_money": 34359,
            "gems": "Сапфир"
        },
        {
            "username": "kismetkings213",
            "spent_money": 16709,
            "gems": "Сапфир"
        },
        {
            "username": "braggadocio",
            "spent_money": 13571,
            "gems": "Изумруд"
        },
        {
            "username": "bellwether",
            "spent_money": 7677,
            "gems": ""
        },
        {
            "username": "nibblethew19",
            "spent_money": 7476,
            "gems": "Изумруд"
        },
    ]
}


class TestCustomerList(APITestCase):
    URL = '/api/v1/analytics/'

    def setUp(self):
        consumer_list_to_check = serializers.UserListSerializer(
            data=EXAMPLE_RESPONSE.get('response'),
            many=True,
        )
        consumer_list_to_check.is_valid()
        self.consumer_list_to_check_serializer = consumer_list_to_check

    def test_get_customer_list_empty(self):
        cache.clear()
        response = self.client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('response') == []

    def test_get_customer_list(self):
        with open('apps/analytics/tests/test_files/test_file_good.csv', 'rb') as file:
            data = {
                'deals': file,
            }

            self.client.post(
                self.URL,
                data=data,
            )
            file.close()
        response = self.client.get(self.URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('response')[0] == self.consumer_list_to_check_serializer.data[0]
