from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',('^$','SADProject.views.showIndex'),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^order/',include('SADProject.orders.urls')),
                       (r'^accounts/',include('SADProject.myUser.urls')),
					   (r'^warehouse/',include('SADProject.warehouse.urls'))
                       # Examples:
                       # url(r'^$', 'SADProject.views.home', name='home'),
                       # url(r'^SADProject/', include('SADProject.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)),
)

