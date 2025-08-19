from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

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
