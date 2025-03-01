from django.db import models
from .user import User

class Notes(models.Model):
  note = models.CharField(max_length=500)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)