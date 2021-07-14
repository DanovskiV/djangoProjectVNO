from django.conf.urls import url
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # post views
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout')
]