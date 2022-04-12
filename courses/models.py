from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name


class MyModelBase(models.Model):
    subject = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject

    class Meta:
        abstract = True


class Course(MyModelBase):
    class Meta:
        unique_together = ('subject', 'category')
        ordering = ['-id']

    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
