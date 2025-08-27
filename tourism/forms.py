from django import forms

class SearchForm(forms.Form):
    district = forms.CharField(max_length=100, label='District Name')