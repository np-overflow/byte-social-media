from django import forms

class PostForm(forms.Form):
    author = forms.CharField(label="Author", max_length=100)
    post_identifier = forms.CharField(label="Post ID", max_length=200, required=False)
    platform = forms.ChoiceField(
        choices=(("facebook", "Facebook"),
                 ("instagram", "Instagram"),
                 ("twitter", "Twitter")))
    caption = forms.CharField(max_length=400, widget=forms.Textarea)
    mediaSrc = forms.CharField(widget=forms.Textarea)
