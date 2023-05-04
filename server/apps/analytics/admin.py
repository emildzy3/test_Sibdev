from django.contrib import admin

from . import models


@admin.register(models.Deals)
class DealsAdmin(admin.ModelAdmin):
    list_display = [
        'customer',
        'total',
        'date',
    ]
    search_fields = [
        'customer',
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


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'login',
    ]

    search_fields = [
        'login',
    ]
