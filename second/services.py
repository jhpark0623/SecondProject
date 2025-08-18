import requests
import xmltodict
from .models import ParkingBasic, ParkingAvailability


def save_parking_basic():
    url = "https://openapigits.gg.go.kr/api/rest/getParkingPlaceInfoList?serviceKey=95b8cff60d5626815e5938356eec4d7ac28384&laeId=31100"  # 실제 API 주소
    response = requests.get(url)
    data = xmltodict.parse(response.text)
    

    items = data['ServiceResult']['msgBody']['itemList']

    # itemList가 하나만 오면 dict, 여러 개면 list
    if isinstance(items, dict):
        items = [items]

    for item in items:
        ParkingBasic.objects.update_or_create(
            pkplcId=item.get('pkplcId', ''),
            defaults={
                "latCrdn": item.get("latCrdn", ""),
                "lonCrdn": item.get("lonCrdn", ""),
                "pkplcNm": item.get("pkplcNm", ""),
                "roadNmAddr": item.get("roadNmAddr", ""),
                "pklotCnt": item.get("pklotCnt", ""),
                "wkdayOprtStartTime": item.get("wkdayOprtStartTime", ""),
                "wkdayOprtEndTime": item.get("wkdayOprtEndTime", ""),
                "satOprtStartTime": item.get("satOprtStartTime", ""),
                "satOprtEndTime": item.get("satOprtEndTime", ""),
                "hldyOprtStartTime": item.get("hldyOprtStartTime", ""),
                "hldyOprtEndTime": item.get("hldyOprtEndTime", ""),
                "parkingBscTime": item.get("parkingBscTime", ""),
                "parkingBscFare": item.get("parkingBscFare", ""),
                "addUnitTime": item.get("addUnitTime", ""),
                "addUnitFare": item.get("addUnitFare", "")
            }
        )


def save_parking_availability():
    url = "https://openapigits.gg.go.kr/api/rest/getParkingPlaceAvailabilityInfoList?serviceKey=95b8cff60d5626815e5938356eec4d7ac28384&laeId=31100"  # 실제 API 주소
    response = requests.get(url)
    data = xmltodict.parse(response.text)

    items = data['ServiceResult']['msgBody']['itemList']
    if isinstance(items, dict):
        items = [items]

    for item in items:
        ParkingAvailability.objects.update_or_create(
            pkplcId=item.get('pkplcId', ''),
            defaults={'laeNm' : item.get("laeNm", ""),
        'pkplcNm' : item.get("pkplcNm", ""),
        'pklotCnt' : item.get("pklotCnt", ""),
        'avblPklotCnt' : item.get("avblPklotCnt", ""),
        'ocrnDt' : item.get("ocrnDt", "")}
        )