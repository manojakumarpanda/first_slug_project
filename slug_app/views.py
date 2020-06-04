from django.shortcuts import render,HttpResponse,get_object_or_404
from .models import Post
from .forms import create
from django.views.generic import View,ListView
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from math import ceil

# Create your views here.
class list_display(ListView):
    # def get(self,request,*args,**kwargs):
    #     user_list = Post.objects.all()
    #     page = request.GET.get('page', 1)
    #
    #     paginator = Paginator(user_list, 10)
    #     try:
    #         users = paginator.page(page)
    #     except PageNotAnInteger:
    #         users = paginator.page(1)
    #     except EmptyPage:
    #         users = paginator.page(paginator.num_pages)
    #
    #     return render(request, 'core/user_list.html', {'users': users})
    template_name = 'post/list_page.html'
    model = Post
    context_object_name = 'data'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        num=Post.objects.all()
        slide=len(num)//5+ceil((len(num)/5)-len(num)//5)
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