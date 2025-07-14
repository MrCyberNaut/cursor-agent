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

  // Inject a simple 3D button that triggers vCard download
  const anchor = document.querySelector("[mindar-image-target]") as HTMLElement | null;
  if (anchor) {
    const button = document.createElement("a-plane");
    button.setAttribute("id", "vcard-button");
    button.setAttribute("color", "#0E9F6E");
    button.setAttribute("width", "0.7");
    button.setAttribute("height", "0.25");
    button.setAttribute("position", "0 -0.7 0");
    button.setAttribute("material", "shader: flat; side: double;");
    button.setAttribute(
      "text",
      "value: Add to Contacts; align: center; color: #ffffff; width: 2;"
    );

    // Handle click → download vCard
    button.addEventListener("click", () => {
      const link = document.createElement("a");
      link.href = "/assets/sawant.vcf";
      link.download = "sawant.vcf";
      document.body.appendChild(link);
      link.click();
      link.remove();
    });

    anchor.appendChild(button);
  }
});