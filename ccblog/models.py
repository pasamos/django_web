from __future__ import unicode_literals
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=30)
    valid = models.BooleanField()
    loginCount = models.IntegerField(default=0)
    
    def __str__(self):
        return 'phone:' + self.phone


class BlogType(models.Model):
    userId = models.IntegerField()
    typeName = models.CharField(max_length=10)


class Blog(models.Model):
    userId = models.IntegerField()
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    createTime = models.DateTimeField(auto_now_add=True)
    blogTypeId = models.IntegerField()
    lastModifyTime = models.DateTimeField(auto_now=True)

