from django.contrib import admin

from cran.package.models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    pass
