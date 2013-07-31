from django.db import models
from django_jalali.db import models as jmodels
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
    user = models.IntegerField()
    status = models.CharField(max_length=1, choices=GOOD_STATUS_CHOICES,default='W')
    name = models.CharField(max_length = 12)
    submitDate = jmodels.jDateField()
    category = models.ForeignKey(Category)
    def __unicode__(self):
        return str(self.pk)