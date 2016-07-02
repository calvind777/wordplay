from django import forms

class SongForm(forms.Form):
    songtopic = forms.CharField(label = 'word', max_length=100)