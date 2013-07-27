# -*- coding: UTF-8 -*-
from django.db import models
from django_jalali.db import models as jmodels
from SADProject.warehouse.models import Category
# Create your models here.

    
class Order(models.Model):
    ORDER_STATUS_CHOICES = (('N','بررسی نشده'),
                            ('A','تایید شده'),
                            ('D','انجام شده'),
                            
                            )
    user = models.IntegerField()
    status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES,default=ORDER_STATUS_CHOICES[0][0])
    submitDate = jmodels.jDateField()
    def __unicode__(self):
        return str(self.pk)
class OrderItem(models.Model):
    ORDER_ITEM_STATUS_CHOICES = (('N','بررسی نشده'),
                                 ('I','موجود'),
                                 ('P','درحال خرید'),
                                 
                                 )
    order = models.ForeignKey(Order)
    name = models.CharField(max_length = 12)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default = 1)
    category = models.ForeignKey(Category)  
    status = models.CharField(max_length=1,choices=ORDER_ITEM_STATUS_CHOICES,default='N')         
    def __unicode__(self):
        return str(self.pk)
    