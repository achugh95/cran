from django.contrib import admin
from django.urls import path, include

from cran.package import urls as package_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("package/", include(package_urls.urlpatterns)),
            ]
        ),
    ),
]
