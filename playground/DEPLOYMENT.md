# Houdinis Playground - Deployment Guide

> **Developed by:** Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)

Complete guide for deploying the Houdinis Quantum Playground to production.

---

##  Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git repository access
- Domain name (optional but recommended)
- Hosting account (Vercel/Netlify/Cloudflare)

---

##  Quick Deploy (Vercel - Recommended)

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Login to Vercel

```bash
vercel login
```

### 3. Deploy from Playground Directory

```bash
cd playground
vercel --prod
```

### 4. Configure Custom Domain (Optional)

```bash
vercel domains add playground.houdinis.dev
```

**Done!** Your playground is now live at `https://playground.houdinis.dev`

---

##  Detailed Setup

### Environment Variables

Create `.env.local` file:

```bash
# App Configuration
NEXT_PUBLIC_APP_NAME="Houdinis Playground"
NEXT_PUBLIC_APP_VERSION="1.0.0"
NEXT_PUBLIC_API_URL="https://api.houdinis.dev"

# JupyterLite Configuration
NEXT_PUBLIC_JUPYTER_LITE_URL="/jupyterlite"
NEXT_PUBLIC_PYODIDE_VERSION="0.25.0"

# Analytics (Optional)
NEXT_PUBLIC_ANALYTICS_ID="G-XXXXXXXXXX"
NEXT_PUBLIC_SENTRY_DSN="https://xxx@sentry.io/xxx"

# Rate Limiting (Optional - for backend features)
UPSTASH_REDIS_URL="redis://..."
UPSTASH_REDIS_TOKEN="..."
RATE_LIMIT_ENABLED="true"
RATE_LIMIT_MAX_REQUESTS="100"
RATE_LIMIT_WINDOW_MS="60000"
```

### Build Configuration

```bash
# Install dependencies
npm install

# Run type check
npm run type-check

# Run linter
npm run lint

# Build production bundle
npm run build

# Test production build locally
npm run start
```

---

##  Hosting Options

### Option 1: Vercel (Recommended)

**Pros:**
- Zero configuration
- Automatic HTTPS
- Edge functions support
- Global CDN
- GitHub integration
- Free tier available

**Steps:**

1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import GitHub repository
4. Select `playground` directory as root
5. Deploy

**Custom Domain:**
```bash
# Add domain
vercel domains add playground.houdinis.dev

# Configure DNS
# Add CNAME record pointing to cname.vercel-dns.com
```

**Cost:** Free for hobby projects, $20/month Pro plan

---

### Option 2: Netlify

**Pros:**
- Similar to Vercel
- Good free tier
- Form handling
- Split testing

**Steps:**

1. Install Netlify CLI:
   ```bash
   npm install -g netlify-cli
   ```

2. Login:
   ```bash
   netlify login
   ```

3. Deploy:
   ```bash
   cd playground
   npm run build
   netlify deploy --prod --dir=.next
   ```

4. Configure `netlify.toml`:
   ```toml
   [build]
     command = "npm run build"
     publish = ".next"

   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

**Cost:** Free for personal projects, $19/month Pro plan

---

### Option 3: Cloudflare Pages

**Pros:**
- Excellent performance
- Generous free tier
- Workers for serverless functions
- DDoS protection

**Steps:**

1. Go to [pages.cloudflare.com](https://pages.cloudflare.com)
2. Connect GitHub repository
3. Configure build settings:
   - Build command: `npm run build`
   - Build output directory: `.next`
   - Root directory: `playground`

4. Deploy

**Cost:** Free with generous limits

---

### Option 4: AWS Amplify

**Pros:**
- Full AWS integration
- Backend services
- Scalable

**Steps:**

1. Install Amplify CLI:
   ```bash
   npm install -g @aws-amplify/cli
   amplify configure
   ```

2. Initialize Amplify:
   ```bash
   cd playground
   amplify init
   ```

3. Add hosting:
   ```bash
   amplify add hosting
   amplify publish
   ```

**Cost:** Pay-as-you-go, typically $5-50/month

---

### Option 5: Self-Hosted (Docker)

**Dockerfile:**

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production image
FROM node:18-alpine AS runner

WORKDIR /app

ENV NODE_ENV production

# Copy built files
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./

RUN npm ci --only=production

EXPOSE 3000

CMD ["npm", "start"]
```

**Deploy:**

```bash
# Build image
docker build -t houdinis-playground .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_APP_NAME="Houdinis Playground" \
  houdinis-playground
```

**Docker Compose:**

```yaml
version: '3.8'

services:
  playground:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_APP_NAME=Houdinis Playground
    restart: unless-stopped
```

**Cost:** VPS $5-20/month (DigitalOcean, Linode, Vultr)

---

##  Security Configuration

### Content Security Policy

Add to `next.config.js`:

