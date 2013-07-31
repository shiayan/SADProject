from django.conf.urls import patterns, include, url

from views import viewOrderJson

'''
Created on Jul 21, 2013

@author: Sina
'''
urlpatterns = patterns('SADProject.warehouse.views', url('^myorders/$', 'myOrdersView'),
                       ('^addorder/$', 'addOrderView'),
					   
					   ('^addgood/$', 'addGoodView'),
                       ('^json/myorders/$', 'myOrdersJson'),
                       (r'^json/orderitem/$', 'viewOrderJson'),
                       (r'^json/unviewedorderitem$', 'viewOrderJson', {'edit': True, 'show_status': False}),
                       (r'^do/addorder/$', 'addOrder'),
					   
					   (r'^do/addgood/$', 'addGood'),
                       (r'^unviewedorders/$', 'unviewedOrdersView'),
                       (r'^json/unviewedorders/$', 'unviewedOrdersJson'),
                       
					   
					   (r'^changeorderitem/$', 'changeOrderItem'),
                       (r'^deleteorderitem/$', 'deleteOrderItem'),
                       (r'^acceptorder/$', 'acceptOrder'),
                       (r'^deleteorder/$', 'deleteOrder'),
                       (r'^allorders/$', 'allOrdersView'),
                       
					   (r'^allgoods/$', 'allGoodsView'),
					   (r'^json/allorders/$', 'allOrdersJson'),
    
					   (r'^json/allgoods/$', 'allGoodsJson'),
					   (r'^acceptedorders/$', 'acceptedOrdersView'),
                       (r'^json/acceptedorders/$','acceptedOrdersJson'),
    (r'^json/acceptedorderitem/$','viewOrderJson', {'edit':False,'show_status' :False,'accepted' : True}),
    (r'^buyorders/$', 'buyOrdersView'),
    (r'^json/buyorders/$','buyOrdersJson'),
    (r'^json/buyorderitem/$','viewOrderJson', {'edit':False,'show_status' :False,'accepted' : False})
)