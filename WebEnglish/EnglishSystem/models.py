
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import random
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    status = models.CharField(max_length=2, choices=(("1",'Active'), ("2",'Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default="")
    title = models.TextField()
    short_description = models.TextField()
    content = RichTextField()
    banner_path = models.ImageField(upload_to='WebEnglish/%Y/%m')
    status = models.CharField(max_length=2, choices=(("1",'Published'), ("2",'Unpublished')), default=2)
    meta_keywords = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now = True)
    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,default="")
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.name} - {self.post.title}"

class Paragraph(TimeStampedModel):
    content = RichTextField()
    type = models.CharField(max_length=2, choices=(("1",'Reading Comprehension'), ("2",'Incomplete Text')), default=1)
    def __str__(self):
        return self.content


class Question(TimeStampedModel):
    ALLOWED_NUMBER_OF_CORRECT_CHOICES = 1

    html = models.TextField(_('Question Text'))
    is_published = models.BooleanField(_('Has been published?'), default=False, null=False)
    maximum_marks = models.DecimalField(_('Maximum Marks'), default=4, decimal_places=2, max_digits=6)
    paragraph = models.ForeignKey(Paragraph,related_name='questions', on_delete = models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.html


class Choice(TimeStampedModel):
    MAX_CHOICES_COUNT = 4

    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    is_correct = models.BooleanField(_('Is this answer correct?'), default=False, null=False)
    html = models.TextField(_('Choice Text'))

    def __str__(self):
        return self.html

