from django.db import models
from .user import User

class Keyword(models.Model):
  target_keyword = models.CharField(max_length=10)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)