from django.conf.urls import url

from article import views

urlpatterns=[
    url(r'^$', views.getlist),
    url(r'^(?P<article_id>\d+)+/$', views.article_detail),
    url(r'^category/(?P<category_id>\d+)+/$',views.category_detail)
]