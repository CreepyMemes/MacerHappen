from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from ..serializers import GetCategoriesSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
@parser_classes([JSONParser])
def get_categories(request):
    """
    Public: Get all categories.
    """
    serializer = GetCategoriesSerializer(data={})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)