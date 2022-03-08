from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='upload/%Y/%m')

class Category(models.Model):
    name = models.CharField(max_length=100,null=False,unique=True)
    def __str__(self):
        return self.name

class ReadingComprehension(models.Model):
    contentreading = models.TextField(null=False)


class MultipleChoice(models.Model):
    content = models.TextField(null= False)
    reading_comprehension = models.ForeignKey(ReadingComprehension,on_delete=models.CASCADE,null=True, related_name='multipleChoice')
    answer_correct  = models.TextField(null = False)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True, related_name='multipleChoice')

class Answers(models.Model):
    answer = models.TextField(null=False)
    question = models.ForeignKey(MultipleChoice, on_delete=models.CASCADE, null=False, related_name='answers')


