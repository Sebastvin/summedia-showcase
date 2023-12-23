from django import forms


class URLInputForm(forms.Form):
    url = forms.URLField(label="Enter Article URL")


class TextInputForm(forms.Form):
    text = forms.CharField(label="Enter text")
