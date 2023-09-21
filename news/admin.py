import textwrap

from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["_title",
                    "content",
                    "link",
                    "published",
                    ]
    search_fields = ["title", "content"]

    @admin.display(description="Title")
    def _title(self, obj: News):
        return textwrap.wrap(obj.title, 25)[0] + "..."


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["session_key", "_session_data", "expire_date"]

    def _session_data(self, obj: Session):
        return obj.get_decoded()
