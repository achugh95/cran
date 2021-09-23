from rest_framework import serializers

from cran.package.model_manager.package import Package, PackageManager


class PackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            "name",
            "version",
            "publication_timestamp",
            "title",
            "description",
            "author_name",
            "author_email",
            "maintainer_name",
            "maintainer_email",
        ]
        read_only_fields = ("id",)

    def get_packages(self, name: str):
        filters = {
            "name__icontains": name,
            "is_active": True,
        }
        return PackageManager.filter_objects(filters=filters)
