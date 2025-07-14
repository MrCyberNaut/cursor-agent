#!/usr/bin/env bash
# deploy.sh — CI helper to trigger Vercel deployment (non-interactive)

set -euo pipefail

# Ensure Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
  echo "Vercel CLI missing. Installing globally..."
  npm i -g vercel@latest
fi

# Pull Vercel env vars (optional) then deploy
vercel pull --yes --environment=production
vercel build --prod
vercel deploy --prebuilt --prod --yes