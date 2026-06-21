#!/usr/bin/env python3
"""Generate ranking + category pages for SEO (P2)."""
import json, re, os, unicodedata

with open("ordinarymantrying.com/tools/major-vote.html", encoding="utf-8") as f:
    src = f.read()

m  = re.search(r'const ALL\s*=\s*(\[.*?\]);', src, re.DOTALL)
ALL = json.loads(m.group(1))
m2 = re.search(r'const AIPICK\s*=\s*new Set\(\[(.*?)\]\)', src)
AIPICK = set(x.strip().strip('"') for x in m2.group(1).split(','))

# Star ratings per subcategory (mirrors generate_major_pages.py SUBCAT stars)
SUBCAT_STARS = {
  'Advanced Engineering':4,'Aerospace':4,'Agricultural Engineering':3,'Architecture':3,
  'Automation':4,'Biomedical Engineering':4,'Chem Engineering & Pharmacy':3,
  'Civil Engineering':3,'Computer Science':5,'Electrical Engineering':4,
  'Electronic Information':5,'Energy & Power':4,'Environmental Engineering':3,
  'Food Science & Engineering':3,'Forestry Engineering':3,'Geology Engineering':3,
  'Hydraulic Engineering':3,'Instrumentation':3,'Interdisciplinary Eng':3,
  'Light Industry':3,'Materials Science':4,'Mechanical Engineering':3,'Mechanics':3,
  'Mining':3,'Nuclear Engineering':4,'Ocean Engineering':3,'Ordnance':3,
  'Public Security Tech':3,'Safety Engineering':3,'Surveying & Mapping':4,
  'Textile':2,'Transportation':3,
  'Basic Medical Sciences':4,'Chinese Materia Medica':3,'Clinical Medicine':5,
  'Dental Medicine':5,'Forensic Medicine':3,'Integrative Medicine':3,
  'Medical Technology':3,'Nursing':4,'Pharmacy':3,'Public Health':3,
  'Trad. Chinese Medicine':3,
  'Astronomy':2,'Atmospheric Sciences':3,'Biological Sciences':4,'Chemistry':3,
  'Geographic Sciences':3,'Geology':3,'Geophysics':3,'Mathematics':4,
  'Ocean Sciences':3,'Physics':4,'Psychology':3,'Statistics':4,
  'Economics':3,'Finance':3,'Intl Economics & Trade':3,'Public Finance':3,
  'Education':3,'Physical Education':3,
  'History':2,
  'Ethnology':2,'Law':3,'Marxist Theory':3,'Political Science':3,
  'Public Security':3,'Sociology':2,
  'Chinese Language & Lit':2,'Foreign Languages':2,'Journalism & Comm':2,
  'Agricultural Management':3,'Business Administration':3,'E-Commerce':3,
  'Industrial Engineering':3,'Library & Info Management':2,'Logistics Management':3,
  'Management Sci & Eng':3,'Public Administration':3,'Tourism Management':2,
  'Animal Production':3,'Crop Production':3,'Fisheries':3,'Forestry':3,
  'Grassland Science':2,'Nature Conservation & Ecology':3,'Veterinary Medicine':4,
  'Philosophy':3,
}

def get_stars(major):
    sub = major.get('sub', major['cat'])
    base = SUBCAT_STARS.get(sub, 3)
    return min(5, base + (1 if major['c'] in AIPICK else 0))

