from django.db import models


class TimestampMixin(models.Model):

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Package(TimestampMixin):

    name = models.CharField(max_length=255, db_index=True)
    version = models.CharField(max_length=255)
    publication_timestamp = models.DateTimeField()
    title = models.CharField(max_length=500)
    description = models.TextField(null=True)
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField(null=True)
    maintainer_name = models.CharField(max_length=255)
    maintainer_email = models.EmailField(null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "package"

    def __str__(self):
        return self.name
