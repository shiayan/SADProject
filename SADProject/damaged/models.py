# -*- coding: UTF-8 -*-
from django.db import models
from SADProject.warehouse.models import Good
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User




class Damaged(models.Model):
    class Meta:
        permissions = (("add_damaged_good", "Add damaged good"),
                       ("view_all_damaged_goods", "View all damaged goods"),
                       ("register_damaged_good_delivery","Register damaged good delivery")

        )
    DAMAGED_STATUS_CHOICES = (('D','خراب'),
                           ('W','در تعمیرگاه'),
                           ('A','در نمایندگی'),
                           ('F','تعمیر شده'),

    )
    good = models.ForeignKey(Good,unique=True)
    description = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=1, choices=DAMAGED_STATUS_CHOICES,default='D')
    address = models.TextField(blank=True,null=True)
    previous_status = models.CharField(max_length=1,choices=Good.GOOD_STATUS_CHOICES)
    def status_string(self):
        return dict(self.DAMAGED_STATUS_CHOICES)[str(self.status)]
    def status_span(self):
        status_span = {'F' : "label label-success"  , 'W' :  "label", 'D' : "label label-inverse" , 'A' : "label label-info"}
        return status_span[str(self.status)]
    def __unicode__(self):
        return str(self.pk)