from django.contrib import admin

from . import models


@admin.register(models.Deal)
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


@admin.register(models.Gem)
class GemsAdmin(admin.ModelAdmin):
    list_display = [
        'title',
    ]

    search_fields = [
        'title',
    ]
