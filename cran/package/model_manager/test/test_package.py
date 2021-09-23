from datetime import datetime

from django.test import TestCase

from cran.package.model_manager.package import PackageManager


class PackageManagerTestCase(TestCase):

    sample_obj = {
        "name": "Test package",
        "version": "1.0.0",
        "publication_timestamp": datetime(
            year=2019, month=11, day=9, hour=16, minute=20, second=2
        ),
        "title": " Sample Title",
        "description": "This is a sample package.",
        "author_name": "Anshul Chugh",
        "author_email": "achugh95@gmail.com",
        "maintainer_name": "Anshul Chugh",
        "maintainer_email": "achugh95@gmail.com",
    }

    def test_create_object(self):
        response = PackageManager.create_object(create_data=self.sample_obj)
        self.assertEqual(response.name, "Test package", "test_create_object failed!")

    def test_get_object(self):
        create_response = PackageManager.create_object(create_data=self.sample_obj)
        get_response = PackageManager.get_object(filters={"name": "Test package"})
        self.assertEqual(create_response, get_response, "test_get_object failed!")

    def test_filter_objects(self):
        obj1 = PackageManager.create_object(self.sample_obj)
        obj2 = PackageManager.create_object(self.sample_obj)
        response = PackageManager.filter_objects(filters={"name": "Test package"})
        self.assertEqual(response.count(), 2, "test_filter_objects failed!")

    def test_update_object(self):
        obj = PackageManager.create_object(self.sample_obj)
        updated_obj = PackageManager.update_object(
            obj=obj, update_data={"name": "Test package updated"}
        )
        self.assertEqual(
            updated_obj.name, "Test package updated", "test_update_object failed!"
        )

    def test_delete_object(self):
        obj = PackageManager.create_object(self.sample_obj)
        # Soft Delete
        soft_deleted_obj = PackageManager.delete_object(obj=obj, soft_delete=True)
        self.assertEqual(soft_deleted_obj.is_active, False, "test_delete_object failed")
        # Hard Delete
        deleted_obj_count, deleted_obj = PackageManager.delete_object(
            obj=obj, soft_delete=False
        )
        self.assertEqual(deleted_obj_count, 1, "test_delete_object failed")
