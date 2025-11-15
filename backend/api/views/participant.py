from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from ..utils import IsParticipantRole
from ..serializers.participant import (
    GetParticipantPreferencesSerializer,
    UpdateParticipantPreferencesSerializer,
    CreateSwipeSerializer, 
    GetSwipeHistorySerializer
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
    

@extend_schema(
    methods=['POST'],
    request=CreateSwipeSerializer,
    responses={201: OpenApiResponse(description="Swipe recorded successfully."),},
    description="Participant only: Create a swipe (like/dislike) for an event.",
)
@api_view(["POST"])
@permission_classes([IsParticipantRole])
@parser_classes([JSONParser])
def create_swipe(request):
    """
    Participant only: Create a swipe (like/dislike) for an event.
    """
    serializer = CreateSwipeSerializer(data=request.data, context={"participant": request.user})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"detail": "Swipe recorded successfully."}, status=status.HTTP_201_CREATED)


@extend_schema(
    methods=['GET'],
    responses={200: GetSwipeHistorySerializer},
    description="Participant only:  Get current preferences (categories + budget).",
)
@api_view(["GET"])
@permission_classes([IsParticipantRole])
@parser_classes([JSONParser])
def get_swipe_history(request):
    """
    Participant only: Get swipe history.
    """
    serializer = GetSwipeHistorySerializer(data={}, context={"participant": request.user})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)