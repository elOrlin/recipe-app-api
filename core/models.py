from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario deberia agregar un correo electronico')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    "User in the system."
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """Recipe Object"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
    title = models.CharField(max_length=255),
    description = models.TextField(blank=True),
    time_minutes = models.IntegerField(),
    price = models.DecimalField(max_digits=5, decimal_places=2),
    link = models.CharField(max_length=255, blank=True),
    tags = models.ManyToManyField("Tag")
    ingredients = models.ManyToManyField('Ingredient')

    class Meta:
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'

    def __str__(self):
        return self.title

class Tag(models.Model):
    """Tag for filtering recipes"""
    name = models.CharField(max_length=255),
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name