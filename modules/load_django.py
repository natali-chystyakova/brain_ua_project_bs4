import os
import sys
import django


def setup_django():
    """
    Инициализация Django из внешних скриптов (парсеры, сервисы и т.д.)
    """

    # Добавляем корень проекта в sys.path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Указываем Django, где настройки
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    # Инициализация Django
    django.setup()


setup_django()
