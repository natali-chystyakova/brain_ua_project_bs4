from django.db import models


class Product(models.Model):
    url = models.URLField(unique=True)

    title = models.CharField(max_length=500, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    memory = models.CharField(max_length=50, null=True, blank=True)
    manufacturer = models.CharField(max_length=200, null=True, blank=True)

    old_price = models.CharField(max_length=100, null=True, blank=True)
    new_price = models.CharField(max_length=100, null=True, blank=True)  # э завжди
    is_discount = models.BooleanField(default=False, blank=True)

    images = models.JSONField(null=True, blank=True, default=list)  # список ссылок на фото
    code = models.CharField(max_length=100, null=True, blank=True)
    reviews_count = models.IntegerField(null=True, blank=True)

    screen_size = models.CharField(max_length=50, null=True, blank=True)
    resolution = models.CharField(max_length=50, null=True, blank=True)

    specifications = models.JSONField(null=True, blank=True, default=dict)  # словарь характеристик

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.url
