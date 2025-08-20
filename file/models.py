from django.db import models

# Create your models here.
class CCTV(models.Model):
    managementNumber = models.CharField(max_length=50, null=True, unique=True)  # 관리번호
    latCrdn = models.CharField(max_length=50, null=True)  # 위도
    lonCrdn = models.CharField(max_length=50, null=True)  # 경도
    roadNmAddr = models.CharField(max_length=300, null=True)  # 도로명 주소
    location = models.CharField(max_length=300, null=True)  # 설치 장소
    baseDate = models.CharField(max_length=50, null=True)  # 기준 일자

    def __str__(self):
        return self.location
