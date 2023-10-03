from django.contrib import admin
from django.urls import include, path

from config.settings import base

from django.conf.urls.static import static

urlpatterns = [
    path('edit/', admin.site.urls),
    path("wiki/", include("apps.wiki.urls")),
    # path("edit/", include("apps.edit.urls")),
    path("archive/", include("apps.archive.urls")),
    path("api/", include("apps.api.urls")),
]

# dev
if (base.DEBUG):
    urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)
    urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)