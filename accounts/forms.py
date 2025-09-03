from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # 1) 아이디 확인
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("❌ 아이디 또는 비밀번호가 잘못되었습니다.\n 아이디와 비밀번호를 정확히 입력해주세요.", code="invalid_login")

        # 2) 비밀번호 확인
        if not user.check_password(password):
            raise forms.ValidationError("❌아이디 또는 비밀번호가 잘못되었습니다.\n 아이디와 비밀번호를 정확히 입력해주세요.", code="invalid_login")

        # 3) 비활성화 계정 확인
        if not user.is_active:
            raise forms.ValidationError("❌ 비활성화된 계정입니다. 관리자에게 문의하세요.", code="inactive")

        # 4) 나머지는 부모 clean()으로 넘겨 처리 (세션 설정 등)
        return super().clean()
