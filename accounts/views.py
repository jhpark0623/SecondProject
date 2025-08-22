from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "accounts/signup.html", {
                "error": "비밀번호가 일치하지 않습니다."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/signup.html", {
                "error": "이미 존재하는 아이디입니다."
            })

        user = User.objects.create_user(
            username=username,
            name=name,
            email=email,
            phone=phone,
            password=password1
        )

        return redirect("login")  # 로그인 페이지로 이동

    return render(request, "accounts/signup.html")

def profile(request):
    return render(request, "accounts/profile.html")

@login_required
def profile_update(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")

        # 비밀번호 확인
        if not request.user.check_password(password1):
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            return render(request, "accounts/profile.html", {"user": request.user})
        else:
            # DB 업데이트
            user = request.user
            user.email = email
            user.phone = phone
            user.save()

            messages.success(request, "회원정보가 수정되었습니다.")
            return redirect("/")  # 수정 후 메인 페이지로 이동

    return render(request, "/")


def admin_page(request):
    query = request.GET.get("q", "")

    users = User.objects.all()

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, "accounts/admin_page.html", {"users": users, "query" :query } )