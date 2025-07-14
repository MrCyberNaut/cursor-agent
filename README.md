# The Sawant Drop — AR Business Card

A lightweight WebAR experience that brings your physical business card to life. Built with A-Frame, MindAR, and Vite.

---

## 📦 Project Structure

```
public/          # Static assets served at root
  ├─ index.html  # Entry HTML w/ A-Frame scene
  ├─ mindar/     # MindAR WASM + target files
  └─ assets/     # 3D models, vCard, textures …
src/             # TypeScript source
  ├─ main.ts     # Bootstrap + runtime logic
  └─ utils/      # Helper utilities
scripts/         # Node & shell scripts (build, deploy)
```

## 🚀 Getting Started

1. **Install dependencies**
   ```bash
   npm i
   ```
2. **Start dev server**
   ```bash
   npm run dev
   ```
   Vite will open `http://localhost:5173` by default.
3. **Build for production**
   ```bash
   npm run build
   ```
4. **Preview production build**
   ```bash
   npm run preview
   ```

## ✈️ Deploy

The project is intended to be deployed on Vercel.
Run the helper script (requires Vercel CLI auth):

```bash
./scripts/deploy.sh
```

## 🔧 glTF Optimisation

Compress individual models:
```bash
npm run optimize path/to/model.glb
```

---

© 2024 Sawant — MIT License
