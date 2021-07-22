from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, UserPhoto, Subscriber, Like, Dislike


class ModelsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test1', password='qwerty',
                                        gender='test_gender', city='test_city',
                                        avatar='test_avatar')
        UserPhoto.objects.create(user_profile=user, photo='test_photo')

    def test_user_profile_gender(self):
        user_profile = User.objects.get(id=1)
        max_length = user_profile._meta.get_field('gender').max_length
        self.assertEquals(max_length, 20)
        self.assertEquals(user_profile.gender, 'test_gender')

    def test_user_profile_city(self):
        user_profile = User.objects.get(id=1)
        max_length = user_profile._meta.get_field('city').max_length
        self.assertEquals(max_length, 50)
        self.assertEquals(user_profile.city, 'test_city')

    def test_user_profile_avatar(self):
        user_profile = User.objects.get(id=1)
        self.assertEquals(str(type(user_profile.avatar)),
                          "<class 'cloudinary.CloudinaryResource'>")

    def test_user_photo_photo(self):
        user_photo = UserPhoto.objects.get(user_profile=User.objects.get(id=1))
        self.assertEquals(str(type(user_photo.photo)),
                          "<class 'cloudinary.CloudinaryResource'>")

    def test_user_photo_likes(self):
        user_photo = UserPhoto.objects.get(user_profile=User.objects.get(id=1))
        self.assertEquals(user_photo.likes, 0)

    def test_user_photo_dislikes(self):
        user_photo = UserPhoto.objects.get(user_profile=User.objects.get(id=1))
        self.assertEquals(user_photo.dislikes, 0)


class ViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test1', password='qwerty1',
                                 email='test1@gmail.com',
                                 gender='test_gender', city='test_city',
                                 avatar='test_avatar')
        user2 = User.objects.create_user(username='test2', password='qwerty2',
                                         email='test2@gmail.com',
                                         gender='test_gender', city='test_city',
                                         avatar='test_avatar')
        UserPhoto.objects.create(user_profile=user2, photo='test_photo')

    def test_registration_get(self):
        client = Client()
        response = client.get(reverse('registration'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "account/registration.html")

    def test_registration_post(self):
        client = Client()
        response = client.post(reverse('registration'),
                               {'username': 'test3',
                                'email': 'test3@gmail.com',
                                'password': 'qwerty3'})
        user = User.objects.get(id=3)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(user.username, 'test3')

    def test_edit_profile_post(self):
        client = Client()
        client.login(username="test1", password="qwerty1")
        user_profile = User.objects.get(username='test1')
        self.assertEquals(user_profile.gender, 'test_gender')
        avatar = SimpleUploadedFile(name='test_image.jpg',
                                    content=open('static/images/test.jpg',
                                                 'rb').read(),
                                    content_type='image/jpeg')
        response = client.post(reverse('edit_profile'),
                               {'first_name': 'first_name_1',
                                'last_name': 'last_name_1',
                                'gender': 'new_test_gender',
                                'city': 'test_city',
                                'avatar': avatar})
        user_profile = User.objects.get(username='test1')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(user_profile.gender, 'new_test_gender')

    def test_profile_get(self):
        client = Client()
        client.login(username="test1", password="qwerty1")
        response = client.get(reverse('profile', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "account/profile.html")

    def test_post_photo_post(self):
        client = Client()
        client.login(username="test1", password="qwerty1")
        photo = SimpleUploadedFile(name='test_image.jpg',
                                   content=open('static/images/test.jpg',
                                                'rb').read(),
                                   content_type='image/jpeg')
        response = client.post(reverse('post'), {'photo': photo})
        user_profile = User.objects.get(id=1)
        new_photo = UserPhoto.objects.get(user_profile=user_profile)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(new_photo.user_profile, user_profile)

    def test_feed_get(self):
        client = Client()
        client.login(username="test1", password="qwerty1")
        response = client.get(reverse('feed', kwargs={'option': 'my'}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "account/feed.html")

    def test_followers_get(self):
        client = Client()
        client.login(username="test1", password="qwerty1")
        response = client.get(reverse('followers', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "account/followers.html")

    def test_show_likes_get(self):
        client = Client()
        client.login(username="test2", password="qwerty2")
        response = client.get(reverse('likes', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "account/likes.html")

    def test_show_dislikes_get(self):
        client = Client()
        client.login(username="test2", password="qwerty2")
        response = client.get(reverse('dislikes', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "account/dislikes.html")

    def test_follow_post(self):
        client = Client()
        client.login(username="test1", password="qwerty1")
        response = client.post(reverse('follow', kwargs={'pk': 2}))
        follower = User.objects.get(id=1)
        user_profile = User.objects.get(id=2)
        new_sub = Subscriber.objects.get(user_profile=user_profile)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(new_sub.follower, follower)

    def test_like_photo_post(self):
        client = Client()
        client.login(username="test1", password="qwerty1")
        response = client.post(reverse('like', kwargs={'pk': 1}))
        user_profile = User.objects.get(id=1)
        photo = UserPhoto.objects.get(id=1)
        new_like = Like.objects.get(photo=photo)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(new_like.user_profile, user_profile)
        self.assertEquals(photo.likes, 1)

    def test_dislike_photo_post(self):
        client = Client()
        client.login(username="test1", password="qwerty1")
        response = client.post(reverse('dislike', kwargs={'pk': 1}))
        user_profile = User.objects.get(id=1)
        photo = UserPhoto.objects.get(id=1)
        new_dislike = Dislike.objects.get(photo=photo)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(new_dislike.user_profile, user_profile)
        self.assertEquals(photo.dislikes, 1)
