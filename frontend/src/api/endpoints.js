/**
 * API endpoint definitions used throughout the application.
 * Dynamic routes are defined using arrow functions with parameters.
 */
export const ENDPOINTS = {
  // Auth Routes
  auth: {
    me: '/auth/me/',
    login: '/auth/login/',
    logout: '/auth/logout/',
    refresh: '/auth/refresh-token/',
    resetPassword: '/auth/reset-password/',
    registerParticipant: '/auth/register/participant/',
    registerOrganizer: '/auth/register/organizer/',
    emailFromToken: (uidb64, token) => `/auth/email/${uidb64}/${token}/`,
    resetPasswordConfirm: (uidb64, token) => `/auth/reset-password/${uidb64}/${token}/`,
    verifyEmail: (uidb64, token) => `/auth/verify/${uidb64}/${token}/`,
  },

  // Organizers Routes
  organizer: {
    profile: '/organizers/profile/',
    events: '/organizers/events/',
    event: (eventId) => `/organizers/events/${eventId}/`,
  },

  // Participant Routes
  participant: {
    profile: '/participants/profile/',
    preferences: '/participants/preferences/',
    feed: '/participants/feed/',
    swipes: '/participants/swipes/',
    swipeHistory: '/participants/swipes/history/',
  },

  // Public Routes
  public: {
    categories: '/public/categories/',
    events: '/public/events/',
    event: (eventId) => `/public/events/${eventId}/`,
  },

  // Image Routes
  image: {
    profile: '/image/profile/',
  },
};
