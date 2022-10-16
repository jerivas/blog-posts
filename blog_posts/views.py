from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from . import models


class FilterForm(forms.Form):
    author = forms.ModelChoiceField(
        User.objects.all(), required=False, empty_label="All"
    )

    def filter(self, queryset):
        if author := self.cleaned_data.get("author"):
            queryset = queryset.filter(author=author)
        return queryset


def blog_post_list(request):
    posts = models.BlogPost.objects.all()
    form = FilterForm(data=request.GET)
    if form.is_valid():
        posts = form.filter(posts)
    return render(request, "blog_post_list.html", {"blog_posts": posts, "form": form})


def blog_post_detail(request, pk):
    post = get_object_or_404(models.BlogPost, pk=pk)
    return render(request, "blog_post_detail.html", {"blog_post": post})


BlogPostForm = forms.modelform_factory(models.BlogPost, fields=("name", "text"))


@login_required
def blog_post_create(request):
    form = BlogPostForm()
    if request.method == "POST":
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Blog Post created successfully")
            return redirect(post.get_absolute_url())
    return render(request, "blog_post_form.html", {"form": form})


@login_required
def blog_post_update(request, pk):
    post = get_object_or_404(models.BlogPost, pk=pk)
    if post.author != request.user:
        raise PermissionDenied

    form = BlogPostForm(instance=post)
    if request.method == "POST":
        form = BlogPostForm(data=request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Blog Post updated successfully")
            return redirect(post.get_absolute_url())
    return render(request, "blog_post_form.html", {"form": form, "blog_post": post})


@login_required
def blog_post_delete(request, pk):
    post = get_object_or_404(models.BlogPost, pk=pk)
    if post.author != request.user:
        raise PermissionDenied

    if request.method == "POST":
        post.delete()
        messages.success(request, "Blog Post deleted successfully")
        return redirect("blog_post_list")
    return render(request, "blog_post_delete.html", {"blog_post": post})
