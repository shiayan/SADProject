# -*- coding: UTF-8 -*-
from django.views.generic.base import TemplateView
from SADProject.warehouse.models import Category
from models import Order,OrderItem

from django.http import HttpResponse
from django.core.context_processors import csrf
import datetime
import json
from django_jalali.db.models import jDateField
from django.shortcuts import render_to_response

def render_to_response_wrapper(request,template):

    c = {}
    c.update(csrf(request))
    return render_to_response(template,c);

def jsonListGenerator(request,columns,data,template,my_dict = {},default_filters = {}):
    filters = ['__gte','__lte','']
    args = default_filters
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
        iDisplayStart = int(request.GET['iDisplayStart'])
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

def changeQuerySet(request,columns,queryset):
    args = {}
    data = request.POST
    pk = int(data['pk'])
    for column in columns:
        if column in data:
            args.update({column:data[column]})

    queryset.filter(pk = pk).update(**args)
    return HttpResponse("Changed");
def ordersJson(request,show_status=True,show_user=False,show_edit=False,filters={}):
    columns = ['pk', 'user', 'submitDate', 'status']
    data = Order.objects.all()
    return jsonListGenerator(request = request, columns = columns, data = data, template = "json/order.json",
                             my_dict={"show_edit":show_edit,"show_status":show_status,"show_user":show_user},
                             default_filters=filters)


def viewOrderJson(request,edit=False,show_status=True,accepted=False,filters={}):
    columns = ['pk','category__name','name','description','quantity','status','order']

    data = OrderItem.objects.all()
    return jsonListGenerator(request = request, columns = columns, data = data,
                             template = "json/orderitem.json",my_dict={"edit":edit,"show_status":show_status,"accepted":accepted},
                             default_filters=filters)

def addOrder(request):
    c = request.POST
    tableData = json.loads( c['tableData']);

    today = jDateField();
    today = today.to_python(datetime.datetime.now())

    order = Order(user=1,submitDate=today)
    order.save()
    #print tableData
    for order_item in tableData:
         #print order_item[2]
         OrderItem(order=order,
                               name=order_item[0],
                               category=Category.objects.filter(pk=order_item[4])[0],
                               quantity=int(order_item[2]),
                               description = order_item[5],
                               status=OrderItem.ORDER_ITEM_STATUS_CHOICES[0][0]
         ).save()
    c = {'rlink' : '../../myorders/' , 'success' : "سفارش شما با موفقیت ثبت شد تا لحظاتی دیگر به فهرست سفارشاتتان خواهید رفت"}
    return render_to_response("success.html",c);

def deleteFromQuerySet(request,queryset):
    pk = int(request.POST['pk'])
    queryset.filter(pk = pk).delete();
    return HttpResponse("Deleted");

def changeOrderItem(request):
    data = request.POST
    columns = ["name","description","quantity","category","status"]
    return changeQuerySet(request,columns,OrderItem.objects)

def acceptOrder(request):
    columns = ["status"]
    return changeQuerySet(request,columns,Order.objects);

def deleteOrderItem(request):
    return deleteFromQuerySet(request,OrderItem.objects);



def deleteOrder(request):
    return deleteFromQuerySet(request,Order.objects)


def unviewedOrdersView(request):
    return render_to_response_wrapper(request,"unacceptedOrders.html")

def myOrdersView(request):
    return render_to_response_wrapper(request,"myOrders.html")

def allOrdersView(request):
    return render_to_response_wrapper(request,"adminAllOrders.html")

def acceptedOrdersView(request):
    return render_to_response_wrapper(request,"acceptedorders.html")

def buyOrdersView(request):
    return render_to_response_wrapper(request,"buyorders.html")

def addOrderView(request):
     return render_to_response_wrapper(request,"addorder.html")

