# CODEX.md - Frontend Architecture & UI/UX Standards

## 1. Core Philosophy

This application is a high-end, professional tripartite platform. The interface must feel elite, trustworthy, and ultra-fluid. Every interaction must corporate a sense of "premium engineering".

## 2. UI & Aesthetic Restraints

- **Strict Emoji Ban:** Do NOT use emojis anywhere in the UI, source code comments, or tooltips. Use professional SVG iconography (Lucide-Vue or Heroicons) exclusively.

- **Typography:** Use a modern, highly legible sans-serif pairing (e.g., Inter for body, Geist or Cl clash Display for headers).

- **Color Theory (Dark/Light Mode):** Deep, authoritative slates and pure whites for backgrounds. Monochromatic scales accented with a single energetic tech color (e.g., Electric Indigo #4F46E5 or Deep Emerald #059669) to draw focus.

## 3. Motion & Animation Guidelines (The "Energetic & Fluid" Rule)

- **Framework:** Use Motion One for Vue or GSAP.
- **Micro-interactions:** Every button press, card hover, and tab switch must have a snappy, elastic physics-based transition (e.g., ease-out cubics or spring physics).
- **Layout Animations:** When a student filters internship offers or an enterprise moves a candidate in the Kanban board, elements must smoothly slide and morph into place (`<TransitionGroup>` with layout morphing).
- **Skeleton Loaders:** Never show a blank screen. Use shimmering, animated skeleton loaders matching the exact shape of incoming data to reduce perceived wait time.

## 4. Component Isolation Rules

- Every Vue component must be a Single File Component (`.vue`).
- Strictly separate Layout, Template (HTML), Script (TypeScript with Composition API), and scoped Tailwind classes.
- Design systems must respect WCAG 2.1 AA accessibility guidelines (screen readers, keyboard navigation).
