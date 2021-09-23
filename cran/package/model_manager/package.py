import logging
from typing import Dict, Union, Tuple, List

from cran.config import CONFIG
from cran.package.models import Package

logging.getLogger().setLevel("INFO")


class PackageManager:
    """
    A model manager for Package model. It contains all the database related functions.
    """

    @staticmethod
    def get_object(filters: Dict) -> Union[Package, Tuple]:
        """
        This method is used to fetch an object which is expected to be present in database.

        :param filters: A dict object containing the relevant key-value pairs of the model columns and their values.
        :return: A Package object if the filters match any of the existing data. Else a tuple of relevant error code &
        message.
        """
        logging.debug("Get object function called")
        logging.info(f"Filters: {filters}")
        try:
            return Package.objects.get(**filters)
        except Package.DoesNotExist:
            logging.error("Object does not exist")
            return CONFIG.DB.OBJECT_NOT_FOUND
        except Exception as e:
            logging.error(f"Error: {e}")
            return CONFIG.DB.FAILURE

    @staticmethod
    def filter_objects(filters: Dict) -> Union[List[Package], Tuple]:
        """
        This method is used to fetch object(s).

        :param filters: A dict object containing the relevant key-value pairs of the model columns and their values.
        :return: A list of Package object(s) if the filters the existing data. Else a tuple of relevant error code &
        message.
        """
        logging.debug("Filter object function called")
        logging.info(f"Filters: {filters}")
        try:
            return Package.objects.filter(**filters)
        except Exception as e:
            logging.error(f"Error: {e}")
            return CONFIG.DB.FAILURE

    @staticmethod
    def update_object(obj: Package, update_data: Dict) -> Union[Package, Tuple]:
        """
        This method is used to update an object.

        :param obj: An instance of Package model which needs to be updated.
        :param update_data: A dict object containing the new key-value pairs for the instance/object.
        :return: The updated object or a tuple of relevant error code & message.
        """
        logging.debug("Update object function called")
        logging.info(f"Object: {obj}")
        logging.info(f"Update Data: {update_data}")
        try:
            for key, value in update_data.items():
                setattr(obj, key, value)
            obj.save()
            return obj
        except Exception as e:
            logging.error(f"Error while updating: {e}")
            return CONFIG.DB.FAILURE

    @staticmethod
    def create_object(create_data: Dict) -> Union[Package, Tuple]:
        """
        This method is used to create an object.

        :param create_data: A dict object containing the key-value pairs for the new instance/object.
        :return: The new object or a tuple of relevant error code & message.
        """
        logging.debug("Create object function called")
        logging.debug(f"Create Data: {create_data}")
        try:
            return Package.objects.create(**create_data)
        except Exception as e:
            logging.error(f"Error: {e}")
            return CONFIG.DB.FAILURE

    @staticmethod
    def delete_object(obj: Package, soft_delete: bool = True) -> Union[Package, Tuple]:
        """
        This method is used to update an object.

        :param obj: An instance of Package model which needs to be updated.
        :param soft_delete: A boolean which specifies the choice of delete (soft/hard). It is set to True(soft delete)
        by default.
        :return: The updated object or a tuple of number of objects deleted and a dictionary with the number of
        deletions per object type. In case of an error, it returns a tuple of relevant error code & message.
        """
        logging.info("Delete object function called")
        logging.info(f"Object: {obj}")
        logging.info(f"Soft Delete: {soft_delete}")
        if soft_delete:
            try:
                return PackageManager.update_object(obj, {"is_active": False})
            except Exception as e:
                logging.error(f"Error: {e}")
                return CONFIG.DB.FAILURE
        else:
            logging.warning(f"Permanently deleting the object : {obj}")
            try:
                return obj.delete()
            except Exception as e:
                logging.error(f"Error: {e}")
                return CONFIG.DB.FAILURE
