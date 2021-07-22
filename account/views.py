from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth import login
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .forms import RegistrationForm, EditProfileForm, PostPhotoForm
from .models import User, UserPhoto, Subscriber, Like, Dislike
from .service import search_subscriptions, create_button, \
    create_or_delete_like, create_or_delete_dislike, create_follow


class Registration(FormView):
    """ Displaying the registration form """

    form_class = RegistrationForm
    template_name = "account/registration.html"
    success_url = reverse_lazy("edit_profile")

    def form_valid(self, form):
        new_user = form.save()
        login(self.request, new_user,
              backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)


class EditProfile(FormView):
    """ Displaying the edit profile form """

    form_class = EditProfileForm
    template_name = "account/edit_profile.html"

    def get_initial(self):
        user_profile = self.request.user
        fields = {'first_name': user_profile.first_name,
                  'last_name': user_profile.last_name,
                  'gender': user_profile.gender,
                  'city': user_profile.city,
                  'avatar': user_profile.avatar}
        return fields

    def form_valid(self, form):
        form.fields['id'] = self.request.user.id
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.id])


class Profile(ListView):
    """ Displaying the user profile """

    template_name = "account/profile.html"
    context_object_name = 'photos'

    def get_queryset(self):
        user_profile = User.objects.get(id=self.kwargs['pk'])
        return UserPhoto.objects.filter(user_profile=user_profile)

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        user_profile = User.objects.get(id=self.kwargs['pk'])
        context['user_profile'] = user_profile
        context['button'] = create_button(user_profile, self.request.user)
        return context


class PostPhoto(FormView):
    """ Displaying the post photo form """

    form_class = PostPhotoForm
    template_name = "account/post_photo.html"

    def form_valid(self, form):
        form.save(self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile", args=[self.request.user.id])


class Feed(ListView):
    """ Displaying the feed """

    template_name = "account/feed.html"
    context_object_name = "feed"

    def get_queryset(self):
        if self.kwargs['option'] == 'all':
            queryset = UserPhoto.objects.all()
        else:
            queryset = search_subscriptions(self.request.user)
        return queryset[::-1]

    def get_context_data(self, **kwargs):
        context = super(Feed, self).get_context_data(**kwargs)
        context['button'] = True if self.kwargs['option'] == 'all' else False
        return context


class Followers(ListView):
    """ Displaying followers """

    template_name = "account/followers.html"
    context_object_name = "followers"

    def get_queryset(self):
        user_profile = User.objects.get(id=self.kwargs['pk'])
        return Subscriber.objects.filter(user_profile=user_profile)

    def get_context_data(self, **kwargs):
        context = super(Followers, self).get_context_data(**kwargs)
        context["user_profile"] = User.objects.get(id=self.kwargs['pk'])
        return context


class Follow(View):
    """ Subscription """

    def post(self, request, pk):
        follower = request.user
        profile = User.objects.get(id=pk)
        if follower.id == profile.id:
            return redirect("profile", id=profile.id)
        button = create_follow(profile, follower)
        return JsonResponse({'button': button})


class LikePhoto(View):
    """ Like photo """

    def post(self, request, pk):
        photo = UserPhoto.objects.get(id=pk)
        user_profile = request.user
        create_or_delete_like(user_profile, photo)
        return JsonResponse({"likes": photo.likes, "dislikes": photo.dislikes})


class DislikePhoto(View):
    """ Dislike photo """

    def post(self, request, pk):
        photo = UserPhoto.objects.get(id=pk)
        user_profile = request.user
        create_or_delete_dislike(user_profile, photo)
        return JsonResponse({"likes": photo.likes, "dislikes": photo.dislikes})


class ShowLikes(ListView):
    """ Displaying likes """

    template_name = "account/likes.html"
    context_object_name = 'likes'

    def get_queryset(self):
        photo = UserPhoto.objects.get(id=self.kwargs['pk'])
        return Like.objects.filter(photo=photo)

    def get_context_data(self, **kwargs):
        context = super(ShowLikes, self).get_context_data(**kwargs)
        context["photo"] = UserPhoto.objects.get(id=self.kwargs['pk'])
        return context


class ShowDislikes(ListView):
    """ Displaying dislikes """

    template_name = "account/dislikes.html"
    context_object_name = 'dislikes'

    def get_queryset(self):
        photo = UserPhoto.objects.get(id=self.kwargs['pk'])
        return Dislike.objects.filter(photo=photo)

    def get_context_data(self, **kwargs):
        context = super(ShowDislikes, self).get_context_data(**kwargs)
        context["photo"] = UserPhoto.objects.get(id=self.kwargs['pk'])
        return context
