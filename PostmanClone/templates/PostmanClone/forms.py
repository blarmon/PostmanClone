from django import forms

class ApiForm(forms.Form):
    baseURL = forms.CharField(label = "Base URL:")