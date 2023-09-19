from django.db import models


class NewsSource(models.Model):

    id_name = models.IntegerField(primary_key=True)
    source = models.CharField(max_length=200)
    link = models.URLField()

    class Meta:
        db_table = "news_sources"
        ordering = ["id_name"]

    def __str__(self):
        return self.source


class News(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.URLField()
    published = models.DateTimeField()
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE, related_name="news")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="news")

    class Meta:
        db_table = "news"
        ordering = ["-published"]

    def __str__(self):
        return self.title
