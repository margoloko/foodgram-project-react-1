from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient

import csv


class Command(BaseCommand):
    help = 'Загрузка базы данных'

    def handle(self, *args, **options):
        with open('../data/ingredients.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(name=name,
                                                 measurement_unit=measurement_unit)