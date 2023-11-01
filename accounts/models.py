from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager




'''class MyUserManager(UserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):

        if not username:
            raise ValueError("Entrer un nom d'utilisateur")

        user = self.model(username=username)
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):

        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user'''


class User(AbstractUser):

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


