from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'image/(?P<id>\d+)$', views.ShowImage.as_view()),
    url(r'$', views.SearchView.as_view()),
)
