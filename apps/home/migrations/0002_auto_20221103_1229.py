# Generated by Django 2.2.3 on 2022-11-03 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='img',
            name='choicesday',
        ),
        migrations.RemoveField(
            model_name='img',
            name='choicesgender',
        ),
        migrations.RemoveField(
            model_name='img',
            name='choiceslanguage',
        ),
        migrations.RemoveField(
            model_name='img',
            name='choicesmonth',
        ),
        migrations.RemoveField(
            model_name='img',
            name='choicesyear',
        ),
        migrations.RemoveField(
            model_name='img',
            name='confirmation',
        ),
        migrations.RemoveField(
            model_name='img',
            name='email',
        ),
        migrations.RemoveField(
            model_name='img',
            name='firstName',
        ),
        migrations.RemoveField(
            model_name='img',
            name='lastName',
        ),
        migrations.RemoveField(
            model_name='img',
            name='location',
        ),
        migrations.RemoveField(
            model_name='img',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='img',
            name='skill',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
    ]
