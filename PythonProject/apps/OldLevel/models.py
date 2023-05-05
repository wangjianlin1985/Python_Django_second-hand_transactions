from django.db import models


class OldLevel(models.Model):
    levelId = models.AutoField(primary_key=True, verbose_name='新旧程度id')
    levelName = models.CharField(max_length=20, default='', verbose_name='新旧程度名称')

    class Meta:
        db_table = 't_OldLevel'
        verbose_name = '新旧程度信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        oldLevel = {
            'levelId': self.levelId,
            'levelName': self.levelName,
        }
        return oldLevel

