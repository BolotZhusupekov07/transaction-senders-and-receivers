from django.urls import include, path

app_label = "transactions"

urlpatterns = [
    path("", include("transactions.api.v1.urls")),
]
