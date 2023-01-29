from django.contrib import admin
from django.urls import path, include

from app.views import index, about, contact_view, render, blog, login_view, single_post, logout_view


urlpatterns = [
    path('', index, name='index'),
    path('about/', about,name='about'),
    path('contact/',contact_view,name='contact'),
    path('single-post/<int:product_id>', single_post,name='single-post'),
    path('blog/', blog, name='blog'),
    path('login/', login_view, name='login'),
    path('logout/',logout_view,name='logout'),

]
# adasd