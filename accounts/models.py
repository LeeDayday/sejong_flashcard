from django.db import models


class NewUserInfo(models.Model):
    student_id = models.CharField(primary_key=True, max_length=10)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    major_status = models.CharField(max_length=10)
    major = models.CharField(max_length=50)
    sub_major = models.CharField(max_length=50, blank=True, null=True)

