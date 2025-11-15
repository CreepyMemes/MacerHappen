import { useAuth } from '@hooks/useAuth';

import Spinner from '@components/common/Spinner/Spinner';
import RoleSwitch from '@components/common/RoleSwitch/RoleSwitch';

import OrganizerSettings from '@pages/organizer/OrganizerSettings/OrganizerSettings';
import ParticipantSettings from '@pages/participant/ParticipantSettings/ParticipantSettings';

export default function Settings() {
  const { isFetchingProfile, profile } = useAuth();

  // Show skeleton while loading profile data
  if (isFetchingProfile || !profile) return <Spinner />;

  return <RoleSwitch organizer={<OrganizerSettings />} participant={<ParticipantSettings />} />;
}
