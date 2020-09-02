from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = "aley_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name