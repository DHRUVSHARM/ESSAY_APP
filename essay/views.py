import os
from django.shortcuts import render, redirect
from django.contrib.auth import logout
import openai
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Essay, GlobalSettings
from .forms import EssayForm
from django.contrib.auth.decorators import login_required
import json
import logging

from essay_in.settings import *

# Create your views here.

from django.shortcuts import get_object_or_404

openai.api_key = OPENAI_API_KEY


def home(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def full_submission(request, essay_id):
    essay = get_object_or_404(Essay, id=essay_id, user=request.user)
    return render(request, "essays/full_submission.html", {"essay": essay})


@login_required
def full_feedback(request, essay_id):
    essay = get_object_or_404(Essay, id=essay_id, user=request.user)
    return render(request, "essays/full_feedback.html", {"essay": essay})


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@login_required
def submit_essay(request):
    if request.method == "POST":
        form = EssayForm(request.POST)
        if form.is_valid():
            essay = form.save(commit=False)
            essay.user = request.user
            essay.submission_time = timezone.now()  # Set submission time

            # Fetch the latest global feedback prompt if not set
            if not essay.feedback_prompt:
                global_settings = GlobalSettings.objects.first()
                if global_settings:
                    essay.feedback_prompt = global_settings.default_feedback_prompt

            essay.save()

            # Use the feedback prompt from the model and append standard instructions
            prompt = (
                f"{essay.feedback_prompt}\n\n"
                "Take the following essay title and body as input:\n"
                f"Essay Title: {essay.title}\n"
                f"Essay Body: {essay.body}\n\n"
                "Provide the feedback in the following pure JSON format without any additional text or formatting:\n"
                "{\n"
                '  "spelling_mistake_count": <number>,\n'
                '  "spelling_mistakes": [\n'
                '    {"word": "<misspelled_word>", "start_index": <start_index>, "end_index": <end_index>},\n'
                "    ...\n"
                "  ],\n"
                '  "related_to_title": <true_or_false>,\n'
                '  "quality_score": <score_out_of_10>\n'
                "}"
            )
            logger.info("Generated prompt: %s", prompt)
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Use a valid model name
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                    ],
                )
                logger.info("Received response from OpenAI: %s", response)
                feedback = response.choices[0].message["content"].strip()

                try:
                    # Attempt to parse the feedback as JSON
                    feedback_data = json.loads(feedback)
                    essay.spelling_mistake_count = feedback_data.get(
                        "spelling_mistake_count", 0
                    )
                    essay.spelling_mistakes = feedback_data.get("spelling_mistakes", [])
                    essay.related_to_title = feedback_data.get(
                        "related_to_title", False
                    )
                    essay.essay_score = feedback_data.get("quality_score", 0)

                except (json.JSONDecodeError, KeyError) as e:
                    # Handle cases where feedback is not in expected format
                    messages.error(request, f"Failed to parse feedback: {str(e)}")
                    logger.error("Failed to parse feedback: %s", str(e))
                    essay.spelling_mistake_count = 0
                    essay.spelling_mistakes = []
                    essay.related_to_title = False
                    essay.essay_score = 0

                essay.save()
                messages.success(request, "Essay submitted successfully with feedback.")
            except Exception as e:
                essay.delete()
                messages.error(
                    request, f"An error occurred while generating feedback: {str(e)}"
                )
                logger.error("An error occurred while generating feedback: %s", str(e))
                return render(request, "essays/submit_essay.html", {"form": form})

            return redirect("essay_list")
    else:
        form = EssayForm()
    return render(request, "essays/submit_essay.html", {"form": form})


@login_required
def essay_list(request):
    essays = Essay.objects.filter(user=request.user).order_by("-submission_time")
    return render(request, "essays/essay_list.html", {"essays": essays})
