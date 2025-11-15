import api from '@api';
import { ENDPOINTS } from '@api/endpoints';

/**
 * Participant only: Get current preferences (categories + budget).
 */
export async function getParticipantPreferences() {
  const { data } = await api.instance.get(ENDPOINTS.participant.preferences);
  return data;
}

/**
 * Participant only: Update preferences (categories + budget).
 * Accepts partial payload: { category_ids?: number[], budget?: string | number }
 */
export async function updateParticipantPreferences(patchData) {
  const { data } = await api.instance.patch(ENDPOINTS.participant.preferences, patchData);
  return data;
}

/**
 * Participant only: Create or update a swipe (like/dislike) on an event.
 * swipeData shape: { event_id: number, liked: boolean }
 */
export async function createSwipe(swipeData) {
  const { data } = await api.instance.post(ENDPOINTS.participant.swipes, swipeData);
  return data;
}

/**
 * Participant only: Get swipe history.
 */
export async function getSwipeHistory() {
  const { data } = await api.instance.get(ENDPOINTS.participant.swipeHistory);
  return data;
}

/**
 * Participant only: Get personalized event feed (AI-ranked).
 */
export async function getFeed() {
  const { data } = await api.instance.get(ENDPOINTS.participant.Feed);
  return data;
}
