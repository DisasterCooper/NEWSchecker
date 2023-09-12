
from django.shortcuts import render
from django.views import generic

from .models import News


class NewsList(generic.View):

    @staticmethod
    def get_queryset():
        return News.objects.all() \
            .values("id", "title", "content", "link", "published", "source")

    def get(self, request):
        """
        Displaying all the news on the main page.
        """
        news = self.get_queryset()
        return render(request, "home.html", {"news": news})


