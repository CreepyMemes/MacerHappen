from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from ..utils import IsParticipantRole
from ..serializers.participant import (
    GetParticipantPreferencesSerializer,
    UpdateParticipantPreferencesSerializer,
)

@extend_schema(
    methods=['GET'],
    responses={200: GetParticipantPreferencesSerializer},
    description="Participant only:  Get current preferences (categories + budget).",
)
@extend_schema(
    methods=['PATCH'],
    request=UpdateParticipantPreferencesSerializer,
    responses={200: OpenApiResponse(description="Profile info updated successfully.")},
    description="Participant only: Update preferences (categories + budget).",
)
@api_view(["GET", "PATCH"])
@permission_classes([IsParticipantRole])
@parser_classes([JSONParser])
def manage_participant_preferences(request):
    """
    Participant only:
    - GET: Get current preferences (categories + budget).
    - PATCH: Update preferences (categories + budget).
    """
    if request.method == "GET":
        serializer = GetParticipantPreferencesSerializer(data={}, context={"participant": request.user})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PATCH":
        serializer = UpdateParticipantPreferencesSerializer(data=request.data, context={"participant": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Preferences updated successfully."}, status=status.HTTP_200_OK)