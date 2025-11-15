from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from ..utils import IsOrganizerRole
from ..serializers import (
    GetOrganizerProfileSerializer,
    DeleteOrganizerProfileSerializer,
    GetOrganizerEventsSerializer,
    CreateOrganizerEventSerializer,
    GetOrganizerEventDetailSerializer,
    UpdateOrganizerEventSerializer,
    DeleteOrganizerEventSerializer,
)

@extend_schema(
    methods=["GET"],
    responses={200: GetOrganizerProfileSerializer},
    description="Organizer only: Get all related profile information for the authenticated organizer.",
)

@extend_schema(
    methods=["DELETE"],
    responses={204: OpenApiResponse(description="Profile deleted successfully.")},
    description="Organizer only: Delete the account of the authenticated organizer.",
)
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsOrganizerRole])
@parser_classes([JSONParser]) 
def manage_organizer_profile(request):
    """
    Organizer only: Handles get, update and delete operations for the authenticated organizer's profile.

    - GET: Updates general profie information by the authenticated organizer.
    - DELETE: Deletes the account of the authenticated organizer.
    """
    if request.method == 'GET':
        serializer = GetOrganizerProfileSerializer(data={}, context={'organizer': request.user})
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        serializer = DeleteOrganizerProfileSerializer(data={}, context={'organizer': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@extend_schema(
    methods=['GET'],
    responses={200: GetOrganizerEventsSerializer},
    description="Organizer only:   List all events for the authenticated organizer.",
)
@extend_schema(
    methods=['POST'],
    request=CreateOrganizerEventSerializer,
    responses={200: OpenApiResponse(description="Profile info updated successfully.")},
    description="Create a new event.",
)
@api_view(["GET", "POST"])
@permission_classes([IsOrganizerRole])
@parser_classes([JSONParser, MultiPartParser])
def manage_organizer_events(request):
    """
    Organizer only:
    - GET: List all events for the authenticated organizer.
    - POST: Create a new event (supports multipart/form-data with picture).
    """
    if request.method == "GET":
        serializer = GetOrganizerEventsSerializer(data={}, context={"organizer": request.user})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = CreateOrganizerEventSerializer(data=request.data, context={"organizer": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Event created and moderated successfully."}, status=status.HTTP_201_CREATED)

@extend_schema(
    methods=['GET'],
    responses={200: GetOrganizerEventDetailSerializer},
    description="Organizer only:   Get details of a specific event.",
)
@extend_schema(
    methods=['PATCH'],
    request=UpdateOrganizerEventSerializer,
    responses={200: OpenApiResponse(description="Profile info updated successfully.")},
    description="Organizer only:   Update the event.",
)
@extend_schema(
    methods=['DELETE'],
    responses={200: DeleteOrganizerEventSerializer},
    description="Organizer only:   Delete the event.",
)
@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsOrganizerRole])
@parser_classes([JSONParser])
def manage_organizer_event(request, event_id):
    """
    Organizer only:
    - GET: Get details of a specific event.
    - PATCH: Update the event.
    - DELETE: Delete the event.
    """
    if request.method == "GET":
        serializer = GetOrganizerEventDetailSerializer(data={}, context={"organizer": request.user, "event_id": event_id})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PATCH":
        serializer = UpdateOrganizerEventSerializer(data=request.data, context={"organizer": request.user, "event_id": event_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Event updated successfully."}, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        serializer = DeleteOrganizerEventSerializer(data={}, context={"organizer": request.user, "event_id": event_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)