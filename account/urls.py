from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(authentication_form=AuthenticationForm,
                                     template_name='account/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', views.Registration.as_view(), name='registration'),
    path('edit/', login_required(views.EditProfile.as_view()),
         name='edit_profile'),
    path('profile/<int:pk>', login_required(views.Profile.as_view()),
         name='profile'),
    path('post/', login_required(views.PostPhoto.as_view()), name='post'),
    path('feed/<option>', login_required(views.Feed.as_view()), name='feed'),
    path('follow/<int:pk>', login_required(views.Follow.as_view()),
         name='follow'),
    path('followers/<int:pk>', login_required(views.Followers.as_view()),
         name='followers'),
    path('like/<int:pk>', login_required(views.LikePhoto.as_view()),
         name='like'),
    path('dislike/<int:pk>', login_required(views.DislikePhoto.as_view()),
         name='dislike'),
    path('likes/<int:pk>', login_required(views.ShowLikes.as_view()),
         name='likes'),
    path('dislikes/<int:pk>', login_required(views.ShowDislikes.as_view()),
         name='dislikes'),
    path('', include('social_django.urls', namespace='social')),
]
