# -*- coding: UTF-8 -*-
import datetime
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from SADProject.myUser import inform_admin,inform_user,inform_purchase_agent,inform_warehouse_manager

from SADProject.utils.view_utils import render_to_response_wrapper, jsonListGenerator, deleteFromQuerySet
from SADProject.warehouse.models import Category, Good
from models import Order,OrderItem
from django_jalali.db.models import jDateField




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
    if not show_user:
        columns.remove('user')
    if not show_status:
        columns.remove('status')
    return jsonListGenerator(request = request, columns = columns, data = data, template = "json/order.json",
                             my_dict={"show_edit":show_edit,"show_status":show_status,"show_user":show_user},
                             default_filters=filters)


def viewOrderJson(request,edit=False,show_status=True,accepted=False,filters={}):
    columns = ['pk','category__name','quantity','description','status','order']
    if not show_status:
        columns.remove('status')

    data = OrderItem.objects.all()
    return jsonListGenerator(request = request, columns = columns, data = data,
                             template = "json/orderitem.json",my_dict={"edit":edit,"show_status":show_status,"accepted":accepted},
                             default_filters=filters)

permission_required("orders.add_new_order")
def addOrder(request):
    c = request.POST
    tableData = json.loads( c['tableData']);

    today = jDateField();
    today = today.to_python(datetime.datetime.now())

    order = Order(submitDate=today)


    status = OrderItem.ORDER_ITEM_STATUS_CHOICES[0][0]
    order.user = request.user
    isforall = 'isforall' in request.POST and request.POST['isforall']
    if request.user.is_superuser:
        order.status = 'A'
        if isforall:
            status = 'P'
            order.user = None



    order.save()
    #print tableData
    for order_item in tableData:
         #print order_item[2]
         if order_item[3] == '':
             category = None
         else:
             category = Category.objects.filter(pk=order_item[3])[0]

         orderitem=OrderItem(order=order,
                               category=category,
                               quantity=int(order_item[1]),
                               description = order_item[4],
                               status= status  #if it's admin and the order belongs to the public ..., if it's admin the order is accepted
         )
         orderitem.save()
         if request.user.is_superuser and isforall:
             inform_purchase_agent(subject='سفارش نیازمند خرید است',message=render_to_string('mail/buy_orderitem.html',{'orderitem' : orderitem}))

    c = {'rlink' : '../../myorders/' , 'success' : "سفارش شما با موفقیت ثبت شد تا لحظاتی دیگر به فهرست سفارشاتتان خواهید رفت"}

    if request.user.is_superuser:
        if not isforall :
            inform_warehouse_manager( message=render_to_string('mail/order_warehouse_manager.html', {'order': order}),
                                      subject='سفارش نیازمند بررسی است')

    else:
        inform_admin('سفارش جدید', render_to_string('mail/order_added.html', {'order': order}))
    return render_to_response("success.html",c);


permission_required("orders.view_unviewed_orders")
def changeOrderItem(request):
    data = request.POST
    columns = ["description","quantity","category","status"]
    return changeQuerySet(request,columns,OrderItem.objects)

permission_required("orders.view_accepted_orders")
def changeOrderItemCat(request):
    data = request.POST
    columns = ["category"]
    return changeQuerySet(request,columns,OrderItem.objects)

permission_required("orders.view_accepted_orders")
def changeOrderItemStatus(request):
    data = request.POST
    pk = data['pk'];
    instock = int(data['instock']);
    orderitem = OrderItem.objects.get(pk = pk);
    order = orderitem.order
    orderitem.status = 'I'

    if instock < orderitem.quantity:
        new_order_item = OrderItem()
        new_order_item.quantity = orderitem.quantity - instock
        new_order_item.category = orderitem.category
        new_order_item.description = orderitem.description
        new_order_item.status = 'P'
        new_order_item.order = orderitem.order
        new_order_item.save()
        inform_purchase_agent(subject='سفارش نیازمند خرید است',message=render_to_string('mail/buy_orderitem.html',{'orderitem' : new_order_item}))

    if instock == 0:
        orderitem.delete()
    else:
        orderitem.quantity = instock
        orderitem.save()
        inner_q = Good.objects.filter(category=orderitem.category,user=None)[:instock]
        Good.objects.filter(pk__in = inner_q).update(user=order.user)
        inform_user(user=order.user, message=render_to_string('mail/orderitem_available.html', {'orderitem': orderitem}),
                    subject='سفارش شما در انبار موجود است')
    #check and change the status of the order
    if OrderItem.objects.filter(order= order,status='N').count() == 0:
        return HttpResponse('order_changed')
    return HttpResponse("success")

permission_required("orders.view_unviewed_orders")
def acceptOrder(request):
    order=Order.objects.get(pk=int(request.POST['pk']))
    if order.user != None:
        inform_user(user=order.user, message=render_to_string('mail/order_accepted.html', {'order': order}),
                subject='سفارش شما تایید شد')
    inform_warehouse_manager( message=render_to_string('mail/order_warehouse_manager.html', {'order': order}),
                              subject='سفارش نیازمند بررسی است')
    columns = ["status"]

    return changeQuerySet(request,columns,Order.objects)

permission_required("orders.view_unviewed_orders")
def deleteOrderItem(request):
    is_last = False;
    order =  OrderItem.objects.get(pk = request.POST['pk']).order
    if OrderItem.objects.filter(order = order ).count() == 1:
        is_last = True
    result = deleteFromQuerySet(request,OrderItem.objects)
    if is_last:
        order.delete()
        return HttpResponse('order_changed')
    else:
        return result


permission_required("orders.view_unviewed_orders")
def deleteOrder(request):
    order=Order.objects.get(pk=int(request.POST['pk']))
    if order.user != None:
         inform_user(user=order.user, message=render_to_string('mail/order_rejected.html', {'order': order}),
                subject='سفارش شما رد شد')
    return deleteFromQuerySet(request,Order.objects)

permission_required("orders.view_unviewed_orders")
def unviewedOrdersView(request):
    return render_to_response_wrapper(request,"unacceptedOrders.html")

permission_required("orders.view_my_orders")
def myOrdersView(request):
    return render_to_response_wrapper(request,"myOrders.html")

permission_required("orders.view_all_orders")
def allOrdersView(request):
    return render_to_response_wrapper(request,"adminAllOrders.html")

permission_required("orders.view_accepted_orders")
def acceptedOrdersView(request):
    return render_to_response_wrapper(request,"acceptedorders.html")

permission_required("orders.view_buy_orders")
def buyOrdersView(request):
    return render_to_response_wrapper(request,"buyorders.html")

permission_required("orders.add_new_order")
def addOrderView(request):
     return render_to_response_wrapper(request,"addorder.html")

