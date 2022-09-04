from django.urls import path
from .views import (
    PostListView, PostDetailView, PostEditView, PostDeleteView,
    CommentDeleteView,
    AddLike, AddHate, AddCare,
)
    

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/edit/', PostEditView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/like/', AddLike.as_view(), name='like'),
    path('post/<int:pk>/hate/', AddHate.as_view(), name='hate'),
    path('post/<int:pk>/care/', AddCare.as_view(), name='care'),
]