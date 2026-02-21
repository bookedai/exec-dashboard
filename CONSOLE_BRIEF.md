# Booked AI Command Console — Build Brief

## Overview
Multi-page dark neon dashboard/console. Same aesthetic as the existing index.html (dark, glassmorphism, neon cyan/magenta/green/amber). This is our internal command center.

## Structure
- `index.html` — Homepage / Command Console
- `seo.html` — SEO Dashboard (rename current index.html to this)
- Shared nav sidebar or top nav linking between pages

## Navigation
Left sidebar (collapsible on mobile), dark with neon accent on active item:
- 🏠 **Command Center** (index.html)
- 📈 **SEO Dashboard** (seo.html) 
- More sections TBD (greyed out placeholder links): Analytics, Campaigns, Engineering, Financials

## Homepage: Command Center (index.html)

### 1. Header
- "BOOKED.AI" with neon glow
- Subtitle: "Command Console"
- Live clock (Melbourne timezone, updating every second)
- Status pill: "All Systems Operational" (green glow)

### 2. Quick Stats Row
- Active Projects: 5
- Open Tasks: 12
- SEO Keywords: 42,374
- Weekly Growth: +27.3%
- Team Members: 3 (Mennan, Daz, Yildiray)

### 3. Active Projects (card grid)
Each card has: name, status pill, progress bar, last activity, owner

Projects:
1. **Website Frontend** — Status: Active | Owner: Daz | Stack: Next.js | Progress: 75% | Note: "315K+ pages, ISR migration pending"
2. **SEO Optimization** — Status: In Progress | Owner: Yildiray | Progress: 40% | Note: "Audit complete, implementing fixes"
3. **Customer Acquisition** — Status: Strategy Phase | Owner: Mennan | Progress: 15% | Note: "Assessing Trip A Deals model"
4. **Strapi Backend** — Status: Active | Owner: Daz | Stack: Strapi/Railway | Progress: 80% | Note: "CMS powering all content"
5. **Mobile App** — Status: Active | Owner: Team | Stack: React Native | Progress: 60% | Note: "iOS + Android live on stores"

### 4. Task Board (Kanban-style, 3 columns)

#### To Do
- Implement FAQPage schema on city blogs
- Fix homepage SSR (client-rendered → server component)
- Convert flight pages from force-dynamic to ISR
- Fix preconnect (staging → production API)
- Add hreflang tags for AU/US/UK markets
- Build link building strategy
- Set up GA4 API integration
- Assess Trip A Deals customer acquisition model

#### In Progress
- SEO audit & implementation planning
- SEMrush API integration ✅
- GSC API integration ✅
- Internal linking strategy review
- Keyword gap analysis vs competitors

#### Done
- Website codebase audit ✅
- SEMrush data pull (42K+ keywords) ✅
- GSC service account setup ✅
- Executive dashboard v1 ✅
- Daily Daz roast automation ✅
- Claude Code integration for coding tasks ✅
- OpenClaw managed browser setup ✅

### 5. Recent Activity Feed (timeline style)
- 2026-02-21 16:37 — Dashboard deployed to GitHub Pages
- 2026-02-21 15:52 — GSC API integration complete
- 2026-02-21 15:30 — SEMrush full data pull (51 databases)
- 2026-02-21 14:30 — Website codebase cloned & audited
- 2026-02-21 10:37 — Daily Daz roast cron job configured
- 2026-02-21 10:35 — OpenClaw browser setup complete

### 6. System Status (bottom row)
Small status indicators:
- OpenClaw Gateway: 🟢 Running
- Slack Integration: 🟢 Connected
- Telegram Bot: 🟢 Connected  
- Claude Code: 🟢 Available
- SEMrush API: 🟢 Connected
- GSC API: 🟢 Connected
- GA4 API: 🔴 Not Connected
- GitHub: 🟢 Authenticated

## Design Requirements
- SAME dark neon theme as existing dashboard
- Same glassmorphism cards, same glow effects, same fonts
- Sidebar nav with neon cyan highlight on active page
- Smooth page transitions (or just consistent styling between pages)
- Kanban board should have subtle drag-handle styling (even if not functional)
- Activity feed should have a glowing timeline line on the left
- Status indicators should pulse gently
- Cards should have hover effects (lift + glow)
- Mobile responsive
- All inline HTML/CSS/JS, Chart.js from CDN for any charts
- No build tools, no frameworks

## Instructions
1. Rename current index.html to seo.html
2. Build new index.html (Command Center)
3. Add shared navigation between the two pages
4. Keep seo.html working exactly as before, just add the nav to it
