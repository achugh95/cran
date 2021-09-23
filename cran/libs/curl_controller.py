import logging

import requests

logging.getLogger().setLevel("INFO")


class CurlController:
    """
    A utility to send requests over network.
    """

    @staticmethod
    def send_get_request(url: str, headers: dict = None):
        """
        A method to send GET request. There is a default timeout of 60 seconds.

        :param url: The endpoint or the url to which the request needs to be made.
        :param headers: The headers required to access the url. The default value for it is None.
        :return: Response content from the url.
        """
        logging.info(f"Sending request to URL: {url}")
        try:
            # Faking as browser request | Faced some latency issues otherwise
            if not headers:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)\
                                        AppleWebKit/537.36 (KHTML, like Gecko)\
                                        Chrome/56.0.2924.76\
                                        Safari/537.36"
                }
            return requests.get(url=url, headers=headers, timeout=60).content
        except Exception as e:
            logging.error(f"Error while calling the given URL: {url} - {e}")
            raise Exception("Network Error")
