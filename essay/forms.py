from django import forms
from .models import Essay
import re


class EssayForm(forms.ModelForm):
    class Meta:
        model = Essay
        fields = ["title", "body"]

    def clean_body(self):
        body = self.cleaned_data.get("body")
        # Use regex to find words, which includes handling spaces and punctuation properly
        word_list = re.findall(r"\b\w+\b", body)
        word_count = len(word_list)
        if word_count > 500:
            raise forms.ValidationError(
                f"The essay body cannot exceed 500 words. Currently, it has {word_count} words."
            )
        return body
