from django.http import HttpRequest


class HttpRequestWithData(HttpRequest):
    data: dict
