# Generated by Django 4.2.5 on 2023-09-20 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewUserInfo',
            fields=[
                ('student_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('major', models.CharField(max_length=50)),
            ],
        ),
    ]
