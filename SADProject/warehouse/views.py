# -*- coding: UTF-8 -*-
from django.views.generic.base import TemplateView
from models import Category

from SADProject.orders.models import OrderItem
from SADProject.orders.models import Order
from django.contrib.auth.models import User
from models import Good

from django.http import HttpResponse
from django.core.context_processors import csrf
import datetime
import json
from django_jalali.db.models import jDateField
from django.shortcuts import render_to_response
from SADProject.utils.view_utils import render_to_response_wrapper, jsonListGenerator

def allGoodsJson(request):
    columns = ['pk','submitDate','status','user']
    data = Good.objects
    return jsonListGenerator(request = request, columns = columns, data = data, template = "json/allgoods.json")
	
def unlabeledGoodsJson(request):
    columns = ['pk','submitDate','status','user']
    data = Good.objects
    return jsonListGenerator(request = request, columns = columns, data = data, template = "json/unlabeledgoods.json")



def addGood(request):
    today = jDateField();
    today = today.to_python(datetime.datetime.now())
    CATinst=Category.objects.filter(pk=request.POST['CAT'])[0]
    OrderInst=Order.objects.filter(pk=request.POST['NO'])[0]
    OrderItemInst=OrderItem.objects.filter(pk=request.POST['NOI'])[0]
    OrderItemInst.status='I'
    OrderItemInst.save()
    OrderItemInst2=OrderItem.objects.filter(order=OrderInst).exclude(status='I')
    if not OrderItemInst2:
		OrderInst.status='D'
    OrderInst.save()
    goodinst = Good(submitDate=today,category=CATinst,orderitem=OrderItemInst)
    goodinst.save()				
    
    c = {'rlink' : '../../allgoods/' , 'success' : " کالای شما ....."}
    return render_to_response("success.html",c);


def deleteFromQuerySet(request,queryset):
    pk = int(request.POST['pk'])
    queryset.filter(pk = pk).delete();
    return HttpResponse("Deleted");

def addGoodView(request):
     return render_to_response_wrapper(request,"addgood.html")
	 
def allGoodsView(request):
    return render_to_response_wrapper(request,"allGoods.html")
def unlabeledGoodsView(request):
    return render_to_response_wrapper(request,"unlabeledGoods.html")
