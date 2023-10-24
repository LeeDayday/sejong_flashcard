from typing import Any
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.request import Request
from accounts.models import NewUserInfo
from quizzes.models import Deck


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    작성자만 수정/삭제 가능
    그 외는 오직 읽기만
    """
    def has_object_permission(self, request: Request, view: Any, obj) -> bool:
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
