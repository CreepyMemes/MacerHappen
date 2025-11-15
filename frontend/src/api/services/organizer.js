import api from '@api';
import { ENDPOINTS } from '@api/endpoints';

/**
 * Retrieves the current organizer's profile information.
 */
export async function getOrganizerProfile() {
  const { data } = await api.instance.get(ENDPOINTS.organizer.profile);
  return data;
}

/**
 * Organizer only: List all events for the authenticated organizer.
 */
export async function getOrganizerEvents() {
  const { data } = await api.instance.get(ENDPOINTS.organizer.events);
  return data;
}

/**
 * Organizer only: Create a new event.
 * Accepts either a plain object (JSON) or FormData when uploading a picture.
 */
export async function createOrganizerEvent(eventPayload) {
  const { data } = await api.instance.post(ENDPOINTS.organizer.events, eventPayload);
  return data;
}

/**
 * Organizer only: Get details of a specific event.
 */
export async function getOrganizerEventDetail(eventId) {
  const { data } = await api.instance.get(ENDPOINTS.organizer.event(eventId));
  return data;
}

/**
 * Organizer only: Update an existing event.
 * Accepts partial payload (only fields to change).
 * For picture updates/removal, send FormData including `picture`
 * (can be null to clear).
 */
export async function updateOrganizerEvent(eventId, patchData) {
  const { data } = await api.instance.patch(ENDPOINTS.organizer.event(eventId), patchData);
  return data;
}

/**
 * Organizer only: Delete an existing event.
 */
export async function deleteOrganizerEvent(eventId) {
  await api.instance.delete(ENDPOINTS.organizer.event(eventId));
}
