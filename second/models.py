from django.db import models
from django.conf import settings

# Create your models here.
class ParkingBasic(models.Model):
    latCrdn = models.CharField(max_length=50, null=True)      # 위도
    lonCrdn = models.CharField(max_length=50, null=True)      # 경도
    pkplcNm = models.CharField(max_length=200, null=True)     # 주차장명
    pkplcId = models.CharField(max_length=50, unique=True, null=True)  # 주차장 ID
    roadNmAddr = models.CharField(max_length=300, null=True)  # 도로명 주소
    pklotCnt = models.CharField(max_length=20, null=True)     # 주차구획 수
    wkdayOprtStartTime = models.CharField(max_length=20, null=True)
    wkdayOprtEndTime = models.CharField(max_length=20, null=True)
    satOprtStartTime = models.CharField(max_length=20, null=True)
    satOprtEndTime = models.CharField(max_length=20, null=True)
    hldyOprtStartTime = models.CharField(max_length=20, null=True)
    hldyOprtEndTime = models.CharField(max_length=20, null=True)
    parkingBscTime = models.CharField(max_length=20, null=True)
    parkingBscFare = models.CharField(max_length=20, null=True)
    addUnitTime = models.CharField(max_length=20, null=True)
    addUnitFare = models.CharField(max_length=20, null=True)

    updated_at = models.DateTimeField(auto_now=True)  # 저장/갱신 시간

    def __str__(self):
        return f"{self.pkplcNm} ({self.pkplcId})"


class ParkingAvailability(models.Model):
    laeNm = models.CharField(max_length=100)       # 지방자치단체명
    pkplcId = models.CharField(max_length=50, unique=True)      # 주차장ID
    pkplcNm = models.CharField(max_length=200)     # 주차장명
    pklotCnt = models.CharField(max_length=20)     # 주차구획 수
    avblPklotCnt = models.CharField(max_length=20) # 가용 주차구획 수
    ocrnDt = models.CharField(max_length=50)       # 제공시간

    saved_at = models.DateTimeField(auto_now_add=True)  # DB 저장 시각

    def __str__(self):
        return f"{self.pkplcNm} ({self.avblPklotCnt}/{self.pklotCnt})"

class Camera(models.Model) :
    name = models.CharField(max_length=100, null=True)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    parking = models.ForeignKey(ParkingBasic, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'parking')  # 같은 유저가 같은 주차장 중복 등록 방지

    def __str__(self):
        return f"{self.user} ♥ {self.parking.pkplcNm}"