from django.core.management.base import BaseCommand, CommandError
import os

from database.utils import generate_thumbnail
from dogs.models import DogPhoto
from cats.models import CatPhoto

class Command(BaseCommand):
    help = 'Генерация недостающих миниатюр фотографий'

    def handle(self, *args, **options):
        dogs_photos = DogPhoto.objects.filter(thumbnail='')
        cats_photos = CatPhoto.objects.filter(thumbnail='')
        count_dogs = 0
        count_cats = 0
        for photo in dogs_photos:
            try:
                with photo.image.open('rb') as file:
                    base = os.path.splitext(os.path.basename(photo.image.name))[0]
                    filename = f'{base}.jpg'
                    thumbnail = generate_thumbnail(file)
                    photo.thumbnail.save(
                        filename, thumbnail, save=False)
                    DogPhoto.objects.filter(pk=photo.pk).update(
                        thumbnail=photo.thumbnail.name
                    )
                    count_dogs += 1
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(
                        f'Ошибка обработки фотографии {photo.pk}: {e}'
                    )
                )
                continue
        for photo in cats_photos:
            try:
                with photo.image.open('rb') as file:
                    base = os.path.splitext(os.path.basename(photo.image.name))[0]
                    filename = f'{base}.jpg'
                    thumbnail = generate_thumbnail(file)
                    photo.thumbnail.save(
                        filename, thumbnail, save=False)
                    CatPhoto.objects.filter(pk=photo.pk).update(
                        thumbnail=photo.thumbnail.name
                    )
                    count_cats += 1
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(
                        f'Ошибка обработки фотографии {photo.pk}: {e}'
                    )
                )
                continue
        print(f'Превью сгенерированы, {count_dogs} собак, {count_cats} кошек')
