# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Post, Comment, Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm
from taggit.models import Tag

# POSTS

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.kwargs.get("tag")
        if tag:
            qs = qs.filter(tags__name__in=[tag])
        return qs

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        ctx["comments"] = self.object.comments.select_related("author").all()
        return ctx

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Post created successfully.")
        return response

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# COMMENTS

@login_required
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added.")
    return redirect(post.get_absolute_url())

@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        messages.error(request, "You don't have permission to edit this comment.")
        return redirect(comment.post.get_absolute_url())

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated.")
            return redirect(comment.post.get_absolute_url())
    else:
        form = CommentForm(instance=comment)
    return render(request, "blog/comment_form.html", {"form": form, "comment": comment})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if comment.author != request.user:
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect(post.get_absolute_url())
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect(post.get_absolute_url())
    return render(request, "blog/comment_confirm_delete.html", {"comment": comment})

# AUTH: register & profile

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # create profile
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("blog:post_list")
    else:
        form = UserRegisterForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        uform = UserUpdateForm(request.POST, instance=user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=getattr(user, "profile", None))
        if uform.is_valid() and pform.is_valid():
            uform.save()
            profile = pform.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Profile updated.")
            return redirect("blog:profile")
    else:
        uform = UserUpdateForm(instance=user)
        pform = ProfileUpdateForm(instance=getattr(user, "profile", None))
    return render(request, "blog/profile.html", {"uform": uform, "pform": pform})

# SEARCH

def search(request):
    query = request.GET.get("q", "")
    results = Post.objects.none()
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, "blog/search_results.html", {"query": query, "results": results})
