from django.shortcuts import render,HttpResponse,get_object_or_404
from .models import Post
from .forms import create
from django.views.generic import View,ListView
from math import ceil

# Create your views here.
class list_display(ListView):
    template_name = 'post/list_page.html'
    model = Post
    context_object_name = 'data'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        num=Post.objects.all()
        slide=len(num)//3+ceil((len(num)/3)-len(num)//3)
        data['pagenum'] = range(1,slide+1)
        return data
    # def get(self,request,*args,**kwargs):
    #     data=Post.objects.all().order_by('-id')
    #
    #     return render(request,'post/list_page.html',context={'data':data,'titles':'This is listing all the posts'})

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