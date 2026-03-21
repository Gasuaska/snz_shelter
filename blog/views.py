from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from blog.models import Category, Post
from dogs.views import render_md

def pages_paginator(request, post_list, posts_per_page=10):
    return (Paginator(post_list, posts_per_page).
            get_page(request.GET.get('page')))


def blog_list(request):
    posts = Post.objects.published().select_related_set()
    page_obj = pages_paginator(request, posts)
    for post in page_obj:
        post.html_text = render_md(post.text)
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        post = get_object_or_404(Post.objects.published(), id=post_id)
    post.html_text = render_md(post.text)
    return render(request,
                  'blog/detail.html',
                  {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category,
                                 slug=category_slug, is_published=True)
    posts = (category.posts
             .published()
             .select_related_set())
    for post in posts:
        post.html_text = render_md(post.text)
    page_obj = pages_paginator(request, posts)
    return render(request, 'blog/category.html', {'page_obj': page_obj,
                                                  'category': category})
