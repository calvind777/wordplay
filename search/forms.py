from django import forms

class SongForm(forms.Form):
    songname = forms.CharField(label = 'word', max_length=100)