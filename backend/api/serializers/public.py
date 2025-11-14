from rest_framework import serializers
from ..utils import(
    OrganizerValidationMixin,
    ParticipantValidationMixin,
    GetOrganizersMixin,
    GetParticipantsMixin,
)


class GetOrganizersPublicSerializer(GetOrganizersMixin, serializers.Serializer):
    """
    Returns all organizers registered and their public data 
    """
    def to_representation(self, instance):
        return {'organizers': self.get_organizers_public()}


class GetOrganizerProfilePublicSerializer(OrganizerValidationMixin, GetOrganizersMixin, serializers.Serializer):
    """
    Returns all the public information related to the profile of a given organizer
    """
    def validate(self, attrs):
        attrs = self.validate_organizer(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        organizer = validated_data['organizer']
        return {'profile': self.get_organizer_public(organizer)}
    

class GetParticipantProfilePublicSerializer(ParticipantValidationMixin, GetParticipantsMixin, serializers.Serializer):
    """
    Returns all the public information related to the profile of a given participant
    """
    def validate(self, attrs):
        attrs = self.validate_participant(attrs)
        return attrs
    
    def to_representation(self, validated_data):
        participant = validated_data['participant']
        return {'profile': self.get_participant_public(participant)}