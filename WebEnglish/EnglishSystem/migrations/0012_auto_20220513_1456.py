# Generated by Django 3.2.12 on 2022-05-13 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EnglishSystem', '0011_alter_paragraph_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='AttemptedQuestion',
        ),
        migrations.DeleteModel(
            name='QuizProfile',
        ),
    ]
