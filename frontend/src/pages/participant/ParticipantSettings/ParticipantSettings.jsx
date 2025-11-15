import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@hooks/useAuth';
import { isAnyFieldSet } from '@utils/utils';
import styles from './ParticipantSettings.module.scss';
import api from '@api';
import StatCard from '@components/ui/StatCard/StatCard';
import Form from '@components/common/Form/Form';
import Input from '@components/common/Input/Input';
import Icon from '@components/common/Icon/Icon';
import Button from '@components/common/Button/Button';
import Modal from '@components/common/Modal/Modal';
import ProfileImage from '@components/ui/ProfileImage/ProfileImage';
import Spinner from '@components/common/Spinner/Spinner';
import Error from '@components/common/Error/Error';

function ParticipantSettings() {
  const { profile, setProfile, logout } = useAuth();

  const [isLoading, setIsLoading] = useState(true);
  const [isUpdatingProfile, setIsUpdatingProfile] = useState(false);

  // Preferences state
  const [preferences, setPreferences] = useState(null);
  const [isLoadingPreferences, setIsLoadingPreferences] = useState(true);
  const [isUpdatingPreferences, setIsUpdatingPreferences] = useState(false);

  // Popup states
  const [uploadPicturePopup, setUploadPicturePopup] = useState(false);
  const [deletePicturePopup, setDeletePicturePopup] = useState(false);
  const [deleteProfilePopup, setDeleteProfilePopup] = useState(false);

  /**
   * Fetch latest profile data
   */
  const fetchProfile = useCallback(async () => {
    setIsLoading(true);
    try {
      const { profile } = await api.client.getParticipantProfile();
      setProfile(profile);
    } finally {
      setIsLoading(false);
    }
  }, [setProfile]);

  /**
   * Fetch participant preferences (categories + budget)
   */
  const fetchPreferences = useCallback(async () => {
    setIsLoadingPreferences(true);
    try {
      const { preferences } = await api.participant.getParticipantPreferences();
      setPreferences(preferences);
    } finally {
      setIsLoadingPreferences(false);
    }
  }, []);

  /**
   *  Fetches on mount to keep data always up to date
   */
  useEffect(() => {
    fetchProfile();
    fetchPreferences();
  }, [fetchProfile, fetchPreferences]);

  // While fetching latest profile data show loading spinner
  if (isLoading) return <Spinner />;

  // Upload picture popup state handlers
  const openUploadPicturePopup = () => setUploadPicturePopup(true);
  const closeUploadPicturePopup = () => setUploadPicturePopup(false);

  // Delete picture popup state handlers
  const openDeletePicturePopup = () => setDeletePicturePopup(true);
  const closeDeletePicturePopup = () => setDeletePicturePopup(false);

  // Delete profile popup state handlers
  const openDeleteProfilePopup = () => setDeleteProfilePopup(true);
  const closeDeleteProfilePopup = () => setDeleteProfilePopup(false);

  /**
   * Handles uploading a new profile picture
   */
  const handleUploadPicture = async (file) => {
    await api.image.uploadProfileImage(file);
    closeUploadPicturePopup();
    await fetchProfile();
  };

  /**
   * Handles deleting a profile picture
   */
  const handleDeletePicture = async () => {
    await api.image.deleteProfileImage();
    closeDeletePicturePopup();
    await fetchProfile();
  };

  /**
   * Handles deleting profile
   */
  const handleDeleteProfile = async () => {
    await api.client.deleteParticipantProfile();
    closeDeleteProfilePopup();
    await logout();
  };

  /**
   * Validate at least one field is provided, matching backend logic
   */
  const validateUpdateProfile = ({ username, name, surname, phone_number }) => {
    if (
      (!username || username.trim() === '') &&
      (!name || name.trim() === '') &&
      (!surname || surname.trim() === '') &&
      (!phone_number || phone_number.trim() === '')
    ) {
      return 'Provide at least one field to update: Username, Name, Surname or Phone Number.';
    }
    return undefined;
  };

  /**
   * Handles form submission for updating the profile data
   * Send only the filled fields to the API
   */
  const handleUpdateProfile = async ({ username, name, surname, phone_number }) => {
    setIsUpdatingProfile(true);
    const payload = {};
    if (username && username.trim() !== '') payload.username = username.trim();
    if (name && name.trim() !== '') payload.name = name.trim();
    if (surname && surname.trim() !== '') payload.surname = surname.trim();
    if (phone_number && phone_number.trim() !== '') payload.phone_number = phone_number.trim();
    try {
      await api.client.updateParticipantProfile(payload);
      await fetchProfile(); // Refresh profile after update
    } finally {
      setIsUpdatingProfile(false);
    }
  };

  /**
   * Validate at least one preference field is provided
   */
  const validateUpdatePreferences = ({ category_ids, budget }) => {
    const any = isAnyFieldSet({ category_ids, budget }, 'Provide at least one field to update: Categories or Budget.');
    return any; // isAnyFieldSet returns string error or undefined
  };

  /**
   * Handles form submission for updating preferences
   * category_ids comes in as comma-separated string, convert to number[]
   */
  const handleUpdatePreferences = async ({ category_ids, budget }) => {
    setIsUpdatingPreferences(true);

    const payload = {};

    // Parse category_ids (string like "1,2,3") to number[]
    if (category_ids && category_ids.trim() !== '') {
      payload.category_ids = category_ids
        .split(',')
        .map((id) => id.trim())
        .filter(Boolean)
        .map((id) => Number(id))
        .filter((n) => !Number.isNaN(n));
    }

    // Normalize budget
    if (budget !== undefined && String(budget).trim() !== '') {
      const numericBudget = Number(budget);
      payload.budget = Number.isNaN(numericBudget) ? budget : numericBudget;
    }

    try {
      await api.participant.updateParticipantPreferences(payload);
      await fetchPreferences(); // Refresh preferences after update
    } finally {
      setIsUpdatingPreferences(false);
    }
  };

  return (
    <>
      <div className={styles.clientSettings}>
        {/* Profile Update Card */}
        <StatCard icon="pen" label="Update Profile">
          {/* Profile Picture Management */}
          <section className={styles.profileImageSection}>
            <ProfileImage src={profile.profile_image} size="15rem" />
            <div className={styles.imageAction}>
              <Button className={styles.actionBtn} type="button" color="primary" size="md" onClick={openUploadPicturePopup}>
                <Icon name="plus" size="ty" />
                <span>Upload picture</span>
              </Button>
              <Button
                className={styles.actionBtn}
                type="button"
                color="translight"
                autoIconInvert
                size="md"
                onClick={openDeletePicturePopup}
              >
                <Icon name="trash" size="ty" black />
                <span>Delete picture</span>
              </Button>
            </div>
          </section>

          {/* Profile Updating Management  */}
          <section className={styles.updateProfileSection}>
            <Form
              className={styles.updateProfileForm}
              initialFields={{ username: '', name: '', surname: '', phone_number: '' }}
              onSubmit={handleUpdateProfile}
              validate={validateUpdateProfile}
            >
              <div className={styles.inputGroup}>
                <Input
                  className={styles.input}
                  label="Username"
                  name="username"
                  type="text"
                  placeholder={profile.username}
                  size="md"
                  disabled={isUpdatingProfile}
                />
                <Input
                  className={styles.input}
                  label="Phone Number"
                  name="phone_number"
                  type="tel"
                  placeholder={profile.phone_number}
                  size="md"
                  disabled={isUpdatingProfile}
                />
              </div>
              <div className={styles.inputGroup}>
                <Input
                  className={styles.input}
                  label="Name"
                  name="name"
                  type="text"
                  placeholder={profile.name}
                  size="md"
                  disabled={isUpdatingProfile}
                />
                <Input
                  className={styles.input}
                  label="Surname"
                  name="surname"
                  type="text"
                  placeholder={profile.surname}
                  size="md"
                  disabled={isUpdatingProfile}
                />
              </div>
              <Button className={styles.saveBtn} type="submit" size="md" color="primary" disabled={isUpdatingProfile} wide>
                <span className={styles.line}>
                  {isUpdatingProfile ? (
                    <>
                      <Spinner size="sm" /> Saving...
                    </>
                  ) : (
                    'Save Changes'
                  )}
                </span>
              </Button>
              <Error />
            </Form>
          </section>
        </StatCard>

        {/* Preferences Update Card */}
        <StatCard icon="settings" label="Preferences">
          <section className={styles.updatePreferencesSection}>
            {isLoadingPreferences ? (
              <Spinner />
            ) : (
              <Form
                className={styles.updatePreferencesForm}
                initialFields={{
                  budget: preferences?.budget ?? '',
                  category_ids: preferences?.category_ids?.join(', ') ?? '',
                }}
                onSubmit={handleUpdatePreferences}
                validate={validateUpdatePreferences}
              >
                <div className={styles.inputGroup}>
                  <Input
                    className={styles.input}
                    label="Budget"
                    name="budget"
                    type="number"
                    placeholder={preferences?.budget ?? 'Enter budget'}
                    size="md"
                    disabled={isUpdatingPreferences}
                  />
                  <Input
                    className={styles.input}
                    label="Category IDs"
                    name="category_ids"
                    type="text"
                    placeholder="e.g. 1, 2, 3"
                    size="md"
                    disabled={isUpdatingPreferences}
                  />
                </div>
                <Button className={styles.saveBtn} type="submit" size="md" color="primary" disabled={isUpdatingPreferences} wide>
                  <span className={styles.line}>
                    {isUpdatingPreferences ? (
                      <>
                        <Spinner size="sm" /> Saving...
                      </>
                    ) : (
                      'Save Preferences'
                    )}
                  </span>
                </Button>
                <Error />
              </Form>
            )}
          </section>
        </StatCard>

        {/* Profile Delete Card */}
        <StatCard icon="trash" label="Delete Profile">
          <section className={styles.deleteProfileSection}>
            <Button
              className={styles.actionBtn}
              type="button"
              color="translight"
              autoIconInvert
              size="md"
              onClick={openDeleteProfilePopup}
            >
              <Icon name="warning" size="ty" black />
              <span>Delete profile</span>
            </Button>
          </section>
        </StatCard>
      </div>

      {/* Upload Picture Modal */}
      <Modal
        open={uploadPicturePopup}
        fields={{ profile_image: null }}
        action={{ submit: 'Upload', loading: 'Uploading...' }}
        onValidate={(payload) => isAnyFieldSet(payload, 'Please select an image to upload.')}
        onSubmit={({ profile_image }) => handleUploadPicture(profile_image)}
        onClose={closeUploadPicturePopup}
      >
        <Modal.Title icon="image">Upload Picture</Modal.Title>
        <Modal.Description>Select a profile image to upload.</Modal.Description>
        <Input label="Profile Picture" name="profile_image" type="file" accept="image/*" placeholder="Choose an image" />
      </Modal>

      {/* Delete Picture Modal */}
      <Modal
        open={deletePicturePopup}
        action={{ submit: 'Delete', loading: 'Deleting...' }}
        onSubmit={handleDeletePicture}
        onClose={closeDeletePicturePopup}
      >
        <Modal.Title icon="warning">Delete Picture</Modal.Title>
        <Modal.Description>Are you sure you want to delete your profile picture? This action cannot be undone.</Modal.Description>
      </Modal>

      {/* Delete Profile Modal */}
      <Modal
        open={deleteProfilePopup}
        action={{ submit: 'Delete', loading: 'Deleting...' }}
        onSubmit={handleDeleteProfile}
        onClose={closeDeleteProfilePopup}
      >
        <Modal.Title icon="warning">Delete Profile</Modal.Title>
        <Modal.Description>Are you sure you want to delete your profile? This action cannot be undone.</Modal.Description>
      </Modal>
    </>
  );
}

export default ParticipantSettings;
