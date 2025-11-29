from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "title",
        "color",
        "memory",
        "manufacturer",
        "old_price",
        "new_price",
        "is_discount",
        "images",
        "code",
        "reviews_count",
        "screen_size",
        "resolution",
        "specifications",
        "created_at",
    )


class ContactInline(admin.TabularInline):
    model = models.Product
