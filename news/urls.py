from django.urls import path

from . import views

#  /news/
urlpatterns = [
    path('', views.NewsList.as_view(), name='home'),
    path('<int:news_id>/', views.ShowOneNews.as_view(), name='one_news'),
    ]
