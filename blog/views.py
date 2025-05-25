import folium

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from blog.models import Comment
from blog.models import Post
from sensive_blog.settings import COMPANY_COORDINATES
from django.shortcuts import render
from .data import SLIDER_POSTS, BLOG_POSTS


def index(request):
    context = {
        'posts': SLIDER_POSTS,
        'blog_posts': BLOG_POSTS
    }
    return render(request, 'index.html', context)

def serialize_post(post):
    return {
        "title": post.title,
        "text": post.text,
        "author": post.author.username,
        "comments_amount": Comment.objects.filter(post=post).count(),
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
    }





def post_detail(request, slug):
    """
    Вьюхи не оптимизированы, потому что в последней задаче модуля Django ORM нужно их оптимизировать как раз на примере этого сайта.
    """
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        })

    serialized_post = {
        "title": post.title,
        "text": post.text,
        "author": post.author.username,
        "comments": serialized_comments,
        'likes_amount': post.likes.count(),
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
    }

    context = {
        'post': serialized_post,
    }
    return render(request, 'blog-details.html', context)


def contact(request):
    """
    Вьюхи не оптимизированы, потому что в последней задаче модуля Django ORM нужно их оптимизировать как раз на примере этого сайта.
    """
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    folium_map = folium.Map(location=COMPANY_COORDINATES, zoom_start=12)
    folium.Marker(
        COMPANY_COORDINATES,
        tooltip="Мы здесь",
    ).add_to(folium_map)
    html_map = folium_map._repr_html_()
    return render(request, 'contact.html', {"html_map": html_map})
