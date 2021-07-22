from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserPhoto


class CustomUserCreationForm(UserCreationForm):
    """ AbstractUser form """

    class Meta:
        model = User
        fields = '__all__'


class RegistrationForm(ModelForm):
    """ Registration form """

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return new_user


class EditProfileForm(ModelForm):
    """ Edit profile form """

    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'Your name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'Your surname'}))
    gender = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'Your gender'}))
    city = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'City'}))
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'gender', 'city', 'avatar']
        exclude = ('id',)

    def save(self, commit=True):
        user_profile = User.objects.get(id=self.fields['id'])
        user_profile.first_name = self.cleaned_data['first_name']
        user_profile.last_name = self.cleaned_data['last_name']
        user_profile.gender = self.cleaned_data['gender']
        user_profile.city = self.cleaned_data['city']
        user_profile.avatar = self.cleaned_data['avatar']
        user_profile.save()


class PostPhotoForm(forms.Form):
    """ Post photo form """

    photo = forms.ImageField()

    def save(self, pk):
        photo = self.cleaned_data['photo']
        new_photo = UserPhoto(user_profile=User.objects.get(id=pk), photo=photo)
        new_photo.save()
