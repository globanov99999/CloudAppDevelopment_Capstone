from django.db import models
from django.utils.timezone import now

BBB='BBB'

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Lada')
    description = models.CharField(null=False, max_length=120, default='Decription')
    
    def __str__(self):
        return self.name

    def full_desc(self):
        return self.name + ': ' + self.description


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.SET_NULL, blank=True, null=True)
    dealer_id= models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=30, default='Niva')
    type_choices = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
        ('Roadster', 'Roadster'))
    car_type = models.CharField(max_length=10,
                                choices=type_choices,
                                default='Sedan')
    year = models.DateField()
    color = models.CharField(null=False, max_length=30, default='Green')
    def __str__(self):
        return str(self.make) + ' ' + self.name + ' ' + str(self.year)


class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
