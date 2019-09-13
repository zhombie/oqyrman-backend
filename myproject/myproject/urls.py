"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from webapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', book_list),
    path('<int:id>/', book_detail, name="detail"),
    path('book_create/', book_create),
    path('book_delete/<int:id>', book_delete),
    path('book_update/<int:id>', book_update),
    path('section/<int:pk>', book_section_list),
    path('api/', BookList.as_view()),
    path('api/<int:pk>/', BookDetail.as_view(), name="detail_api"),
    path('api/section=<int:pk>', BookSectionList.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
