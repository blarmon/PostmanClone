from django import forms

class ApiForm(forms.Form):
    baseURL = forms.CharField(label = "Base URL:")
    headersa1 = forms.CharField()
    headersb1 = forms.CharField()
    headersa2 = forms.CharField()
    headersb2 = forms.CharField()
    headersa3 = forms.CharField()
    headersb3 = forms.CharField()
