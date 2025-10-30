⭐[click here for demo](https://youtu.be/59QD0ccXBAg?si=d1PRrHYaeBWltY4o)

# AlgoLeap AI 

A Generative AI-powered adaptive advisor for technical interview preparation.
Built in 24 hours for the GenAIversity Hackathon 2025.

## The Problem Statement

Preparing for technical (DSA) interviews is a high-stakes, high-stress challenge for computer science students.

Current platforms like LeetCode or HackerRank act as **static problem-checkers**, not as **personal advisors**. They offer a one-size-fits-all "grind" and provide binary pass/fail feedback.

This is a broken learning model:
1.  **No Actionable Guidance:** When a student's code fails, they are given a "Wrong Answer" or forced to look at the full, optimal solution. This teaches them to *memorize* solutions, not *how to find* them.
2.  **Inefficient Practice:** The difficulty jump between "Easy," "Medium," and "Hard" is often a wall. There is no adaptive ramp to bridge the gap.
3.  **Impersonal:** The process is isolating and frustrating, failing to replicate the 1-on-1 guidance of a real mentor.

## Our Solution

AlgoLeap AI is a **personal AI advisor** that makes interview prep adaptive, interactive, and effective.

Instead of just checking for correctness, our platform:
1.  **Provides Actionable Hints:** When your code fails, our AI doesn't just fail you. It analyzes your code and gives you a **direct, actionable hint**, just like a senior developer would (e.g., "**Hint:** Your solution is timing out. Your nested loop is $O(n^2)$. Try using a **Hash Map** to check for duplicates in a single pass.").
2.  **Offers Strategic Advice:** If you're stuck on a problem, you can ask for a high-level strategic hint (e.g., "**Hint:** This problem can be solved efficiently using the **'Two Pointers'** technique.").
3.  **Generates Adaptive Problems:** If you're consistently struggling with a topic, our AI generates a *new, custom* problem at a slightly easier level to help you build the skills and confidence you need.


## implementation

## Project summary

This repository is a frontend application built with React + TypeScript and Vite. The codebase includes Firebase-related configuration and an `AuthContext`, suggesting the app uses Firebase for authentication and data storage. Primary code lives under `src/` and UI primitives are in `src/components/ui/`.

Files to inspect for details:
- `src/lib/firebase.ts` — Firebase initialization and config (if present).
- `FIREBASE_SETUP.md` — Firebase setup instructions (exists at repo root).
- `src/contexts/AuthContext.tsx` — Authentication context and usage patterns.
- `package.json` — scripts and dependencies.

If you need a deeper analysis of backend configuration (Cloud Functions, REST APIs), search for `functions`, `firebase.json`, `cloud` or `api` in the repo.

---

## Frontend

Tech stack (inferred)
- React 18+ (TypeScript)
- Vite as bundler/dev server
- Tailwind CSS for styling (see `tailwind.config.ts`)
- Firebase client SDK for auth and possibly Firestore
- UI components under `src/components/ui/`

Key responsibilities
- UI rendering, routing, navigation and client-side state
- Communicates directly with Firebase SDK for auth and data
- Hosts interactive pages: `Index`, `Auth`, `Dashboard`, `ProblemSolve`, `CategoryProblems`

Important files & locations
- `src/main.tsx` — App entry.
- `src/App.tsx` — Router and top-level layout.
- `src/pages/*` — Page components.
- `src/components/ui/*` — Reusable UI components.
- `src/contexts/AuthContext.tsx` — Authentication context/provider for the app.
- `src/lib/firebase.ts` — Firebase initialisation and exported helpers.

State & data flow
- Local React state and contexts (AuthContext) are used for auth and session data.
- UI components are small, focused presentational elements used by pages.
- Data fetching is likely performed directly in components/pages using Firebase client SDK or fetch() to REST endpoints (if present).

Frontend build & scripts (typical)
- Install dependencies: `npm install` (or `pnpm install` / `bun install` if project uses those)
- Dev server: `npm run dev` (starts Vite dev server)
- Build: `npm run build` (produces production assets)
- Preview: `npm run preview`

(Confirm the actual scripts by opening `package.json`.)

---

## Backend

Current repo state
- There is no obvious server folder (e.g., `server/`, `api/`) in the repository root based on the file tree provided. There are strong indicators that Firebase services are used as the backend (see `src/lib/firebase.ts` and `FIREBASE_SETUP.md`).

Possible backend patterns
- Serverless (Firebase) only: Authentication and data stored in Firebase Auth and Firestore/Realtime DB, using client SDK directly from the frontend.
- Cloud Functions: If present, HTTP Cloud Functions may serve as REST API endpoints.
- External third-party APIs: The frontend may call third-party APIs (e.g., AI endpoints) directly from the client or via a server proxy.

What to look for to confirm backend type
- `firebase.json`, `firebaserc`, or a `functions/` directory — indicates Cloud Functions.
- `package.json` scripts referencing `functions` or `deploy` to Firebase.
- Any server or API subproject or `server`/`api` folders.

If you intend to add a backend: recommended options
- Keep using Firebase (Auth, Firestore, Functions) for simplicity.
- Introduce a Node/Express server for custom server-side logic and API proxies (common when needing secret keys or server-side compute).

---

## API & network

How the app likely communicates
- Frontend -> Firebase SDK (client-side) for auth and database reads/writes.
- Frontend -> HTTP(S) endpoints (if Cloud Functions or an external API are used).

Requests & security
- When using Firebase client SDK, the SDK uses the Firebase project's API keys and tokens. Security rules in Firestore or Realtime DB must enforce authorization.
- For third-party APIs that require secrets (for example, LLM or payment providers), do not store secrets in client-side code; instead, use Cloud Functions or a server to keep secrets safe.

Network diagram (ASCII)

Frontend (browser)
  |
  |--(Firebase SDK HTTPS/Realtime)--> Firebase Auth (login, tokens)
  |
  |--(Firestore / Realtime DB HTTPS)--> Firebase DB (reads/writes, secured by rules)
  |
  |--(Optional HTTP POST)--> Cloud Functions / External API (server-side logic or AI calls)

Notes about latency & caching
- Use Firestore SDK listeners for real-time updates where appropriate to reduce polling.
- Cache static data in memory or localStorage when useful and safe.

---

## Environment variables & secrets

Where to look
- `.env`, `.env.local` or `.env.*` in project root for Vite/React environment variables.
- `src/lib/firebase.ts` for the Firebase config object (apiKey, authDomain, projectId, etc.).
- `FIREBASE_SETUP.md` for instructions about creating Firebase project and adding config to the app.

Security guidance
- Do not commit private keys or service account files. Client-side Firebase apiKey is expected to be public-ish (it's used to identify the project). Keep service account JSON files off the repo and use environment variables for server-side apps.

---

## Local setup & run (PowerShell examples)

Below are the commands to run locally in PowerShell from the repository root (`c:\Users\harsh\OneDrive\Desktop\algo\algoleap-ai`):

1) Install dependencies (npm):

```powershell
npm install
```

If you use pnpm or bun (check `package.json` or presence of `pnpm-lock.yaml` / `bun.lockb`):

```powershell
pnpm install
# or
bun install
```

2) Start dev server:

```powershell
npm run dev
```

3) Open the logged local URL in your browser (Vite usually prints `http://localhost:5173`).

4) If Firebase config is required, ensure environment variables or a local config file is present before starting. Follow `FIREBASE_SETUP.md`.

---

## Build & deploy

- Build locally: `npm run build`
- Preview production build: `npm run preview`
- If deploying to Firebase Hosting, follow `FIREBASE_SETUP.md` and use `firebase deploy` (after installing Firebase CLI and logging in).

---
