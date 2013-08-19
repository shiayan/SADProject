from SADProject.damaged.models import Damaged

__author__ = 'Sina'
'''
Created on Jul 22, 2013

@author: Sina
'''
from django import template
from SADProject.orders.models import Order,OrderItem
from  SADProject.warehouse.models import  Category
from django.template.loader import render_to_string
from django.contrib.auth.models import Group, User
from SADProject.warehouse.models import Good

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

@register.filter(name='user_group_span')
def user_group_span(value):
    value = str(value)
    status_span = {'A' : "label label-important"  , 'S' :  "label label-info", 'T' : "label label-success" , 'B' : "label label-inverse"  , 'U' : 'label label-danger'}
    return status_span[value]

@register.filter(name = 'user_group_label')
def user_group_label(value):
    value = str(value)
    group_label_dict= {'A' : 'مدیر','S' : 'انباردار' , 'T' : 'امین انبار','B' : 'مسئول خرید','U' : 'متقاضی' }
    return group_label_dict[value]

@register.simple_tag
def warehouse_count_free_cat(cat):
    return Good.objects.filter(category=cat,user=None).count()
@register.simple_tag
def user_list():
    return render_to_string("user_list.html",{"data":User.objects.all()})
@register.simple_tag
def user_groups():
    return render_to_string("user_groups.html",{"data" : Group.objects.all()})

@register.simple_tag
def good_cats(json = False):
    result = render_to_string("warehouse_cats.html",{"data" : Category.objects.all()})
    if json:
        result = result.replace('"',r'\"')
    return result
@register.filter(name='good_status_span')
def good_status_span(value):
    status_span = {'L' : "label label-success"  , 'W' :  "label", 'D' : "label label-inverse" , 'U' : "label label-info"}
    return status_span[value]

@register.filter(name = 'good_status')
def good_status(good):
    result = dict(Good.GOOD_STATUS_CHOICES)[good.status]
    if good.status == 'D':
        if Damaged.objects.filter(good = good).count() > 0:
            result += ' : ' + dict(Damaged.DAMAGED_STATUS_CHOICES)[Damaged.objects.get(good = good).status]
    return result
