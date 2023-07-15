import os
import csv

from django.core.management.base import BaseCommand

from backend.settings import BASE_DIR
from recepts.models import Ingredients


class Command(BaseCommand):
    help = 'Загрузка данных из CSV файлов в Django ORM'

    def handle(self, *args, **options):
        file_path = os.path.join(BASE_DIR, 'data')
        with open(
            f'{file_path}/ingredients.csv', 'r', encoding='UTF-8'
        ) as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                Ingredients.objects.get_or_create(
                    name=row[0], measurement_unit=row[1]
                )
