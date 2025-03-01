from django.db import models
from .user import User

class Website(models.Model):
  url = models.URLField()
  site_name = models.TextField(max_length=255)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)