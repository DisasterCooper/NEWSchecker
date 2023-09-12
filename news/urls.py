from django.urls import path

from . import views

#  /news/
urlpatterns = [
    path('', views.NewsList.as_view(), name='home'),
    ]
