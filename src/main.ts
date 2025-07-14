// src/main.ts
// Entry point for The Sawant Drop WebAR experience.
// Currently bootstraps simple console log and hooks into A-Frame load event.

import { isLowEndDevice } from "./utils/device";

document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 The Sawant Drop — AR Business Card booting up...");

  // Example of runtime performance/device check (placeholder)
  if (isLowEndDevice()) {
    console.warn("⚠️ Low-end device detected — minimal experience will be used.");
    // TODO: toggle lower-LOD assets or skip scene complexity.
  }

  // Future: add listeners for MindAR events, e.g. targetFound/targetLost
});