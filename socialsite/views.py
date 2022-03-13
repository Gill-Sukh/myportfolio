from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from . import forms
from . import models
from django.views import generic
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.db import IntegrityError
from braces.views import SelectRelatedMixin
from django.contrib import messages
from django.http import Http404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .models import Group, GroupMember, User, Post
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
User = get_user_model()


class TestPage(TemplateView):
    template_name = 'socialsite/test.html'


class ThanksPage(TemplateView):
    template_name = 'socialsite/thanks.html'


class HomePage(TemplateView):
    template_name = 'socialsite/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("socialsite:test"))
        return super().get(request, *args, **kwargs)


# Account  views here.


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("socialsite:login")
    template_name = "socialsite/signup.html"


class SocialLoginView(LoginView):
    template_name = 'socialsite/login.html'

    def get_success_url(self):
        url = reverse_lazy("socialsite:socialhome")
        return url

# Group View here.


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Group


class SingleGroup(generic.DetailView):
    model = Group


class ListGroups(generic.ListView):
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("socialsite:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get("slug"))

        try:
            a = GroupMember.objects.create(
                user=self.request.user, group=group)

        except IntegrityError:
            messages.warning(
                self.request, ("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(
                self.request, "You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )

        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)

# Post views here


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "socialsite/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message', 'group')
    model = Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Post
    select_related = ("user", "group")
    success_url = reverse_lazy("socialsite:posts")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
