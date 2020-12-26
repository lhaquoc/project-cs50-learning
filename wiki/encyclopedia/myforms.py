from django import forms

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'myfieldclass',
        'placeholder': 'Search'
    }))

class Post(forms.Form):
    title = forms.CharField(label='title')
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Question(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')