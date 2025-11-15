import api from '@api';
import { ENDPOINTS } from '@api/endpoints';

/**
 * Public: Get all categories.
 */
export async function getCategories() {
  const { data } = await api.instance.get(ENDPOINTS.public.categories);
  return data;
}

/**
 * Public: List all approved events.
 */
export async function getEvents() {
  const { data } = await api.instance.get(ENDPOINTS.public.events);
  return data;
}

/**
 * Public: Get details of a specific approved event.
 */
export async function getEventDetail(eventId) {
  const { data } = await api.instance.get(ENDPOINTS.public.event(eventId));
  return data;
}
