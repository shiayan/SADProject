'''
Created on Jul 22, 2013

@author: Sina
'''
from django import template
from ..models import Order,OrderItem
from  SADProject.warehouse.models import  Category
from django.template.loader import render_to_string
register = template.Library()
@register.filter(name='order_status_span')
def order_status_span(value):
    status_span = {'A' : "label label-success"  , 'N' :  "label", 'D' : "label label-inverse" }
    return status_span[value]

@register.filter(name = 'order_status')
def order_status(value):
    return dict(Order.ORDER_STATUS_CHOICES)[value]

@register.filter(name='order_item_status_span')
def order_item_status_span(value):
    status_span = {'I' : "label label-success"  , 'N' :  "label", 'P' : "label label-info"  }
    return status_span[value]

@register.filter(name = 'order_item_status')
def order_item_status(value):
    return dict(OrderItem.ORDER_ITEM_STATUS_CHOICES)[value]

@register.simple_tag
def good_cats():
 return render_to_string("warehouse_cats.html",{"data" : Category.objects.all()})
