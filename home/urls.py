from django.conf.urls import url

from home import views

urlpatterns=[
    url(r'^$',views.home),
    url(r'^contact_us/$',views.contact_us_form,name='contact_us'),
    url(r'^about_us/$',views.about_us,name='about_us')
    ]