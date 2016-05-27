from django.conf.urls import include, url
from django.contrib import admin
import search.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'wordplay.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('search.urls')),
    url(r'^$', search.views.home),

]
