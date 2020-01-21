"""slug_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path
from django.conf.urls import static
from django.conf.urls import url
from django.conf.urls.static import serve,settings
from slug_app.models import Post
from slug_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.list_display,name='list_display'),
    path('list_display/',views.list_display,name='list_page'),
    path('create/',views.create_post,name='create_display'),
    path('detail/<str:slug>/',views.detail_display,name='detail_page'),
    #re_path(r'^media/image/(?P<path>.*)$', 'django.views.static',{'document_root': settings.MEDIA_ROOT})
]#+re_path['django.views.static.serve',{'document_root': settings.MEDIA_ROOT},]

if settings.DEBUG:
    urlpatterns+=[
        url(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})
    ]