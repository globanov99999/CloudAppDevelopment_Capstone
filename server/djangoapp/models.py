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




# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
