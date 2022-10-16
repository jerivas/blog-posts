from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-published_at",)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("blog_post_detail", kwargs={"pk": self.pk})


admin.site.register(BlogPost, list_display=("name", "published_at"))
