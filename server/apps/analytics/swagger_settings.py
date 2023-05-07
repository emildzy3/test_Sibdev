from drf_yasg import openapi
from rest_framework import status

CREATE_RESPONSE_SCHEMA = {
    status.HTTP_202_ACCEPTED:
    openapi.Response(
        description='OK',
        examples={'application/json': {
            'Status': 'Ok',
        }},
    ),
    status.HTTP_500_INTERNAL_SERVER_ERROR:
    openapi.Response(
        description='ERROR',
        examples={
            'application/json': {
                'Status': 'ERROR, Desc: as "..."- в процессе обработки файла произошла ошибка.',
            }
        },
    ),
}
