from django.db import models


class PriceRegion(models.Model):
    regionId = models.AutoField(primary_key=True, verbose_name='区间id')
    regionName = models.CharField(max_length=20, default='', verbose_name='区间名称')

    class Meta:
        db_table = 't_PriceRegion'
        verbose_name = '价格区间信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        priceRegion = {
            'regionId': self.regionId,
            'regionName': self.regionName,
        }
        return priceRegion