```javascript
async headers() {
  return [
    {
      source: '/:path*',
      headers: [
        {
          key: 'Content-Security-Policy',
          value: [
            "default-src 'self'",
            "script-src 'self' 'unsafe-eval' cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "font-src 'self' data:",
            "connect-src 'self' https://cdn.jsdelivr.net",
            "worker-src 'self' blob:",
          ].join('; '),
        },
        {
          key: 'X-Frame-Options',
          value: 'DENY',
        },
        {
          key: 'X-Content-Type-Options',
          value: 'nosniff',
        },
        {
          key: 'Referrer-Policy',
          value: 'strict-origin-when-cross-origin',
        },
        {
          key: 'Permissions-Policy',
          value: 'camera=(), microphone=(), geolocation=()',
        },
      ],
    },
  ];
}
```

### Rate Limiting (Optional)

For API routes, use Upstash Redis:

```typescript
// lib/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

export const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(100, '1 m'),
  analytics: true,
});
```

---

##  Monitoring & Analytics

### Vercel Analytics

```bash
npm install @vercel/analytics
```

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### Google Analytics

```typescript
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <script
          async
          src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
        />
        <script
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}');
            `,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### Sentry Error Tracking

```bash
npm install @sentry/nextjs
```

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  environment: process.env.NODE_ENV,
});
```

---

##  Testing Before Deployment

### Lighthouse Audit

```bash
npm install -g @lhci/cli

lhci autorun --config=lighthouserc.json
```

**lighthouserc.json:**
```json
{
  "ci": {
    "collect": {
      "url": ["http://localhost:3000/playground"],
      "numberOfRuns": 3
    },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.9}],
        "categories:accessibility": ["error", {"minScore": 0.9}],
        "categories:best-practices": ["error", {"minScore": 0.9}],
        "categories:seo": ["error", {"minScore": 0.9}]
      }
    }
  }
}
```

### Load Testing

```bash
npm install -g artillery

artillery quick --count 100 --num 10 https://playground.houdinis.dev
```

---

##  CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy-playground.yml`:

```yaml
name: Deploy Playground

on:
  push:
    branches: [main]
    paths:
      - 'playground/**'
  pull_request:
    branches: [main]
    paths:
      - 'playground/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: playground/package-lock.json
      
      - name: Install dependencies
        working-directory: playground
        run: npm ci
      
      - name: Type check
        working-directory: playground
        run: npm run type-check
      
      - name: Lint
        working-directory: playground
        run: npm run lint
      
      - name: Build
        working-directory: playground
        run: npm run build
        env:
          NEXT_PUBLIC_APP_NAME: "Houdinis Playground"
      
      - name: Deploy to Vercel
        if: github.ref == 'refs/heads/main'
        working-directory: playground
        run: npx vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
        env:
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```

---

##  Cost Estimation

### Free Tier (Hobby/Personal)
- **Hosting**: Vercel Free ($0/month)
- **Bandwidth**: 100GB/month included
- **Builds**: Unlimited
- **Analytics**: Basic included
- **Custom Domain**: Free
- **SSL**: Free (automatic)
- **Total**: **$0/month**

### Basic Plan (Small Community)
- **Hosting**: Vercel Pro ($20/month)
- **Analytics**: Vercel Analytics ($10/month)
- **Monitoring**: Sentry Developer ($26/month)
- **CDN**: Cloudflare (free)
- **Total**: **$56/month**

### Production Plan (Large Community)
- **Hosting**: Vercel Enterprise ($150/month)
- **Redis**: Upstash Pro ($50/month)
- **Monitoring**: Datadog ($100/month)
- **CDN**: Cloudflare Pro ($20/month)
- **Total**: **$320/month**

---

##  Performance Optimization

### 1. Code Splitting

Already handled by Next.js automatically.

### 2. Image Optimization

```typescript
import Image from 'next/image';

<Image
  src="/logo.png"
  width={200}
  height={50}
  alt="Houdinis Logo"
  priority
/>
```

### 3. Bundle Analysis

```bash
ANALYZE=true npm run build
```

### 4. Caching Strategy

```typescript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};
```

---

##  Troubleshooting

### Issue: Pyodide Not Loading

**Solution:**
- Check CORS headers
- Verify CDN URL in `pyodide.ts`
- Check browser console for errors

### Issue: Monaco Editor Not Rendering

**Solution:**
- Ensure `'unsafe-eval'` in CSP for scripts
- Check webpack configuration
- Verify monaco-editor package version

### Issue: High Bundle Size

**Solution:**
```bash
# Analyze bundle
ANALYZE=true npm run build

# Consider dynamic imports
const Editor = dynamic(() => import('@monaco-editor/react'), {
  ssr: false,
});
```

---

##  Pre-Launch Checklist

- [ ] Environment variables configured
- [ ] Custom domain set up (optional)
- [ ] SSL certificate active
- [ ] Analytics integrated
- [ ] Error tracking enabled
- [ ] Performance tested (Lighthouse score >90)
- [ ] Mobile responsiveness verified
- [ ] Cross-browser testing completed
- [ ] Security headers configured
- [ ] Rate limiting enabled (if needed)
- [ ] Monitoring dashboard set up
- [ ] Backup/disaster recovery plan
- [ ] Documentation updated
- [ ] Announcement prepared

---

##  Support

- **Documentation**: https://docs.houdinis.dev
- **GitHub Issues**: https://github.com/maurorisonho/Houdinis/issues
- **Community Discord**: https://discord.gg/houdinis

---

**Built with  for the quantum cryptanalysis community**
