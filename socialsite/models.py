from django import template
from django.db import models
from django.contrib import auth
from django.urls import reverse
from django.utils.text import slugify
# pip install misaka
import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
register = template.Library()

# Create your models here.

# account model


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)

# Group model


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through="GroupMember")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("socialsite:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["name"]


class GroupMember(models.Model):
    group = models.ForeignKey(
        Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("group", "user")

# Post Model here:


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts",
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(
        Group, related_name="posts", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "socialsite:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        # unique_together = ["user", "message"]
