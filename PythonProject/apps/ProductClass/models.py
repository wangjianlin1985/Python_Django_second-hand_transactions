from django.db import models


class ProductClass(models.Model):
    classId = models.AutoField(primary_key=True, verbose_name='类别id')
    className = models.CharField(max_length=40, default='', verbose_name='类别名称')
    classDesc = models.CharField(max_length=500, default='', verbose_name='类别描述')

    class Meta:
        db_table = 't_ProductClass'
        verbose_name = '商品类别信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        productClass = {
            'classId': self.classId,
            'className': self.className,
            'classDesc': self.classDesc,
        }
        return productClass

