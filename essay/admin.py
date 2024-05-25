from django.contrib import admin
from .models import GlobalSettings, Essay


class EssayAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "submission_time", "feedback_prompt")
    search_fields = ("title", "body")
    fields = (
        "user",
        "title",
        "body",
        "submission_time",
        "feedback_prompt",
    )  # Include feedback_prompt here
    readonly_fields = ("submission_time",)


admin.site.register(Essay, EssayAdmin)
admin.site.register(GlobalSettings)
