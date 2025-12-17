# Houdinis Quantum Playground 

> **Developed by:** Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)

**Interactive browser-based quantum cryptanalysis platform**

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://playground.houdinis.dev)
[![Status](https://img.shields.io/badge/status-beta-yellow)](https://github.com/maurorisonho/Houdinis)
[![License](https://img.shields.io/badge/license-MIT-blue)](../LICENSE)

###  Tech Stack

**Frontend:**

![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=flat-square&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?style=flat-square&logo=tailwind-css&logoColor=white)
![Monaco Editor](https://img.shields.io/badge/Monaco_Editor-VSCode-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white)

**Backend & Runtime:**

![Pyodide](https://img.shields.io/badge/Pyodide-0.25-3776AB?style=flat-square&logo=python&logoColor=white)
![JupyterLite](https://img.shields.io/badge/JupyterLite-Browser-F37626?style=flat-square&logo=jupyter&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat-square&logo=node.js&logoColor=white)
![WebAssembly](https://img.shields.io/badge/WebAssembly-WASM-654FF0?style=flat-square&logo=webassembly&logoColor=white)

**State Management & Tools:**

![Zustand](https://img.shields.io/badge/Zustand-State-FF6B6B?style=flat-square)
![Radix UI](https://img.shields.io/badge/Radix_UI-Components-161618?style=flat-square)
![Recharts](https://img.shields.io/badge/Recharts-Visualization-22B5BF?style=flat-square)
![Three.js](https://img.shields.io/badge/Three.js-3D-000000?style=flat-square&logo=three.js&logoColor=white)

**DevOps:**

![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-Orchestration-2496ED?style=flat-square&logo=docker&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deploy-000000?style=flat-square&logo=vercel&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-Proxy-009639?style=flat-square&logo=nginx&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?style=flat-square&logo=redis&logoColor=white)

---

##  Overview

The Houdinis Quantum Playground is a **zero-installation, browser-based environment** for learning and experimenting with quantum cryptanalysis. No local setup required - just open your browser and start breaking crypto!

### Key Features

-  **Zero Installation**: Runs entirely in your browser
-  **Interactive Editor**: Monaco-based code editor with syntax highlighting
-  **Live Execution**: Python kernel powered by JupyterLite/Pyodide
-  **Visual Feedback**: Real-time circuit diagrams and quantum visualizations
-  **20+ Templates**: Pre-built quantum attack scenarios
-  **Multilingual**: Support for EN, PT-BR, ES, ZH
-  **Responsive**: Works on desktop, tablet, and mobile
-  **Secure**: Sandboxed execution, no server-side code execution

---

##  Architecture

```

                    Houdinis Playground                       
                 (Single Page Application)                     

                            
        
                                              
                                              
    
   Frontend        JupyterLite         Backend    
  React/Next       (Pyodide)          (Optional)  
    
                                              
                                              
                                              
    
  Monaco          Python Kernel       Serverless  
  Editor          (Browser)           Functions   
    
```

### Technology Stack

#### Frontend Layer
- **Framework**: Next.js 14 (React 18, App Router)
- **UI Components**: Shadcn/ui + Radix UI
- **Styling**: Tailwind CSS 3.x
- **Code Editor**: Monaco Editor (VS Code engine)
- **State Management**: Zustand + React Query
- **Animations**: Framer Motion
- **Icons**: Lucide React

#### Execution Layer
- **Python Runtime**: JupyterLite + Pyodide (WASM)
- **Quantum Libraries**: Qiskit 1.0+ (WASM-compiled)
- **Notebooks**: JupyterLab components
- **File System**: Browser IndexedDB
- **Kernel**: IPython kernel in browser

#### Visualization Layer
- **Quantum Circuits**: Qiskit Circuit Drawer (SVG)
- **Charts**: Recharts + D3.js
- **3D Graphics**: Three.js (optional)
- **LaTeX**: KaTeX for math rendering

#### Backend Layer (Optional/Minimal)
- **Platform**: Vercel Edge Functions / AWS Lambda
- **API**: tRPC for type-safe APIs
- **Database**: Upstash Redis (rate limiting)
- **Analytics**: Vercel Analytics
- **Monitoring**: Sentry

#### Infrastructure
- **Hosting**: Vercel (frontend + edge functions)
- **CDN**: Vercel Edge Network
- **DNS**: Cloudflare
- **SSL**: Automatic (Vercel)

---

##  Project Structure

```
playground/
 README.md                          # This file
 ARCHITECTURE.md                    # Detailed architecture doc
 DEPLOYMENT.md                      # Deployment guide
 package.json                       # Node dependencies
 tsconfig.json                      # TypeScript config
 next.config.js                     # Next.js config
 tailwind.config.js                 # Tailwind config
 .env.example                       # Environment variables template

 public/                            # Static assets
    templates/                     # Circuit templates (JSON)
       shor.json
       grover.json
       [18 more...]
    examples/                      # Code examples
       beginner/
       intermediate/
       advanced/
    assets/
        images/
        fonts/

 src/
    app/                          # Next.js App Router
       layout.tsx                # Root layout
       page.tsx                  # Homepage
       playground/
          page.tsx              # Main playground
       api/                      # API routes (minimal)
          trpc/
       globals.css
   
    components/                   # React components
       playground/
          CodeEditor.tsx        # Monaco editor wrapper
          OutputPanel.tsx       # Execution results
          CircuitViewer.tsx     # Quantum circuit viz
          ControlPanel.tsx      # Toolbar/controls
          TemplateSelector.tsx  # Template chooser
       visualizations/
          Histogram.tsx         # Measurement results
          StateVector.tsx       # Quantum state viz
          BlochSphere.tsx       # 3D qubit visualization
          CircuitDiagram.tsx    # Circuit rendering
       layout/
          Header.tsx
          Footer.tsx
          Sidebar.tsx
       ui/                       # Reusable UI components
           button.tsx
           dialog.tsx
           [20+ more...]
   
    lib/                          # Core libraries
       jupyter/
          kernel.ts             # Jupyter kernel manager
          pyodide.ts            # Pyodide loader
          executor.ts           # Code execution
       quantum/
          circuit-parser.ts     # Parse Qiskit circuits
          visualizer.ts         # Circuit visualization
          simulator.ts          # Quantum simulation
       storage/
          indexeddb.ts          # Browser storage
          cache.ts              # Code/result caching
       utils/
           format.ts
           validation.ts
   
    hooks/                        # React hooks
       useJupyter.ts             # Jupyter kernel hook
       useCodeExecution.ts       # Code execution hook
       useTemplates.ts           # Template management
       useKeyboardShortcuts.ts   # Keyboard bindings
   
    stores/                       # Zustand stores
       editorStore.ts            # Editor state
       executionStore.ts         # Execution state
       uiStore.ts                # UI preferences
   
    types/                        # TypeScript types
       jupyter.d.ts
       quantum.d.ts
       template.d.ts
   
    config/
        templates.ts              # Template definitions
        shortcuts.ts              # Keyboard shortcuts
        constants.ts              # App constants

 scripts/                          # Build/deploy scripts
    build-templates.js            # Generate template JSON
    optimize-assets.js            # Asset optimization
    deploy.sh                     # Deployment script

 docs/                             # Documentation
    USER_GUIDE.md                 # User documentation
    API.md                        # API reference
    TEMPLATES.md                  # Template creation guide
    CONTRIBUTING.md               # Contribution guide

 tests/                            # Testing
     unit/
     integration/
     e2e/
```

---

##  Getting Started

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm 9+ or yarn 1.22+
- Modern browser (Chrome 90+, Firefox 88+, Safari 15+, Edge 90+)

### Installation

```bash
# Clone the repository
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis/playground

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Start development server
npm run dev
```

Visit `http://localhost:3000/playground` to see the playground.

### Build for Production

```bash
# Build optimized production bundle
npm run build

# Preview production build locally
npm run start

# Run tests
npm run test

# Lint code
npm run lint
```

---

##  Features in Detail

### 1. Interactive Code Editor

**Monaco Editor** (VS Code engine) with:
- Syntax highlighting for Python
- IntelliSense (autocomplete)
- Error highlighting
- Code formatting (Black)
- Vim/Emacs keybindings (optional)
- Multi-cursor editing
- Find/replace with regex
- Code folding

**Keyboard Shortcuts:**
- `Ctrl+Enter` / `Cmd+Enter`: Run code
- `Ctrl+S` / `Cmd+S`: Save to browser storage
- `Ctrl+Shift+P`: Command palette
- `Ctrl+/`: Toggle line comment
- `F11`: Fullscreen editor

### 2. JupyterLite Kernel

**Pyodide-powered Python** runtime with:
- Python 3.11 (compiled to WebAssembly)
- Qiskit 1.0+ (quantum computing)
- NumPy, SciPy, Matplotlib
- Pandas (optional, heavy)
- Full Houdinis framework

**Features:**
- Local execution (no server needed)
- Persistent state across runs
- Import custom modules
- Install packages (micropip)
- Access browser APIs

### 3. Quantum Circuit Visualizations

**Real-time rendering** of:
- Circuit diagrams (SVG, interactive)
- Bloch sphere (3D, rotatable)
- State vector visualization
- Measurement histograms
- Density matrix heatmaps
- Quantum teleportation diagrams

**Visualization Libraries:**
- Qiskit's circuit drawer
- D3.js for interactive charts
- Three.js for 3D Bloch sphere
- Recharts for histograms

### 4. Pre-built Templates

**20+ quantum attack scenarios:**

#### Beginner (5 templates)
1. **Hello Quantum**: First quantum circuit
2. **Quantum Teleportation**: Entanglement demo
3. **Bell State**: Superposition and measurement
4. **Deutsch Algorithm**: First quantum speedup
5. **Quantum Random Number Generator**: True randomness

#### Intermediate (8 templates)
6. **Grover's Algorithm**: Symmetric key search
7. **Shor's Algorithm**: RSA factorization
8. **Simon's Algorithm**: Period finding
9. **Quantum Phase Estimation**: Eigenvalue finding
10. **Bernstein-Vazirani**: Hidden bitstring
11. **Amplitude Amplification**: Generalized Grover
12. **QAOA**: Combinatorial optimization
13. **VQE**: Variational quantum eigensolver

#### Advanced (7 templates)
14. **HHL Algorithm**: Linear systems solver
15. **Quantum Annealing**: Optimization problems
16. **QML Adversarial Attack**: Break quantum classifiers
17. **Lattice Crypto Attack**: NTRU/LWE analysis
18. **Hash Collision (Quantum)**: Birthday attack
19. **Zero-Knowledge Proof Attack**: Schnorr protocol
20. **Multi-Backend Comparison**: Performance testing

### 5. Output Panel

**Comprehensive result display:**
- Standard output (print statements)
- Error messages (formatted, clickable)
- Execution time
- Memory usage
- Quantum resource usage (gates, qubits, depth)
- Measurement results (histogram)
- Circuit diagram (auto-generated)
- Export results (JSON, PNG, SVG)

### 6. Responsive Design

**Works on all devices:**
- Desktop: Full 3-panel layout (editor, output, circuit)
- Tablet: 2-panel layout (tabs for output/circuit)
- Mobile: Single panel with bottom sheet

**Accessibility:**
- WCAG 2.1 AA compliant
- Keyboard navigation
- Screen reader support
- High contrast mode
- Adjustable font sizes

---

##  Deployment

### Option 1: Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to production
vercel --prod
```

**Costm Domain:**
```bash
vercel domains add playground.houdinis.dev
```

### Option 2: Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

### Option 3: Static Hosting (Cloudflare Pages, GitHub Pages)

```bash
# Build static site
npm run build
npm run export

# Upload /out directory to hosting provider
```

### Option 4: Docker

```bash
# Build Docker image
docker build -t houdinis-playground .

# Run container
docker run -p 3000:3000 houdinis-playground
```

---

##  Cost Estimation

### Free Tier (Good for demos/personal use)
- **Vercel Free Plan**: 100GB bandwidth/month, unlimited deployments
- **JupyterLite**: Runs in browser (no server costs)
- **Cloudflare**: Free DNS + SSL
- **Total**: **$0/month**

### Basic Plan (Small community)
- **Vercel Pro**: $20/month (1TB bandwidth, no function limits)
- **Upstash Redis**: $10/month (rate limiting, analytics)
- **Monitoring (Sentry)**: $26/month (50k events)
- **Total**: **$56/month**

### Production Plan (Large community)
- **Vercel Enterprise**: $150/month (10TB bandwidth, SLA)
- **Upstash Redis Pro**: $50/month
- **Monitoring Suite**: $100/month (Sentry + Datadog)
- **CDN (Cloudflare)**: $20/month (advanced features)
- **Total**: **$320/month**

---

##  Success Metrics

### User Engagement
- **Target**: 10,000+ unique visitors/month
- **Sessions**: 50,000+ playground sessions/month
- **Avg Session**: 15+ minutes
- **Bounce Rate**: <30%

### Technical Performance
- **Load Time**: <2 seconds (first paint)
- **Kernel Start**: <5 seconds (Pyodide initialization)
- **Code Execution**: <3 seconds (simple circuits)
- **Uptime**: 99.9%

### Educational Impact
- **Template Usage**: 80% of users try templates
- **Code Completion**: 60% of sessions result in successful execution
- **Return Rate**: 40% of users return within 7 days
- **Sharing**: 20% of users share results

---

##  Development

### Commands

```bash
# Development
npm run dev              # Start dev server
npm run dev:turbo        # Start with Turbopack (faster)

# Building
npm run build            # Production build
npm run analyze          # Analyze bundle size

# Testing
npm run test             # Run all tests
npm run test:watch       # Watch mode
npm run test:coverage    # Coverage report
npm run test:e2e         # End-to-end tests

# Code Quality
npm run lint             # ESLint
npm run lint:fix         # Auto-fix issues
npm run format           # Prettier
npm run type-check       # TypeScript check

# Deployment
npm run deploy           # Deploy to production
npm run deploy:preview   # Deploy preview branch
```

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=https://api.houdinis.dev
NEXT_PUBLIC_JUPYTER_LITE_URL=/jupyterlite
NEXT_PUBLIC_ANALYTICS_ID=G-XXXXXXXXXX
NEXT_PUBLIC_SENTRY_DSN=https://...

# Optional (for backend features)
UPSTASH_REDIS_URL=redis://...
UPSTASH_REDIS_TOKEN=...
RATE_LIMIT_ENABLED=true
```

---

##  Security

### Browser Sandboxing
- All code runs in WebAssembly sandbox
- No server-side code execution
- No file system access (except IndexedDB)
- CORS-protected API calls

### Rate Limiting (Optional Backend)
- 100 requests/minute per IP
- 1000 executions/hour per user
- DDoS protection via Cloudflare

### Content Security Policy
```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'unsafe-eval';  # Required for Pyodide
  style-src 'self' 'unsafe-inline'; # Required for Monaco
  img-src 'self' data:;
  font-src 'self' data:;
```

---

##  Documentation

- **User Guide**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **API Reference**: [docs/API.md](docs/API.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contributing**: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)
- **Templates**: [docs/TEMPLATES.md](docs/TEMPLATES.md)

---

##  Contributing

We welcome contributions! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly: `npm run test`
5. Commit: `git commit -m "feat: add amazing feature"`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

---

##  Roadmap

### Phase 1: MVP (Weeks 1-4) 
- [x] Basic playground UI
- [x] Monaco editor integration
- [x] JupyterLite kernel
- [x] 5 beginner templates
- [x] Circuit visualization
- [x] Deploy to Vercel

### Phase 2: Enhanced Features (Weeks 5-6)
- [ ] 20+ templates (all difficulty levels)
- [ ] Advanced visualizations (Bloch sphere, state vector)
- [ ] Code sharing (URL params)
- [ ] Export results (PNG, JSON)
- [ ] Keyboard shortcuts
- [ ] Mobile responsive design

### Phase 3: Community Features (Weeks 7-8)
- [ ] User accounts (optional, anonymous by default)
- [ ] Save/load projects
- [ ] Share playground sessions
- [ ] Embed playground in docs
- [ ] Analytics dashboard
- [ ] Performance monitoring

### Phase 4: Advanced (Post-Launch)
- [ ] Collaborative editing (multiplayer)
- [ ] AI code suggestions (Copilot integration)
- [ ] Video tutorials embedded
- [ ] Gamification (achievements, leaderboards)
- [ ] API for programmatic access

---

##  License

MIT License - see [../LICENSE](../LICENSE) for details.

---

##  Acknowledgments

- **JupyterLite**: Browser-based Jupyter
- **Pyodide**: Python in WebAssembly
- **Qiskit**: Quantum computing framework
- **Monaco Editor**: VS Code editor engine
- **Next.js**: React framework
- **Vercel**: Hosting and deployment

---

**Built with  for the quantum cryptanalysis community**
