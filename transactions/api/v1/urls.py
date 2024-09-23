from django.urls import path

from transactions.api.v1 import views

urlpatterns = [
    path(
        "api/v1/transactions/",
        views.TransactionCreateAPIView.as_view(),
        name="transaction-create",
    ),
]
