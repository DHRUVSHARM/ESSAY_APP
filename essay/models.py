from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class GlobalSettings(models.Model):
    default_feedback_prompt = models.TextField(
        default=(
            "Please provide feedback on the following essay:\n\n"
            "1. Count the number of spelling mistakes and provide the list of misspelled words with their start and end indexes.\n"
            "2. Determine if the content of the essay is related to the title (yes/no).\n"
            "3. Calculate a quality score for the essay out of 10."
        )
    )

    def __str__(self):
        return "Global Settings"


class Essay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    submission_time = models.DateTimeField(
        default=timezone.now
    )  # Field to store submission time

    # Feedback fields
    spelling_mistake_count = models.IntegerField(blank=True, null=True)
    spelling_mistakes = models.JSONField(
        blank=True, null=True
    )  # Store start and end indexes as JSON
    quality_score = models.FloatField(blank=True, null=True)
    related_to_title = models.BooleanField(
        default=False
    )  # Field to store if content is related to the title
    essay_score = models.IntegerField(
        blank=True, null=True
    )  # Field to store the essay score out of 10
    feedback_prompt = models.TextField(blank=True)  # Removed default value here

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.feedback_prompt:
            global_settings = GlobalSettings.objects.first()
            if global_settings:
                self.feedback_prompt = global_settings.default_feedback_prompt
        super().save(*args, **kwargs)
