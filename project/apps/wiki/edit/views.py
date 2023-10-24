from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import loader

from ..models import Category, Page

from ..fetch import create_heirarchy

from ..renderer import render_to_html, markdown_builder

import re


md = markdown_builder()

def dashboard(request):
    return HttpResponse("Hello, world. You're at the edit index.")


# def browse(request: HttpRequest):
#     heirarchy = create_heirarchy()

#     z = ""

#     def recur(z, w, indent=0):
#         z += f"{'&emsp;' * indent * 2}= <a href=\"./category/{w.node.id}\">{w.node.title}</a><br/>"

#         for p in w.pages:
#             z += f"{'&emsp;' * indent * 2}- <a href=\"./page/{p.id}\">{p.title}</a><br/>"

#         for child_w in w.wrappers:
#             z = recur(z, child_w, indent+1)

#         # return recur(z, w, indent+1)
#         return z

#     for wrapper in heirarchy:
#         z = recur(z, wrapper)
#         z += "<br/>"
        

#     return HttpResponse(f'<p>{z}</p>')


def category(request: HttpRequest, pk: int):
    c = Category.objects.get(pk=pk)
    # x