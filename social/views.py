from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Post, Comment, Like, Profile, Follow


# =========================
# HOME
# =========================

def home(request):
    return render(request, 'social/home.html')


# =========================
# REGISTER
# =========================

def register(request):

    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':

        username = request.POST.get(
            'username', ''
        ).strip()

        email = request.POST.get(
            'email', ''
        ).strip()

        password = request.POST.get(
            'password', ''
        )

        confirm_password = request.POST.get(
            'confirm_password', ''
        )

        if not username or not email or not password:
            messages.error(
                request,
                'Please fill in all fields.'
            )
            return redirect('register')

        if password != confirm_password:
            messages.error(
                request,
                'Passwords do not match.'
            )
            return redirect('register')

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists.'
            )
            return redirect('register')

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                'Email already exists.'
            )
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.get_or_create(
            user=user
        )

        messages.success(
            request,
            'Account created successfully. Please login.'
        )

        return redirect('login')

    return render(
        request,
        'social/register.html'
    )


# =========================
# LOGIN
# =========================

def login_user(request):

    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':

        username = request.POST.get(
            'username', ''
        ).strip()

        password = request.POST.get(
            'password', ''
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('feed')

        messages.error(
            request,
            'Invalid username or password.'
        )

        return redirect('login')

    return render(
        request,
        'social/login.html'
    )


# =========================
# FEED
# =========================

@login_required(login_url='login')
def feed(request):

    posts = (
        Post.objects
        .select_related('user', 'user__profile')
        .prefetch_related(
            'likes',
            'comments',
            'comments__user',
            'comments__user__profile'
        )
        .order_by('-created_at')
    )

    liked_post_ids = set(
        Like.objects.filter(
            user=request.user
        ).values_list(
            'post_id',
            flat=True
        )
    )

    return render(
        request,
        'social/feed.html',
        {
            'posts': posts,
            'liked_post_ids': liked_post_ids
        }
    )


# =========================
# CREATE POST
# =========================

@login_required(login_url='login')
def create_post(request):

    if request.method == 'POST':

        content = request.POST.get(
            'content', ''
        ).strip()

        image = request.FILES.get(
            'image'
        )

        if not content and not image:

            messages.error(
                request,
                'Please add some text or an image.'
            )

            return redirect('create_post')

        Post.objects.create(
            user=request.user,
            content=content,
            image=image
        )

        messages.success(
            request,
            'Post created successfully.'
        )

        return redirect('feed')

    return render(
        request,
        'social/create_post.html'
    )


# =========================
# EDIT POST
# =========================

@login_required(login_url='login')
def edit_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
    )

    if request.method == 'POST':

        content = request.POST.get(
            'content', ''
        ).strip()

        new_image = request.FILES.get(
            'image'
        )

        remove_image = request.POST.get(
            'remove_image'
        )

        if new_image:
            post.image = new_image

        elif remove_image == 'on':
            post.image = None

        if not content and not post.image:

            messages.error(
                request,
                'A post must contain text or an image.'
            )

            return render(
                request,
                'social/edit_post.html',
                {
                    'post': post
                }
            )

        post.content = content
        post.save()

        messages.success(
            request,
            'Post updated successfully.'
        )

        return redirect('feed')

    return render(
        request,
        'social/edit_post.html',
        {
            'post': post
        }
    )


# =========================
# DELETE POST
# =========================

@login_required(login_url='login')
@require_POST
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
    )

    post.delete()

    messages.success(
        request,
        'Post deleted successfully.'
    )

    return redirect('feed')


# =========================
# ADD COMMENT
# =========================

@login_required(login_url='login')
@require_POST
def add_comment(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    content = request.POST.get(
        'content', ''
    ).strip()

    if content:

        Comment.objects.create(
            post=post,
            user=request.user,
            content=content
        )

    return redirect('feed')


# =========================
# DELETE COMMENT
# =========================

@login_required(login_url='login')
@require_POST
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user
    )

    comment.delete()

    return redirect('feed')


# =========================
# LIKE / UNLIKE
# =========================

@login_required(login_url='login')
@require_POST
def toggle_like(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    like = Like.objects.filter(
        post=post,
        user=request.user
    ).first()

    if like:
        like.delete()

    else:
        Like.objects.create(
            post=post,
            user=request.user
        )

    return redirect('feed')


# =========================
# MY PROFILE
# =========================

@login_required(login_url='login')
def profile(request):

    profile_object, created = (
        Profile.objects.get_or_create(
            user=request.user
        )
    )

    posts = (
        Post.objects
        .filter(user=request.user)
        .prefetch_related('likes')
        .order_by('-created_at')
    )

    followers_count = Follow.objects.filter(
        following=request.user
    ).count()

    following_count = Follow.objects.filter(
        follower=request.user
    ).count()

    return render(
        request,
        'social/profile.html',
        {
            'profile': profile_object,
            'posts': posts,
            'followers_count': followers_count,
            'following_count': following_count
        }
    )


# =========================
# EDIT PROFILE
# =========================

@login_required(login_url='login')
def edit_profile(request):

    profile_object, created = (
        Profile.objects.get_or_create(
            user=request.user
        )
    )

    if request.method == 'POST':

        bio = request.POST.get(
            'bio', ''
        ).strip()

        profile_picture = request.FILES.get(
            'profile_picture'
        )

        profile_object.bio = bio

        if profile_picture:
            profile_object.profile_picture = (
                profile_picture
            )

        profile_object.save()

        messages.success(
            request,
            'Profile updated successfully.'
        )

        return redirect('profile')

    return render(
        request,
        'social/edit_profile.html',
        {
            'profile': profile_object
        }
    )


# =========================
# OTHER USER PROFILE
# =========================

@login_required(login_url='login')
def user_profile(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    if profile_user == request.user:
        return redirect('profile')

    profile_object, created = (
        Profile.objects.get_or_create(
            user=profile_user
        )
    )

    posts = (
        Post.objects
        .filter(user=profile_user)
        .prefetch_related('likes')
        .order_by('-created_at')
    )

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    return render(
        request,
        'social/user_profile.html',
        {
            'profile_user': profile_user,
            'profile': profile_object,
            'posts': posts,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count
        }
    )


# =========================
# FOLLOW / UNFOLLOW
# =========================

@login_required(login_url='login')
@require_POST
def toggle_follow(request, username):

    user_to_follow = get_object_or_404(
        User,
        username=username
    )

    if user_to_follow == request.user:
        return redirect('profile')

    follow = Follow.objects.filter(
        follower=request.user,
        following=user_to_follow
    ).first()

    if follow:
        follow.delete()

    else:
        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )

    return redirect(
        'user_profile',
        username=username
    )


# =========================
# SEARCH USERS
# =========================

@login_required(login_url='login')
def search_users(request):

    query = request.GET.get(
        'q', ''
    ).strip()

    users = User.objects.none()

    if query:

        users = (
            User.objects
            .filter(
                username__icontains=query
            )
            .exclude(
                id=request.user.id
            )
            .select_related('profile')
            .order_by('username')
        )

    return render(
        request,
        'social/search_users.html',
        {
            'users': users,
            'query': query
        }
    )


# =========================
# LOGOUT
# =========================

@login_required(login_url='login')
@require_POST
def logout_user(request):

    logout(request)

    return redirect('home')