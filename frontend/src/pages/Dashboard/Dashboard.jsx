import { useAuth } from '@hooks/useAuth';

import Spinner from '@components/common/Spinner/Spinner';
import RoleSwitch from '@components/common/RoleSwitch/RoleSwitch';

import OrganizerDashboard from '@pages/organizer/OrganizerDashboard/OrganizerDashboard';
import ParticipantDashboard from '@pages/participant/ParticipantDashboard/ParticipantDashboard';

export default function Dashboard() {
  const { isFetchingProfile, profile } = useAuth();

  // Show skeleton while loading profile data
  if (isFetchingProfile || !profile) return <Spinner />;

  return <RoleSwitch organizer={<OrganizerDashboard />} participant={<ParticipantDashboard />} />;
}
