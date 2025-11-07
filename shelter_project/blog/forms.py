from django import forms

from .models import Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {'post': forms.Textarea(),
                   'pub_date': forms.
                   DateTimeInput(attrs={'type': 'datetime-local'})}
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
