from .models import Subscriber, UserPhoto, Like, Dislike


def search_subscriptions(user):
    """ Search subscriptions """

    sub = Subscriber.objects.filter(follower=user).values("user_profile")
    return UserPhoto.objects.filter(user_profile__in=sub)


def create_button(user_profile, follower):
    """ Creating a button """

    return "Unfollow" if Subscriber.objects.filter(
        user_profile=user_profile,
        follower=follower) else "Follow"


def create_follow(profile, follower):
    """ Create or remove a follow object """

    if Subscriber.objects.filter(user_profile=profile, follower=follower):
        button = False
        Subscriber.objects.get(user_profile=profile, follower=follower).delete()
    else:
        button = True
        new_follower = Subscriber(user_profile=profile, follower=follower)
        new_follower.save()
    return button


def create_or_delete_like(user_profile, photo):
    """ Create or remove a like object """

    if Like.objects.filter(user_profile=user_profile, photo=photo):
        Like.objects.get(user_profile=user_profile, photo=photo).delete()
        photo.likes -= 1
    else:
        new_like = Like(user_profile=user_profile, photo=photo)
        new_like.save()
        photo.likes += 1
        if Dislike.objects.filter(user_profile=user_profile, photo=photo):
            Dislike.objects.get(user_profile=user_profile, photo=photo).delete()
            photo.dislikes -= 1
    photo.save()


def create_or_delete_dislike(user_profile, photo):
    """ Create or remove a dislike object """

    if Dislike.objects.filter(user_profile=user_profile, photo=photo):
        Dislike.objects.get(user_profile=user_profile, photo=photo).delete()
        photo.dislikes -= 1
    else:
        new_dislike = Dislike(user_profile=user_profile, photo=photo)
        new_dislike.save()
        photo.dislikes += 1
        if Like.objects.filter(user_profile=user_profile, photo=photo):
            Like.objects.get(user_profile=user_profile, photo=photo).delete()
            photo.likes -= 1
    photo.save()
