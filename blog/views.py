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
        'posts': SLIDER_POSTS,  # Исправлено имя переменной
        'blog_posts': BLOG_POSTS
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    all_posts = SLIDER_POSTS + BLOG_POSTS
    post = next((p for p in all_posts if p['slug'] == slug), None)

    if not post:
        return render(request, '404.html')

    # Добавить пагинацию комментариев при необходимости
    return render(request, 'blog-details.html', {
        'post': post,
        'comments': post.get('comments', [])
    })




def contact(request):

    folium_map = folium.Map(location=COMPANY_COORDINATES, zoom_start=12)
    folium.Marker(
        COMPANY_COORDINATES,
        tooltip="Мы здесь",
    ).add_to(folium_map)
    html_map = folium_map._repr_html_()
    return render(request, 'contact.html', {"html_map": html_map})
