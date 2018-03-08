from django.db import models

# Create your models here.
class Pizza(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()


class Order(models.Model):
    class Size:
        _30CM = '30'
        _50CM = '50'

    pizza = models.ForeignKey(Pizza,
                                 on_delete=models.SET_NULL,
                                 null=True)

    size = models.CharField(choices=[(Size._30CM, '30cm'),
                                     (Size._50CM, '50cm')],
                            max_length=2)
    customer_name = models.CharField(max_length=40)
    customer_address = models.TextField()
