import logging
import re
from string import Template
from typing import Union, Tuple

from django.core.management.base import BaseCommand

from cran.config import CONFIG
from cran.libs import datetime_util
from cran.libs import filestore
from cran.libs.curl_controller import CurlController
from cran.libs.text import remove_prefix, remove_suffix
from cran.package.model_manager.package import PackageManager

logging.getLogger().setLevel("INFO")


class Command(BaseCommand):
    help = "Populates the package table."

    def handle(self, *args, **kwargs) -> None:
        """
        A command to populate the package information from the external end-points.
        """
        logging.info("Populating the package table...")
        Command.populate_package(package_count=100)
        logging.info("Done!")

    @staticmethod
    def populate_package(package_count: int) -> None:
        """
        A method which is called by the command method(handle). It reads the information present on the homepage(package
        list) and extracts package name and version. With package_name and package_version, it generates the package
        specific urls and downloads the tar file. Post that, it extracts the DESCRIPTION file from it and reads the
        details and extracts the required columns for `package` table.

        :param package_count: Number of packages to be inserted in the DB.
        """
        logging.info(f"Fetching {package_count} packages")
        response = CurlController.send_get_request(url=CONFIG.EXTERNAL_API.ALL_PACKAGES)
        get_version = False
        count = 0
        temp_dir = filestore.generate_temp_dir()
        # Local Testing
        # response_arr = ['Package: A3', 'Version: 1.0.0', 'Depends: R (>= 2.15.0), xtable, pbapply', 'Suggests: randomForest, e1071', 'License: GPL (>= 2)', 'MD5sum: 027ebdd8affce8f0effaecfcd5f5ade2', 'NeedsCompilation: no', '', 'Package: aaSEA', 'Version: 1.1.0', 'Depends: R(>= 3.4.0)', 'Imports: DT(>= 0.4), networkD3(>= 0.4), shiny(>= 1.0.5),', '        shinydashboard(>= 0.7.0), magrittr(>= 1.5), Bios2cor(>= 2.0),', '        seqinr(>= 3.4-5), plotly(>= 4.7.1), Hmisc(>= 4.1-1)', 'Suggests: knitr, rmarkdown', 'License: GPL-3', 'MD5sum: 0f9aaefc1f1cf18b6167f85dab3180d8', 'NeedsCompilation: no', '', 'Package: AATtools', 'Version: 0.0.1', 'Depends: R (>= 3.6.0)', 'Imports: magrittr, dplyr, doParallel, foreach', 'License: GPL-3', 'MD5sum: 3bd92dbd94573afb17ebc5eab23473cb', 'NeedsCompilation: no', '', 'Package: ABACUS', 'Version: 1.0.0', 'Depends: R (>= 3.1.0)', 'Imports: ggplot2 (>= 3.1.0), shiny (>= 1.3.1),', 'Suggests: rmarkdown (>= 1.13), knitr (>= 1.22)', 'License: GPL-3', 'MD5sum: 50c54c4da09307cb95a70aaaa54b9fbd', 'NeedsCompilation: no', '', 'Package: abbyyR', 'Version: 0.5.5', 'Depends: R (>= 3.2.0)', 'Imports: httr, XML, curl, readr, plyr, progress', 'Suggests: testthat, rmarkdown, knitr (>= 1.11), lintr', 'License: MIT + file LICENSE', 'MD5sum: e048a3bca6ea32126e6c367415c0bfaf', 'NeedsCompilation: no', '', 'Package: abc', 'Version: 2.1', 'Depends: R (>= 2.10), abc.data, nnet, quantreg, MASS, locfit', 'License: GPL (>= 3)', 'MD5sum: c9fffe4334c178917f762735aba59653', 'NeedsCompilation: no', '', 'Package: abc.data', 'Version: 1.0', 'Depends: R (>= 2.10)', 'License: GPL (>= 3)', 'MD5sum: 799079dbbdd0cfc9d9c61c3e35241806', 'NeedsCompilation: no', '', 'Package: ABC.RAP', 'Version: 0.9.0', 'Depends: R (>= 3.1.0)', 'Imports: graphics, stats, utils', 'Suggests: knitr, rmarkdown', 'License: GPL-3', 'MD5sum: 38c65a7251d28ef2462ee430ded95700', 'NeedsCompilation: no', '', 'Package: abcADM', 'Version: 1.0', 'Imports: Rcpp (>= 1.0.1)', 'LinkingTo: Rcpp, BH', 'License: GPL-3', 'MD5sum: 8134f67912b506194e3dab4ccd6e75f7', 'NeedsCompilation: yes', '', 'Package: ABCanalysis', 'Version: 1.2.1', 'Depends: R (>= 2.10)', 'Imports: plotrix', 'License: GPL-3', 'MD5sum: 678e03837e25a922bf71bafe1f8de617', 'NeedsCompilation: no', '', 'Package: abcdeFBA', 'Version: 0.4', 'Depends: Rglpk,rgl,corrplot,lattice,R (>= 2.10)', 'Suggests: LIM,sybil', 'License: GPL-2', 'MD5sum: c84d45a85d8ab6bbe517365e8845db83', 'NeedsCompilation: no', '', 'Package: ABCoptim', 'Version: 0.15.0', 'Imports: Rcpp, graphics, stats, utils', 'LinkingTo: Rcpp', 'Suggests: testthat, covr', 'License: MIT + file LICENSE', 'MD5sum: a62ed03650273c09899655065437078f', 'NeedsCompilation: yes', '', 'Package: ABCp2', 'Version: 1.2', 'Depends: MASS', 'License: GPL-2', 'MD5sum: e920282d5a369df71e15241be40cb60e', 'NeedsCompilation: no', '', 'Package: abcrf', 'Version: 1.8.1', 'Depends: R(>= 3.1)', 'Imports: readr, MASS, matrixStats, ranger, doParallel, parallel,', '        foreach, stringr, Rcpp (>= 0.11.2)', 'LinkingTo: Rcpp, RcppArmadillo', 'License: GPL (>= 2)', 'MD5sum: 4d5a304f46d117226791523cef4e2427', 'NeedsCompilation: yes', '', 'Package: abcrlda', 'Version: 1.0.3', 'Imports: stats', 'License: GPL-3', 'MD5sum: 651e6e18e08916b443aaf011b5a63525', 'NeedsCompilation: no', '', 'Package: abctools', 'Version: 1.1.3', 'Depends: R (>= 2.10), abc, abind, parallel, plyr, Hmisc', 'Suggests: ggplot2, abc.data', 'License: GPL (>= 2)', 'MD5sum: c5937b65837ef7e6bfbe141cea257f40', 'NeedsCompilation: yes', '', 'Package: abd', 'Version: 0.2-8', 'Depends: R (>= 3.0), nlme, lattice, grid, mosaic', 'Suggests: boot, car, ggplot2, plyr, HH, ICC, vcd, Hmisc', 'License: GPL-2', 'MD5sum: 1913d76a0fbc44222709381f63f385b9', 'NeedsCompilation: no', '', 'Package: abdiv', 'Version: 0.2.0', 'Imports: ape', 'Suggests: testthat (>= 2.1.0), vegan', 'License: MIT + file LICENSE', 'MD5sum: 80931c0ca85ba5386000bf617552c5ce', 'NeedsCompilation: no', '', 'Package: abe', 'Version: 3.0.1', 'License: GPL (>= 2)', 'MD5sum: 9c151db5397422c8927dee41dabfbfab', 'NeedsCompilation: no', '', 'Package: abess', 'Version: 0.3.0', 'Depends: R (>= 3.1.0)', 'Imports: Rcpp, MASS, methods, Matrix', 'LinkingTo: Rcpp, RcppEigen', 'Suggests: testthat, knitr, rmarkdown', 'License: GPL (>= 3) | file LICENSE', 'MD5sum: e0ea7d068147c49c011c7135ab290bd3', 'NeedsCompilation: yes', '', 'Package: abf2', 'Version: 0.7-1', 'License: Artistic-2.0', 'MD5sum: 6792a51c6fb3e239165d69aa8a71d3cd', 'NeedsCompilation: no', '', 'Package: abglasso', 'Version: 0.1.1', 'Imports: MASS, pracma, stats, statmod', 'Suggests: testthat', 'License: GPL-3', 'MD5sum: 18bd0759cd005c5ac6fb515799b3f3d8', 'NeedsCompilation: no', '', 'Package: ABHgenotypeR', 'Version: 1.0.1', 'Imports: ggplot2, reshape2, utils', 'Suggests: knitr, rmarkdown', 'License: GPL-3', 'MD5sum: ca4397ba7390c0e0a3728c0cda864494', 'NeedsCompilation: no', '', 'Package: abind', 'Version: 1.4-5', 'Depends: R (>= 1.5.0)', 'Imports: methods, utils', 'License: LGPL (>= 2)', 'MD5sum: 136f981e1c4f618b64a87faaa7797c97', 'NeedsCompilation: no', '', 'Package: abjutils', 'Version: 0.3.1', 'Depends: R (>= 4.0)', 'Imports: dplyr, magrittr, purrr, rlang, rstudioapi, stringi, stringr,', '        tidyr', 'Suggests: testthat', 'License: MIT + file LICENSE', 'MD5sum: a596c07aaa7f82e5d123b2f7354e5b55', 'NeedsCompilation: no', '', 'Package: abmR', 'Version: 1.0.2', 'Depends: R (>= 3.5)', 'Imports: sp, rgdal, table1, googledrive, swfscMisc, geosphere,', '        kableExtra, gtsummary, ggplot2, gstat, purrr, rnaturalearth,', '        rnaturalearthdata, sf, tmap, raster, utils, stats, methods,', '        rgeos', 'Suggests: jpeg, knitr', 'License: GPL (>= 3)', 'MD5sum: cf96d']
        response_arr = response.decode("utf-8").split("\n")
        with temp_dir:
            for item in response_arr:
                if count >= package_count:
                    break
                if get_version:
                    # Fetching the version, once we have the package name
                    package_version = Command.get_package_version(item=item)
                    if package_version:
                        # Generating the required URL for the package to fetch the details
                        package_url = Template(
                            CONFIG.EXTERNAL_API.PACKAGE_DETAIL
                        ).substitute(
                            package_name=package_name,
                            separator="_",
                            package_version=package_version,
                        )
                        logging.info(f"Downloading {package_url}")
                        # Downloading the details of the package and extracting the DESCRIPTION file
                        extract_file_path = filestore.join_paths(
                            prefix=package_name,
                            suffix=CONFIG.EXTERNAL_API.DETAIL_FILE_NAME,
                        )
                        target_dir = filestore.download_file(
                            url=package_url,
                            temp_dir=temp_dir,
                            extract_file_path=extract_file_path,
                        )
                        # Reading contents of DESCRIPTION file
                        package_details = filestore.join_paths(
                            prefix=temp_dir.name,
                            suffix=extract_file_path,
                        )
                        with open(package_details) as details_file:
                            for line in details_file:
                                if line.startswith(PackageInfoPrefix.PUBLICATION_DATE):
                                    publication_time_str = (
                                        Command.get_publication_timestamp(line)
                                    )
                                    publication_timestamp = (
                                        datetime_util.string_to_datetime(
                                            publication_time_str
                                        )
                                    )
                                elif line.startswith(PackageInfoPrefix.TITLE):
                                    title = Command.get_package_title(line)
                                elif line.startswith(PackageInfoPrefix.DESCRIPTION):
                                    description = Command.get_package_description(line)
                                elif line.startswith(PackageInfoPrefix.AUTHOR):
                                    (
                                        author_name,
                                        author_email,
                                    ) = Command.get_package_author(line)
                                elif line.startswith(PackageInfoPrefix.MAINTAINER):
                                    (
                                        maintainer_name,
                                        maintainer_email,
                                    ) = Command.get_package_maintainer(line)

                            package_info_dict = {
                                "name": package_name,
                                "version": package_version,
                                "publication_timestamp": publication_timestamp,
                                "title": title,
                                "description": description,
                                "author_name": author_name,
                                "author_email": author_email,
                                "maintainer_name": maintainer_name,
                                "maintainer_email": maintainer_email,
                            }
                            logging.info(package_info_dict)
                            obj = PackageManager.create_object(
                                create_data=package_info_dict
                            )
                            if obj == CONFIG.DB.FAILURE:
                                raise Exception(f"Could not insert package in DB")
                        count += 1
                    get_version = False
                # Fetching the package name
                package_name = Command.get_package_name(item=item)
                if package_name:
                    get_version = True

    @staticmethod
    def get_package_name(item: str) -> Union[str, None]:
        """
        A helper method to extract package name.
        :param item: A string containing the prefix and the package name.
        :return: package name or nothing.
        """
        return remove_prefix(item, PackageInfoPrefix.PACKAGE)

    @staticmethod
    def get_package_version(item: str) -> Union[str, None]:
        """
        A helper method to extract package version.
        :param item: A string containing the prefix and the version.
        :return: package version or nothing.
        """
        return remove_prefix(item, PackageInfoPrefix.VERSION)

    @staticmethod
    def get_publication_timestamp(item: str) -> Union[str, None]:
        """
        A helper method to extract publication timestamp.
        :param item: A string containing the prefix and the publication timestamp.
        :return: publication timestamp or nothing.
        """
        publication_timestamp = remove_prefix(item, PackageInfoPrefix.PUBLICATION_DATE)
        # NOTE: Assuming all the timestamps in DESCRIPTION file are in UTC
        return remove_suffix(
            remove_suffix(publication_timestamp, "\n").strip(), "UTC"
        ).strip()

    @staticmethod
    def get_package_title(item: str) -> Union[str, None]:
        """
        A helper method to extract package title.
        :param item: A string containing the prefix and the package title.
        :return: package title or nothing.
        """
        title = remove_prefix(item, PackageInfoPrefix.TITLE)
        return remove_suffix(title, "\n")

    @staticmethod
    def get_package_description(item: str) -> Union[str, None]:
        """
        A helper method to extract package description.
        :param item: A string containing the prefix and the package description.
        :return: package description or nothing.
        """
        description = remove_prefix(item, PackageInfoPrefix.DESCRIPTION)
        return remove_suffix(description, "\n")

    @staticmethod
    def get_package_author(item: str) -> Tuple[str, Union[str, None]]:
        """
        A helper method to extract package author information.
        :param item: A string containing the prefix and the package author information.
        :return: package author name and email or nothing.
        """
        author_info = remove_prefix(item, PackageInfoPrefix.AUTHOR)
        author_info_arr = remove_suffix(author_info, "\n").split(",")
        # Handling multiple authors
        name = email = ""
        for idx, author_info in enumerate(author_info_arr):
            temp_name, temp_email = Command.separate_name_and_email(
                person_info=author_info
            )
            if idx > 0:
                if (
                    len(name) > 0
                    and isinstance(temp_name, str)
                    and len(temp_name.strip()) > 0
                ):
                    name += ", "
                if (
                    len(email) > 0
                    and isinstance(temp_email, str)
                    and len(temp_email.strip()) > 0
                ):
                    email += ", "
            if temp_name is not None:
                name += temp_name
            if temp_email is not None:
                email += temp_email
        return name, email

    @staticmethod
    def get_package_maintainer(item: str) -> Tuple[str, Union[str, None]]:
        """
        A helper method to extract package maintainer information.
        :param item: A string containing the prefix and the package maintainer information.
        :return: package maintainer name and email or nothing.
        """
        maintainer_info = remove_prefix(item, PackageInfoPrefix.MAINTAINER)
        maintainer_info = remove_suffix(maintainer_info, "\n")
        return Command.separate_name_and_email(person_info=maintainer_info)

    @staticmethod
    def separate_name_and_email(person_info: str) -> Tuple[str, Union[str, None]]:
        """
        A helper method to separate name and email from a single string. It extracts based upon the less-than character.

        :param person_info: A string containing name and/or email of the person.
        :return: A tuple of name and email.
        """
        name = email = None
        for idx, ch in enumerate(person_info):
            if ch == "<":
                name = person_info[: idx - 1]
                # Email Validation
                if Command.validate_email(person_info[idx + 1: -1]):
                    email = person_info[idx + 1: -1]
        if not name:
            name = person_info
        return name, email

    @staticmethod
    def validate_email(input_email: str) -> bool:
        """
        A helper method to validate the email.

        :param input_email: An input email address in the form of string.
        :return: True or False
        """
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex, input_email):
            return True
        return False


class PackageInfoPrefix:
    """
    A class containing the prefixes of data in DESCRIPTION file.
    """

    PACKAGE = "Package: "
    VERSION = "Version: "
    PUBLICATION_DATE = "Date/Publication: "
    TITLE = "Title: "
    DESCRIPTION = "Description: "
    AUTHOR = "Author: "
    MAINTAINER = "Maintainer: "
