from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListCreateApiView.as_view(), name='posts'),
    path('<int:pk>/', views.PostDetailApiView.as_view(), name='post_details'),
]