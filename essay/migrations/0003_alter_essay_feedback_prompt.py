# Generated by Django 4.2.13 on 2024-05-24 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("essay", "0002_essay_essay_score_essay_related_to_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="essay",
            name="feedback_prompt",
            field=models.CharField(
                default='Please provide feedback on the following essay:\n\n1. Count the number of spelling mistakes and provide the list of misspelled words with their start and end indexes.\n2. Determine if the content of the essay is related to the title (yes/no).\n3. Calculate a quality score for the essay out of 10.\n\nFormat the feedback as JSON with keys: \'spelling_mistake_count\', \'spelling_mistakes\', \'related_to_title\', and \'quality_score\'.\nFor \'spelling_mistakes\', provide a list of dictionaries with \'word\', \'start_index\', and \'end_index\'.\nExample:\n{\n  "spelling_mistake_count": 2,\n  "spelling_mistakes": [\n    {"word": "wong", "start_index": 10, "end_index": 14},\n    {"word": "exampl", "start_index": 30, "end_index": 36}\n  ],\n  "related_to_title": true,\n  "quality_score": 8\n}',
                help_text="Default feedback prompt for evaluating essays.",
                max_length=255,
            ),
        ),
    ]
