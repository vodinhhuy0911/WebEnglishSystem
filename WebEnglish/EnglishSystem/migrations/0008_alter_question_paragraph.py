# Generated by Django 3.2.12 on 2022-05-03 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EnglishSystem', '0007_alter_question_paragraph'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='paragraph',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='EnglishSystem.paragraph'),
        ),
    ]
