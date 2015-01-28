from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'kater.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)), 
    url(r'^$', 'mysite.views.home'),
    url(r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^home/', 'mysite.views.home'),	
    url(r'^login/', 'mysite.views.login'),
    url(r'^signup/', 'mysite.views.signup'),
    url(r'^create_user/', 'mysite.views.create_user'),
    url(r'^get_items/', 'mysite.views.get_items'),
    url(r'^order_now/', 'mysite.views.order_now'),
]
