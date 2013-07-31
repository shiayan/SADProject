from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
urlpatterns = patterns('' ,(r'^login/$', login,{'template_name' : 'login.html'}),
                        (r'^logout/$', logout,{'next_page': '/accounts/login/'}))
urlpatterns += patterns('SADProject.myUser.views',(r'^users/$','usersView'),
    (r'^json/users/','usersJson'),
    (r'^changeuser/$','changeUser'),
    (r'^deleteuser/$','deleteUser'),
    (r'^adduser/$','addUser'))
