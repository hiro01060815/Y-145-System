from django.db import models
from django.contrib.auth.models import User


class D31Info(models.Model):
    user = models.ForeignKey(User,verbose_name='ユーザ',related_name='user',on_delete=models.CASCADE)
    SELECTION=((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'))
    #数字と半角空白で管理
    yasumi = models.CharField('希望休',max_length = 255,default="")
    #SELECTION1=((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10'),(11,'11'),(12,'12'))
    #month = models.IntegerField('月',choices=SELECTION1,default=1)
    SELECTION1=((0,'--'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10'),(11,'11'),(12,'12'))
    month = models.IntegerField('月',choices=SELECTION1,default=0)
    SELECTION2 = ((0,'未選択'),(1,'選択中'),(2,'選択済み'))
    status = models.IntegerField('ステータス',choices=SELECTION2,default=0)
    form = models.CharField('フォーム内容',max_length = 10000,default = "")
    table = models.IntegerField('テーブル優先順位',default=0)
    def __str__(self):
        return str(self.user.username)+"/"+str(self.month)