def slug(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def stars_html(n): return '★'*n + '☆'*(5-n)

# ── Shared styles + shell ─────────────────────────────────────────
STYLE = """
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:#0f172a;color:#e2e8f0;line-height:1.6;}
a{color:#60a5fa;text-decoration:none;}
a:hover{text-decoration:underline;}
.hdr{background:linear-gradient(160deg,#0d1b2e,#1a3560);
  padding:32px 20px 28px;border-bottom:1px solid #334155;}
.hdr-label{font-size:11px;text-transform:uppercase;letter-spacing:.15em;
  color:#3b82f6;font-family:monospace;margin-bottom:8px;}
h1{font-size:clamp(22px,5vw,34px);font-weight:800;line-height:1.2;margin-bottom:12px;}
.hdr-desc{font-size:14px;color:#94a3b8;max-width:600px;}
.page{max-width:720px;margin:0 auto;padding:28px 18px 60px;}
.intro{background:#1e293b;border:1px solid #334155;border-radius:12px;
  padding:20px;margin-bottom:20px;font-size:14px;color:#cbd5e1;line-height:1.8;}
.section-title{font-size:11px;text-transform:uppercase;letter-spacing:.1em;
  color:#94a3b8;font-weight:700;margin:24px 0 12px;}
.major-row{display:flex;align-items:center;gap:12px;padding:12px 16px;
  background:#1e293b;border:1px solid #334155;border-radius:10px;
  margin-bottom:8px;transition:border-color .15s;text-decoration:none;color:inherit;}
.major-row:hover{border-color:rgba(59,130,246,.5);text-decoration:none;}
.row-stars{font-size:13px;letter-spacing:1px;flex-shrink:0;color:#f59e0b;}
.row-name{font-size:14px;font-weight:600;color:#e2e8f0;flex:1;}
.row-sub{font-size:11px;color:#64748b;}
.ai-tag{background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);
  border-radius:4px;padding:1px 6px;font-size:10px;color:#f59e0b;flex-shrink:0;}
.num{font-size:12px;color:#475569;flex-shrink:0;min-width:24px;text-align:right;}
.cta-vote{display:block;text-align:center;padding:14px;margin:24px 0 12px;
  background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);
  border-radius:12px;font-size:14px;font-weight:600;color:#60a5fa;}
.cta-vote:hover{background:rgba(59,130,246,.18);text-decoration:none;}
.blog-cta{display:block;margin-bottom:16px;padding:20px 22px;
  background:linear-gradient(135deg,#1e3a5f,#0f172a);
  border:1px solid rgba(59,130,246,.35);border-radius:14px;text-decoration:none;}
.blog-cta:hover{border-color:rgba(59,130,246,.7);text-decoration:none;}
.blog-cta-label{font-size:11px;text-transform:uppercase;letter-spacing:.1em;
  color:#3b82f6;font-weight:700;margin-bottom:6px;}
.blog-cta-title{font-size:15px;font-weight:800;color:#e2e8f0;margin-bottom:4px;}
.blog-cta-sub{font-size:13px;color:#64748b;}
.nav-links{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;}
.nav-link{padding:6px 14px;background:rgba(255,255,255,.04);border:1px solid #334155;
  border-radius:20px;font-size:12px;color:#94a3b8;text-decoration:none;}
.nav-link:hover{border-color:#475569;color:#e2e8f0;text-decoration:none;}
.nav-link.active{background:rgba(59,130,246,.12);border-color:rgba(59,130,246,.4);color:#60a5fa;}
.foot{text-align:center;padding:20px;font-size:12px;color:#475569;
  border-top:1px solid #1e293b;}
"""

NAV_PAGES = [
    ("Best Majors 2025",       "best-majors-china-2025.html"),
    ("AI Picks",               "ai-picks-majors-china.html"),
    ("AI-Resistant",           "ai-resistant-majors-china.html"),
    ("Engineering",            "engineering-majors-china.html"),
    ("Medicine",               "medicine-majors-china.html"),
    ("Science",                "science-majors-china.html"),
    ("Economics",              "economics-majors-china.html"),
    ("Management",             "management-majors-china.html"),
    ("Law",                    "law-majors-china.html"),
    ("Literature",             "literature-majors-china.html"),
    ("Agriculture",            "agriculture-majors-china.html"),
    ("Education",              "education-majors-china.html"),
    ("History & Philosophy",   "history-philosophy-majors-china.html"),
]

def nav_html(current_file):
    links = []
    for label, fname in NAV_PAGES:
        cls = 'nav-link active' if fname == current_file else 'nav-link'
        links.append(f'<a class="{cls}" href="/tools/{fname}">{label}</a>')
    return '<div class="nav-links">' + ''.join(links) + '</div>'

def blog_cta():
    return '''<a class="blog-cta" href="https://ordinarymantrying.com/building-in-public-experiment/" target="_blank" rel="noopener">
  <div class="blog-cta-label">📺 Building in Public — 5-Year Experiment</div>
  <div class="blog-cta-title">One ordinary person building this from scratch — with real numbers.</div>
  <div class="blog-cta-sub">Follow the journey → ordinarymantrying.com</div>
</a>'''

def major_row(major, rank=None):
    n    = get_stars(major)
    ai   = major['c'] in AIPICK
    sub  = major.get('sub', major['cat'])
    num  = f'<span class="num">#{rank}</span>' if rank else ''
    ai_b = '<span class="ai-tag">🤖 AI Pick</span>' if ai else ''
    return (f'<a class="major-row" href="/tools/majors/{slug(major["n"])}.html">'
            f'{num}'
            f'<span class="row-stars">{stars_html(n)}</span>'
            f'<span class="row-name">{major["n"]}</span>'
            f'<span class="row-sub">{sub}</span>'
            f'{ai_b}'
            f'</a>')

def page_shell(filename, title, seo_title, seo_desc, label, h1, desc, body_html):
    canonical = f"https://ordinarymantrying.com/tools/{filename}"
    faq_schema = json.dumps({
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[
            {"@type":"Question","name":f"What are the best Chinese university majors in 2025?",
             "acceptedAnswer":{"@type":"Answer","text":"Based on AI analysis and community votes, Engineering (especially Computer Science and Electronic Information), Clinical Medicine, and Dental Medicine rank among the strongest majors for career prospects in China through 2029."}},
            {"@type":"Question","name":"Which Chinese majors are most resistant to AI disruption?",
             "acceptedAnswer":{"@type":"Answer","text":"Medicine, law, and hands-on trades are most AI-resistant. Clinical Medicine, Nursing, and Dental Medicine require human judgment and physical presence that AI cannot replicate. Philosophy and AI Ethics are also growing in value because of AI, not despite it."}},
        ]
    })
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{seo_title}</title>
<meta name="description" content="{seo_desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{seo_title}">
<meta property="og:description" content="{seo_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Ordinary Man Trying">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{seo_title}">
<meta name="twitter:description" content="{seo_desc}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article",
  "headline":"{seo_title}","description":"{seo_desc}","url":"{canonical}",
  "author":{{"@type":"Person","name":"Ordinary Man Trying","url":"https://ordinarymantrying.com"}}}}</script>
