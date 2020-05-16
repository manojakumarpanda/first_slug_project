from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=100,blank=False,null=False)
    slug=models.SlugField(max_length=200,unique=True)
    image=models.ImageField(upload_to='immage',
                            null=True,
                            blank=True,
                            width_field='width_field',
                            height_field='height_field'
                            )
    context=models.CharField(max_length=300)
    updated_at=models.DateTimeField(auto_created=False,auto_now=True)
    time_stamp=models.DateTimeField(auto_created=True,auto_now=True)
    width_field=models.IntegerField(default=0)
    height_field=models.IntegerField(default=0)


    def __str__(self):
        return 'title is:{}'.format(self.title)
    class Meta:
        ordering=['-id']

    def get_absolute_url(self):
        return reverse('detail_page',kwargs={'slug':self.slug})


# def create_slug(instance,new_slug=None):
#     slug=slugify(instance.title)
#     if new_slug is not None:
#         slug=new_slug
#     qs=Post.objects.filter(slug=slug).order_by('-id')
#     exists=qs.exists()
#     if exists:
#         new_slug=" {}-{} ".format(slug,qs.first().id)
#         return create_slug(instance,new_slug)
#     return slug

import string
import random
def create_slug(instance,new_slug=None):
    slug=slugify(instance.title)
    if new_slug is not None:
        slug=new_slug
    quary=Post.objects.filter(slug=slug)
    exist=quary.exists()
    if exist:
        random_str=''
        for i in range(7):
            random_str+=random.choice(string.ascii_letters)
        new_slug= '{}-{}'.format(slug,random_str)
        return create_slug(instance,new_slug=new_slug)
    return slug

@receiver(signals.pre_save, sender=Post)
def presave_post_reciver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)
    # slug=slugify(instance.title)
    # return slug



