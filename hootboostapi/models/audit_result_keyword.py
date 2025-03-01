from django.db import models
from .keyword import Keyword
from .audit_result import Audit_result


class Audit_Result_Keyword(models.Model): 
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    audit_result = models.ForeignKey(Audit_result, on_delete=models.CASCADE)