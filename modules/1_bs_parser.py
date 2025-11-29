import os  # noqa: F401
import sys  # noqa: F401
import django  # noqa: F401
from load_django import *  # noqa: F403,F401
from bs4 import BeautifulSoup
import re


from parser_app.models import Product

import requests


URL = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Referer": "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html",
}

response = requests.get(URL, headers=headers)


def pars():
    """Парсинг сайта и запись атнибутов в словарь"""

    # soup = BeautifulSoup(html, "html.parser")
    soup = BeautifulSoup(response.text, "lxml")

    print("Файл загружен и обработан.")
    product = {}

    try:
        product["title"] = soup.find("h1").get_text(strip=True)
    except AttributeError:
        product["title"] = None

    try:
        product["old_price"] = soup.find("div", class_="br-pr-op").find("span").get_text(strip=True)
    except AttributeError:
        product["old_price"] = None

    # новая цена - всегда есть
    try:
        block = soup.find("div", class_="br-pr-np")
        red = block.find(class_="red-price")

        if red:
            product["new_price"] = red.get_text(strip=True)
            product["is_discount"] = True
        else:
            product["new_price"] = block.find("span").get_text(strip=True)
            product["is_discount"] = False

    except AttributeError:
        product["new_price"] = None
        product["is_discount"] = False

    try:
        product["product_code"] = soup.find("span", class_="br-pr-code-val").get_text(strip=True)
    except AttributeError:
        product["product_code"] = None  # код товара

    try:
        product["product_id"] = soup.find("div", id="product_code").get("data-pid")
    except AttributeError:
        product["product_id"] = None  # внутренний id товара в магазине остаётся стабильны

    try:
        product["reviews_count"] = soup.find("a", class_="reviews-count").find("span").get_text(strip=True)
    except AttributeError:
        product["reviews_count"] = None  # количество отзывов

    try:
        chars_block = soup.find("div", id="br-pr-7")  #
        sections = chars_block.find_all("div", class_="br-pr-chr-item")

        specifications_dict = {}

        for section in sections:
            section_name = section.find("h3").get_text(strip=True)
            specifications_dict[section_name] = {}

            items = section.find_all("div")
            for item in items:
                name = item.find_all("span")[0].get_text(strip=True)
                value = item.find_all("span")[1].get_text(" ", strip=True).replace("\xa0", " ")
                value = re.sub(r"\s+", " ", value).strip()  # убирем лишние пробелы
                specifications_dict[section_name][name] = value

    except AttributeError:
        specifications_dict = None

    product["specifications"] = specifications_dict

    # ищем все картинки с классом br-main-img
    try:
        images = soup.find_all("img", class_="br-main-img")
        base_url = "https://brain.com.ua"

        photo_urls = [img["src"] if img["src"].startswith("http") else base_url + img["src"] for img in images]

    except AttributeError:
        photo_urls = None
    product["images"] = photo_urls

    try:
        product["color"] = specifications_dict.get("Фізичні характеристики", {}).get("Колір")
    except AttributeError:
        product["color"] = None

    try:
        product["memory"] = specifications_dict.get("Функції пам'яті", {}).get("Вбудована пам'ять")
    except AttributeError:
        product["memory"] = None

    try:
        product["manufacturer"] = specifications_dict.get("Інші", {}).get("Виробник")  # Производитель
    except AttributeError:
        product["manufacturer"] = None

    try:
        product["screen_size"] = specifications_dict.get("Дисплей", {}).get("Діагональ екрану")  # Диагональ экрана
    except AttributeError:
        product["screen_size"] = None

    try:
        product["resolution"] = specifications_dict.get("Дисплей", {}).get(
            "Роздільна здатність екрану"
        )  # роздiльна здатнiсть дiсплея
    except AttributeError:
        product["resolution"] = None

    for key, value in product.items():
        print("=" * 50)
        print(f"{key}: {value}")

    return product


def save_product(url: str, data: dict):
    """Сохраняет продукт в базу данных (update or create)."""

    product, created = Product.objects.get_or_create(url=url)

    product.title = data.get("title")
    product.color = data.get("color")
    product.memory = data.get("memory")
    product.manufacturer = data.get("manufacturer")

    product.old_price = data.get("old_price")
    product.new_price = data.get("new_price")
    product.is_discount = data.get("is_discount")

    product.images = data.get("images")
    product.code = data.get("product_code")
    product.reviews_count = data.get("reviews_count")
    product.screen_size = data.get("screen_size")
    product.resolution = data.get("resolution")
    product.specifications = data.get("specifications")

    product.save()


# URL

save_product(url=URL, data=pars())
