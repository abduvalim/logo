from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import integer_validator
from django.db import models
from django.db.models import CASCADE


class Category(models.Model):
    title = models.CharField(max_length=155)

    def __str__(self):
        return self.title


class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email


class Product(models.Model):
    img = models.ImageField(upload_to='product/')
    title = models.CharField(max_length=155)
    price = models.FloatField()
    text = models.TextField()
    category = models.ForeignKey('app.Category', on_delete=models.CASCADE)
    user = models.ForeignKey('app.User', on_delete=CASCADE)



class UserManager(BaseUserManager):

    def create_user(self,email, password=None,  **kwargs):
        if not email:
            raise ValueError('email not found')
        user = self.model(email=email,  **kwargs)
        user.set_password(password)
        user.save(self._db)
        return user

    def create_superuser(self,email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=155, unique=False)
    phone_number = models.CharField(max_length=13, validators=[integer_validator])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Post(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

