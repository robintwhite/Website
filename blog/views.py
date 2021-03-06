from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from .models import Post, Comment, Category
from .forms import CommentForm, PostForm
import random

# Create your views here.
def index(request):
    last = Post.objects.count() - 1
    ind = random.randint(0, last)
    post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0] #Post.objects.all()[ind]
    posts = Post.objects.all()
    categories = Category.objects.all()
    category = Category.objects.get(title = post.category)
    latest_post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0]
    return render(request, 'blog/index.html', {'post': post, 'posts': posts, 'categories': categories, 'category': category, 'latest_post': latest_post})

def projects(request):
    categories = Category.objects.all()
    latest_post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0]
    return render(request, 'blog/projects.html', {'categories': categories, 'latest_post': latest_post})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    categories = Category.objects.all()
    latest_post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0]
    return render(request, 'blog/post_list.html', {'posts': posts, 'categories': categories, 'latest_post': latest_post})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()
    category = Category.objects.get(title = post.category)
    latest_post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0]
    return render(request, 'blog/post_detail.html', {'post': post, 'category': category, 'categories': categories, 'latest_post': latest_post})

def category_list(request):
    categories = Category.objects.all() # this will get all categories, you can do some filtering if you need (e.g. excluding categories without posts in it)
    latest_post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0]
    return render (request, 'blog/category_list.html', {'categories': categories, 'latest_post': latest_post}) # blog/category_list.html should be the template that categories are listed.

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    categories = Category.objects.all()
    posts = Post.objects.filter(category=category)
    latest_post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0]
    return render(request, 'blog/category_detail.html', {'category': category, 'categories': categories, 'posts': posts, 'latest_post': latest_post}) # in this template, you will have access to category and posts under that category by (category.post_set).

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_edit(request, pk):

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return render(request, 'blog/post_detail.html', {'post': post})
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
