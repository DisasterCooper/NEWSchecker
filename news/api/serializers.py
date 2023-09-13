from rest_framework import serializers
from news.models import News, NewsSource


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"

    def to_representation(self, instance: News) -> dict:
        result: dict = super().to_representation(instance)
        return result


class NewsSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSource
        fields = "__all__"

    def to_representation(self, instance: NewsSource) -> dict:
        result: dict = super().to_representation(instance)
        return result
