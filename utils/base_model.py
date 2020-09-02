from django.db import models

class BaseModel(models.Model):
    "基本模型， 所有的模型都继承这个模型, 抽象模型类，不会生成实体表"

    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        abstract = True
