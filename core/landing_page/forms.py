from django import forms

class URLInputForm(forms.Form):
    url = forms.URLField(label='Enter Article URL')