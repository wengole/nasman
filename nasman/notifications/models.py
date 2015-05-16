from django.db import models
from model_utils.models import TimeStampedModel


class Notification(TimeStampedModel):
    message = models.TextField()
