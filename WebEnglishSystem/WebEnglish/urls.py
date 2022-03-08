from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from . import views



routers = routers.DefaultRouter()
routers.register('categories',views.CategoryViewSet,'category')
routers.register('user',views.UserViewsSet,'user')
routers.register('multiplechoice',views.MultipleChoiceViewSet,'multiplechoice')

urlpatterns = [
    path('',include(routers.urls)),
    path('oauth2-info/', views.AuthInfo.as_view())
]