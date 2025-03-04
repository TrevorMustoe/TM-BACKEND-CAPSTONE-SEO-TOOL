"""hootboost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls import include
from rest_framework import routers
from hootboostapi.views import UserView, NotesView, KeywordView,WebsiteView, Audit_resultView, Audit_Result_KeywordView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', UserView, 'user')
router.register(r'note', NotesView, 'note')
router.register(r'keyword', KeywordView, 'keyword')
router.register(r'website', WebsiteView, 'website')
router.register(r'audit_result', Audit_resultView, 'audit_result')
router.register(r'audit_result_keyword', Audit_Result_KeywordView, 'audit_result_keyword')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
