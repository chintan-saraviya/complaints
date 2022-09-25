from django.contrib.auth.models import User
from django.db import models
from complaints_app.choices import *

# Create your models here.


class Complaint(models.Model):
    complaint_text = models.TextField(null=True, blank=True, default=None)
    complainant = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    status = models.CharField(max_length=24, choices=ComplaintStatus.choices, default=ComplaintStatus.WORK_IN_PROGRESS)
