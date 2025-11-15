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

  - `/auth/` → login / signup
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

## **4. Implementation**

Perfect — here’s a **clean, complete list of endpoints** your Tinder-for-Events app needs.
I’ll group them by feature and clearly describe what each one should do.

---

# ⭐ **AUTH ENDPOINTS**

### **POST /auth/register/**

- Register a new user (participant or organizer).
- Body includes role, username, email, password, and specific fields (name, surname…).

### **POST /auth/login/**

- Returns JWT access + refresh tokens.

### **POST /auth/logout/**

- Invalidates refresh token.

### **GET /auth/me/**

- Returns the logged-in user’s profile.

---

# ⭐ **PARTICIPANT ENDPOINTS**

### **GET /participants/preferences/**

- Get the participant’s category selections + budget range.

### **PUT /participants/preferences/**

- Update categories + budget (for the recommendation system).

---

# ⭐ **ORGANIZER ENDPOINTS**

### **POST /organizers/events/**

- Organizer creates an event.
- After creation:

  - Run AI moderation → set `approved=True/False`.

### **GET /organizers/events/**

- List all events created by the logged-in organizer.

### **GET /organizers/events/<id>/**

- Get full details of an event they own.

### **PUT /organizers/events/<id>/**

- Update event details (title, description, price, categories…).

### **DELETE /organizers/events/<id>/**

- Delete their event.

---

# ⭐ **EVENT ENDPOINTS**

### **GET /events/**

- Public list of events (only approved ones).

### **GET /events/<id>/**

- Get event details.

### **GET /events/categories/**

- Returns all event categories (for filters & preferences page).

---

# ⭐ **SWIPE ENDPOINTS**

### **POST /swipes/**

- Body: `{ event_id, liked: true/false }`
- Creates or updates swipe.
- Used when participant swipes left/right.

### **GET /swipes/history/**

- List of events the participant has swiped on (optional, but useful for debugging).

---

# ⭐ **RECOMMENDATION ENDPOINT**

### **GET /recommendations/feed/**

Returns personalized event feed based on:

- participant’s categories
- participant’s budget
- excluding already-swiped events
- sorted by relevance

This is the Tinder-like event feed.

---

# 🎯 Summary of all endpoints you need

### **Auth**

- POST /auth/register/
- POST /auth/login/
- POST /auth/logout/
- GET /auth/me/

### **Participants**

- GET /participants/preferences/
- PUT /participants/preferences/

### **Organizers**

- POST /organizers/events/
- GET /organizers/events/
- GET /organizers/events/<id>/
- PUT /organizers/events/<id>/
- DELETE /organizers/events/<id>/

### **Events**

- GET /events/
- GET /events/<id>/
- GET /events/categories/

### **Swipes**

- POST /swipes/
- GET /swipes/history/

### **Recommendations**

- GET /recommendations/feed/
