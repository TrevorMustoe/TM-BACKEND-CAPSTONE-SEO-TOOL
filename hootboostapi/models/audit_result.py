from django.db import models
from .website import Website
from .notes import Notes
from .user import User

class Audit_result(models.Model):
  website_id = models.ForeignKey(Website, on_delete=models.CASCADE)
  title_tag = models.BooleanField(default=False)
  meta_desc_found = models.BooleanField(default=False)
  heading_tags_found = models.CharField(max_length=255)
  keyword_page_frequency = models.IntegerField(0)
  created_at = models.DateTimeField()
  score = models.IntegerField(default=0)
  audit_notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)