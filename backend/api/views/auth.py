from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from ..utils import(
    send_participant_verify_email,
    send_organizer_verify_email,
    send_password_reset_email,
)
from ..serializers import (
    GetCurrentUserSerializer,
    RegisterParticipantSerializer,
    GetEmailFromTokenSerializer,
    VerifyUserEmailSerializer,
    LoginSerializer,
    RegisterOrganizerSerializer,
    LogoutSerializer,
    RequestPasswordResetSerializer,
    ConfirmPasswordResetSerializer,
    RefreshTokenCustomSerializer,
)


@extend_schema(
    methods=['GET'],
    responses={200: GetCurrentUserSerializer},
    description="Returns the current authenticated user's information.",
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser]) 
def get_current_user(request):
    """
    Returns the current authenticated user's information.
    """
    serializer = GetCurrentUserSerializer(data={}, context={'user': request.user})
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    methods=['POST'],
    request=RegisterParticipantSerializer,
    responses={
        201: OpenApiResponse(description="Participant registered, check your email to verify."),
        400: OpenApiResponse(description="Validation error."),
    },
    description="Register a new participant. Creates an inactive participant account and sends a verification email link.",
)
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def register_participant(request):
    """
    Participant self registration. Creates inactive participant and sends confirmation email.
    """
    serializer = RegisterParticipantSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    participant = serializer.save()

    uid = urlsafe_base64_encode(force_bytes(participant.pk))
    token = default_token_generator.make_token(participant)
    send_participant_verify_email(participant.email, uid, token, settings.FRONTEND_URL)

    return Response({'detail': 'Participant registered, check your email to verify.'}, status=status.HTTP_201_CREATED)

@extend_schema(
    methods=['POST'],
    request=RegisterParticipantSerializer,
    responses={
        201: OpenApiResponse(description="Participant registered, check your email to verify."),
        400: OpenApiResponse(description="Validation error."),
    },
    description="Register a new participant. Creates an inactive participant account and sends a verification email link.",
)
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def register_organizer(request):
    """
    Organizer self registration. Creates inactive organizer and sends confirmation email.
    """
    serializer = RegisterOrganizerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    organizer = serializer.save()

    uid = urlsafe_base64_encode(force_bytes(organizer.pk))
    token = default_token_generator.make_token(organizer)
    send_organizer_verify_email(organizer.email, uid, token, settings.FRONTEND_URL)

    return Response({'detail': 'Organizer registered, check your email to verify.'}, status=status.HTTP_201_CREATED)


@extend_schema(
    methods=['GET'],
    responses={200: GetEmailFromTokenSerializer},
    description="Returns the email associated to the user from a valid given uid64 and token.",
)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
@parser_classes([JSONParser])
def get_email_from_token(request, uidb64, token):
    """
    Returns the email associated to the user from a valid given uid64 and token
    """
    serializer = GetEmailFromTokenSerializer(data={}, context={'uidb64': uidb64, 'token': token})
    serializer.is_valid(raise_exception=True) 
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    methods=['GET'],
    responses={
        200: OpenApiResponse(description="Email verified successfully."),
        400: OpenApiResponse(description="Invalid or expired confirmation link."),
    },
    description="Verify participant account via email confirmation link.",
)
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def verify_user_email(request, uidb64, token):
    """
    Verifies a participant or organizer user from confirmation email link.
    """
    serializer = VerifyUserEmailSerializer(data=request.data, context={'uidb64': uidb64, 'token': token})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({'detail': 'Email verified successfully.'}, status=status.HTTP_200_OK)


@extend_schema(
    methods=['POST'],
    request=LoginSerializer,
    responses={
        200: LoginSerializer,
        400: OpenApiResponse(description="Validation error or invalid credentials."),
        403: OpenApiResponse(description="Account inactive or forbidden."),
    },
    description="Login by email OR username and password. Returns user and JWT tokens.",
)
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def login_user(request):
    """
    Login with email OR username + password.
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    methods=['POST'],
    request=LogoutSerializer,
    responses={
        200: OpenApiResponse(description="Logout successful."),
        400: OpenApiResponse(description="Invalid or expired refresh token."),
    },
    description="Logout by blacklisting the refresh token.",
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser]) 
def logout_user(request):
    """
    Logout by blacklisting the refresh token.
    """
    serializer = LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return Response({'detail': 'Logout successful.'}, status=status.HTTP_200_OK)
    

@extend_schema(
    methods=['POST'],
    request=RequestPasswordResetSerializer,
    responses={
        200: OpenApiResponse(description="If this email is registered, a password reset email has been sent."),
        400: OpenApiResponse(description="Validation error."),
    },
    description="Request password reset by email - sends reset email with token.",
)
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def request_password_reset(request):
    """
    Request password reset by email, sends reset email with token.
    """
    serializer = RequestPasswordResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.get_user()

    if user: # Fail silently for security
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        send_password_reset_email(user.email, uid, token, settings.FRONTEND_URL)

    return Response({'detail': 'If this email is registered, a password reset email has been sent.'}, status.HTTP_200_OK)


@extend_schema(
    methods=['POST'],
    request=ConfirmPasswordResetSerializer,
    responses={
        200: OpenApiResponse(description="Password has been reset successfully."),
        400: OpenApiResponse(description="Invalid or expired reset link/token."),
    },
    description="Confirm password reset by setting new password using token from email.",
)
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def confirm_password_reset(request, uidb64, token):
    """
    Confirm password reset by setting new password.
    """
    serializer = ConfirmPasswordResetSerializer(data=request.data, context={'uidb64': uidb64, 'token': token})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)


@extend_schema(
    methods=['POST'],
    request=RefreshTokenCustomSerializer,
    responses={
        200: OpenApiResponse(description="Access token refreshed successfully."),
        400: OpenApiResponse(description="Invalid or expired refresh token."),
    },
    description="Refresh the access token using a refresh token.",
)
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([]) 
@parser_classes([JSONParser]) 
def refresh_token(request):
    """
    Refresh the access token using a refresh token passed as 'refresh_token' in the request.
    """
    serializer = RefreshTokenCustomSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.get_response(), status=status.HTTP_200_OK)
