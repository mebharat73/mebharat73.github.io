from django.urls import path
from .import views
from .views import upload_profile_picture, view_profile


urlpatterns= [
    path('accounts/login/', views.login_view, name="login_page"),
    path('upload_profile_picture/', upload_profile_picture, name='upload_profile_picture'),
    path('profile/', view_profile, name='profile'),
    path('accounts/logout/', views.logout_view, name="logout_page"),
    path('accounts/signup/', views.signup_view, name="signup_page"),
    path('accounts/post/', views.post_view, name="post_page"),
    path('blog/category/add/', views.add_category, name="add_category_page"),
    path('blog/create/', views.create_post, name="create_post_page"),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('comment/', views.add_comment, name="add_comment"),
    path('like_unlike/', views.like_unlike, name='like_unlike'),
    path('add_comment_reply/<int:comment_id>/', views.add_comment_reply, name='add_comment_reply'),
    path('', views.home, name="home_page"),
    path('accounts/contact_us/', views.contact_us, name='contact_us'),
    path('chat/', views.index, name='index'),
    path('chat/create/', views.create_room, name='create_room'),  # URL for creating a room
    path('chat/<str:room_name>/', views.room_view, name='room_view'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/<str:room_name>/', views.get_messages, name='get_messages'),
    
    
   
]

