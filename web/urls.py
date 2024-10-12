from django.urls import path
from .import views



urlpatterns= [
    path('accounts/login/', views.login_view, name="login_page"),
    path('accounts/logout/', views.logout_view, name="logout_page"),
    path('accounts/signup/', views.signup_view, name="signup_page"),
    #path('accounts/contact/', views.contact_view, name="contact_page"),
    path('accounts/post/', views.post_view, name="post_page"),
    path('blog/category/add/', views.add_category, name="add_category_page"),
    path('blog/create/', views.create_post, name="create_post_page"),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('comment', views.add_comment, name="add_comment"),
    path('like_unlike/', views.like_unlike, name='like_unlike'),
    path('add_comment_reply/<int:comment_id>', views.add_comment_reply, name='add_comment_reply'),
    path('', views.home, name="home_page"),
    path('accounts/contact_us/', views.contact_us, name='contact_us'),
    path("chat/<str:room_name>/", views.room, name="room"),
    path("chat/", views.index, name="index"),
   
   
]

