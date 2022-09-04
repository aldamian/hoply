from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment, Reaction
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-stamp')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-stamp')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user_id = request.user
            new_post.save()
        
        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)

        
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post=self.get_object()
        return self.request.user == post.user_id


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post=self.get_object()
        return self.request.user == post.user_id


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


"""
Reactions will be implemented as a post request to a form. 
It either adds or removes a reaction to a post.
"""
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        reaction = Reaction.objects.filter(post=post, author=request.user)

        is_hate = False
        is_care = False

        is_like = False

        # if no reaction, create one
        if not reaction:
            new_reaction = Reaction(post=post, author=request.user, choice=1)
            new_reaction.save()
            post.likes.add(request.user)
            is_like = True

        if reaction and is_like == False:

            reaction = Reaction.objects.get(post=post, author=request.user)

            if reaction.choice == 1:
                reaction.choice = 0
                reaction.save()
                post.likes.remove(request.user)

            elif reaction.choice != 1:
                reaction.choice = 1
                reaction.save()
                post.likes.add(request.user)
      
                # remove hate reaction if it exists
                for hate in post.hates.all():
                    if hate == request.user:
                        is_hate = True
                    break

                if is_hate:
                    post.hates.remove(request.user)

                # remove care reaction if it exists
                for care in post.cares.all():
                    if care == request.user:
                        is_care = True
                    break

                if is_care:
                    post.cares.remove(request.user)


        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

        
class AddHate(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        reaction = Reaction.objects.filter(post=post, author=request.user)
        
        is_like = False
        is_care = False

        is_hate = False

        # if no reaction, create one
        if not reaction:
            new_reaction = Reaction(post=post, author=request.user, choice=2)
            new_reaction.save()
            post.hates.add(request.user)
            is_hate = True

        if reaction and is_hate == False:
            
            reaction = Reaction.objects.get(post=post, author=request.user)

            if reaction.choice == 2:
                reaction.choice = 0
                reaction.save()
                post.hates.remove(request.user)

            elif reaction.choice != 2:
                reaction.choice = 2
                reaction.save()
                post.hates.add(request.user)
    
                # remove like reaction if it exists
                for like in post.likes.all():
                    if like == request.user:
                        is_like = True
                    break

                if is_like:
                    post.likes.remove(request.user)

                # remove care reaction if it exists
                for care in post.cares.all():
                    if care == request.user:
                        is_care = True
                    break

                if is_care:
                    post.cares.remove(request.user)


        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

"""
This is funny because adding "Not care" as a reaction is a paradox. 
If someone reacts with this, they actually care. 
"""
class AddCare(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        reaction = Reaction.objects.filter(post=post, author=request.user)
        
        is_like = False
        is_hate = False

        is_care = False

        if not reaction:
            new_reaction = Reaction(post=post, author=request.user, choice=3)
            new_reaction.save()
            post.cares.add(request.user)
            is_care = True
        
        if reaction and is_care == False:

            reaction = Reaction.objects.get(post=post, author=request.user)
                    
            if reaction.choice == 3:
                reaction.choice = 0
                reaction.save()
                post.cares.remove(request.user)

            elif reaction.choice != 3:
                reaction.choice = 3
                reaction.save()
                post.cares.add(request.user)
    
                # remove like reaction if it exists
                for like in post.likes.all():
                    if like == request.user:
                        is_like = True
                    break

                if is_like:
                    post.likes.remove(request.user)

                # remove hate reaction if it exists
                for hate in post.hates.all():
                    if hate == request.user:
                        is_hate = True
                    break

                if is_hate:
                    post.hates.remove(request.user)


        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
