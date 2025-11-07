from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from blog.forms import PostForm, ProfileForm
from blog.models import Category, Post, User


def pages_paginator(request, post_list, posts_per_page=10):
    return (Paginator(post_list, posts_per_page).
            get_page(request.GET.get('page')))


def blog_list(request):
    posts = Post.objects.published().select_related_set()
    page_obj = pages_paginator(request, posts)
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        post = get_object_or_404(Post.objects.published(), id=post_id)
    return render(request,
                  'blog/detail.html',
                  {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category,
                                 slug=category_slug, is_published=True)
    posts = (category.posts
             .published()
             .select_related_set())
    page_obj = pages_paginator(request, posts)
    return render(request, 'blog/category.html', {'page_obj': page_obj,
                                                  'category': category})


# Профиль:
def profile(request, username):
    author = get_object_or_404(User, username=username,)
    posts = author.posts
    if request.user != author:
        posts = posts.published()
    posts = posts.select_related_set()
    page_obj = pages_paginator(request, posts)
    return render(request, 'blog/profile.html', {'profile': author,
                                                 'page_obj': page_obj})


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/user.html', {'form': form})


# Посты:
@login_required
def create_post(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'blog/create.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('blog:profile', post.author.username)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post_id)

    form = PostForm(request.POST or None, instance=post)

    if not form.is_valid():
        return render(request, 'blog/create.html', {'form': form})

    post = form.save(commit=False)
    post.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', {'form': form})