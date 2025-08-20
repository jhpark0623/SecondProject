import csv
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from .forms import UploadCSVForm
from .models import CCTV


def upload_csv(request):
    if request.method == "POST":
        # CSV → DB 컬럼명 매핑
        column_mapping = {
            '무인교통단속카메라관리번호': 'managementNumber',
            '위도': 'latCrdn',
            '경도': 'lonCrdn',
            '소재지지번주소': 'roadNmAddr',
            '설치장소': 'location',
            '데이터기준일자': 'baseDate',

        }

        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]

            # 파일이 csv인지 확인
            if not csv_file.name.endswith(".csv"):
                return render(request, "file/upload.html", {"form": form, "error": "CSV 파일만 업로드 가능합니다."})

            # CSV 읽기
            decoded_file = csv_file.read().decode("utf-8-sig").splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                CCTV.objects.update_or_create(
                    managementNumber=row['무인교통단속카메라관리번호'],
                    defaults={
                        'latCrdn': row['위도'],
                        'lonCrdn': row['경도'],
                        'roadNmAddr': row['소재지지번주소'],
                        'location': row['설치장소'],
                        'baseDate': row['데이터기준일자']
                    }
                )

            return redirect("upload_success")  # 업로드 완료 페이지로 이동
    else:
        form = UploadCSVForm()

    return render(request, "file/upload.html", {"form": form})
