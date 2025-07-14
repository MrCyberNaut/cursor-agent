#!/usr/bin/env node
/**
 * optimise-gltf.mjs
 * Lightweight wrapper around gltf-pipeline & gltf-transform for batch compression.
 * Usage: `npm run optimise` or `node scripts/optimise-gltf.mjs path/to/model.glb`.
 */
import { execSync } from "node:child_process";
import { basename, dirname, join } from "node:path";
import { existsSync } from "node:fs";

const input = process.argv[2];
if (!input || !existsSync(input)) {
  console.error("❌  Please provide a valid .glb/.gltf file path.");
  process.exit(1);
}

const output = join(dirname(input), `${basename(input, ".glb")}.compressed.glb`);

try {
  console.log(`🔧 Compressing ${input} → ${output}`);
  // Example command using gltf-pipeline (needs to be installed globally or in project devDependencies)
  execSync(`npx gltf-pipeline -i ${input} -o ${output} -d`, { stdio: "inherit" });
  console.log("✅  Optimisation complete!");
} catch (err) {
  console.error("❌  glTF optimisation failed", err);
  process.exit(1);
}