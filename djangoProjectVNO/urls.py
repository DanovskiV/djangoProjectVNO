"""VNO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.urls import path
from django.views.generic.base import TemplateView

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    
    url('admin/', admin.site.urls),
    url(r'^ckeditor', include('ckeditor_uploader.urls')),
    url(r'^', include(('blog.urls', 'blog'), namespace='blog')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^account/', include('account.urls')),
    # url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^questions/', include(('questions.urls', 'questions'), namespace="questions")),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
