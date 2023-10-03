from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import loader

from .fetch import page_from_path, text_from_page, path_from_string

from .renderer.run import render_to_html, markdown_builder

import re

prefix = '/wiki'


md = markdown_builder()

def index(request):
    return HttpResponse("Hello, world. You're at the wiki index.")


def content(request: HttpRequest):
    path = path_from_string(request.path, prefixes=1)
    page = page_from_path(path)
    text = text_from_page(page)

    if (text):
        rendered_page_text = render_to_html(md, text)

        context = {
            "page_title": page.title, 
            "sections": rendered_page_text.sections,
            "content": rendered_page_text.content, 
            "base_dir": "wiki/",
        }
        template = loader.get_template("wiki/content.html")

        return HttpResponse(template.render(context, request))
    return HttpResponse('404')
