from django.urls import include, path

app_label = "users"

urlpatterns = [
    path("", include("users.api.v1.urls")),
]
