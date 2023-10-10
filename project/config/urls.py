from django.contrib import admin
from django.urls import include, path

from config import settings

from django.conf.urls.static import static

urlpatterns = [
    path('edit/', admin.site.urls),
    # path("wiki/", include("apps.wiki.urls")),
    # path("edit/", include("apps.edit.urls")),
    path("archive/", include("apps.archive.urls")),
    path("api/", include("apps.api.urls")),
]

# dev
if (settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)