'''
Created on Jul 20, 2013

@author: Sina
'''
from django.contrib import admin
from SADProject.warehouse.models import Category
from SADProject.warehouse.models import Good

admin.site.register(Category)
admin.site.register(Good)