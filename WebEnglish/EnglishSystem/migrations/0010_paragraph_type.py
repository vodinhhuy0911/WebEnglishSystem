# Generated by Django 3.2.12 on 2022-05-04 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EnglishSystem', '0009_alter_question_paragraph'),
    ]

    operations = [
        migrations.AddField(
            model_name='paragraph',
            name='type',
            field=models.CharField(choices=[('1', 'Reading Comprehension'), ('2', 'Incomplete Text')], default=1, max_length=2),
        ),
    ]
