from rest_framework import mixins, status, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from . import exceptions, models, serializers, services


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
    parser_classes = [JSONParser, MultiPartParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.AnalyticsSerializer
        if self.action == 'list':
            return serializers.UserListSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        received_file = serializer.validated_data.get('deals')
        try:
            services.DealsDataCreate(received_file=received_file).create_deals()
            return Response(
                {'Status': 'OK'},
                status=status.HTTP_202_ACCEPTED,
            )
        except exceptions.ReadFileError as exc:
            return Response(
                {
                    'Status':
                    f'ERROR, Desc: as "{exc}"- в процессе обработки файла произошла ошибка.'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request, *args, **kwargs):
        user_list = services.UserList().get_customer_with_data()
        serializar = self.get_serializer(
            data=user_list,
            many=True,
        )
        serializar.is_valid()
        return Response(
            {'response”': serializar.data},
            status=status.HTTP_200_OK,
        )
        # if serializar.is_valid():
        #     return Response(
        #         {'response”': serializar.data},
        #         status=status.HTTP_200_OK,
        #     )
        # return Response(
        #     {'response': serializer.errors},
        #     status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        # )
