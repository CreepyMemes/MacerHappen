from django.urls import reverse
from django.core.mail import send_mail


def send_participant_verify_email(email, uid, token, domain):
    """
    Sends email confirmation link to participant after registration.
    """
    link = f'{domain}/verify/{uid}/{token}'

    subject = '[MacerHappen] Verify your email to register as a participant'
    message = (
        f'Thank you for registering.\n\n'
        f'Please click the link below to verify your account:\n'
        f'{link}\n\n'
        'If you did not register, please ignore this email.'
    )
    send_mail(subject, message, 'organizer.manager.verify@gmail.com', [email])


def send_organizer_verify_email(email, uid, token, domain):
    """
    Sends email confirmation link to participant after registration.
    """
    link = f'{domain}/verify/{uid}/{token}'

    subject = '[MacerHappen] Verify your email to register as an organizer'
    message = (
        f'Thank you for registering.\n\n'
        f'Please click the link below to verify your account:\n'
        f'{link}\n\n'
        'If you did not register, please ignore this email.'
    )
    send_mail(subject, message, 'organizer.manager.verify@gmail.com', [email])


def send_password_reset_email(email, uid, token, domain):
    """
    Sends password reset email with reset link.
    """
    link = f'{domain}/reset-password/{uid}/{token}'

    subject = '[OrganizerManager] You have requested to reset your password'
    message = (
        f'We received a request to reset your password.\n\n'
        f'Please click the link below to set a new password:\n'
        f'{link}\n\n'
        'If you did not request a password reset, please ignore this email.'
    )
    send_mail(subject, message, 'organizer.manager.verify@gmail.com', [email])
