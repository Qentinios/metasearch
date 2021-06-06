from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from model_utils import Choices


class OfferWebsite(models.Model):
    name = models.CharField(verbose_name='Strona', max_length=128)

    def __str__(self):
        return "{}".format(self.name)


class OfferCity(models.Model):
    name = models.CharField(verbose_name='Miasto', max_length=128)

    def __str__(self):
        return "{}".format(self.name)


class OfferPhoto(models.Model):
    photo = models.ImageField()


class Offer(models.Model):
    TYPES = Choices(
        (1, 'house', 'Dom'),
        (2, 'flat', 'Mieszkanie'),
        (3, 'rent', 'Wynajem'),
        (4, 'plot', 'Działka'),
    )
    title = models.CharField(verbose_name='Tytuł', max_length=255)
    city = models.ForeignKey(OfferCity, verbose_name='Miasto', on_delete=models.CASCADE)
    address = models.CharField(verbose_name='Adres', max_length=255)
    type = models.IntegerField(verbose_name='Rodzaj', choices=TYPES)
    website = models.ForeignKey(OfferWebsite, verbose_name='Strona', on_delete=models.CASCADE)
    area = models.DecimalField(verbose_name='Powierzchnia', decimal_places=2, max_digits=6,
                               validators=[MinValueValidator(1)])
    rooms = models.IntegerField(verbose_name='Ilość pokoi', validators=[MinValueValidator(1)])
    price = models.DecimalField(verbose_name='Cena', decimal_places=2, max_digits=8,
                                validators=[MinValueValidator(1)])
    created = models.DateTimeField(verbose_name='Utworzono', default=timezone.now)
    modified = models.DateTimeField(verbose_name='Ostatnia edycja', null=True, blank=True)
    photos = models.ManyToManyField(OfferPhoto, verbose_name="Zdjęcia")
    link = models.URLField(verbose_name='Link')

    @property
    def price_per_square_meter(self):
        return int(self.price / self.area)
