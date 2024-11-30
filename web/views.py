
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile, Post, Like, Comment
from .forms import PostImageForm
from .forms import CreateBlogForm, CategoryForm, CommentForm
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .forms import CommentForm, CommentReplyForm
from django.core.mail import send_mail
from .models import Message, Room
from django.shortcuts import get_object_or_404
from .models import Message, Room  # Make sure to import your models
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Room, Message
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from web.models import BlogImage  # Ensure this is the correct import
from .forms import PostForm, PostImageForm


@login_required
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        Room.objects.create(name=room_name)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'main/create_room.html')  # Create a template for this


def index(request):
    rooms = Room.objects.all()  # Get all chat rooms
    return render(request, 'main/index.html', {'rooms': rooms})



@login_required
def room_view(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    messages = Message.objects.filter(room=room).order_by('timestamp')
    return render(request, 'main/room.html', {'room': room, 'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        print("Request received")  # Debugging line
        message = request.POST.get('message')
        room_name = request.POST.get('room_name')
        print("Message:", message)  # Debugging line
        room = get_object_or_404(Room, name=room_name)

        # Check for duplicate message (optional)
        if Message.objects.filter(user=request.user, room=room, message=message).exists():
            return JsonResponse({'error': 'Duplicate message'}, status=400)

        new_message = Message.objects.create(user=request.user, room=room, message=message)
        return JsonResponse({
            'user': new_message.user.username,
            'message': new_message.message,
            'timestamp': new_message.timestamp.isoformat(),
            'profile_picture': new_message.user.profile.profile_picture.url
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def get_messages(request, room_name, last_timestamp=None):
    # Convert last_timestamp to a datetime object if provided
    if last_timestamp:
        last_timestamp = datetime.datetime.fromisoformat(last_timestamp)

    # Fetch messages for the specified room, ordered by timestamp
    messages = Message.objects.filter(room__name=room_name)

    # Filter messages if last_timestamp is provided
    if last_timestamp:
        messages = messages.filter(timestamp__gt=last_timestamp)

    # Limit the number of messages fetched (e.g., last 10 messages)
    messages = messages.order_by('-timestamp')[:10]  # Adjust the number as needed

    # Construct a list of dictionaries to return as JSON
    messages_data = [
        {
            'user': msg.user.username,
            'message': msg.message,
            'timestamp': msg.timestamp.isoformat(),  # Return timestamp in ISO format
            'profile_picture': msg.user.profile.profile_picture.url  # Include profile picture URL
        } 
        for msg in messages
    ]

    # Reverse the list to return the oldest messages first
    messages_data.reverse()

    return JsonResponse(messages_data, safe=False)




def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Send an email to the admin's email address
        send_mail(
            'New Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}',
            'mebharat73@gmail.com',
            ['mebharat73@gmail.com'],
            fail_silently=False,
        )

        # Send a confirmation email to the user
        send_mail(
            'Thank you for contacting us!',
            f'Dear {name},\n\nThank you for reaching out to us. We will get back to you soon.\n\nBest regards,\n[Your Name]',
            'mebharat73@gmail.com',
            [email],
            fail_silently=False,
        )

        # Render the template with a success message
        context = {'success': True, 'name': name}
        return render(request, 'main/contact.html', context)
    else:
        return render(request, 'main/contact.html')



@require_POST
@login_required
def add_comment(request):
    print("add_comment view called")
    blog_id = request.POST.get('blog_id')
    blog = get_object_or_404(Post, id=blog_id)
    form_data = CommentForm(request.POST)

    if form_data.is_valid():
        comment = form_data.save(commit=False)  # Don't save yet
        comment.author = request.user  # Set the author field
        comment.post = blog  # Set the post field
        comment.save()  # Now save the comment
        return redirect("blog_detail", blog_id=blog_id)
    else:
        # If the form is invalid, render the same page with errors
        comments = blog.comments.all().order_by('-created_at')  # Ensure comments are ordered
        context = {
            'blog': blog,
            'content': blog.content,
            'comment_form': form_data,
            'comments': comments
        }
        return render(request, 'main/blog_detail.html', context)
    
    

@api_view(['POST'])
def like_unlike(request):
    print("like_unlike view called")
    obj_id = request.POST.get("obj_id")
    obj_type = request.POST.get("obj_type")

    # Get the content object
    if obj_type == 'post':
        content_object = get_object_or_404(Post, id=obj_id)
    elif obj_type == 'comment':
        content_object = get_object_or_404(Comment, id=obj_id)

    # Check if a like already exists for the content object
    like, created = Like.objects.get_or_create(user=request.user, content_type=ContentType.objects.get_for_model(content_object), object_id=obj_id)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    # Update the likes count property
    total_likes = Like.objects.filter(content_type=ContentType.objects.get_for_model(content_object), object_id=obj_id).count()

    # Return the updated likes count and the link to the like button as a JSON response
    if liked:
        link = "Unlike"
    else:
        link = "Like"
    return JsonResponse({"likes_count": total_likes, "link": link, "obj_type": obj_type, "obj_id": obj_id})



def blog_detail(request, blog_id):
    blog = get_object_or_404(Post, id=blog_id)
    images = BlogImage.objects.filter(post=blog)  # Fetch images related to the blog post
    comments = blog.comments.all().order_by('-created_at')  # Ensure comments are ordered

    # Ensure replies are ordered when rendering
    for comment in comments:
        comment.replies = comment.commentreply_set.all().order_by('-created_at')  # Order replies by created_at

    context = {
        'blog': blog,
        'content': blog.content,
        'comment_form': CommentForm(),
        'comment_reply_form': CommentReplyForm(),
        'comments': comments,  # Access comments using related_name
        'images': images,  # Include images in the context
    }
    return render(request, 'main/blog_detail.html', context)


@require_POST
@login_required
def add_comment_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    form = CommentReplyForm(request.POST)
    
    if form.is_valid():
        reply = form.save(commit=False)
        reply.comment = comment
        reply.author = request.user
        reply.save()
        
        # Prepare the response data
        response_data = {
            "reply": reply.content,
            "id": reply.id,
            "author": str(reply.author),  # Get the author's name
            "profile_pic": reply.author.profile.profile_picture.url if reply.author.profile.profile_picture else '',  # Get the profile picture URL
            "created_at": reply.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format the timestamp
        }
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Invalid form data"}, status=400)

#.......................................................................................

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_post_page")
        else:
            return render(request, "main/add_category.html", {'form':form})
        
    else:
        form = CategoryForm()
        return render(request, "main/add_category.html", {'form':form})

#.............................................................................................................



@login_required


def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user  # Set the author to the current user
            post.save()

            # Handle image uploads
            images = request.FILES.getlist('images')  # Use the name of the image input field
            for image in images:
                BlogImage.objects.create(post=post, image=image)

            return redirect('home_page')  # Redirect to a success page
    else:
        post_form = PostForm()

    return render(request, 'main/create_blog.html', {'post_form': post_form})



def home(request):
    latest_blogs = Post.objects.all().order_by('-created_at')
    paginator = Paginator(latest_blogs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    


    context={
        'page_obj': page_obj
    }
    return render(request,'main/home.html', context)




#............................................................................
def post_view(request):
    return render(request, 'main/post.html')


#............................................................................................................................

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # This will be 'on' if checked

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Set session expiry if "remember me" is checked
            if remember_me:
                request.session.set_expiry(7 * 24 * 60 * 60)  # 7 days
            return redirect("home_page")  # Redirect to the home page
        else:
            messages.error(request, 'Invalid username or password.')  # Use messages framework for better UX
            return render(request, 'main/login.html')  # Render the login page again with an error message
    else:
        return render(request, 'main/login.html')  # Render the login page for GET requests


# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    return render(request, 'main/profile.html')  # Ensure this template exists

@login_required
def settings_view(request):
    return render(request, 'main/settings.html')  # Ensure this template exists
#*********************************************************************************

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile  # Ensure you import your Profile model

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', 'default_name')
        last_name = request.POST.get('last_name', 'default_name')
        profile_pic = request.FILES.get('profile_picture')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'main/signup.html', {'error': "Username must be unique"})

        # Validate username
        if len(username) < 3:
            return render(request, 'main/signup.html', {'error': "Username must be at least 6 characters and contain '@'"})

        # Validate password
        if password != password_confirm:
            return render(request, 'main/signup.html', {'error': "Password and Confirm password must be the same"})
        
        if len(password) < 3:
            return render(request, 'main/signup.html', {'error': "Password must be at least 6 characters long"})

        # Create the user
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)

        # Create the profile if a profile picture is provided
        if profile_pic:
            Profile.objects.create(profile_picture=profile_pic, user=user)

        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect("login_page")  # Redirect to the login page or another page

    return render(request, 'main/signup.html')


#...................................................................................................................................



#...................................................................................................................................


def logout_view(request):
    logout(request)
    return redirect("home_page")

#....................................................................jSon type like and unlike



