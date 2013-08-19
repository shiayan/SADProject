from django.conf.urls import patterns, include, url


'''
Created on Jul 21, 2013

@author: Sina
'''
urlpatterns = patterns('SADProject.damaged.views', url(r'^adddamaged/$', 'addDamagedView'),
            (r'^json/add/$','addJson'),
    (r'^json/alldamaged/$','allDamagedJson'),
    (r'^finaladd/$', 'finalAdd'),
    (r'^changedamaged/$','changeDamaged'),
    (r'^deletedamaged/$','deleteDamaged'),
    (r'^returndamaged/$','returnDamaged'),
    (r'^alldamaged/$','allDamagedView'),
    (r'^deliverdamaged/$','deliverDamagedView'),
    (r'^json/deliverdamaged/$','deliverDamagedJson'),
    (r'^finaldamageddeliver/$','finalDamagaedDeliver'))