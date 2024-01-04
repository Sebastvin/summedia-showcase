from django import forms
import pycountry
from summedia.level import SimplificationLevel


class TextComplexityForm(forms.Form):
    COMPLEXITY_CHOICES = [(level.name, level.value) for level in SimplificationLevel]

    complexity = forms.ChoiceField(choices=COMPLEXITY_CHOICES)


class LanguageForm(forms.Form):
    LANGUAGE_CHOICES = [
        (language.alpha_2, language.name)
        for language in pycountry.languages
        if hasattr(language, "alpha_2")
    ]

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)


class URLInputForm(forms.Form):
    url = forms.URLField(
        label="Enter Article URL",
        widget=forms.URLInput(attrs={"class": "full-width-textarea"}),
    )


class TextInputForm(forms.Form):
    text = forms.CharField(
        label="Enter text",
        max_length=1500,
        widget=forms.Textarea(attrs={"class": "full-width-textarea"}),
    )


class NumericInputForm(forms.Form):
    number = forms.IntegerField(
        label="Enter words number",
        min_value=1,
        max_value=500,
        initial=100,
        widget=forms.NumberInput(attrs={"class": "w-50"}),
    )
