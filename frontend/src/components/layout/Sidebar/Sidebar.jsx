import { useState } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './Sidebar.module.scss';

import Spinner from '@components/common/Spinner/Spinner';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import ProfileImage from '@components/ui/ProfileImage/ProfileImage';

// Define role-based navigation

const organizerNav = [
  { to: '/organizer/dashboard', label: 'Dashboard', icon: 'dashboard' },
  { to: '/organizer/services', label: 'Services', icon: 'service' },
  { to: '/organizer/appointments', label: 'Appointments', icon: 'appointment' },
  { to: '/organizer/availabilities', label: 'Availabilities', icon: 'availability' },
  { to: '/organizer/reviews', label: 'Reviews', icon: 'review' },
  { to: '/organizer/settings', label: 'Settings', icon: 'settings' },
];
const participantNav = [
  { to: '/participant/dashboard', label: 'Dashboard', icon: 'dashboard' },
  { to: '/participant/barbers', label: 'Barbers', icon: 'barber' },
  { to: '/participant/appointments', label: 'Appointments', icon: 'appointment' },
  { to: '/participant/reviews', label: 'Reviews', icon: 'review' },
  { to: '/participant/settings', label: 'Settings', icon: 'settings' },
];

function Sidebar() {
  const { isAuthenticated, profile, isFetchingProfile } = useAuth();
  const [open, setOpen] = useState(true); // Sidebar open/collapsed state

  // Get role specific nav items
  let navItems = [];
  if (!isFetchingProfile && profile) {
    if (profile.role === 'ORGANIZER') navItems = organizerNav;
    else if (profile.role === 'PARTICIPANT') navItems = participantNav;
  }

  return (
    <aside className={`${styles.sidebar} ${open ? styles.open : styles.close}`}>
      {isFetchingProfile ? (
        <Spinner />
      ) : (
        <div className={styles.sidebarContent}>
          <div className={`${styles.inner} ${open ? styles.show : styles.hide}`}>
            <div className={styles.top}>
              {isAuthenticated && profile && (
                <div className={styles.profile}>
                  <ProfileImage src={profile.profile_image} />

                  <div className={styles.profileText}>
                    <div className={styles.username}>{profile.username || profile.email}</div>
                    <div className={styles.role}>{profile.role?.toLowerCase() || ''}</div>
                  </div>
                </div>
              )}
            </div>

            <nav className={styles.nav}>
              <ul>
                {navItems.map((item) => (
                  <li key={item.to}>
                    <Button
                      className={styles.navBtn}
                      nav
                      href={item.to}
                      size="md"
                      activeClassName={styles.active}
                      color="borderless"
                      wide
                    >
                      <span className={styles.line}>
                        <Icon name={item.icon} size={'md'} />
                        {item.label}
                      </span>
                    </Button>
                  </li>
                ))}
              </ul>
            </nav>
          </div>

          <Button
            className={styles.toggleBtn}
            onClick={() => setOpen((v) => !v)}
            size="sm"
            color="primary"
            type="button"
            width="content"
          >
            <Icon name="menu" size="ty" />
          </Button>
        </div>
      )}
    </aside>
  );
}

export default Sidebar;
