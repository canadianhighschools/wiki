from django.contrib import admin
from django.urls import include, path

import settings.base as settings

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("wiki/", include("apps.wiki.urls")),
]

# add media as an url pattern in dev
if (settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)