#!/bin/bash

# ============ CONFIG =============
GH_USER="yourusername"               # 🔁 Your GitHub username
REPO_NAME="your-vue-repo"            # 🔁 Your Vue project repository name
CUSTOM_DOMAIN="www.yourdomain.com"   # 🔁 Your custom domain (from Namecheap)

# ============ BUILD & DEPLOY ============
echo "🏗️  Building Vue project..."
npm run build

echo "📁 Creating CNAME file..."
echo "$CUSTOM_DOMAIN" > dist/CNAME

echo "🚀 Deploying to GitHub Pages..."
npm run deploy

# ============ REMINDER ============
echo "✅ Pushed to GitHub Pages."

cat <<EOF

📌 FINAL STEPS — ONCE PER PROJECT:

1️⃣ Go to GitHub → $GH_USER/$REPO_NAME → Settings → Pages
   → Set Custom domain to: $CUSTOM_DOMAIN
   → Enable "Enforce HTTPS"

2️⃣ Go to Namecheap:
   → Domain List → Manage your domain → Advanced DNS
   → Add the following records:

▶ CNAME Record
  Type:   CNAME
  Host:   www
  Value:  $GH_USER.github.io
  TTL:    30 min

▶ (Optional) Redirect Root Domain
  Type:   URL Redirect
  Host:   @
  Value:  https://$CUSTOM_DOMAIN
  TTL:    30 min

⏳ Wait for DNS propagation and test:
   → https://$CUSTOM_DOMAIN

EOF
