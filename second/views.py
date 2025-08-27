from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token

from file.models import CCTV
from second.models import ParkingBasic, Camera, ParkingAvailability, Favorite


def map_view(request):
    basics = ParkingBasic.objects.all()
    availability = ParkingAvailability.objects.all()
    cctv = CCTV.objects.all()

    # 로그인 사용자 즐겨찾기 pkplcId 집합
    fav_ids = set()
    if request.user.is_authenticated:
        fav_ids = set(
            Favorite.objects.filter(user=request.user)
            .values_list('parking__pkplcId', flat=True)
        )

    availability_dict = {
        a.pkplcNm: {
            "available": int(a.avblPklotCnt),
            "time": a.ocrnDt
        }
        for a in availability
    }

    basics_list = []
    for b in basics:
        name = b.pkplcNm
        pkplc_id = b.pkplcId
        basic_info = {
            "id": pkplc_id,  # ← JS에서 즐겨찾기 토글 시 사용 (data-pk로 전달)
            "name": name,
            "lat": float(b.latCrdn),
            "lng": float(b.lonCrdn),
            "total": int(b.pklotCnt) if b.pklotCnt else 0,
            "address": b.roadNmAddr,
            "weekdayTime": f"{b.wkdayOprtStartTime} ~ {b.wkdayOprtEndTime}",
            "saturdayTime": f"{b.satOprtStartTime} ~ {b.satOprtEndTime}",
            "holidayTime": f"{b.hldyOprtStartTime} ~ {b.hldyOprtEndTime}",
            "basicRate": f"{b.parkingBscFare}원 / {b.parkingBscTime}분",
            "addRate": f"{b.addUnitFare}원 / {b.addUnitTime}분",
            "avblPklotCnt": availability_dict.get(name, {}).get("available", "정보 없음"),
            "ocrnDt": availability_dict.get(name, {}).get("time", "-"),

            "isFavorite": pkplc_id in fav_ids,
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

    # 자동완성에 쓸 이름 리스트 생성 (중복 제거)
    autocomplete_names = list(set(
        [b["name"] for b in basics_list] +
        [c["name"] for c in cctvList]
    ))
    autocomplete_names.sort()

    autocomplete_json = json.dumps(autocomplete_names)

    context = {
        "basics": basics_list,
        "basics_json": basics_json,
        "cctv_json": cctv_json,
        "availability_json": availability_json,
    }
    return render(request, "main.html", context)


@require_POST
@login_required
def toggle_favorite(request, pkplcId: str):
    try:
        parking = ParkingBasic.objects.get(pkplcId=pkplcId)
    except ParkingBasic.DoesNotExist:
        return JsonResponse({"ok": False, "error": "NOT_FOUND"}, status=404)

    fav, created = Favorite.objects.get_or_create(user=request.user, parking=parking)
    if created:
        return JsonResponse({"ok": True, "status": "added"})
    else:
        fav.delete()
        return JsonResponse({"ok": True, "status": "removed"})


@login_required
def favorite_ids(request):
    ids = list(
        Favorite.objects.filter(user=request.user)
        .select_related("parking")
        .values_list("parking__pkplcId", flat=True)
    )
    return JsonResponse({"ok": True, "ids": ids, "csrfToken": get_token(request)})

@login_required
def favorite_list(request):
    qs = (Favorite.objects
          .filter(user=request.user)
          .select_related('parking')
          .order_by('-created_at'))
    return render(request, "favorite_list.html", {
        "favorites": qs,
    })
