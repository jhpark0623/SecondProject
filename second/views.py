from django.shortcuts import render

from second.models import ParkingBasic, Camera, ParkingAvailability


def map_view(request):
    basics = ParkingBasic.objects.all()
    cameras = Camera.objects.all()
    availability = ParkingAvailability.objects.all()

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
        basic_info = {
            "name": name,
            "lat": float(b.latCrdn),
            "lng": float(b.lonCrdn),
            "total": int(b.pklotCnt) if b.pklotCnt else 0,
            "avblPklotCnt": availability_dict.get(name, {}).get("available", "정보 없음"),
            "ocrnDt": availability_dict.get(name, {}).get("time", "-")
        }
        basics_list.append(basic_info)

    # JSON 데이터
    import json
    basics_json = json.dumps(basics_list)
    cameras_json = json.dumps([
        {"name": c.name, "lat": c.lat, "lng": c.lon}
        for c in cameras
    ])
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
        "cameras_json": cameras_json,
        "availability_json": availability_json,
    }
    return render(request, "main.html", context)
