from django.conf import settings
from django.conf.urls.static import static
from django.urls import URLPattern, URLResolver, include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Scramble Transactions Test Task",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns: list[URLResolver | URLPattern] = [
    path("", include("transactions.urls")),
    path("", include("users.urls")),
]

if settings.ENABLE_DEBUG_TOOLBAR:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )


if settings.SWAGGER_ENABLED:
    urlpatterns += [
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]
