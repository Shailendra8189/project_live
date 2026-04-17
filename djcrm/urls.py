from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib import admin
from django.urls import path, include
from leads.views import SignupView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("leads.urls")),
    path("agent/", include("agent.urls", namespace="agent")),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("reset_password/", PasswordResetView.as_view(), name="reset_password"),
    path(
        "reset_password_done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset_password_confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
