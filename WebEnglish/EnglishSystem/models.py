
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
    content = models.TextField()

    def __str__(self):
        return self.content


class Question(TimeStampedModel):
    ALLOWED_NUMBER_OF_CORRECT_CHOICES = 1

    html = models.TextField(_('Question Text'))
    is_published = models.BooleanField(_('Has been published?'), default=False, null=False)
    maximum_marks = models.DecimalField(_('Maximum Marks'), default=4, decimal_places=2, max_digits=6)
    paragraph = models.ForeignKey(Paragraph, on_delete = models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.html


class Choice(TimeStampedModel):
    MAX_CHOICES_COUNT = 4

    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    is_correct = models.BooleanField(_('Is this answer correct?'), default=False, null=False)
    html = models.TextField(_('Choice Text'))

    def __str__(self):
        return self.html


class QuizProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.DecimalField(_('Total Score'), default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return f'<QuizProfile: user={self.user}>'



    def get_new_question(self):
        used_questions_pk = AttemptedQuestion.objects.filter(quiz_profile=self).values_list('question__pk', flat=True)
        # print(used_questions_pk)
        remaining_questions = Question.objects.exclude(pk__in=used_questions_pk)
        # print(remaining_questions.pk)
        if not remaining_questions.exists():
            return
        return random.choice(remaining_questions)

    def create_attempt(self, question):
        attempted_question = AttemptedQuestion(question=question, quiz_profile=self)
        attempted_question.save()

    def evaluate_attempt(self, attempted_question, selected_choice):
        if attempted_question.question_id != selected_choice.question_id:
            return

        attempted_question.selected_choice = selected_choice
        if selected_choice.is_correct is True:
            attempted_question.is_correct = True
            attempted_question.marks_obtained = attempted_question.question.maximum_marks

        attempted_question.save()
        self.update_score()

    def update_score(self):
        marks_sum = self.attempts.filter(is_correct=True).aggregate(
            models.Sum('marks_obtained'))['marks_obtained__sum']
        self.total_score = marks_sum or 0
        self.save()


class AttemptedQuestion(TimeStampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz_profile = models.ForeignKey(QuizProfile, on_delete=models.CASCADE, related_name='attempts')
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(_('Was this attempt correct?'), default=False, null=False)
    marks_obtained = models.DecimalField(_('Marks Obtained'), default=0, decimal_places=2, max_digits=6)

    def get_absolute_url(self):
        return f'/submission-result/{self.pk}/'


