from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length="10")
    def __unicode__(self):
        return str(self.pk)

class Good(models.Model):
    GOOD_STATUS_CHOICES = (('W','موجود در انبار'),
                            ('U','تحویل داده بی برچسب'),
                            ('L','تحویل داده شده'),
							('D','خراب'),
                            
                            )
   # user = models.ForeignKey(User)
    status = models.CharField(max_length=1, choices=GOOD_STATUS_CHOICES,default='W')
    submitDate = jmodels.jDateField()
    category = models.ForeignKey(Category)
    orderitem=models.ForeignKey('orders.OrderItem')
    def __unicode__(self):
        return str(self.pk)