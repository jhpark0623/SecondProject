from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Suggestion, SuggestionReply

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

@login_required(login_url="/accounts/login/")
def profile(request):
    return render(request, "accounts/profile.html")

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

@staff_member_required(login_url="/accounts/login/")
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

@login_required(login_url="/accounts/login/")
def suggestion_create(request):
    if request.method == "POST" :
        title = request.POST.get("title")
        content = request.POST.get("content")
        Suggestion.objects.create(
            title=title,
            content=content,
            author=request.user
        )

        return redirect("suggestion_list")
    return render(request, "accounts/suggestion_form.html")

@login_required(login_url="/accounts/login/")
def suggestion_list(request):
    if request.user.is_staff:

        suggestions = Suggestion.objects.select_related("reply").all().order_by("-created_at")
    else:

        suggestions = Suggestion.objects.select_related("reply").filter(author=request.user).order_by("-created_at")

    return render(request, "accounts/suggestion_list.html", {"suggestions": suggestions})


@login_required(login_url="/accounts/login/")
def suggestion_detail(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)

    if suggestion.author != request.user and not request.user.is_staff:
        return redirect("accounts/suggestion_list")
    return render(request, "accounts/suggestion_detail.html", {"suggestion": suggestion})

@login_required(login_url="/accounts/login/")
def suggestion_reply(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)

    if request.user.is_staff:
        if request.method == "POST":
            reply_content = request.POST.get("content")

            SuggestionReply.objects.create(
                suggestion=suggestion,
                content=reply_content,
                admin=request.user
            )

            return redirect("suggestion_detail", pk=pk)


        return render(request, "accounts/suggestion_detail.html", {"suggestion": suggestion})

    else:
        return redirect("suggestion_detail", pk=pk)

@login_required(login_url="/accounts/login/")
def suggestion_reply_delete(request, reply_id):
    reply = get_object_or_404(SuggestionReply, id=reply_id)

    if not request.user.is_staff:  # 관리자가 아닌 경우 차단
        return redirect("suggestion_detail", pk=reply.suggestion.pk)

    if request.method == "POST":
        reply.delete()
        return redirect("suggestion_detail", pk=reply.suggestion.pk)



