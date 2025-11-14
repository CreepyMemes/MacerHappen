from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """
    Allows access only to users with the ADMIN role.
    """
    def has_permission(self, request, view):
        from ..models import Roles 

        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role == Roles.ADMIN.value
        )


class IsParticipantRole(BasePermission):
    """
    Allows access only to users with the PARTICIPANT role.
    """
    def has_permission(self, request, view):
        from ..models import Roles 

        return (
            request.user 
            and request.user.is_authenticated
            and request.user.role == Roles.PARTICIPANT.value
        )


class IsOrganizerRole(BasePermission):
    """
    Allows access only to users with the ORGANIZER role.
    """
    def has_permission(self, request, view):
        from ..models import Roles 
        
        return (
            request.user 
            and request.user.is_authenticated
            and request.user.role == Roles.ORGANIZER.value
        )