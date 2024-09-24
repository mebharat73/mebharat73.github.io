from django.urls import path
from django.views.decorators.http import require_http_methods
from .import views



urlpatterns= [
    path('accounts/login/', views.login_view, name="login_page"),
    path('accounts/logout/', views.logout_view, name="logout_page"),
    path('accounts/signup/', views.signup_view, name="signup_page"),
    path('accounts/contact/', views.contact_view, name="contact_page"),
    path('accounts/post/', views.post_view, name="post_page"),
    path('blog/category/add/', views.add_category, name="add_category_page"),
    path('blog/create/', views.create_post, name="create_post_page"),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('comment', views.add_comment, name="add_comment"),
    path('blog/<int:blog_id>/like/', views.add_like, name='add_like'),


    path('comment/<int:comment_id>/like/', views.add_like_comment, name='add_like_comment'),
    path('', views.home, name="home_page"),
]