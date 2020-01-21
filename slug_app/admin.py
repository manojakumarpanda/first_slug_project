from django.contrib import admin
from .models import Post

# Register your models here.

class Post_Admin(admin.ModelAdmin):
    list_display = ['title','slug','time_stamp']
    #list_editable = ['title','slug']

admin.site.register(Post,Post_Admin)