# 📄 CHANGELOG

All notable changes to this project will be documented here.

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
