from django.db import models

import datetime
YEAR_CHOICES = []
for r in range(1900, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r, r))

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Lada')
    description = models.CharField(null=False, max_length=120, default='Decription')

    def __str__(self):
        return self.name

    def full_desc(self):
        return str(self.name) + ': ' + str(self.description)


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.SET_NULL, blank=True, null=True)
    dealer_id = models.IntegerField()
    name = models.CharField(null=False, max_length=30, default='Niva')
    type_choices = (('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Wagon', 'Wagon'), ('Roadster', 'Roadster'))
    car_type = models.CharField(max_length=10, choices=type_choices, default='Sedan')
    year = models.IntegerField('year', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    color = models.CharField(null=False, max_length=30, default='Green')

    def __str__(self):
        return str(self.make) + ' ' + str(self.name) + ' ' + str(self.year)


class CarDealer:
    def __init__(self, address, city, full_name, dealer_id, lat, long, short_name, st, dealer_zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.dealer_id = dealer_id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = dealer_zip

    def __str__(self):
        return "Dealer name: " + self.full_name + " state: " + self.st


class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment,
                 review_id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.review_id = review_id
