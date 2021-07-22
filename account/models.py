from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    """ Extended user model """

    gender = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    avatar = CloudinaryField('avatar')


class UserPhoto(models.Model):
    """ Photo model """

    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = CloudinaryField('photos')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)


class Subscriber(models.Model):
    """ Subscription model """

    user_profile = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='profile')
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='follower')


class Like(models.Model):
    """ Like model """

    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(UserPhoto, on_delete=models.CASCADE)


class Dislike(models.Model):
    """ Dislike model """

    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(UserPhoto, on_delete=models.CASCADE)
