from django.http import HttpResponse, HttpRequest

prefix = '/archive'


def index(request):
    return HttpResponse("Hello, world. You're at the archive index.")


def item(request: HttpRequest, item_id: int):
    return HttpResponse(f"Hello, world. You're at the archive item index for {item_id}.")
