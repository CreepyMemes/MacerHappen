import { useState } from 'react';
import styles from './SwipeCard.module.scss';

/**
 * A single swipeable event card (handles drag/swipe gestures).
 */
function SwipeCard({ event, onSwipe, disabled, categoryMap = {} }) {
  const [dragStartX, setDragStartX] = useState(null);
  const [dragDeltaX, setDragDeltaX] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [isAnimatingOut, setIsAnimatingOut] = useState(false);
  const [pendingLike, setPendingLike] = useState(null); // true / false / null

  const swipeThreshold = 120; // px

  const getPointerX = (e) => {
    if (e.touches && e.touches[0]) return e.touches[0].clientX;
    if (e.changedTouches && e.changedTouches[0]) return e.changedTouches[0].clientX;
    return e.clientX;
  };

  const startDrag = (e) => {
    if (disabled || isAnimatingOut) return;
    setIsDragging(true);
    setDragStartX(getPointerX(e));
  };

  const moveDrag = (e) => {
    if (!isDragging || disabled || isAnimatingOut) return;
    const currentX = getPointerX(e);
    setDragDeltaX(currentX - dragStartX);
    if (e.preventDefault) e.preventDefault(); // avoid scrolling while swiping
  };

  const endDrag = () => {
    if (!isDragging || disabled || isAnimatingOut) {
      setIsDragging(false);
      setDragDeltaX(0);
      return;
    }

    if (Math.abs(dragDeltaX) > swipeThreshold) {
      const liked = dragDeltaX > 0;
      setPendingLike(liked);
      setIsAnimatingOut(true); // trigger fly-out animation
    } else {
      setDragDeltaX(0); // snap back
    }

    setIsDragging(false);
  };

  const triggerSwipe = (liked) => {
    if (disabled || isAnimatingOut) return;
    setPendingLike(liked);
    setIsAnimatingOut(true);
  };

  const handleKeyDown = (e) => {
    if (disabled || isAnimatingOut) return;
    if (e.key === 'ArrowLeft') triggerSwipe(false);
    if (e.key === 'ArrowRight') triggerSwipe(true);
  };

  const handleTransitionEnd = () => {
    if (!isAnimatingOut || pendingLike === null) return;
    const liked = pendingLike;
    setIsAnimatingOut(false);
    setPendingLike(null);
    setDragDeltaX(0);
    onSwipe(liked); // tell parent to go to next event
  };

  // Position + rotation
  const translateX = isAnimatingOut
    ? pendingLike
      ? 1000 // fly out right
      : -1000 // fly out left
    : dragDeltaX;

  const rotation = translateX * 0.05;
  const opacity = isAnimatingOut ? 0 : Math.max(0.6, 1 - Math.abs(translateX) / 600);

  const cardStyle = {
    transform: `translateX(${translateX}px) rotate(${rotation}deg)`,
    opacity,
    cursor: disabled ? 'default' : isDragging ? 'grabbing' : 'grab',
    transition: isDragging ? 'none' : 'transform 0.25s ease-out, opacity 0.25s ease-out',
  };

  // Tinder-like “LIKE / SKIP” labels
  const likeOpacity = dragDeltaX > 0 ? Math.min(1, dragDeltaX / swipeThreshold) : 0;
  const skipOpacity = dragDeltaX < 0 ? Math.min(1, -dragDeltaX / swipeThreshold) : 0;

  return (
    <div
      className={styles.cardWrapper}
      style={cardStyle}
      onMouseDown={startDrag}
      onMouseMove={moveDrag}
      onMouseUp={endDrag}
      onMouseLeave={endDrag}
      onTouchStart={startDrag}
      onTouchMove={moveDrag}
      onTouchEnd={endDrag}
      onTouchCancel={endDrag}
      onKeyDown={handleKeyDown}
      onTransitionEnd={handleTransitionEnd}
      tabIndex={0}
      aria-label="Swipeable event card"
    >
      <div className={styles.card}>
        {/* Tinder-style badges */}
        <div className={styles.badgeLike} style={{ opacity: likeOpacity }}>
          SAVE
        </div>
        <div className={styles.badgeSkip} style={{ opacity: skipOpacity }}>
          SKIP
        </div>

        {event.picture && (
          <div className={styles.imageWrapper}>
            <img src={event.picture} alt={event.title} className={styles.image} />
          </div>
        )}

        <div className={styles.cardBody}>
          <div className={styles.cardHeader}>
            <h2 className={styles.eventTitle}>{event.title}</h2>
            {event.price != null && <span className={styles.price}>€{Number(event.price).toFixed(2)}</span>}
          </div>

          {event.date && (
            <div className={styles.metaRow}>
              <span className={styles.metaLabel}>Date</span>
              <span className={styles.metaValue}>{new Date(event.date).toLocaleString()}</span>
            </div>
          )}

          {event.organizer_name && (
            <div className={styles.metaRow}>
              <span className={styles.metaLabel}>Organizer</span>
              <span className={styles.metaValue}>{event.organizer_name}</span>
            </div>
          )}

          {/* UPDATED: event.categories is [1,2,...], use categoryMap[id] */}
          {Array.isArray(event.categories) && event.categories.length > 0 && (
            <div className={styles.categories}>
              {event.categories.map((id) => (
                <span key={id} className={styles.categoryChip}>
                  {categoryMap[id]}
                </span>
              ))}
            </div>
          )}

          {event.description && <p className={styles.description}>{event.description}</p>}
        </div>

        <div className={styles.actions}>
          <button
            type="button"
            className={`${styles.actionButton} ${styles.dislike}`}
            onClick={() => triggerSwipe(false)}
            disabled={disabled}
          >
            Skip
          </button>
          <button
            type="button"
            className={`${styles.actionButton} ${styles.like}`}
            onClick={() => triggerSwipe(true)}
            disabled={disabled}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}

export default SwipeCard;
