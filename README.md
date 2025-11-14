## **1. Define Project Structure**

### **Backend (Django)**

- **App Structure:**

  - `users` → handle organizers & participants, authentication, profile, preferences (categories, budget).
  - `events` → event creation, moderation, fetching events for feed.
  - `recommendation` → AI logic for personalized feed.

- **Models:**

  - `User` → type (organizer/participant), email, password, budget, categories (many-to-many).
  - `Event` → title, description, category, price, organizer, date/time, status (approved/blocked).
  - `Swipe` → participant, event, liked (boolean).

- **Endpoints (REST API with DRF):**

  - `/auth/` → login/signup
  - `/events/` → list events, create event, get event by ID
  - `/swipe/` → record swipe
  - `/recommendations/` → personalized event feed
  - `/notifications/` → new relevant events

---

### **Frontend (React)**

- **Pages/Components:**

  - `Login/Register`
  - `Profile Setup` → choose categories, set budget
  - `EventFeed` → swipe interface (like/dislike)
  - `Notifications` → list of new suggested events
  - `EventCreation` → form for organizers
  - `EventDetails` → modal or page showing event info

- **State Management:**

  - Use React Context or Redux for:

    - User session
    - Event feed
    - Notifications

- **API Integration:**

  - Fetch recommended events from `/recommendations/`
  - Post swipes to `/swipe/`
  - Get notifications

---

### **Database (PostgreSQL)**

- **Tables:**

  - `users`
  - `events`
  - `categories`
  - `swipes`

- **Relationships:**

  - `users` → `swipes` → `events` (many-to-many via swipes)
  - `events` → `categories` (many-to-many)
  - `participants` → `categories` (many-to-many)

---

## **2. AI Integration**

- **Organizer moderation:**

  - Lightweight solution: Python function/class in Django that checks text (and optionally image URLs) for inappropriate content using a library or small model.

- **Participant feed:**

  - Simple filter: match event categories and price to participant preferences.
  - Optional enhancement: prioritize events that match past likes.

---

## **3. Development Plan (Step by Step)**

### **Phase 1: Setup**

- Set up Django + DRF project
- Connect to PostgreSQL
- Set up React project with basic routing
- Set up authentication

### **Phase 2: Models & Backend APIs**

- Create `User`, `Event`, `Swipe`, `Category` models
- Build CRUD APIs for events
- Build swipe API

### **Phase 3: AI/Recommendation Logic**

- Implement category & budget-based filtering
- Implement moderation check on event creation

### **Phase 4: Frontend**

- Build login/register
- Build swipe feed with recommendations
- Build organizer event creation page
- Build notifications page

### **Phase 5: Testing & Polish**

- Test end-to-end flow
- Add basic styling
- Optional: add notification triggers for new events
