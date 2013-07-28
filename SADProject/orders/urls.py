from django.conf.urls import patterns, include, url

from views import viewOrderJson

'''
Created on Jul 21, 2013

@author: Sina
'''
urlpatterns = patterns('SADProject.orders.views', url('^myorders/$', 'myOrdersView'),
                       ('^addorder/$', 'addOrderView'),
                       ('^json/myorders/$', 'ordersJson',{'filters':{'user': '1'}}),
                       (r'^json/orderitem/$', 'viewOrderJson'),
                       (r'^json/unviewedorderitem$', 'viewOrderJson', {'edit': True, 'show_status': False}),
                       (r'^do/addorder/$', 'addOrder'),
                       (r'^unviewedorders/$', 'unviewedOrdersView'),
                       (r'^json/unviewedorders/$','ordersJson', {'show_user': True, 'show_edit': True,'show_status':False},{'filters':{'status':'N'}}),
                       (r'^changeorderitem/$', 'changeOrderItem'),
                       (r'^deleteorderitem/$', 'deleteOrderItem'),
                       (r'^acceptorder/$', 'acceptOrder'),
                       (r'^deleteorder/$', 'deleteOrder'),
                       (r'^allorders/$', 'allOrdersView'),
                       (r'^json/allorders/$', 'ordersJson', {'show_user': True}),
                       (r'^acceptedorders/$', 'acceptedOrdersView'),
                       (r'^json/acceptedorders/$','ordersJson',{'show_user':True,'show_status':False},{'filters':{'orderitem__status':'N','status':'A'}}),
    (r'^json/acceptedorderitem/$','viewOrderJson', {'edit':False,'show_status' :False,'accepted' : True},{'filters':{'status':'N'}}),
    (r'^buyorders/$', 'buyOrdersView'),
    (r'^json/buyorders/$','ordersJson',{'show_user':True,'show_status':False},{'filters':{'orderitem__status':'P','status':'A'}}),
    (r'^json/buyorderitem/$','viewOrderJson', {'edit':False,'show_status' :False,'accepted' : False})
)