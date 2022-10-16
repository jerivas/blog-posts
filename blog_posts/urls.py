"""blog_posts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.blog_post_list, name="blog_post_list"),
    path("blog/create", views.blog_post_create, name="blog_post_create"),
    path("blog/<int:pk>", views.blog_post_detail, name="blog_post_detail"),
    path("blog/<int:pk>/update", views.blog_post_update, name="blog_post_update"),
    path("blog/<int:pk>/delete", views.blog_post_delete, name="blog_post_delete"),
]
