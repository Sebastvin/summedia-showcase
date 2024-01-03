from django import forms


class URLInputForm(forms.Form):
    url = forms.URLField(label="Enter Article URL")


class TextInputForm(forms.Form):
    text = forms.CharField(
        label="Enter text",
        widget=forms.Textarea(attrs={"class": "full-width-textarea"}),
    )


class NumericInputForm(forms.Form):
    number = forms.IntegerField(label="Enter words number", min_value=1, max_value=500)
