# Generated by Django 3.2.12 on 2022-03-05 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WebEnglish', '0004_alter_multiplechoice_reading_comprehension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiplechoice',
            name='reading_comprehension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WebEnglish.readingcomprehension'),
        ),
    ]
