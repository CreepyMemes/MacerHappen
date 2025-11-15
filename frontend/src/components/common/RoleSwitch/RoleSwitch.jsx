import { useAuth } from '@hooks/useAuth';

/**
 * Just dispatches Page based on role, (NO loading/auth logic)
 */
function RoleSwitch({ organizer, participant, fallback = null }) {
  const { profile } = useAuth();

  switch (profile.role) {
    case 'ORGANIZER':
      return organizer;
    case 'PARTICIPANT':
      return participant;
    default:
      return fallback;
  }
}

export default RoleSwitch;
