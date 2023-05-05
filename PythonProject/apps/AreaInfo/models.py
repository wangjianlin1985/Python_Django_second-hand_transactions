from django.db import models


class AreaInfo(models.Model):
    areaId = models.AutoField(primary_key=True, verbose_name='区域id')
    areaName = models.CharField(max_length=20, default='', verbose_name='区域名称')

    class Meta:
        db_table = 't_AreaInfo'
        verbose_name = '所在区域信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        areaInfo = {
            'areaId': self.areaId,
            'areaName': self.areaName,
        }
        return areaInfo