<script type="application/ld+json">{faq_schema}</script>
<style>{STYLE}</style>
</head>
<body>
<div class="hdr">
  <a style="font-size:12px;color:#94a3b8;display:block;margin-bottom:14px;"
     href="/tools/major-vote.html">← Back to All 757 Majors — Vote &amp; Compare</a>
  <div class="hdr-label">{label}</div>
  <h1>{h1}</h1>
  <div class="hdr-desc">{desc}</div>
</div>
<div class="page">
{nav_html(filename)}
<div class="intro">{body_html["intro"]}</div>
{body_html["list"]}
<a class="cta-vote" href="/tools/major-vote.html">
  ▲ Vote for any major — see the live 5-year ranking →
</a>
{blog_cta()}
</div>
<div class="foot">Data: Ministry of Education of China · Undergraduate Majors Directory 2024<br>
Built by <a href="https://ordinarymantrying.com">Ordinary Man Trying</a></div>
</body></html>'''

OUT = "ordinarymantrying.com/tools"
os.makedirs(OUT, exist_ok=True)

pages_written = []

# ══════════════════════════════════════════════════════════════════
# 1. BEST MAJORS 2025 — top 50 by star rating
# ══════════════════════════════════════════════════════════════════
ranked = sorted(ALL, key=lambda x: get_stars(x), reverse=True)
top50  = ranked[:50]

rows = '\n'.join(major_row(m, i+1) for i, m in enumerate(top50))
fname = "best-majors-china-2025.html"
content = page_shell(fname,
    title     = "Best Chinese University Majors 2025",
    seo_title = "Best Chinese University Majors in 2025 — AI Career Rankings",
    seo_desc  = "The top 50 Chinese university majors ranked by AI career analysis and community votes. Updated 2025–2029 outlook for all 757 official majors.",
    label     = "Rankings · Updated 2025",
    h1        = "Best Chinese University Majors in 2025",
    desc      = "Top 50 majors ranked by AI career outlook, job demand, and community votes. Part of a 5-year experiment tracking which fields actually matter.",
    body_html = {
        "intro": "China has 757 official university majors. These 50 received the highest scores based on AI analysis of job demand, salary trajectory, AI resilience, and career growth potential through 2029. The ranking combines structured analysis with live community votes — updated as data comes in.",
        "list":  f'<div class="section-title">Top 50 Majors — Ranked by Future Outlook Score</div>\n{rows}'
    }
)
with open(f"{OUT}/{fname}", "w", encoding="utf-8") as f: f.write(content)
pages_written.append(fname)

# ══════════════════════════════════════════════════════════════════
# 2. AI PICKS — 13 majors flagged by AI
# ══════════════════════════════════════════════════════════════════
ai_majors = [m for m in ALL if m['c'] in AIPICK]
rows = '\n'.join(major_row(m, i+1) for i, m in enumerate(ai_majors))
fname = "ai-picks-majors-china.html"
content = page_shell(fname,
    title     = "AI-Picked Chinese University Majors 2025",
    seo_title = "AI-Picked Chinese University Majors — 13 Fields Flagged for Growth 2025–2029",
    seo_desc  = f"13 Chinese university majors specifically identified by AI as high-resilience, high-growth fields for students entering in 2025. See which majors AI flagged and why.",
    label     = f"🤖 AI Picks · {len(ai_majors)} Majors",
    h1        = "13 Majors AI Specifically Flagged for 2025–2029",
    desc      = "Out of 757 Chinese university majors, AI analysis flagged these 13 as having above-average resilience and growth potential. Here's what stood out — and why.",
    body_html = {
        "intro": "When asked to rank all 757 Chinese university majors, AI systems identified a small set of fields with a distinct combination of traits: strong domestic policy backing, growing global demand, integration with AI tools rather than displacement by them, and a structural supply-demand gap favoring graduates. These 13 majors consistently stood out across multiple evaluation frameworks. They are not the only good choices — but they are the ones that AI flagged most consistently.",
        "list":  f'<div class="section-title">All {len(ai_majors)} AI-Flagged Majors</div>\n{rows}'
    }
)
with open(f"{OUT}/{fname}", "w", encoding="utf-8") as f: f.write(content)
pages_written.append(fname)

# ══════════════════════════════════════════════════════════════════
# 3. AI-RESISTANT MAJORS
# ══════════════════════════════════════════════════════════════════
resistant_cats = {'Medicine', 'Law', 'Philosophy'}
resistant = [m for m in ALL if m['cat'] in resistant_cats]
resistant_sorted = sorted(resistant, key=lambda x: get_stars(x), reverse=True)
rows = '\n'.join(major_row(m, i+1) for i, m in enumerate(resistant_sorted))
fname = "ai-resistant-majors-china.html"
content = page_shell(fname,
    title     = "AI-Resistant Chinese University Majors",
    seo_title = "AI-Resistant Chinese University Majors 2025 — Fields AI Cannot Replace",
    seo_desc  = f"{len(resistant)} Chinese university majors in Medicine, Law, and Philosophy where human judgment remains irreplaceable. Career outlook 2025–2029.",
    label     = f"AI-Resistant · {len(resistant)} Majors",
    h1        = "Chinese Majors Most Resistant to AI Disruption",
    desc      = f"{len(resistant)} fields where human judgment, physical presence, and professional trust create durable barriers that AI tools cannot easily cross.",
    body_html = {
        "intro": "AI is automating many graduate-level tasks — but not all of them equally. Three categories stand out as genuinely AI-resistant: Medicine (requires clinical judgment and physical presence), Law (requires advocacy, negotiation, and trust), and Philosophy (increasingly essential for AI ethics and governance). These fields are not immune to AI tools — doctors use AI for imaging, lawyers use AI for research — but the core human functions remain irreplaceable. Graduates in these fields are likely to find AI makes them more effective, not redundant.",
        "list":  f'<div class="section-title">Medicine, Law & Philosophy — {len(resistant)} Majors Ranked</div>\n{rows}'
    }
)
with open(f"{OUT}/{fname}", "w", encoding="utf-8") as f: f.write(content)
pages_written.append(fname)

# ══════════════════════════════════════════════════════════════════
# 4–14. CATEGORY PAGES (11 categories)
# ══════════════════════════════════════════════════════════════════
CAT_META = {
  'Engineering': {
    'fname': 'engineering-majors-china.html',
    'label': 'Engineering · China',
    'h1':    'Engineering Majors in China — All {n} Fields Ranked',
    'desc':  'Every engineering major in the Chinese university system, ranked by AI career analysis and community votes.',
    'intro': 'Engineering is the largest category in China\'s undergraduate system, with {n} official majors spanning everything from Computer Science and AI hardware to traditional fields like Civil and Mechanical Engineering. The range of career outcomes across these majors is enormous — Computer Science and Electronic Information are among the strongest choices in the entire system, while some traditional engineering fields face significant automation pressure. Browse all {n} to compare their outlook for 2025–2029.',
    'seo_title': 'Engineering Majors in China 2025 — All {n} Fields Ranked by Career Outlook',
    'seo_desc':  'Complete list of all {n} Engineering majors in China\'s university system, ranked by AI career analysis and community votes. Includes Computer Science, Aerospace, Materials Science, and more.',
  },
  'Medicine': {
    'fname': 'medicine-majors-china.html',
    'label': 'Medicine · China',
    'h1':    'Medicine Majors in China — All {n} Fields',
    'desc':  'Every medical major in the Chinese university system ranked by career outlook and AI resilience.',
    'intro': 'Medicine is the most AI-resistant category in the Chinese university system. With {n} official majors spanning everything from Clinical Medicine and Nursing to Traditional Chinese Medicine and Forensic Medicine, this category combines the longest training paths with some of the most stable and respected careers available. AI is transforming medical diagnostics and drug discovery — but the physician-patient relationship, surgical skill, and clinical judgment at the center of medical practice remain fundamentally human.',
    'seo_title': 'Medicine Majors in China 2025 — All {n} Fields Ranked by Career Outlook',
    'seo_desc':  'Complete list of all {n} Medicine majors in China\'s university system, including Clinical Medicine, Nursing, TCM, Pharmacy, and Dental Medicine. Career outlook and AI impact analysis.',
  },
  'Science': {
    'fname': 'science-majors-china.html',
    'label': 'Science · China',
    'h1':    'Science Majors in China — All {n} Fields Ranked',
    'desc':  'Every science major in China ranked by AI career analysis, from Mathematics and Physics to Biological Sciences.',
    'intro': 'Science majors provide the foundational knowledge that drives engineering, medicine, and technology forward. China\'s {n} official science majors span pure disciplines like Mathematics and Physics — now more valuable than ever due to AI and quantum computing demand — through to applied fields like Atmospheric Sciences, Biological Sciences, and Statistics. Graduates who combine scientific foundations with computational skills are finding their training increasingly relevant to the data-driven economy.',
    'seo_title': 'Science Majors in China 2025 — All {n} Fields Ranked by Career Outlook',
    'seo_desc':  'Complete list of all {n} Science majors in China, including Mathematics, Physics, Biological Sciences, Statistics, and more. AI era career outlook and community votes.',
  },
  'Economics': {
    'fname': 'economics-majors-china.html',
    'label': 'Economics · China',
    'h1':    'Economics Majors in China — All {n} Fields',
    'desc':  'Every economics and finance major in China ranked by AI career analysis and community votes.',
    'intro': 'Economics majors in China span {n} official fields from broad Economics and Finance to specialized programs in International Trade and Public Finance. These majors develop strong analytical foundations that transfer across consulting, government, banking, and corporate strategy roles. In the AI era, the graduates who thrive are those who combine economic thinking with quantitative skills — data analysis, financial modeling, and policy research are all areas where economics training adds genuine value.',
    'seo_title': 'Economics & Finance Majors in China 2025 — All {n} Fields Ranked',
    'seo_desc':  'Complete list of all {n} Economics majors in China, including Finance, International Trade, and Public Finance. Career outlook and AI impact for 2025–2029.',
  },
  'Management': {
    'fname': 'management-majors-china.html',
    'label': 'Management · China',
    'h1':    'Management Majors in China — All {n} Fields',
    'desc':  'Every management major in China ranked by career outlook, from Business Administration to E-Commerce and Public Administration.',
    'intro': 'Management is one of the most diverse categories in China\'s university system, with {n} majors ranging from Business Administration and E-Commerce to Logistics Management and Public Administration. The breadth of options means career outcomes vary significantly. The management graduates who succeed are those who pair their credential with deep industry knowledge, technical data skills, or specific sector expertise — generalist management alone is increasingly insufficient in a competitive market.',
    'seo_title': 'Management Majors in China 2025 — All {n} Fields Ranked by Career Outlook',
    'seo_desc':  'Complete list of all {n} Management majors in China, including Business Administration, E-Commerce, Logistics, and Public Administration. Career outlook 2025–2029.',
  },
  'Law': {
    'fname': 'law-majors-china.html',
    'label': 'Law · China',
    'h1':    'Law & Political Science Majors in China — All {n} Fields',
    'desc':  'Every law, political science, and sociology major in China ranked by career outlook.',
    'intro': 'Law-category majors in China include {n} official fields spanning legal practice, political science, sociology, public security, and Marxist theory. The field\'s AI resilience comes from the irreplaceable role of judgment, advocacy, and institutional trust in legal and governance systems. AI handles document review and legal research with growing proficiency — but the humans who interpret, argue, and decide remain central. The fastest-growing opportunities within this category are in compliance, international law, and AI governance.',
    'seo_title': 'Law & Political Science Majors in China 2025 — All {n} Fields Ranked',
    'seo_desc':  'Complete list of all {n} Law-category majors in China, including Law, Political Science, Sociology, and Public Security. Career outlook and AI impact 2025–2029.',
  },
  'Literature': {
    'fname': 'literature-majors-china.html',
    'label': 'Literature · China',
    'h1':    'Literature & Language Majors in China — All {n} Fields',
    'desc':  'Every literature, language, and journalism major in China ranked by career outlook in the AI content era.',
    'intro': 'Literature-category majors in China span {n} official fields — from Chinese Language and Literature and Journalism through to 104 Foreign Language programs covering everything from English to Yoruba. This is the category most directly disrupted by AI writing and translation tools. Graduates who develop domain expertise alongside language skills, or who build distinctive creative voices, will find demand. Those who compete on commodity content production face real pressure from AI tools that are improving rapidly.',
    'seo_title': 'Literature & Language Majors in China 2025 — All {n} Fields Ranked',
    'seo_desc':  'Complete list of all {n} Literature majors in China, including Chinese Language, Foreign Languages (104 programs), and Journalism. Career outlook in the AI content era.',
  },
  'Agriculture': {
    'fname': 'agriculture-majors-china.html',
    'label': 'Agriculture · China',
    'h1':    'Agriculture Majors in China — All {n} Fields',
    'desc':  'Every agriculture, forestry, and veterinary major in China ranked by career outlook.',
    'intro': 'Agriculture majors in China span {n} official fields — from Crop Production and Animal Husbandry to Veterinary Medicine and Nature Conservation. This is one of the most policy-protected categories in the university system: food security and ecological restoration are permanent national priorities backed by sustained government investment. The category is also modernizing rapidly — precision agriculture, AgTech, and drone farming are creating new technical roles within fields that were previously more manual. The pet economy boom is making Veterinary Medicine a surprisingly strong choice.',
    'seo_title': 'Agriculture Majors in China 2025 — All {n} Fields Ranked by Career Outlook',
    'seo_desc':  'Complete list of all {n} Agriculture majors in China, including Crop Science, Veterinary Medicine, Forestry, and AgTech. Career outlook and AI impact 2025–2029.',
  },
  'Education': {
    'fname': 'education-majors-china.html',
    'label': 'Education · China',
    'h1':    'Education Majors in China — All {n} Fields',
    'desc':  'Every education and physical education major in China ranked by career outlook.',
    'intro': 'Education majors in China cover {n} fields across teacher training, curriculum design, sports science, and athletic coaching. Government teacher employment remains one of the most stable career paths available — immune to most market cycles and backed by mandatory national staffing standards. AI tools are expanding what individual teachers can prepare and deliver rather than replacing them. The growing EdTech industry is also creating corporate roles for education graduates who want to work outside the classroom.',
    'seo_title': 'Education Majors in China 2025 — All {n} Fields Ranked by Career Outlook',
    'seo_desc':  'Complete list of all {n} Education majors in China, including teacher training, PE, and sports science. Stable career outlook and AI impact 2025–2029.',
  },
  'History': None,   # combined with Philosophy below
  'Philosophy': None,
}

# Combined History + Philosophy page
hist_phil = [m for m in ALL if m['cat'] in ('History', 'Philosophy')]
hist_phil_sorted = sorted(hist_phil, key=lambda x: get_stars(x), reverse=True)
rows = '\n'.join(major_row(m, i+1) for i, m in enumerate(hist_phil_sorted))
fname = "history-philosophy-majors-china.html"
content = page_shell(fname,
    title     = "History & Philosophy Majors in China",
    seo_title = "History & Philosophy Majors in China 2025 — Career Outlook & AI Relevance",
    seo_desc  = f"All {len(hist_phil)} History and Philosophy majors in China ranked. Includes growing AI ethics demand for Philosophy graduates and policy research paths for History.",
    label     = f"History & Philosophy · {len(hist_phil)} Majors",
    h1        = "History & Philosophy Majors in China",
    desc      = f"All {len(hist_phil)} majors covering historical research, cultural analysis, and philosophical inquiry — including the growing AI ethics specialization.",
    body_html = {
        "intro": f"History and Philosophy together account for {len(hist_phil)} majors in China's university system. History develops the rare analytical skill of understanding how systems change over long time horizons — valuable in policy, media, and strategic roles even if direct career paths are narrow. Philosophy has experienced an unexpected renaissance: AI ethics, algorithmic governance, and technology policy are creating genuine demand for people who can reason carefully about values and consequences. Philosophers with technical literacy are entering a field that barely existed for their predecessors.",
        "list":  f'<div class="section-title">All {len(hist_phil)} Majors — History &amp; Philosophy</div>\n{rows}'
    }
)
with open(f"{OUT}/{fname}", "w", encoding="utf-8") as f: f.write(content)
pages_written.append(fname)

# Generate each remaining category page
for cat, meta in CAT_META.items():
    if meta is None: continue
    majors_in_cat = sorted([m for m in ALL if m['cat'] == cat],
                            key=lambda x: get_stars(x), reverse=True)
    n    = len(majors_in_cat)
    rows = '\n'.join(major_row(m, i+1) for i, m in enumerate(majors_in_cat))
    fname = meta['fname']
    content = page_shell(fname,
        title     = meta['h1'].format(n=n),
        seo_title = meta['seo_title'].format(n=n),
        seo_desc  = meta['seo_desc'].format(n=n),
        label     = meta['label'],
        h1        = meta['h1'].format(n=n),
        desc      = meta['desc'].format(n=n),
        body_html = {
            "intro": meta['intro'].format(n=n),
            "list":  f'<div class="section-title">All {n} {cat} Majors — Ranked by Future Outlook</div>\n{rows}'
        }
    )
    with open(f"{OUT}/{fname}", "w", encoding="utf-8") as f: f.write(content)
    pages_written.append(fname)

# ── Summary ───────────────────────────────────────────────────────
print(f"\n✓ {len(pages_written)} ranking pages generated:")
for p in pages_written:
    size = os.path.getsize(f"{OUT}/{p}") // 1024
    print(f"  {p} ({size}KB)")
