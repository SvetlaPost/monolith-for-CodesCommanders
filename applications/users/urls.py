from django.urls import path
from applications.users.views.auth import (
    UserRegisterAPIView,
    LogInAPIView,
    LogOutAPIView,
    TokenRefreshView,
)
from applications.users.views.users import (
    UserListView,
    UserProfileUpdateView,
)

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', LogInAPIView.as_view(), name='user-login'),
    path('logout/', LogOutAPIView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
]
