from django.conf.urls import url

from author import views

urlpatterns=[
    url(r'^updatearticle/+(?P<article_id>\d+)+/$',views.update_article),
    url(r'^insertarticle/$',views.insertarticle),
    url(r'^viewauthor/+(?P<author_id>\d+)+/$',views.view_author),
    url(r'^login/$',views.login),
    url(r'^forgotpassword/$',views.forgotpassword,name='forgot'),
    url(r'^verifyotp/(?P<author_id>\d+)+/$',views.verifyotp,name='verifyotp'),
    url(r'^setpassword/(?P<author_id>\d+)+/$',views.setpassword,name='setpassword'),
    url(r'^logout/$',views.logout),
    url(r'^register/$',views.register),
    url(r'^dashboard/',views.dashboard),
    url(r'^updateinfo/',views.update_personal_info)

]