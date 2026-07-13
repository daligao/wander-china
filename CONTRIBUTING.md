# Contributing a City

Thank you for helping make Wander China better for foreign travelers.

## What we need

Each city needs:
1. **10–12 attraction entries** (spots)
2. **Travel time matrix** between those spots

## Spot format

Open `cities-data.js` and look at the Changsha entry — that's the reference.

Each spot looks like this:

```js
{
  id: 'chengdu_research_base',      // snake_case, unique within city — also used as image filename
  nm: 'Chengdu Research Base of Giant Panda Breeding',
  ic: '🐼',                          // one emoji
  cat: 'nature',                     // landmark / culture / park / nature / history / food / shopping / entertainment
  dmin: 2,                           // minimum visit hours
  dmax: 4,                           // maximum visit hours
  pref: 'day',                       // 'day' / 'night' / 'both'
  cl: null,                          // closed day: 'Mon' / 'Tue' / etc, or null
  hr: '07:30–18:00 (last entry 17:00)',
  price: 55,                         // ticket price in ¥ (0 = free)
  pn: '¥55 (under 1.2m free)',       // human-readable price note
  metro: 'Line 3, Panda Avenue Stn Exit 1',
  desc: 'A 2–3 sentence description from a local perspective. Why does this place matter? What will a foreigner feel when they visit?',
  tip: 'Practical insider advice. Best time to go. Queue hacks. What to skip. Booking requirements if any.'
}
```

## Travel time matrix (tm)

The `tm` field is an N×N matrix where N = number of spots.

`tm[i][j]` = `[taxi_minutes, metro_minutes]` from spot i to spot j.

Rules:
- Diagonal is always `[0,0]`
- Matrix is symmetric: `tm[i][j]` should equal `tm[j][i]`
- Use rough estimates from Google Maps — exact precision isn't required
- If metro doesn't connect two spots directly, use a realistic transfer estimate

Example for a 3-spot city:
```js
tm: [
  [[0,0],  [15,20], [25,35]],   // spot 0 → all others
  [[15,20],[0,0],   [12,18]],   // spot 1 → all others
  [[25,35],[12,18], [0,0]]      // spot 2 → all others
]
```

## How to submit

1. Fork this repo
2. In `cities-data.js`, find your city (e.g. `chengdu`) — it currently has `spots:[], tm:[]`
3. Fill in the spots array and tm matrix following the Changsha example
4. Open a Pull Request with title: `Add [City] attraction data`
5. In the PR description, briefly note your source (lived there / visited / local contacts / verified against official sites)

## Content standards

- **Prices**: current as of your research date — add a comment with the date if possible
- **Hours**: use the format `HH:MM–HH:MM` so the planner's opening-hours filter can parse it
- **desc**: write for a foreign traveler who has never been to China — assume no Chinese, no context
- **tip**: must contain at least one specific detail (exact time, price, distance, queue trick)
- **No generic content**: "a famous historical site" is not useful. "Built in 976 AD, one of China's four great ancient academies" is.

## Questions?

Open an issue and tag it `[city-data]`.
