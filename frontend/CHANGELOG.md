# 📄 CHANGELOG

All notable changes to this project will be documented here.

## 📦 v0.2.0 – Task management (CRUD), feedback UX and pagination

**Date:** 2025-07-05

### ✅ CRUD: Create, Edit, Delete
- Implemented full task management flow:
  - Created new tasks using a validated form with react-hook-form + zod.
  - Enabled editing using the same form, pre-filled with existing task data.
  - Added task deletion with confirmation prompt using window.confirm.
  - Integrated with backend API using axios, including JWT-based auth headers.
  - Task list refreshes automatically after create, update, or delete actions.

### 🌀 UX: Loading spinners and visual feedback
- Added loading spinner and “Saving...” label to the submit button during create/update.
- Displayed per-task spinner and “Deleting...” label when deleting.
- Disabled buttons during async operations to prevent duplicate actions.
- Integrated react-hot-toast for success and error feedback messages.

### 📄 Pagination
- Implemented basic pagination based on skip and limit query parameters:
  - "Previous" and "Next" navigation buttons.
  - Displays 10 tasks per page.
  - Keeps current page after performing create/edit/delete actions.


## 📦 v0.1.0 – Frontend structure and JWT authentication flow

**Date:** 2025-07-05

### 🧱 Project structure

- Complete restructuring of the project folder layout:
  - Moved all backend files into a dedicated `/backend` directory.
  - Created a new `/frontend` directory using React + Vite + TypeScript + Tailwind CSS.
- Adjusted paths, Docker configurations, and scripts to support the new structure cleanly.

### 🔐 Authentication (JWT)

- Implemented a complete JWT-based login/logout flow:
  - Created a login screen integrated with FastAPI’s `/auth/login` endpoint.
  - Persisted the JWT token securely in `localStorage`.
  - Setup of a global authentication context with React Context API.
  - Decoding of JWT token using `jwt-decode` to extract user data (e.g., `email`).
  - Protected routes using a reusable `PrivateRoute` component that redirects unauthenticated users.

### 💡 Layout and UI

- Created a responsive authenticated layout (`LayoutAutenticado`) with:
  - Top navigation bar showing the logged-in user's email.
  - Logout button triggering context-based state reset and redirect.
- Applied Tailwind CSS styling across screens for consistent design.
