# Dashboard Brief

Build a single-page HTML dashboard (index.html) with inline CSS and JS. No build tools, no frameworks — pure HTML/CSS/JS with Chart.js from CDN.

## Theme
- Dark background (#0a0a0f or similar deep dark)
- Neon accent colors: cyan (#00f0ff), magenta (#ff00e5), electric green (#00ff88), amber (#ffaa00)
- Glassmorphism cards (semi-transparent backgrounds, blur, subtle borders)
- Subtle glow effects on key metrics
- Modern sans-serif font (Inter from Google Fonts)
- Responsive grid layout

## Sections

### 1. Header
- "BOOKED.AI" logo text with neon glow
- Subtitle: "Executive Dashboard"
- Last updated timestamp

### 2. Key Metrics Row (big neon numbers)
- Total Keywords: 42,374 (global)
- Weekly Clicks: 2,147 (trending up arrow)
- Monthly Impressions: 1.74M
- Indexed Pages: 108,546
- Referring Domains: 905
- Traffic Value: $5,571/mo

### 3. Growth Charts (Chart.js)

#### Weekly Clicks Trend (line chart, neon cyan)
Data:
```
W43: 131, W44: 968, W45: 966, W46: 967, W47: 849, W48: 886, W49: 785, W50: 930, W51: 959, W52: 615, W00: 530, W01: 1166, W02: 1007, W03: 911, W04: 989, W05: 1073, W06: 1682, W07: 2147
```

#### US Keyword & Traffic Growth (dual axis, cyan + magenta)
```
Aug 2025: 4914 kw, 1405 traffic
Sep 2025: 4950 kw, 1639 traffic
Oct 2025: 4901 kw, 1272 traffic
Nov 2025: 5090 kw, 1213 traffic
Dec 2025: 6859 kw, 1787 traffic
Jan 2026: 10827 kw, 2428 traffic
Feb 2026: 14766 kw, 3164 traffic
```

### 4. Top Keywords Table (dark themed, scrollable)
| Keyword | Position | Clicks (28d) | Impressions | CTR |
|---------|----------|-------------|-------------|-----|
| booked ai | 1 | 178 | 286 | 62.2% |
| ai travel agent | 3.4 | 143 | 2,210 | 6.5% |
| flight booking ai | 4.6 | 27 | 126 | 21.4% |
| flight booking ai agent | 2.5 | 27 | 115 | 23.5% |
| travel agent ai | 5.5 | 26 | 529 | 4.9% |
| booking ai | 5.5 | 20 | 691 | 2.9% |
| ai flight booking | 7.1 | 18 | 309 | 5.8% |
| travel ai agent | 8.1 | 15 | 411 | 3.6% |
| ai for flight booking | 4.7 | 14 | 175 | 8.0% |
| ai flight finder | 10.2 | 12 | 410 | 2.9% |

### 5. Global Presence (horizontal bar chart or world map style)
Top countries by clicks (28 days):
```
Australia: 828
USA: 654
UK: 403
India: 377
Germany: 231
Canada: 196
Netherlands: 123
Malaysia: 120
Italy: 118
Saudi Arabia: 111
Spain: 108
France: 107
```

### 6. Market Breakdown (table)
| Market | Rank | Keywords | Traffic | Value |
|--------|------|----------|---------|-------|
| US | 460,483 | 14,766 | 3,164 | $2,029 |
| AU | 62,856 | 7,088 | 3,205 | $1,692 |
| UK | 214,800 | 4,059 | 1,547 | $502 |
| CA | 203,941 | 2,427 | 932 | $478 |
| IN | 225,303 | 960 | 1,455 | $4 |
| DE | 453,589 | 1,145 | 573 | $64 |
| NZ | 68,874 | 775 | 344 | $54 |
| SG | 103,357 | 675 | 174 | $91 |

### 7. SEO Health Card
- Indexed: 108,546 pages ✅
- Not indexed: 34,893 pages ⚠️
- Backlinks: 3,906 (905 domains)
- Follow ratio: 71% ✅
- CTR: 0.35% ⚠️ (target: 1%+)
- Avg Position: 12.8

### 8. Issues & Actions (kanban-style cards)
#### 🔴 Critical
- Homepage is client-rendered (hurts SEO)
- www/non-www splitting authority
- Flight pages force-dynamic (no caching)

#### 🟡 Quick Wins
- Add FAQPage schema to city blogs
- Fix preconnect (staging → prod)
- Keyword-optimize meta descriptions

#### 🟢 In Progress
- SEMrush integration ✅
- GSC API integration ✅
- Codebase audit complete ✅

### 9. Device Split (donut chart)
- Mobile: 3,674 clicks (61%)
- Desktop: 2,218 clicks (37%)
- Tablet: 122 clicks (2%)

### 10. Projects Section
Cards for each active project:
1. **Booked AI Website** - Status: Active, Next.js, 315K+ pages
2. **SEO Optimization** - Status: Audit Complete, Link building needed
3. **Customer Acquisition** - Status: Strategy Phase

## Technical Requirements
- Single index.html file
- Chart.js 4.x from CDN
- Google Fonts (Inter)
- Responsive (works on mobile too)
- No external dependencies beyond CDN
- Smooth animations on load
- Make it look SICK — this is for the CEO
