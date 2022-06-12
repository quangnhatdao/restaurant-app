from django import forms

"""
form for uploading image
"""
class UploadImageForm(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.ImageField()