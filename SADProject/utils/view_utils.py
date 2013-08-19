# -*- coding: UTF-8 -*-
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from django.utils import simplejson

__author__ = 'Sina'


def render_to_response_wrapper(request,template,my_dict= {}):
    apps = [
			{'title' : 'انبارداری' , 'name':'warehouse' ,'perm' : 'warehouse' , 'icon' : 'book', 'links' : [
				{ 'title' : 'لیست کالاها' , 'url' : '/warehouse/allgoods/' , 'perm' : 'warehouse.view_all_goods' },
				{ 'title' : 'ثبت کالای جدید' , 'url' : '/warehouse/addgood/' , 'perm' : 'warehouse.add_new_good' },
				{ 'title' : 'ثبت تحویل کالا' , 'url' : '/warehouse/delivery/' , 'perm' : 'warehouse.view_all_goods' },
				{ 'title' : 'دسته‌ها' , 'url' : '/warehouse/categories/' , 'perm' : 'warehouse.change_categories' }]
			} ,
			
			{'title' : 'سفارش‌ها' , 'name':'order' ,'perm' : 'orders' , 'icon' : 'file-alt', 'links' : [
				{ 'title' : 'سفارش‌های من' , 'url' : '/order/myorders/' , 'perm' : 'orders.view_my_orders' },
				{ 'title' : 'ثبت سفارش' , 'url' : '/order/addorder/' , 'perm' : 'orders.add_new_order' },
				{ 'title' : 'سفارش‌های بررسی نشده' , 'url' : '/order/unviewedorders/' , 'perm' : 'orders.view_unviewed_orders' },
				{ 'title' : 'کل سفارش‌ها' , 'url' : '/order/allorders/' , 'perm' : 'orders.view_all_orders' },
				{ 'title' : 'سفارش‌های تایید شده' , 'url' : '/order/acceptedorders/' , 'perm' : 'orders.view_accepted_orders' },
				{ 'title' : 'سفارش‌های غیر موجود' , 'url' : '/order/buyorders/' , 'perm' : 'orders.view_buy_orders' }]
			} ,
			{'title' : 'کاربران' , 'name':'accounts' ,'perm' : 'auth' , 'icon' : 'user', 'links' : [
				{ 'title' : 'مدیریت کاربران' , 'url' : '/accounts/users/' , 'perm' : 'auth.change_user' }]
			}
			
			
			
	
	
	
	]
    apps_file = open('menu.json')
    apps = json.loads(apps_file.read())
    apps_file.close()
    my_dict.update(csrf(request))
    my_dict.update({'apps' : apps})

    my_dict.update({'current_app' : request.path.split('/')[1]})
    my_dict.update({'current_url' : request.path})
    my_dict.update({'request' : request})
    return render_to_response(template,my_dict,context_instance=RequestContext(request));


def jsonListGenerator(request,columns,data,template,my_dict = {},default_filters = {}):
    filters = ['__gte','__lte','']
    args = {}
    args.update(default_filters)

    for column in columns:
        for fltr in filters:
            if column + fltr in request.GET:
                args.update({column + fltr : request.GET[column+fltr]})


    data = data.filter(**args).distinct()

    iTotalRecords = data.count()
    iTotalDisplayRecords = data.count()

    if 'iSortCol_0' in request.GET:
        order_str = columns[int(request.GET['iSortCol_0'])]
        if request.GET['sSortDir_0'] == 'desc':
            order_str =  '-' + order_str

        order_arg = []
        order_arg.append(order_str)
        data = data.order_by(*order_arg)

    if 'iDisplayStart' in request.GET:
        iDisplayStart =  int(request.GET['iDisplayStart'])
        iDisplayLength =  int(request.GET['iDisplayLength'])
    else:
        iDisplayStart = 0
        iDisplayLength  = iTotalRecords

    iDisplayEnd = min(iDisplayLength + iDisplayStart ,data.count() )
    if 'sEcho' in request.GET:
        sEcho = int(request.GET['sEcho'])
    else:
        sEcho = 1

    if iDisplayLength > 0:
        data = data[iDisplayStart:iDisplayEnd]

    my_dict.update({"objects" : data,'iTotalRecords' : iTotalRecords , 'iTotalDisplayRecords' : iTotalDisplayRecords,'sEcho' : sEcho})
    return render_to_response(template,my_dict,mimetype='application/json')


def deleteFromQuerySet(request,queryset):
    pk = int(request.POST['pk'])
    queryset.filter(pk = pk).delete();
    return HttpResponse("Deleted");