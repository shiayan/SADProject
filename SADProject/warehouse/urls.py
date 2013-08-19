from django.conf.urls import patterns, include, url
from SADProject.warehouse.views import myGoodsView, myGoodsJson

'''
Created on Jul 21, 2013

@author: Sina
'''
urlpatterns = patterns('SADProject.warehouse.views', url('^addgood/$', 'addGoodView'),

                       
					   (r'^do/addgood/$', 'addGood'),
                       (r'^orderitemlist/$','orderItemList'),
                       (r'^delivery/$',"goodDeliveryView"),
                       (r'^json/delivery/$','deliveryJson'),
					   (r'^allgoods/$', 'allGoodsView'),
                       (r'^mygoods/$','myGoodsView'),
                       (r'^json/mygoods/$','myGoodsJson'),
                       (r'^upload/$','uploadAjax'),
                       (r'^finaldelivery/$','finalDelivery'),
					   (r'^json/allgoods/$', 'allGoodsJson'),
					   (r'^json/categories/$','categoriesJson'),
                       (r'^categories/$','categoriesView'),
                       (r'^addcategory/$','addCategory'),
                       (r'^deletecategory/$','deleteCategory'),
                       (r'^categorylist/$','categoryList'),
                       (r'^changecategory/$','changeCategory'),
                       (r'^changegood/$','changeGood'),
                       (r'^deletegood/$','deleteGood')



)