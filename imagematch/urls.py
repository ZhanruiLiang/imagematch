from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
import image_match_app

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'imagematch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^main/', include('image_match_app.urls')),
    url(r'^image/(?P<id>\d+)$', image_match_app.views.ShowImage.as_view()),

    url(r'^admin/', include(admin.site.urls)),
    # For debug purpose only
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
