from datetime import timedelta
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


def set_jwt_cookies(response, user):
    """
    Generates JWT tokens and sets them as HTTP-only cookies.
    """
    refresh = RefreshToken.for_user(user)

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=False,  # set to True in production with HTTPS
        samesite='Lax',
        max_age=60 * 15
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='Lax',
        max_age=60 * 60 * 24 * 7
    )
