from django.urls import path

from cran.package.views import PackageListView

urlpatterns = [
    path("search/", PackageListView.as_view()),
]
