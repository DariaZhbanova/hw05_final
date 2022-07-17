# from django.views.decorators.cache import cache_page
import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render)
from .forms import PostForm, CommentForm
from .models import Group, Post, User, Follow


def my_own_paginator(queryset, request):
    paginator = Paginator(queryset, settings.LIMIT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


# @cache_page(20)
def index(request):
    page_obj = my_own_paginator(Post.objects.all(), request)
    now = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    context = {
        'page_obj': page_obj,
        'now': now,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    page_obj = my_own_paginator(group.posts.all(), request)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    page_obj = my_own_paginator(Post.objects.filter(
        author=author), request)
    user = request.user
    following = user.is_authenticated and author.following.exists()
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm(request.POST or None)
    following = (
        request.user.is_authenticated
        and post.author.following.filter(user=request.user).exists()
    )
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'author': post.author,
        'following': following,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if request.method == 'POST':
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('posts:profile', username=request.user)
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post_id and request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/post_create.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect('posts:post_detail', post_id=post_id)


login_required
def follow_index(request):
    user = request.user
    page_obj = my_own_paginator(Post.objects.filter(author__following__user=request.user), request)
    context = {
        'user': user,
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)

@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    user = request.user
    if author != user:
        Follow.objects.get_or_create(user=user, author=author)
    return render(request, 'posts/follow.html')


@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    user = request.user
    Follow.objects.get(user=user, author=author).delete()
    return render(request, 'posts/follow.html')
