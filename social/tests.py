from django.test import TestCase
from .models import User, Post, Comment, Reaction


class RegisterTest(TestCase):
    def test_user_registration(self):
        response = self.client.post('/accounts/signup/', {
            'email': 'test@test.com',
            'username': 'testuser',
            'password1': 'testapp123',
            'password2': 'testapp123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/social/')

    def test_user_login(self):
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testapp123'
        })
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        response = self.client.post('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')


class PostTest(TestCase):
    def test_post_creation(self):
        user = User.objects.create(username='testuser')
        post = Post.objects.create(body='Test Post Content', user_id=user)
        self.assertEqual(post.body, 'Test Post Content')

    def test_edit_post(self):
        user = User.objects.create(username='testuser')
        post = Post.objects.create(body='Test Post Content', user_id=user)
        response = self.client.post('/social/post/1/edit/', {
            'body': 'Test Post Content'
        })
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(body='Test Post Content')
        self.assertEqual(post.body, 'Test Post Content')


class CommentCreationTest(TestCase):
    def test_comment_creation(self):
        user = User.objects.create(username='testuser')
        post = Post.objects.create(body='Test Post Content', user_id=user)
        comment = Comment.objects.create(post_id=post.id, author_id=user.id)
        self.assertEqual(comment.post, post)

    def test_delete_comment(self):
        user = User.objects.create(username='testuser')
        post = Post.objects.create(body='Test Post Content', user_id=user)
        comment = Comment.objects.create(post_id=post.id, author_id=user.id)
        response = self.client.post('/social/post/1/comment/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)
    

class AddReactionTest(TestCase):
    def test_add_like(self):
        user = User.objects.create(username='testuser')
        post = Post.objects.create(body='Test Post Content', user_id=user)
        reaction = Reaction.objects.create(post=post, author=user, choice=1)
        self.assertEqual(reaction.choice, 1)
    
    def test_add_hate(self):
        user = User.objects.create(username='testuser')
        post = Post.objects.create(body='Test Post Content', user_id=user)
        reaction = Reaction.objects.create(post=post, author=user, choice=2)
        self.assertEqual(reaction.choice, 2)

    def test_add_care(self):
        user = User.objects.create(username='testuser')
        post = Post.objects.create(body='Test Post Content', user_id=user)
        reaction = Reaction.objects.create(post=post, author=user, choice=3)
        self.assertEqual(reaction.choice, 3)




