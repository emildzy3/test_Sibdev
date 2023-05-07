from django.contrib import admin

from . import models


@admin.register(models.Deals)
class DealsAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'total',
        'date',
    ]
    search_fields = [
        'username',
        'total',
    ]


@admin.register(models.Gems)
class GemsAdmin(admin.ModelAdmin):
    list_display = [
        'title',
    ]

    search_fields = [
        'title',
    ]
