from django.urls import path

from users.api.v1 import views

urlpatterns = [
    path(
        "api/v1/users/<uuid:user_id>/balance/",
        views.UserBalanceAPIView.as_view(),
        name="user-balance",
    ),
]
