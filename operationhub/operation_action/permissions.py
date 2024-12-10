from rest_framework.permissions import BasePermission

class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # 사용자가 인증된 상태인지 확인
        if not user.is_authenticated:
            return False

        # 관리자는 모든 데이터에 접근 가능
        if user.is_staff:
            return True

        # 일반 사용자는 자신의 데이터만 조회 가능
        email_id = request.query_params.get('email_id')  # URL 파라미터에서 email_id 추출
        if email_id and user.email == email_id:
            return True
        
        return False

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # 사용자가 인증된 상태인지 확인
        if not user.is_authenticated:
            return False

        # 관리자는 모든 데이터에 접근 가능
        if user.is_staff:
            return True

        return False

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # 사용자가 인증된 상태인지 확인
        if not user.is_authenticated:
            return False

        # 슈퍼유저는 모든 데이터에 접근 가능
        if user.is_superuser:
            return True

        return False
