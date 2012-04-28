from django import forms

class CustomMenuForm(forms.Form):
    custom_title = forms.CharField(max_length=100)
    custom_url = forms.URLField()

