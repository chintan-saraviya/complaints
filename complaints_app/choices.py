from django.utils.translation import gettext_lazy as _
from django.db import models


class ComplaintStatus(models.TextChoices):
    WORK_IN_PROGRESS = 'work in progress', _('work_in_progress')
    COMPLETED = 'completed', _('completed')
