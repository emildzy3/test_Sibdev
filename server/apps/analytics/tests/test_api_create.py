from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Deal


class TestCreate(APITestCase):
    URL = '/api/v1/analytics/'

    def test_post_create_data(self):
        with open('apps/analytics/tests/test_files/test_file_good.csv', 'rb') as file:
            data = {
                'deals': file,
            }

            response = self.client.post(
                self.URL,
                data=data,
            )
            file.close()
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.data.get('Status') == 'OK'

        count_deals = Deal.objects.all().count()
        assert count_deals == 48

    def test_post_create_second_data(self):
        count_deals_start = Deal.objects.all().count()
        assert count_deals_start == 0
        with open('apps/analytics/tests/test_files/test_file_good.csv', 'rb') as file:
            data = {
                'deals': file,
            }

            self.client.post(
                self.URL,
                data=data,
            )
            file.close()
        count_deals_first_send = Deal.objects.all().count()
        assert count_deals_first_send == 48

        with open('apps/analytics/tests/test_files/test_file_good.csv', 'rb') as file:
            data = {
                'deals': file,
            }

            self.client.post(
                self.URL,
                data=data,
            )
            file.close()
        count_deals_second_send = Deal.objects.all().count()
        assert count_deals_second_send == 48

    def test_post_create_break_file(self):
        count_deals_start = Deal.objects.all().count()
        assert count_deals_start == 0
        with open('apps/analytics/tests/test_files/test_file_break.csv', 'rb') as file:
            data = {
                'deals': file,
            }

            response = self.client.post(
                self.URL,
                data=data,
            )
            file.close()
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data.get('Status') == (
            'ERROR, Desc: as "Ошибка при распарсивании данных. Убедитесь, что файл соотвествует ' +
            'шаблону"- в процессе обработки файла произошла ошибка.')

        count_deals_start = Deal.objects.all().count()
        assert count_deals_start == 0

    def test_post_create_second_break_file(self):
        count_deals_start = Deal.objects.all().count()
        assert count_deals_start == 0

        with open('apps/analytics/tests/test_files/test_file_good.csv', 'rb') as file:
            data = {
                'deals': file,
            }

            self.client.post(
                self.URL,
                data=data,
            )
            file.close()
        count_deals_first_send = Deal.objects.all().count()
        assert count_deals_first_send == 48

        with open('apps/analytics/tests/test_files/test_file_break.csv', 'rb') as file:
            data = {
                'deals': file,
            }

            response = self.client.post(
                self.URL,
                data=data,
            )
            file.close()
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data.get('Status') == (
            'ERROR, Desc: as "Ошибка при распарсивании данных. Убедитесь, что файл соотвествует ' +
            'шаблону"- в процессе обработки файла произошла ошибка.')

        count_deals = Deal.objects.all().count()
        assert count_deals == 48
