class CONFIG:
    class GENERIC:
        SUCCESS = 0
        FAILURE = 1

    class DB:
        OBJECT_NOT_FOUND = 1
        MULTIPLE_OBJECTS_EXIST = 2
        FAILURE = 3
        INVALID_OPERATION_REQUESTED = 4

    class EXTERNAL_API:
        ALL_PACKAGES = "https://cran.r-project.org/src/contrib/PACKAGES"
        PACKAGE_DETAIL = "https://cran.r-project.org/src/contrib/$package_name$separator$package_version.tar.gz"
        DETAIL_FILE_NAME = "DESCRIPTION"
