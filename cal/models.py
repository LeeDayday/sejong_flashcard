import datetime

from django.db import models
from django.contrib.auth.models import User
from accounts.models import NewUserInfo
from django.utils import timezone
from django.urls import reverse

# Create your models here.
# class Calendar(models.Model):
#     owner = models.ForeignKey(NewUserInfo, on_delete=models.CASCADE)
#     # content = models.ForeignKey(Content, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         db_table = "calendar"

class Content(models.Model):
    # calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    owner = models.ForeignKey(NewUserInfo, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content"
        ordering = ['start_time']

    @property
    def get_html_url(self):
        url = reverse('cal:content_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'