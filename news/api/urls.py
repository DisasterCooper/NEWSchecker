from django.urls import path

from . import views

# /api/

urlpatterns = [
    path("news", views.NewsListApiViewGEN.as_view()),
    path("news_sourse", views.NewsSourceListApiViewGEN.as_view()),
]
