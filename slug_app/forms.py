from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout
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


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.healper=FormHelper()
        self.healper.form_method='post'
        self.healper.add_input(layout.Submit('Submit','Create new'))