# Generated by Django 4.2.5 on 2023-12-06 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('quizzes', '0004_alter_flashcard_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(max_length=4)),
                ('flashcard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.flashcard')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.newuserinfo')),
            ],
        ),
        migrations.AddConstraint(
            model_name='uservote',
            constraint=models.UniqueConstraint(fields=('user', 'flashcard'), name='unique_user_flashcard_vote'),
        ),
    ]