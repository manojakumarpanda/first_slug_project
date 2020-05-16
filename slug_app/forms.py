from django import forms
from .models import Post
from django.core.validators import ValidationError

class create(forms.ModelForm):
    # def clean_title(self):
    #     title=self.cleaned_data['title']
    #     print(title)
    #     if len(title) <=5:
    #         raise ValidationError('The title should be greater then 5 charecter')
    #     return title
    # context=forms.CharField(
    #     widget=forms.Textarea()
    # )

    class Meta:
        model=Post
        exclude=('time_stamp','updated_at','slug')

