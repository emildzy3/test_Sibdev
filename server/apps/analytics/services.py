import codecs
import csv
from dataclasses import dataclass
from datetime import datetime
from itertools import chain
from typing import Iterator, List, Tuple, TypeAlias, TypedDict

from django.conf import settings
from django.contrib.postgres.aggregates.general import ArrayAgg
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Sum
from django.utils.timezone import make_aware

from . import exceptions, models

DealsDataItem: TypeAlias = Tuple[str, str, str, str, str]


class CustomerData(TypedDict):
    username: str
    spent_money: int
    gems: str


@dataclass
class DealsDataCreateService:
    received_file: InMemoryUploadedFile

    def create_deals(self) -> None:
        received_file_read = self._get_clean_received_file()
        deals_list = self._get_deals_list_for_create(received_file_read=received_file_read)
        self._delete_old_deals()
        self._create_new_deals(deals_list=deals_list)

    def _get_clean_received_file(self) -> Iterator[list[str]]:
        try:
            received_file_read = csv.reader(
                codecs.iterdecode(self.received_file, 'utf-8'),
                delimiter=',',
            )
            # пропустить заголовок
            next(received_file_read)
        except csv.Error as exc:
            raise exceptions.ReadFileError(
                'Ошибка при чтении файла. Убедитесь, что файл передается корректно',
            ) from exc
        return received_file_read

    def _get_deals_list_for_create(
        self,
        received_file_read: Iterator[list[str]],
    ) -> List['models.Deals']:
        deals_list = []
        for row in received_file_read:
            if row:
                deals = DealsDataParse(row=row).convert_row_for_deals()
                deals_list.append(deals)
        return deals_list

    def _delete_old_deals(self) -> None:
        models.Deals.objects.all().delete()

    def _create_new_deals(
        self,
        deals_list: List['models.Deals'],
    ) -> None:
        try:
            models.Deals.objects.bulk_create(deals_list)
        except ValueError as exc:
            raise exceptions.ReadFileError(
                'Ошибка при сохранении данных. Убедитесь, что данные внутри файла соответсвуют \
                    шаблону',
            ) from exc


@dataclass
class DealsDataParse:
    row: list[str]

    def convert_row_for_deals(self) -> models.Deals:
        gem_title, datetime_str, customer_login, total, quantity = self._get_items_by_row()
        date = self._convert_str_to_datetime(datetime_str=datetime_str)
        gems, _ = models.Gems.objects.get_or_create(title=gem_title)
        try:
            return models.Deals(
                username=customer_login,
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
        print(self.row)
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
            return make_aware(datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f'))
        except ValueError as exc:
            raise exceptions.ReadFileError(
                'Ошибка при конвертации даты. Убедитесь, что файл соотвествует шаблону',
            ) from exc


class UserListService:

    def __init__(self, *args, **kwargs):
        self.top_customer_list = models.Deals.objects.values('username')\
            .annotate(spent_money=Sum('total'))\
            .annotate(gems_list=ArrayAgg('gems__title', distinct=True))\
            .order_by('-spent_money')[:settings.NUMBER_OF_CLIENTS]

    def get_customer_with_data(self) -> list[CustomerData]:
        popular_gems_list = self._get_popular_gems_list()
        return self._get_customer_data_list(popular_gems_list=popular_gems_list)

    def _get_popular_gems_list(self) -> list[str]:
        result_gems_list = list(
            chain(*self.top_customer_list.values_list(
                'gems_list',
                flat=True,
            )))
        popular_gems = []

        for i in result_gems_list:
            if result_gems_list.count(i) > 1 and i not in popular_gems:
                popular_gems.append(i)
        return popular_gems

    def _get_customer_data_list(
        self,
        popular_gems_list: list[str],
    ) -> list[CustomerData]:
        customer_data: list[CustomerData] = []
        for username in self.top_customer_list:
            customer_gems = username.get('gems_list')
            popular_gems_in_gems_customer = list(set(popular_gems_list) & (set(customer_gems)))
            customer_data.append(
                {
                    'username': username.get('username'),
                    'spent_money': username.get('spent_money'),
                    'gems': ', '.join(popular_gems_in_gems_customer)
                })
        return customer_data
