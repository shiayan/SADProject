from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from SADProject.orders.views import *

'''
Created on Jul 21, 2013

@author: Sina
'''
urlpatterns = patterns('SADProject.orders.views', url('^myorders/$', 'myOrdersView'),

                       ('^json/myorders/$', permission_required("orders.view_my_orders")(
                           lambda request: ordersJson(request, filters={'user': request.user}))),
                       (r'^json/orderitem/$', permission_required("orders.view_my_orders")(
                           lambda request: viewOrderJson(request, filters={'order__user': request.user}))),
                       (r'^json/unviewedorders/$', permission_required("orders.view_unviewed_orders")(
                           lambda request: ordersJson(request, show_user=True, show_edit=True, show_status=False,
                                                      filters={'status': 'N'}))),
                       (r'^json/unviewedorderitem$', permission_required("orders.view_unviewed_orders")(
                           lambda request: viewOrderJson(request,edit=True, show_status=False))),
                       (r'^json/allorders/$',
                        permission_required("orders.view_all_orders")(lambda request: ordersJson(request,show_user=True))),
                       (r'^json/allorderitem/$', permission_required("orders.view_all_orders")(lambda request: viewOrderJson(request))),
                       (r'^json/acceptedorders/$', permission_required("orders.view_accepted_orders")(lambda request: ordersJson(request,show_user= True, show_status= False,
                                                                  filters= {'orderitem__status': 'N',
                                                                              'status': 'A'}))),
                       (r'^json/acceptedorderitem/$',  permission_required("orders.view_accepted_orders")(lambda request: viewOrderJson(request,edit= False, show_status = False, accepted = True, filters = {'status': 'N'}))),
                       (r'^json/buyorders/$', permission_required("orders.view_buy_orders")(lambda request: ordersJson(request,show_user= True, show_status= False,
                                                             filters= {'orderitem__status': 'P', 'status': 'A'}))),
                       (r'^json/buyorderitem/$',permission_required("orders.view_buy_orders")(lambda request:  viewOrderJson(request,edit= False, show_status= False, accepted = False, filters={'status' : 'P'}))),
                       ('^addorder/$', 'addOrderView'),
                       (r'^do/addorder/$', 'addOrder'),
                       (r'^unviewedorders/$', 'unviewedOrdersView'),
                       (r'^changeorderitem/$', 'changeOrderItem'),
                       (r'^changeorderitemcat/$', 'changeOrderItemCat'),
                       (r'^changeorderitemstatus', 'changeOrderItemStatus'),
                       (r'^deleteorderitem/$', 'deleteOrderItem'),
                       (r'^acceptorder/$', 'acceptOrder'),
                       (r'^deleteorder/$', 'deleteOrder'),
                       (r'^allorders/$', login_required(allOrdersView)),

                       (r'^acceptedorders/$', 'acceptedOrdersView'),


                       (r'^buyorders/$', 'buyOrdersView')

)