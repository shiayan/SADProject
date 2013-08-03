from django.conf.urls import patterns, include, url

'''
Created on Jul 21, 2013

@author: Sina
'''
urlpatterns = patterns('SADProject.warehouse.views', url('^addgood/$', 'addGoodView'),
                       
					   (r'^do/addgood/$', 'addGood'),
                       
					   
					   
					   (r'^allgoods/$', 'allGoodsView'),
					   
					   (r'^json/allgoods/$', 'allGoodsJson'),
					   (r'^unlabeledgoods/$', 'unlabeledGoodsView'),
					   (r'^json/unlabeledgoods/$', 'unlabeledGoodsJson')
)