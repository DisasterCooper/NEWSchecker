from rest_framework import generics

from news.models import News, NewsSource
from .permission import IsSuperUserOrReadOnly, IsSuperUser
from .serializers import NewsSerializer, NewsSourceSerializer


class NewsListApiViewGEN(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class NewsSourceListApiViewGEN(generics.ListAPIView):
    queryset = NewsSource.objects.all()
    serializer_class = NewsSourceSerializer
    permission_classes = [IsSuperUser]
