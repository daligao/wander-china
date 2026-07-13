# Wander China — Open Source Trip Planner

A free, drag-and-drop China trip itinerary builder for foreign travelers. No Chinese needed.

**[Live demo →](https://ordinarymantrying.com/tools/wander-china/planner.html)**

![Wander China Planner](https://ordinarymantrying.com/wp-content/uploads/2026/07/wander-china-planner-interface.jpg)

## What it does

- Drag attractions onto a day timeline
- Auto-plan with smart algorithm (nearest-neighbor + opening hours filter)
- Real opening hours, ticket prices, metro stops
- Budget calculator
- Works for 31 Chinese cities (data community-contributed)

## How it works

All city data lives in `cities-data.js`. Each city entry has:
- Spot cards with hours, prices, metro directions, insider tips
- Travel time matrix between spots (taxi + metro)

The planner engine reads this data and handles all the UI.

**Changsha is the only fully-populated city in this repo.** All other cities are empty shells waiting for community contributions.

## Run locally

No build step needed. Just open `planner.html` in a browser.

```bash
git clone https://github.com/YOUR_USERNAME/wander-china.git
cd wander-china
open planner.html
```

## Add a city — see [CONTRIBUTING.md](CONTRIBUTING.md)

Each city needs ~10 attraction entries and a travel time matrix. If you know a Chinese city well (lived there, traveled there, have local contacts), your contribution will be seen by thousands of foreign travelers planning trips.

## Stack

- Vanilla JS, no framework
- Pure CSS (no Tailwind, no Bootstrap)
- Zero dependencies for core planner
- QRCode.js (CDN) for quiz stamp image

## License

MIT — use it, fork it, build on it.
