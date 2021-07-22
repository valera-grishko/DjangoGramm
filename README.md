# DjangoGramm

The application is a mini social network.  
  
User can post photos and view photos of other users.  
Also implemented the ability to put likes and dislikes on photos.  
A user can subscribe or unsubscribe from another user.  
The application has the ability to authorize via Google and GitHub.  
  
Tech stack: Python, Django, PostgreSQL, HTML, CSS, Bootstrap, JQuery, AJAX, Webpack, Cloudinary, Django social auth  
  
The application is deployed on heroku. Link: https://djangogramm21.herokuapp.com/account/registration/  
Heroku resources: Heroku Postgres  
  
 --- Endpoints ---  
  
/account/registration/ ---> register new user  
/account/login/ ---> login  
/account/logout/ ---> logout  
/account/edit/ ---> edit profile  
/account/profile/pk ---> desired profile (profile.id = pk)  
/account/feed/all ---> all photos in social network  
/account/feed/my ---> photos of users you follow  
/account/post/ ---> post new photo  
/account/likes/pk ---> show likes on photo (photo.id = pk)  
/account/dislikes/pk ---> show dislikes on photo (photo.id = pk)  
/account/followers/pk ---> show profile subscribers (profile.id = pk)  
  
For localhosting comment second database and uncomment first database in web_app/settings.py  
  
run tests: python manage.py test  
