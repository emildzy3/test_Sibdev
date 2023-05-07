from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from . import exceptions, models, serializers, services
from .swagger_settings import CREATE_RESPONSE_SCHEMA


class AnalyticsViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
):
    """
    Работа с Аналитикой
    """

    model = models.Deals
    serializer_class = serializers.AnalyticsSerializer
    parser_classes = (MultiPartParser, )

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.AnalyticsSerializer
        if self.action == 'list':
            return serializers.UserListSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(operation_description='Добавить файл', responses=CREATE_RESPONSE_SCHEMA)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        received_file = serializer.validated_data.get('deals')
        try:
            services.DealsDataCreateService(received_file=received_file).create_deals()
            cache.clear()
            return Response({'Status': 'OK'}, status=status.HTTP_202_ACCEPTED)
        except exceptions.ReadFileError as exc:
            return Response(
                {
                    'Status':
                    f'ERROR, Desc: as "{exc}"- в процессе обработки файла произошла ошибка.'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        cached_data = cache.get('response_data')
        if cached_data:
            return Response({'response': cached_data}, status=status.HTTP_200_OK)

        user_list = services.UserListService()
        customer_data = user_list.get_customer_with_data()
        serializar = self.get_serializer(
            data=customer_data,
            many=True,
        )
        if serializar.is_valid():
            cache.set('response_data', serializar.data, 60 * 15)
            return Response({'response”': serializar.data}, status=status.HTTP_200_OK)
        return Response(
            {'response': serializar.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
