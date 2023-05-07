from apps.analytics.routers import router as analytics_router
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

admin.site.site_header = 'Аналитика'
admin.site.site_title = 'Аналитика'
admin.site.index_title = 'Панель управления'

router = routers.DefaultRouter()
router.registry.extend(analytics_router.registry)

api_urlpatterns = [
    path('api/v1/', include(router.urls)),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Analytics",
        default_version='v1',
        description="",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns_swagger = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    re_path(
        r'^swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
] + api_urlpatterns + urlpatterns_swagger

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
