from apps.analytics.routers import router as analytics_router
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

admin.site.site_header = 'Аналитика'
admin.site.site_title = 'Аналитика'
admin.site.index_title = 'Панель управления'

router = routers.DefaultRouter()
router.registry.extend(analytics_router.registry)

api_urlpatterns = [
    path('api/v1/', include(router.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
] + api_urlpatterns

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
