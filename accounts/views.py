from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
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
    return render(request, "accounts/profile.html", {"profile_user": request.user})

@user_passes_test(lambda u: u.is_staff, login_url="/accounts/login/")
def profile_admin(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    return render(request, "accounts/profile.html", {"profile_user": profile_user})


def profile_update(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")


        # 비밀번호 확인
        if not request.user.check_password(password1):
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            return render(request, "accounts/profile.html", {"profile_user": request.user})
        else:
            # DB 업데이트
            user = request.user
            user.email = email
            user.phone = phone
            user.save()

            messages.success(request, "회원정보가 수정되었습니다.")
            return redirect("/")  # 수정 후 메인 페이지로 이동

    return render(request, "/")

@user_passes_test(lambda u: u.is_staff)  # 관리자만 실행 가능
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_staff:
        messages.error(request, "관리자는 비활성화할 수 없습니다.")
    else:
        user.is_active = not user.is_active
        user.save()

        if user.is_active :
            messages.success(request, f"{user.username} 계정이 활성화되었습니다.")
        else:
            messages.success(request, f"{user.username} 계정이 비활성화되었습니다.")

    return redirect("admin_page")


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
    # ✅ 페이지네이션 추가
    paginator = Paginator(users, 10)  # 페이지당 10명
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # ✅ 페이지 번호 범위 (현재 페이지 ±2)
    current_page = page_obj.number
    total_pages = paginator.num_pages
    start_page = max(current_page - 2, 1)
    end_page = min(current_page + 2, total_pages)
    page_range = range(start_page, end_page + 1)

    return render(request, "accounts/admin_page.html", {
        "users": page_obj,     # 목록
        "page_obj": page_obj,  # 페이지네이션 UI용
        "page_range": page_range,
        "query": query,
    })

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
    search = request.GET.get("search", "")


    if request.user.is_staff:

        suggestions = Suggestion.objects.select_related("reply").all().order_by("-created_at")
    else:

        suggestions = Suggestion.objects.select_related("reply").filter(author=request.user).order_by("-created_at")

    if search:
        suggestions = suggestions.filter(
            Q(title__icontains=search)  |
            Q(content__icontains=search) |
            Q(author__username__icontains=search)

        )

    # 페이지네이션 (한 페이지당 10개)
    paginator = Paginator(suggestions, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # ✅ 페이지 범위 커스터마이즈 (현재 페이지 기준 ±2)
    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(current_page - 2, 1)
    end_page = min(current_page + 2, total_pages)
    page_range = range(start_page, end_page + 1)

    return render(request, "accounts/suggestion_list.html", {
        "suggestions": page_obj,  # 목록
        "page_obj": page_obj,  # 기본 page_obj
        "page_range": page_range,  # 우리가 커스텀한 범위
        "search": search,
    })


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



