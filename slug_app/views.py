from django.shortcuts import render,HttpResponse,get_object_or_404
from .models import Post
from .forms import create

# Create your views here.
def list_display(request):
    data=Post.objects.all()
    return render(request,'post/list_page.html',context={'data':data,'titles':'This is listing all the posts'})

def detail_display(request,slug=None):
    data=get_object_or_404(Post,slug=slug)

    return render(request,'post/detail_page.html',context={'data':data,'titles':'This is the detail of {}'.format(data.title)})

def create_post(request):
    forms=create()
    if request.method=='POST':
        form=create(request.POST,request.FILES)
        if form.is_valid():
            tit=form.cleaned_data.get('title')
            print(tit)
            form.save()
            return HttpResponse('data is created successfully')
        raise form.errors
    return render(request,'post/create.html',context={'form':forms,'titles':'upload_data'})