from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from ..serializers import (
    GetOrganizersPublicSerializer,
    GetOrganizerProfilePublicSerializer,
    GetParticipantProfilePublicSerializer
)


@extend_schema(
    responses={200: GetOrganizersPublicSerializer},
    description="Return a list of all active organizers.",
)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
@parser_classes([JSONParser]) 
def get_organizers_public(request):
    """
    Return a list of all active organizers
    """
    serializer = GetOrganizersPublicSerializer(data={}, instance={}) 
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GetOrganizerProfilePublicSerializer},
    description="Get all public profile information for a organizer. (Public)",
)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def get_organizer_profile_public(request, organizer_id):
    """
    Get all services for the given organizer.
    """
    serializer = GetOrganizerProfilePublicSerializer(data={}, context={'organizer_id': organizer_id})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: GetParticipantProfilePublicSerializer},
    description="Get all public profile information for a participant. (Public)",
)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def get_participant_profile_public(request, participant_id):
    """
    Get all services for the given participant.
    """
    serializer = GetParticipantProfilePublicSerializer(data={}, context={'participant_id': participant_id})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)