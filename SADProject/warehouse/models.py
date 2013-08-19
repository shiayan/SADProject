from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):


    name = models.CharField(max_length="10")
    def __unicode__(self):
        return str(self.pk)

class Good(models.Model):
    class Meta:
        permissions = (("add_receipt", "Add receipts"),
                       ("view_all_goods", "View all goods"),
                       ("view_my_goods","View my goods"),
                        ("register_delivery","Register delivery"),
                       ("add_new_good","Add new goods"),
                       ("change_categories", "Change categories")


        )
    GOOD_STATUS_CHOICES = (('W','موجود در انبار'),
                            ('U','تحویل داده بی برچسب'),
                            ('L','تحویل داده شده'),
							('D','خراب'),
                            
                            )
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL)
    status = models.CharField(max_length=1, choices=GOOD_STATUS_CHOICES,default='W')
    submitDate = jmodels.jDateField()
    category = models.ForeignKey(Category,blank=True, null=True,on_delete=models.SET_NULL)
    orderitem=models.ForeignKey('orders.OrderItem')
    def __unicode__(self):
        return str(self.pk)