import codecs
import csv
from dataclasses import dataclass
from datetime import datetime
from itertools import chain
from typing import Tuple, TypeAlias

from django.contrib.postgres.aggregates.general import ArrayAgg
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Sum

from . import exceptions, models

DealsDataItem: TypeAlias = Tuple[str, str, str, str, str]


@dataclass
class DealsDataCreate:
    received_file: InMemoryUploadedFile

    def create_deals(self) -> None:
        self._update_data()

    def _update_data(self) -> None:
        received_file_read = self._get_clean_received_file()
        deals_list = []
        for row in received_file_read:
            try:
                row = row[0].split(';')
            except IndexError as exc:
                raise exceptions.ReadFileError(
                    'Ошибка при чтении строчек файла. Убедитесь, что файл соотвествует шаблону'
                ) from exc
            deals_list.append(DealsDataParse(row=row).get_deals_row())
        self._delete_old_data()
        models.Deals.objects.bulk_create(deals_list)

    # TODO Дописать тип
    def _get_clean_received_file(self) -> str:
        try:
            received_file_read = csv.reader(
                codecs.iterdecode(self.received_file, 'utf-8'),
                delimiter=',',
            )
            next(received_file_read)
        except csv.Error as exc:
            raise exceptions.ReadFileError(
                'Ошибка при чтении файла. Убедитесь, что файл передается корректно',
            ) from exc
        return received_file_read

    def _delete_old_data(self) -> None:
        models.Deals.objects.all().delete()


@dataclass
class DealsDataParse:
    row: list[str]

    def get_deals_row(self) -> models.Deals:
        gem_title, datetime_str, customer_login, total, quantity = self._get_items_by_row()
        date = self._convert_str_to_datetime(datetime_str=datetime_str)
        gems = models.Gems.objects.get_or_create(title=gem_title)[0]
        customer = models.Customer.objects.get_or_create(login=customer_login)[0]
        try:
            return models.Deals(
                customer=customer,
                gems=gems,
                total=total,
                quantity=quantity,
                date=date,
            )
        except IndexError as exc:
            raise exceptions.ReadFileError(
                'Ошибка при создании Deals. Убедитесь, что файл соотвествует шаблону',
            ) from exc

    def _get_items_by_row(self) -> DealsDataItem:
        #eample row: ['bellwether', 'Цаворит', '612', '6', '2018-12-14 08:29:52.506166']
        try:
            gem_title = self.row[1]
            datetime_str = self.row[4]
            customer_login = self.row[0]
            total = self.row[2]
            quantity = self.row[3]
        except IndexError as exc:
            raise exceptions.ReadFileError(
                'Ошибка при распарсивании данных. Убедитесь, что файл соотвествует шаблону',
            ) from exc
        return gem_title, datetime_str, customer_login, total, quantity

    def _convert_str_to_datetime(
        self,
        datetime_str: str,
    ) -> datetime:
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError as exc:
            raise exceptions.ReadFileError(
                'Ошибка при конвертации даты. Убедитесь, что файл соотвествует шаблону',
            ) from exc


@dataclass
class UserList:

    def get_customer_with_data(self):
        top_customer_list = models.Deals.objects.values('customer__login')\
            .annotate(spent_money=Sum('total'))\
            .annotate(g=ArrayAgg('gems__title', distinct=True))\
            .order_by('-spent_money')[:5]

        result_gems_list = list(chain(*top_customer_list.values_list('g', flat=True)))
        popular_gems = []
        for i in result_gems_list:
            if result_gems_list.count(i) > 1 and i not in popular_gems:
                popular_gems.append(i)

        customer_data = []
        for customer in top_customer_list:
            customer_gems = customer.get('g')
            popular_gems_in_gems_customer = list(set(popular_gems) & (set(customer_gems)))
            customer_data.append(
                {
                    'login': customer.get('customer__login'),
                    'spent_money': customer.get('spent_money'),
                    'gems': ', '.join(popular_gems_in_gems_customer)
                })
        return customer_data
