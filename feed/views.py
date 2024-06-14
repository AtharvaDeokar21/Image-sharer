#from django.shortcuts import render
#The above is default for function based views
# Create your views here.

from typing import Any
from django.contrib import messages
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView, DetailView ,FormView
from .forms import PostForm
from .models import Post

class HomePageView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-id')
        
        return context 
    
class PostDetailView(DetailView):
    template_name = "detail.html"
    model = Post
    
class AddPostView(FormView):
    template_name = "new_post.html"
    form_class = PostForm
    success_url = "/"
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        #Create a new post
        
        new_object = Post.objects.create(
            text = form.cleaned_data['text'],
            image = form.cleaned_data['image']
        )
        messages.add_message(self.request, messages.SUCCESS, 'Your post was successful')
        return super().form_valid(form)
    