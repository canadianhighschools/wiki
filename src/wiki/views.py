from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import loader

from core.models import Category, Page, Revision, TextContent
from common.fetch import text_from_path

from .parser.run import render_to_html

import re

prefix = '/wiki'


def index(request):
    return HttpResponse("Hello, world. You're at the wiki index.")


def content(request: HttpRequest):
    text = text_from_path(request.path)
    if (text):
        page_content = render_to_html(text)

        context = { "page_content": page_content }
        template = loader.get_template("wiki/content.html")

        return HttpResponse(template.render(context, request))
    return HttpResponse('404')

    # parent_c = Category.objects.get(cat_slug=)

    # return HttpResponse(' '.join(groups))
