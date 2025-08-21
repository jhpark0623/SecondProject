from django.shortcuts import render

from file.models import CCTV
from second.models import ParkingBasic, Camera, ParkingAvailability


def map_view(request):
    basics = ParkingBasic.objects.all()
    availability = ParkingAvailability.objects.all()
    cctv = CCTV.objects.all()

    # 가용 데이터를 dict로 바꿔서 빠르게 조회
    availability_dict = {
        a.pkplcNm: {
            "available": int(a.avblPklotCnt),
            "time": a.ocrnDt
        }
        for a in availability
    }

    # 템플릿에서 바로 사용 가능한 기본 + 가용 데이터 포함 리스트
    basics_list = []

    for b in basics:
        name = b.pkplcNm
        pkplc_id = b.pkplcId
        basic_info = {
            "id": pkplc_id,
            "name": name,
            "lat": float(b.latCrdn),
            "lng": float(b.lonCrdn),
            "total": int(b.pklotCnt) if b.pklotCnt else 0,
            "address": b.roadNmAddr,

            # 운영시간
            "weekdayTime": f"{b.wkdayOprtStartTime} ~ {b.wkdayOprtEndTime}",
            "saturdayTime": f"{b.satOprtStartTime} ~ {b.satOprtEndTime}",
            "holidayTime": f"{b.hldyOprtStartTime} ~ {b.hldyOprtEndTime}",

            # 요금
            "basicRate": f"{b.parkingBscFare}원 / {b.parkingBscTime}분",
            "addRate": f"{b.addUnitFare}원 / {b.addUnitTime}분",

            # 가용 정보
            "avblPklotCnt": availability_dict.get(name, {}).get("available", "정보 없음"),
            "ocrnDt": availability_dict.get(name, {}).get("time", "-")
        }
        basics_list.append(basic_info)


        basics_list.sort(key=lambda b: b["name"])

    import json
    basics_json = json.dumps(basics_list)

    cctvList = []
    for c in cctv:
        roadNmAddr = c.roadNmAddr
        cctv_info = {"name": roadNmAddr, "lat": float(c.latCrdn), "lng": float(c.lonCrdn)}
        cctvList.append(cctv_info)

    cctv_json = json.dumps(cctvList)

    availability_json = json.dumps([
        {
            "name": a.pkplcNm,
            "total": int(a.pklotCnt),
            "available": int(a.avblPklotCnt),
            "time": a.ocrnDt
        }
        for a in availability
    ])

    context = {
        "basics": basics_list,  # 여기에 기본 + 가용 정보 포함됨
        "basics_json": basics_json,
        "cctv_json": cctv_json,
        "availability_json": availability_json,
    }
    return render(request, "main.html", context)
