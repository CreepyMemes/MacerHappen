import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import styles from './ParticipantDashboard.module.scss';
import api from '@api';
import Spinner from '@components/common/Spinner/Spinner';
import SwipeCard from '@components/ui/SwipeCard/SwipeCard';

function ParticipantDashboard() {
  const { profile, setProfile } = useAuth();

  const [isLoadingProfile, setIsLoadingProfile] = useState(true);
  const [isLoadingFeed, setIsLoadingFeed] = useState(true);
  const [feed, setFeed] = useState([]); // array of events
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isSendingSwipe, setIsSendingSwipe] = useState(false);
  const [error, setError] = useState(null);

  // NEW: category ID -> name map, e.g. { 1: "Music", 2: "Tech" }
  const [categoryMap, setCategoryMap] = useState({});

  // Fetch participant profile (so dashboard always has fresh data)
  const fetchProfile = useCallback(async () => {
    setIsLoadingProfile(true);
    try {
      const { profile } = await api.participant.getParticipantProfile();
      setProfile(profile);
    } catch (err) {
      console.error('Failed to load profile', err);
    } finally {
      setIsLoadingProfile(false);
    }
  }, [setProfile]);

  // Fetch recommendation feed
  const fetchFeed = useCallback(async () => {
    setIsLoadingFeed(true);
    setError(null);
    try {
      const { events } = await api.participant.getFeed();
      setFeed(events || []);
      setCurrentIndex(0);
    } catch (err) {
      console.error('Failed to load feed', err);
      setError('Could not load your event feed. Please try again.');
    } finally {
      setIsLoadingFeed(false);
    }
  }, []);

  // NEW: fetch all categories once and build an ID->name map
  const fetchCategories = useCallback(async () => {
    try {
      // Adjust this call to your actual API client method if different
      const { categories } = await api.pub.getCategories();
      const map = {};
      (categories || []).forEach((c) => {
        map[c.id] = c.name;
      });
      setCategoryMap(map);
    } catch (err) {
      console.error('Failed to load categories', err);
      // Not fatal for the page, so we don't set error banner here
    }
  }, []);

  useEffect(() => {
    fetchProfile();
    fetchFeed();
    fetchCategories(); // NEW
  }, [fetchProfile, fetchFeed, fetchCategories]);

  const hasEvents = feed && currentIndex < feed.length;
  const currentEvent = hasEvents ? feed[currentIndex] : null;

  const handleSwipe = async (liked) => {
    if (!currentEvent || isSendingSwipe) return;

    setIsSendingSwipe(true);
    setError(null);

    try {
      await api.participant.createSwipe({
        event_id: currentEvent.id,
        liked,
      });

      setCurrentIndex((prev) => prev + 1);

      if (currentIndex + 1 >= feed.length) {
        // Optionally trigger a new fetch here
      }
    } catch (err) {
      console.error('Failed to register swipe', err);
      setError('Unable to register your swipe. Please try again.');
    } finally {
      setIsSendingSwipe(false);
    }
  };

  if (isLoadingProfile || isLoadingFeed) {
    return (
      <div className={styles.loadingWrapper}>
        <Spinner />
      </div>
    );
  }

  return (
    <div className={styles.participantDashboard}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Welcome{profile?.name ? `, ${profile.name}` : ''}!</h1>
          <p className={styles.subtitle}>Swipe through personalized events. Right to save, left to skip.</p>
        </div>
        {profile && (
          <div className={styles.preferences}>
            <span className={styles.prefLabel}>Your budget:</span>
            <span className={styles.prefValue}>{profile.budget ? `€${profile.budget}` : 'Not set'}</span>
          </div>
        )}
      </div>

      <div className={styles.feedContainer}>
        {error && <div className={styles.errorBanner}>{error}</div>}

        {currentEvent ? (
          <>
            <SwipeCard
              key={currentEvent.id}
              event={currentEvent}
              onSwipe={handleSwipe}
              disabled={isSendingSwipe}
              categoryMap={categoryMap} // NEW: pass map down
            />
            <div className={styles.counter}>
              {currentIndex + 1} / {feed.length}
            </div>
          </>
        ) : (
          <div className={styles.emptyState}>
            <h2 className={styles.emptyTitle}>No more events</h2>
            <p className={styles.emptyText}>
              You&apos;ve reached the end of your recommendations. Adjust your preferences or reload the feed.
            </p>
            <button type="button" className={styles.reloadButton} onClick={fetchFeed}>
              Reload feed
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default ParticipantDashboard;
