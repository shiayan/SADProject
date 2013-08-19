# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels
from SADProject.warehouse.models import Category
# Create your models here.

    
class Order(models.Model):
    class Meta:
        permissions = (("view_my_orders", "View my orders"),
                       ("view_all_orders", "View all orders"),
                           ("view_unviewed_orders", "View unviewed orders"),
                           ("view_accepted_orders", "View accepted orders"),
                           ("view_buy_orders", "View orders needing purchase"),
                           ("add_new_order", "Add a new order")
        )
    ORDER_STATUS_CHOICES = (('N','بررسی نشده'),
                            ('A','تایید شده'),
                            ('D','انجام شده'),
                            
                            )
    user = models.ForeignKey(User,blank=True,null=True)
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
    description = models.TextField()
    quantity = models.PositiveIntegerField(default = 1)
    category = models.ForeignKey(Category,null=True)
    status = models.CharField(max_length=1,choices=ORDER_ITEM_STATUS_CHOICES,default='N')         
    def __unicode__(self):
        return str(self.pk)
    