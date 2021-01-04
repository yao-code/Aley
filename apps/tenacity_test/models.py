from django.db import models

# Create your models here.
from django.db import models


class Article(models.Model):
    """文章模型"""
    title = models.CharField('标题', max_length=200, )

    class Meta:
        indexes = [models.Index(fields=['title']), ]
