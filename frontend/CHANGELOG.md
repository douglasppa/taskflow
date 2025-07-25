# 📄 CHANGELOG

All notable changes to this project will be documented here.

## 🎨 v0.3.0 – Visual improvements, navbar and login enhancements

**Date:** 2025-07-24

### 🧭 Layout: Navigation bar and authenticated experience

- Implemented a global **navbar layout** for authenticated pages, including:
  - "Dashboard" and "Tarefas" navigation with current page highlight.
  - Logged-in user email and version display.
  - Styled logout button with icon and hover effect.
- Added consistent **AuthenticatedLayout** to wrap protected pages.

### 🧑‍🎨 UX/UI: Visual polish and icons

- Redesigned `TaskCard` with cleaner structure and action buttons positioned externally.
- Converted **Edit** and **Delete** buttons into minimalist **icons only**, improving focus and reducing clutter.
- Used `Lucide` icons throughout the app for consistent and modern visuals:
  - Task list icon (`ListChecks`) next to page title.
  - Floating button to create new task uses `PlusCircle`.
- Improved layout spacing, borders, and hover transitions for cards and buttons.

### 🔐 Login page: Structure and style for future expansion

- Improved **visual hierarchy** with emphasis on **TaskFlow** brand in title.
- Reorganized the form with better input contrast and spacing.
- Included **fully styled authentication UI features**:
  - Visual links for **"Create account"** and **"Forgot password"** sections.
  - Social login buttons for **Google** and **Facebook**, properly styled.

> This version focused on front-end refinement to elevate usability and prepare for future authentication features.

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
