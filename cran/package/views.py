from rest_framework import status as rest_status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from cran.config import CONFIG
from cran.package.serializers import PackageListSerializer


class PackageListView(ListAPIView):
    """
    A List API view class for search the packages.
    """
    serializer_class = PackageListSerializer

    def get(self, request, *args, **kwargs) -> Response:
        """
        A GET end-point to filter out the packages based on name. It returns the list of packages matching the input
        name. Here, the term match implies substring match without considering the case (upper/lower).

        :param request: request received from the user.
        :return: Response object containing the matching packages(if any) along with other meta-details.
        """
        name = request.query_params.get("name")
        results = self.serializer_class().get_packages(name=name)
        serialized_results = self.serializer_class(results, many=True).data
        response = {
            "status": CONFIG.GENERIC.SUCCESS,
            "message": "Success",
            "result_count": len(results),
            "data": serialized_results,
        }
        return Response(response, status=rest_status.HTTP_200_OK)
