#!/usr/bin/env python3
"""
Generate 757 individual major detail pages.
Layer 1: Unique title / meta / canonical per major
Layer 2: Subcategory-level pros / cons / careers / stars (88 subcategories)
Layer 3: AI Verdict paragraph — star-level opening + subcategory insight + AI-pick modifier
SEO+:   FAQ section (3 unique Q&A per major) + FAQ JSON-LD schema
"""
import json, re, os, unicodedata

with open("ordinarymantrying.com/tools/major-vote.html", encoding="utf-8") as f:
    src = f.read()

m  = re.search(r'const ALL\s*=\s*(\[.*?\]);', src, re.DOTALL)
ALL = json.loads(m.group(1))
m2 = re.search(r'const AIPICK\s*=\s*new Set\(\[(.*?)\]\)', src)
AIPICK = set(x.strip().strip('"') for x in m2.group(1).split(','))

# ═══════════════════════════════════════════════════════════════════
# LAYER 2 — Subcategory-level data (88 entries)
# Format: pros[3], cons[2], careers[3], stars(1-5)
# ═══════════════════════════════════════════════════════════════════
SUBCAT = {

  # ── Engineering ───────────────────────────────────────────────────
  'Advanced Engineering': {
    'pros':    ['At the frontier of quantum, photonics, and next-gen computing','Small cohort means less competition for top research roles','Strong pathway to national labs and elite graduate programs'],
    'cons':    ['Extremely high academic pressure and abstract coursework','Limited employers outside top-tier research institutions'],
    'careers': ['Quantum Computing Researcher','Photonics Engineer','Advanced Systems Scientist'],
    'stars': 4,
  },
  'Aerospace': {
    'pros':    ["China's space program is a national priority with guaranteed long-term funding",'Commercial aerospace expanding rapidly after regulatory opening','High starting salary in both state-owned and private aerospace firms'],
    'cons':    ['Most roles require security clearance limiting job mobility','Graduate numbers are growing while top-tier positions remain scarce'],
    'careers': ['Aerospace Engineer','Satellite Systems Specialist','Propulsion Engineer'],
    'stars': 4,
  },
  'Agricultural Engineering': {
    'pros':    ['Drone, sensor, and AI integration is modernizing this field fast','Government subsidies keep rural tech investment steady','Rare graduates with both engineering and farming domain knowledge'],
    'cons':    ['Salary lags urban tech roles significantly','Perceived lower prestige versus pure CS or EE paths'],
    'careers': ['Precision Agriculture Engineer','AgTech Product Developer','Farm Automation Specialist'],
    'stars': 3,
  },
  'Architecture': {
    'pros':    ['Generative AI as a design tool expands what one architect can deliver','Green building standards creating sustained retrofit and new-build demand','Cross-disciplinary skills valued in urban planning and real estate'],
    'cons':    ['Real estate market slowdown has reduced domestic project volume','Long path to licensure with uncertain income in early career'],
    'careers': ['Architect','Urban Designer','BIM Specialist'],
    'stars': 3,
  },
  'Automation': {
    'pros':    ['Industrial robot density in China is rising every year, all need automation engineers','Graduates enter both manufacturing and software-defined control systems','Core skill set transferable across automotive, electronics, and energy sectors'],
    'cons':    ['Requires strong mathematics and coding skills to stay competitive','Entry-level roles often in factory settings with limited flexibility'],
    'careers': ['Automation Engineer','Robotics Systems Integrator','Industrial IoT Specialist'],
    'stars': 4,
  },
  'Biomedical Engineering': {
    'pros':    ['Medical device industry is growing fast to serve aging population','AI diagnostics creating entirely new product categories requiring this skill set','Strong crossover demand from both tech companies and hospitals'],
    'cons':    ['Requires depth in both biology and engineering — a difficult combination to master','Regulatory approval cycles make product timelines very long'],
    'careers': ['Medical Device Engineer','Clinical Systems Analyst','Health AI Product Manager'],
    'stars': 4,
  },
  'Chem Engineering & Pharmacy': {
    'pros':    ['Battery chemistry and specialty chemicals are national strategic priorities','Pharmaceutical manufacturing is scaling rapidly for domestic and export markets','Recession-resistant: chemicals and drugs are always needed'],
    'cons':    ['Physically demanding lab and plant work in early career','Chemical plant accidents create public perception and safety pressures'],
    'careers': ['Process Engineer','Pharmaceutical Production Specialist','Battery Materials Researcher'],
    'stars': 3,
  },
  'Civil Engineering': {
    'pros':    ['BIM and AI-assisted structural design increasing graduate productivity','Maintenance of existing infrastructure creates steady work beyond new construction','International projects — Belt and Road — create overseas opportunities'],
    'cons':    ['Domestic construction market has peaked in many coastal cities','On-site work conditions and hours are demanding in project phases'],
    'careers': ['Structural Engineer','Project Manager','Infrastructure Planner'],
    'stars': 3,
  },
  'Computer Science': {
    'pros':    ['Highest industry salary ceiling among all Chinese university majors','AI, cloud, and cybersecurity demand outpacing graduate supply at senior levels','Skills are globally portable with minimal friction'],
    'cons':    ['Entry-level market is crowded — a CS degree alone no longer guarantees a top job','Continuous learning requirement is non-negotiable: what you know today may be obsolete in 3 years'],
    'careers': ['Software Engineer','AI/ML Engineer','Cloud Architect'],
    'stars': 5,
  },
  'Electrical Engineering': {
    'pros':    ['EV industry, smart grid, and renewable energy all require electrical engineers','Cross-industry: power, automotive, and consumer electronics all hire','Strong foundation for graduate study in power electronics or power systems'],
    'cons':    ['Power grid work often involves shift work and field postings','Salary ramp is slower than software in early career'],
    'careers': ['Power Systems Engineer','EV Electrical Engineer','Smart Grid Specialist'],
    'stars': 4,
  },
  'Electronic Information': {
    'pros':    ['Semiconductor self-sufficiency is a national mission — enormous funding behind it','Chipset design, RF engineering, and signal processing all critically needed','Strong research collaboration between universities and state chip firms'],
    'cons':    ['US export controls are reshaping the competitive landscape unpredictably','Cutting-edge IC design requires a very long learning curve'],
    'careers': ['IC Design Engineer','RF Communications Engineer','Embedded Systems Developer'],
    'stars': 5,
  },
  'Energy & Power': {
    'pros':    ['Carbon neutrality 2060 is a legally binding commitment — long funding horizon','Nuclear, hydrogen, and wind all expanding simultaneously','Global energy transition means skills are internationally valued'],
    'cons':    ['State-owned enterprise culture dominates — slower promotion paths','Many positions in remote locations near power infrastructure'],
    'careers': ['Power Plant Engineer','Renewable Energy Analyst','Nuclear Systems Engineer'],
    'stars': 4,
  },
  'Environmental Engineering': {
    'pros':    ['Environmental compliance legally mandated and enforcement tightening','Carbon trading market creating new specialist roles in monitoring and verification','Cross-border demand: environmental consultancies work internationally'],
    'cons':    ['Government work often pays less than tech despite similar education requirements','Regulatory environments change with political priorities'],
    'careers': ['Environmental Consultant','Carbon Credit Analyst','Pollution Control Engineer'],
    'stars': 3,
  },
  'Food Science & Engineering': {
    'pros':    ['Food safety is politically untouchable — demand is floor-protected','Plant-based proteins and functional foods are creating new R&D roles','Supply chain transparency technology is an emerging specialist area'],
    'cons':    ['Starting salaries are modest relative to other engineering fields','Consumer brand work can involve significant travel and field work'],
    'careers': ['Food Safety Engineer','R&D Food Scientist','Supply Chain Quality Manager'],
    'stars': 3,
  },
  'Forestry Engineering': {
    'pros':    ['Carbon credit valuation and ecological accounting are new specialist functions','Government afforestation programs ensure steady public sector demand','Drone and remote sensing integration is modernizing the field'],
    'cons':    ['Rural postings are common and relocation is often required','Career ceiling is lower than urban engineering disciplines'],
    'careers': ['Forestry Engineer','Carbon Accounting Specialist','Remote Sensing Analyst'],
    'stars': 3,
  },
  'Geology Engineering': {
    'pros':    ['Critical mineral exploration for lithium, cobalt, and rare earths is strategically vital','Graduates needed for both extraction site assessment and environmental remediation','International field work in Asia, Africa, and South America'],
    'cons':    ['Extensive field work in remote locations required','Physical demands are high and working conditions can be harsh'],
    'careers': ['Exploration Geologist','Mine Site Engineer','Environmental Remediation Specialist'],
    'stars': 3,
  },
  'Hydraulic Engineering': {
    'pros':    ['Water security is a long-term national priority with sustained budget allocation','Dam safety, flood control systems, and irrigation infrastructure all require specialists','AI-assisted hydrological modeling creating new technical roles'],
    'cons':    ['Work is heavily project-based with long field deployment periods','State-owned enterprise employment dominates, with slower private sector presence'],
    'careers': ['Hydraulic Engineer','Water Resource Planner','Flood Control Specialist'],
    'stars': 3,
  },
  'Instrumentation': {
    'pros':    ['Precision equipment is essential for advanced manufacturing and scientific research','Import substitution in high-end instrumentation is a national priority creating demand','Niche expertise means less competition than broader engineering fields'],
    'cons':    ['Very specialized knowledge makes lateral moves difficult','Market size is smaller than mainstream engineering disciplines'],
    'careers': ['Instrumentation Engineer','Metrology Specialist','Quality Assurance Engineer'],
    'stars': 3,
  },
  'Interdisciplinary Eng': {
    'pros':    ['Designed to fill emerging gaps like smart manufacturing, AI hardware, and green tech','Flexibility to work across multiple industries as specializations evolve','Often the newest programs with most modern curriculum'],
    'cons':    ['Employers sometimes unsure how to evaluate non-traditional degrees','Depth in any one area may be less than a specialized program'],
    'careers': ['Systems Integration Engineer','Emerging Tech Specialist','Cross-disciplinary R&D Researcher'],
    'stars': 3,
  },
  'Light Industry': {
    'pros':    ['Consumer goods manufacturing is upgrading toward premium and sustainable products','Packaging innovation, material efficiency, and circular design are growth areas','China remains the global manufacturing hub — scale creates volume of roles'],
    'cons':    ['Volume manufacturing roles face automation pressure','Salary ceiling is lower than high-tech engineering disciplines'],
    'careers': ['Product Design Engineer','Packaging Technology Specialist','Manufacturing Quality Manager'],
    'stars': 3,
  },
  'Materials Science': {
    'pros':    ['Battery materials, semiconductors, composites — all named national priority sectors','Every physical product depends on materials innovation','Strong research-to-industry pipeline with significant government R&D funding'],
    'cons':    ['Graduate career often starts in lab work with slow salary progression','Some specializations require years of research before commercial application'],
    'careers': ['Battery Materials Researcher','Semiconductor Process Engineer','Advanced Composites Specialist'],
    'stars': 4,
  },
  'Mechanical Engineering': {
    'pros':    ['Foundation for robotics, precision manufacturing, and smart factory design','Still one of the largest engineering employers in China by absolute headcount','Digital twin and simulation skills elevating the field beyond traditional machining'],
    'cons':    ['Many routine mechanical design tasks being automated or offshored','Manufacturing career paths often require factory floor postings'],
    'careers': ['Mechanical Engineer','Robotics Design Engineer','Manufacturing Systems Manager'],
    'stars': 3,
  },
  'Mechanics': {
    'pros':    ['Rigorous theoretical foundation valued in aerospace, defense, and research','Strong basis for graduate study in engineering disciplines','Niche expertise that AI tools currently cannot replicate easily'],
    'cons':    ['Narrow direct career paths outside research and academia','Industry application often requires supplementing with applied engineering skills'],
    'careers': ['Structural Mechanics Researcher','Aerospace Stress Analyst','Engineering R&D Specialist'],
    'stars': 3,
  },
  'Mining': {
    'pros':    ['EV transition has made critical mineral mining strategically essential','Salaries in overseas mining projects are significantly above average','Sustainable mining and environmental compliance creating new specialist roles'],
    'cons':    ['Environmental opposition to new mining projects is growing','Physical risk and remote locations are inherent to field work'],
    'careers': ['Mining Engineer','Critical Minerals Analyst','Mine Safety Specialist'],
    'stars': 3,
  },
  'Nuclear Engineering': {
    'pros':    ['China is building more nuclear reactors than any other country right now','Small graduate cohort means job security for qualified engineers is very high','Specialist salary premium is significant versus generalist engineering'],
    'cons':    ['Security clearance required limits portability to civilian roles','Public perception and political risks create project uncertainty'],
    'careers': ['Nuclear Reactor Engineer','Radiation Safety Specialist','Nuclear Fuel Systems Analyst'],
    'stars': 4,
  },
  'Ocean Engineering': {
    'pros':    ['Offshore wind installation is scaling rapidly along the Chinese coast','Deep-sea mineral and energy resources are long-term strategic investment areas','Marine data infrastructure and underwater robotics are emerging specializations'],
    'cons':    ['Offshore work involves extended sea deployments','Market size is smaller than land-based engineering disciplines'],
    'careers': ['Offshore Structural Engineer','Marine Systems Engineer','Ocean Data Scientist'],
    'stars': 3,
  },
  'Ordnance': {
    'pros':    ['Defense sector provides exceptional job stability and competitive compensation','Specialized knowledge that is genuinely rare and valued','Clear career progression within the military-industrial system'],
    'cons':    ['Career portability outside the defense sector is very limited','Requires political reliability background checks and restricted international travel'],
    'careers': ['Weapons Systems Engineer','Defense Technology Researcher','Military Equipment Analyst'],
    'stars': 3,
  },
  'Public Security Tech': {
    'pros':    ['Government employment with stable salary and benefits','AI-powered surveillance and forensics creating genuinely new technical roles','National demand is consistent regardless of economic cycles'],
    'cons':    ['Career is almost entirely within the public security apparatus','Limited private sector equivalents for most skills'],
    'careers': ['Security Technology Engineer','Forensic Systems Specialist','Emergency Response Technologist'],
    'stars': 3,
  },
  'Safety Engineering': {
    'pros':    ['Legally mandated safety compliance means demand is floor-protected','Industrial accidents create political and corporate urgency for specialists','AI-assisted risk monitoring is elevating the technical level of the work'],
    'cons':    ['Historically undercompensated relative to risk management value provided','Perception as a compliance function rather than a strategic role'],
    'careers': ['Safety Engineer','Risk Assessment Specialist','Industrial Hazard Consultant'],
    'stars': 3,
  },
  'Surveying & Mapping': {
    'pros':    ['GIS and spatial data are now infrastructure for smart cities, logistics, and autonomous driving','LiDAR, satellite imagery, and drone mapping are making this a high-tech field','Demand from government, logistics, and urban planning sectors simultaneously'],
    'cons':    ['Field data collection still requires physical site work','Commoditization of basic mapping services is compressing some entry-level roles'],
    'careers': ['GIS Specialist','Remote Sensing Analyst','Spatial Data Engineer'],
    'stars': 4,
  },
  'Textile': {
    'pros':    ['High-performance fabrics for medical, military, and sports use are a growth area','Sustainable textile and circular economy roles are expanding globally','China still produces the majority of the world\'s textile output — scale creates opportunities'],
    'cons':    ['Mass-market textile production is moving to lower-cost countries','Brand and design value accrues mostly to Western companies rather than Chinese manufacturers'],
    'careers': ['Technical Textile Engineer','Sustainable Materials Specialist','Textile Process Manager'],
    'stars': 2,
  },
  'Transportation': {
    'pros':    ['High-speed rail, smart highways, and metro expansion continue at scale','Autonomous vehicle infrastructure is an emerging engineering specialty','Aviation, maritime, and logistics all have active hiring pipelines'],
    'cons':    ['Many roles are in state-owned transport enterprises with bureaucratic structures','Infrastructure projects are often in less developed regions requiring relocation'],
    'careers': ['Transportation Systems Engineer','Traffic Data Analyst','Rail Infrastructure Specialist'],
    'stars': 3,
  },

  # ── Medicine ──────────────────────────────────────────────────────
  'Basic Medical Sciences': {
    'pros':    ['Strong research pathway into pharmaceutical R&D and biotech','Foundation for MD-PhD programs at leading universities','AI is expanding what researchers can do with genomic and clinical data'],
    'cons':    ['Direct clinical practice is not the typical outcome','Academic career path is long and competitive globally'],
    'careers': ['Biomedical Researcher','Pharmaceutical Scientist','Medical AI Data Analyst'],
    'stars': 4,
  },
  'Chinese Materia Medica': {
    'pros':    ['AI-assisted compound discovery is finding new applications for traditional herbs','WHO integration of TCM is opening international regulatory pathways','Growing wellness and nutraceutical market creating commercial applications'],
    'cons':    ['Western medicine skepticism in international markets can limit some export roles','Evidence requirements for clinical claims are increasing'],
    'careers': ['TCM Pharmacognosist','Natural Product Researcher','Herbal Medicine Quality Analyst'],
    'stars': 3,
  },
  'Clinical Medicine': {
    'pros':    ['AI assists diagnosis but does not replace physician judgment and patient relationships','Among the highest lifetime income potential of any Chinese degree','Career demand is structurally protected by licensing and practice requirements'],
    'cons':    ['8+ years of education and residency before independent practice','Mental and physical burnout risk is high in Chinese hospital settings'],
    'careers': ['Physician','Medical Specialist','Clinical Department Director'],
    'stars': 5,
  },
  'Dental Medicine': {
    'pros':    ['China has significantly fewer dentists per capita than comparable economies','Rising middle-class demand for cosmetic dentistry is growing the market fast','Private dental clinic ownership offers entrepreneurship pathway with high income ceiling'],
    'cons':    ['Long training path — 5 years undergraduate plus specialty training','High upfront equipment investment cost for private practice'],
    'careers': ['Dentist','Orthodontics Specialist','Dental Implant Surgeon'],
    'stars': 5,
  },
  'Forensic Medicine': {
    'pros':    ['Niche expertise with very low competition for qualified specialists','Stable government and judicial system employment','DNA analysis, toxicology, and digital forensics are modernizing the field'],
    'cons':    ['Emotionally demanding work with exposure to difficult circumstances','Career path is almost entirely within the public legal system'],
    'careers': ['Forensic Pathologist','Forensic Toxicologist','Legal Medicine Expert'],
    'stars': 3,
  },
  'Integrative Medicine': {
    'pros':    ['Combines the credibility of Western medicine with TCM practice breadth','Government policy explicitly supports integrative approaches in hospital settings','Growing international research interest in integrative oncology and pain management'],
    'cons':    ['Must develop genuine depth in two distinct medical traditions','Acceptance varies significantly across hospitals and regions'],
    'careers': ['Integrative Medicine Physician','Clinical TCM-Western Hybrid Specialist','Integrative Health Researcher'],
    'stars': 3,
  },
  'Medical Technology': {
    'pros':    ['Clinical laboratories, imaging, and diagnostics are expanding with healthcare coverage growth','Automation of basic lab work creating demand for technologists who manage AI systems','Steady demand growth without the extreme pressure of clinical medicine training'],
    'cons':    ['Income ceiling is lower than physician career paths','Shift work in hospital laboratory settings is common'],
    'careers': ['Clinical Laboratory Technologist','Medical Imaging Specialist','Pathology Lab Manager'],
    'stars': 3,
  },
  'Nursing': {
    'pros':    ['China faces a structural nursing shortage that is worsening with an aging population','Guaranteed employment in almost any city or region','Specialized nursing roles — ICU, oncology, geriatrics — carry significant salary premiums'],
    'cons':    ['Physical and emotional demands are very high, with high burnout rates','Starting salary is lower than many technical fields despite critical importance'],
    'careers': ['Registered Nurse','Specialized Care Nurse','Community Health Practitioner'],
    'stars': 4,
  },
  'Pharmacy': {
    'pros':    ['Clinical pharmacy in hospitals is expanding as medication management becomes more complex','Drug safety monitoring and pharmacovigilance are growing regulatory roles','AI-assisted drug discovery is creating R&D roles that blend pharmacy with data science'],
    'cons':    ['Retail pharmacy roles face margin pressure and AI prescription management','Salary growth is slower than engineering counterparts'],
    'careers': ['Clinical Pharmacist','Drug Safety Specialist','Pharmaceutical Regulatory Affairs Manager'],
    'stars': 3,
  },
  'Public Health': {
    'pros':    ['COVID investment in public health infrastructure will sustain increased funding for years','Epidemiology and disease surveillance are genuinely valued after the pandemic','International organizations — WHO, CDC, UNICEF — actively recruit public health graduates'],
    'cons':    ['Government-focused career path with limited private sector equivalents','Emergency response work requires rapid deployment under pressure'],
    'careers': ['Epidemiologist','Public Health Policy Analyst','Disease Surveillance Specialist'],
    'stars': 3,
  },
  'Trad. Chinese Medicine': {
    'pros':    ['Government policy mandates TCM integration in Chinese healthcare at every level','Growing international patient base for acupuncture and traditional therapies','Licensed practitioners can build private practice with direct patient relationships'],
    'cons':    ['Evidence-based medicine standards create friction for traditional practice claims','Earning trajectory is slower to ramp than Western clinical medicine'],
    'careers': ['TCM Physician','Acupuncturist','TCM Product Developer'],
    'stars': 3,
  },

  # ── Science ───────────────────────────────────────────────────────
  'Astronomy': {
    'pros':    ["China's FAST telescope and space telescope programs are creating domestic research roles",'Extremely selective programs mean those who get in have exceptional analytical training','Cross-training in computation and AI methods opens adjacent tech industry roles'],
    'cons':    ['Career paths in research are globally competitive with very few positions','Industry applications are indirect — almost no "astronomy jobs" outside academia or space agencies'],
    'careers': ['Astrophysicist','Space Agency Researcher','Data Scientist (from computational astronomy)'],
    'stars': 2,
  },
  'Atmospheric Sciences': {
    'pros':    ['Climate modeling and weather AI are high-investment areas for government and tech firms','Extreme weather forecasting is becoming a commercial product, not just a public service','International collaboration in climate science is active despite geopolitical tensions'],
    'cons':    ['Data-intensive field requires strong programming and mathematical skills','Career paths are concentrated in meteorological agencies and research institutions'],
    'careers': ['Meteorologist','Climate Data Scientist','Atmospheric Research Scientist'],
    'stars': 3,
  },
  'Biological Sciences': {
    'pros':    ['Genomics, gene editing, and cell therapy are globally high-investment fields','China is building biotech industrial parks with active hiring pipelines','Computational biology is merging with data science — strong career crossover potential'],
    'cons':    ['Research career path requires significant graduate education investment','Some research roles depend on government funding cycles'],
    'careers': ['Biotech Research Scientist','Genomics Data Analyst','Cell Therapy Development Specialist'],
    'stars': 4,
  },
  'Chemistry': {
    'pros':    ['Battery chemistry, catalyst design, and specialty chemicals are national priorities','Cross-industry demand from pharma, energy, and materials','Graduate school in chemistry opens doors to both academic and industry R&D careers'],
    'cons':    ['Lab-based work requires years of hands-on experience to become independently productive','Starting salary is modest without graduate credentials'],
    'careers': ['Materials Chemist','Pharmaceutical Chemist','Energy Storage Researcher'],
    'stars': 3,
  },
  'Geographic Sciences': {
    'pros':    ['GIS and remote sensing are now embedded in logistics, urban planning, and climate work','Autonomous vehicle mapping is a fast-growing commercial application','Satellite data analysis skills are highly valued in both government and private sectors'],
    'cons':    ['Commoditization of basic GIS services is compressing entry-level salaries','Field data collection remains part of the work despite digital advances'],
    'careers': ['GIS Analyst','Remote Sensing Specialist','Urban Data Scientist'],
    'stars': 3,
  },
  'Geology': {
    'pros':    ['Critical mineral supply chains for EV and semiconductor industries are geologically determined','Environmental site assessment and remediation are growing legal requirements for businesses','Geospatial and 3D modeling skills bridge geology with high-tech industries'],
    'cons':    ['Field season work requires extended periods in remote locations','Academic and industry paths diverge sharply after undergraduate study'],
    'careers': ['Exploration Geologist','Hydrogeologist','Environmental Site Assessor'],
    'stars': 3,
  },
  'Geophysics': {
    'pros':    ['Seismic interpretation for oil, gas, and carbon storage is AI-transforming','Earthquake early warning systems are a public safety priority with government funding','Strong computational foundation that bridges to data science careers'],
    'cons':    ['Strongly tied to energy industry cycles — particularly oil and gas prices','Field seismic surveys involve remote deployment'],
    'careers': ['Geophysicist','Seismic Data Interpreter','Earthquake Risk Analyst'],
    'stars': 3,
  },
  'Mathematics': {
    'pros':    ['ML, cryptography, optimization, and statistical modeling all begin with mathematics','Finance, tech, and consulting all actively recruit strong mathematics graduates','The most fundamental transferable analytical skill set — depreciates slowest of any discipline'],
    'cons':    ['Pure mathematics career paths outside academia are narrow without a second specialization','Applied roles require additional technical skills — programming, domain knowledge'],
    'careers': ['Quantitative Analyst','Machine Learning Researcher','Actuarial Scientist'],
    'stars': 4,
  },
  'Ocean Sciences': {
    'pros':    ['China\'s maritime ambitions and offshore energy investments create sustained research funding','Climate-ocean interaction is a high-priority research area internationally','Underwater robotics and autonomous ocean monitoring are emerging commercial areas'],
    'cons':    ['Research careers dominate — commercial applications are still developing','Ship and field deployments require extended time away from home'],
    'careers': ['Oceanographer','Marine Data Scientist','Offshore Resource Specialist'],
    'stars': 3,
  },
  'Physics': {
    'pros':    ['Quantum computing is China\'s most heavily funded scientific moonshot','Photonics and semiconductor physics underpin the chip independence strategy','Physics training provides the strongest analytical foundation across all of science'],
    'cons':    ['Theoretical physics career path is extremely competitive globally','Industry transition usually requires graduate training in applied areas'],
    'careers': ['Quantum Computing Researcher','Semiconductor Physicist','Scientific Instrument Engineer'],
    'stars': 4,
  },
  'Psychology': {
    'pros':    ['Mental health awareness is rising rapidly in Chinese society — demand is real and growing','Employee wellbeing roles in large corporations are expanding','AI behavioral tools are creating product design roles that blend psychology with technology'],
    'cons':    ['Clinical practice requires post-graduate qualification and supervised hours','Salary is relatively low in the early career phase'],
    'careers': ['Clinical Psychologist','Organizational Behavior Consultant','UX Research Specialist'],
    'stars': 3,
  },
  'Statistics': {
    'pros':    ['The mathematical foundation of data science, ML, and evidence-based policy','Statisticians who can communicate clearly are scarce and highly valued','Applicable across healthcare, finance, government, and technology sectors simultaneously'],
    'cons':    ['Roles often described as "data analyst" rather than "statistician" — requires rebranding for job search','Competition from CS graduates in data roles is intense'],
    'careers': ['Biostatistician','Data Scientist','Quantitative Risk Analyst'],
    'stars': 4,
  },

  # ── Economics ─────────────────────────────────────────────────────
  'Economics': {
    'pros':    ['Develops rigorous analytical thinking applicable across finance, policy, and strategy','Strong foundation for MBA or graduate economics programs','International organizations actively recruit economics graduates for policy roles'],
    'cons':    ['A generalist degree in an era that rewards specialists — second skill is essential','Entry-level analyst roles are increasingly going to data-skilled candidates'],
    'careers': ['Economic Policy Analyst','Strategy Consultant','Development Finance Specialist'],
    'stars': 3,
  },
  'Finance': {
    'pros':    ['Highest starting and ceiling salary of any economics-family discipline','Investment banking, asset management, and fintech all actively recruit','Strong quantitative finance skills are globally portable credentials'],
    'cons':    ['AI is automating credit scoring, basic analysis, and routine trading','Competition for front-office roles is intense — top schools dominate placement'],
    'careers': ['Investment Analyst','Risk Manager','Fintech Product Manager'],
    'stars': 3,
  },
  'Intl Economics & Trade': {
    'pros':    ['Cross-border compliance and export control expertise is newly in demand','Belt and Road project management creating roles for those with trade and language skills','International trade law knowledge is increasingly valuable in an era of sanctions and tariffs'],
    'cons':    ['Geopolitical tensions are reshaping trade flows — some specializations are at risk','Straightforward import/export roles face automation from customs AI'],
    'careers': ['Trade Compliance Specialist','International Market Analyst','Export Control Consultant'],
    'stars': 3,
  },
  'Public Finance': {
    'pros':    ['Stable government employment across all levels of administration','Tax reform and fiscal policy work is driven by policy change — steady demand','Bond market and municipal finance roles expanding with government debt management needs'],
    'cons':    ['Salary ceiling is determined by government rank — limited upside','Private sector equivalent roles are narrower than in general finance'],
    'careers': ['Government Budget Analyst','Fiscal Policy Advisor','Tax Administration Specialist'],
    'stars': 3,
  },

  # ── Education ─────────────────────────────────────────────────────
  'Education': {
    'pros':    ['Government teacher employment is one of the most stable careers in China','AI tools expanding what individual teachers can prepare and deliver','Growing EdTech industry creating corporate roles for education professionals'],
    'cons':    ['Salary ceiling below comparable private sector roles with similar education','Administrative workload and parental pressure are high in Chinese school system'],
    'careers': ['Teacher','Curriculum Developer','EdTech Product Specialist'],
    'stars': 3,
  },
  'Physical Education': {
    'pros':    ['Fitness and wellness industry growing alongside health consciousness in urban China','Sports medicine, athletic training, and performance analytics are specialist growth areas','PE graduates can build individual coaching practices with direct income control'],
    'cons':    ['School PE teaching is stable but low-ceiling','Physical demands limit career longevity in performance-focused roles'],
    'careers': ['PE Teacher','Athletic Performance Coach','Sports Health Manager'],
    'stars': 3,
  },

  # ── History ───────────────────────────────────────────────────────
  'History': {
    'pros':    ['Develops the rarest analytical skill: understanding long-term systemic change','Valued in policy institutes, media, and cultural institutions','Archival and museum management careers are small but stable government roles'],
    'cons':    ['Direct commercial applications are narrow — a second skill is essential','Academic positions are scarce and extremely competitive'],
    'careers': ['Historical Researcher','Policy Institute Analyst','Museum Curator'],
    'stars': 2,
  },

  # ── Law ───────────────────────────────────────────────────────────
  'Ethnology': {
    'pros':    ['Policy work on ethnic minority affairs and cultural preservation','Academic positions in anthropology and cultural studies','Specialized knowledge with very low competition for qualified candidates'],
    'cons':    ['Career paths are almost entirely academic or government cultural institutions','Extremely small field limiting networking and advancement options'],
    'careers': ['Ethnology Researcher','Cultural Affairs Officer','Minority Policy Analyst'],
    'stars': 2,
  },
  'Law': {
    'pros':    ['AI handles document review — lawyers handle judgment, negotiation, and courtroom advocacy','Regulatory complexity is growing, not shrinking — compliance roles expanding','International commercial law is a high-value specialization with global application'],
    'cons':    ['Bar examination pass rates are low — professional entry is genuinely hard','Routine legal work — contracts, discovery — is being automated steadily'],
    'careers': ['Corporate Lawyer','Legal Compliance Specialist','International Arbitration Counsel'],
    'stars': 3,
  },
  'Marxist Theory': {
    'pros':    ['Explicitly valued for party, government, and university administrative roles','Political reliability within the system is a genuine career asset','Graduate programs in Marxist theory are heavily subsidized by the state'],
    'cons':    ['Career scope is defined entirely by the institutional system — no private sector equivalent','International career portability is essentially zero'],
    'careers': ['Party School Lecturer','Government Policy Researcher','University Political Affairs Staff'],
    'stars': 3,
  },
  'Political Science': {
    'pros':    ['Think tanks, international organizations, and government policy offices all recruit','Strong foundation for diplomatic service examination','International relations expertise is in demand given geopolitical complexity'],
    'cons':    ['Civil service examination is highly competitive for top-tier positions','Academic career path is globally competitive with limited domestic placement'],
    'careers': ['Policy Analyst','Diplomatic Affairs Officer','International Relations Researcher'],
    'stars': 3,
  },
  'Public Security': {
    'pros':    ['Direct pipeline into police, border control, and public safety agencies','Stable salary, benefits, and clear promotion structure','Growing technical roles in cybercrime, digital forensics, and smart surveillance'],
    'cons':    ['Career is almost entirely within the public security system','Physical demands and shift work are inherent'],
    'careers': ['Police Officer','Criminal Investigation Specialist','Cybercrime Investigator'],
    'stars': 3,
  },
  'Sociology': {
    'pros':    ['Social research skills in demand as organizations build diversity, equity, and social impact functions','AI behavioral data analysis is creating new applied sociology roles','NGO, think tank, and international organization careers are viable paths'],
    'cons':    ['Low starting salary in most direct sociology roles','Commercial employers often prefer economics or psychology graduates for similar roles'],
    'careers': ['Social Researcher','Corporate Social Responsibility Specialist','Community Development Officer'],
    'stars': 2,
  },

  # ── Literature ────────────────────────────────────────────────────
  'Chinese Language & Lit': {
    'pros':    ['Content creation economy is large and growing — narrative and editorial skills are valued','Teaching and academic paths remain stable even as industry evolves','Cultural consulting, screenwriting, and publishing are creative career paths with real demand'],
    'cons':    ['AI writing tools are direct competition for generic content production','Income variance is high — top earners succeed, median outcomes are modest'],
    'careers': ['Content Strategist','Editor','Screenwriter / Cultural Consultant'],
    'stars': 2,
  },
  'Foreign Languages': {
    'pros':    ['Domain-specialized translation — legal, medical, technical — resists AI commoditization','Diplomatic service, international business, and overseas Chinese enterprise roles all require language skills','Language paired with subject expertise commands significant salary premium'],
    'cons':    ['AI translation handles routine tasks with increasing accuracy — commodity translation is at risk','104 majors in this category means fierce competition for the same roles'],
    'careers': ['Technical / Legal Interpreter','International Business Manager','Language Technology Specialist'],
    'stars': 2,
  },
  'Journalism & Comm': {
    'pros':    ['Data journalism, investigative reporting, and visual storytelling are human-judgment intensive','New media and social content creation are growth industries','Brand communication and PR roles are expanding in corporate China'],
    'cons':    ['Traditional media employment is declining rapidly','Routine content production and basic reporting are being AI-automated'],
    'careers': ['Data Journalist','Content Strategy Director','Brand Communications Manager'],
    'stars': 2,
  },

  # ── Management ────────────────────────────────────────────────────
  'Agricultural Management': {
    'pros':    ['Rural revitalization is a national policy priority with dedicated funding','Agribusiness supply chain management requires rare domain expertise','E-commerce for agricultural products is growing fast and needs specialized managers'],
    'cons':    ['Roles often require willingness to work in rural or semi-rural settings','Income ceiling is lower than urban management disciplines'],
    'careers': ['Agribusiness Manager','Rural Development Officer','Agricultural Supply Chain Director'],
    'stars': 3,
  },
  'Business Administration': {
    'pros':    ['Universal credential recognized across all industries and company sizes','Strong pathway to MBA programs and general management tracks','Entrepreneurship is a real and accessible path from this degree'],
    'cons':    ['Most generalist management credential on the market — differentiation requires effort','Technical specialists often outcompete MBA generalists for data-driven management roles'],
    'careers': ['Business Development Manager','Operations Director','Entrepreneur / Startup Founder'],
    'stars': 3,
  },
  'E-Commerce': {
    'pros':    ['China\'s e-commerce market is the world\'s largest and most sophisticated','Logistics, live commerce, and cross-border e-commerce are all expanding','Strong quantitative skills in this field — analytics, conversion, and user behavior'],
    'cons':    ['Industry moves fast — skills learned today may be obsolete in 3 years','Platform dependence creates career fragility if major platforms change algorithms or policies'],
    'careers': ['E-Commerce Operations Manager','Cross-Border Trade Specialist','Digital Marketing Analyst'],
    'stars': 3,
  },
  'Industrial Engineering': {
    'pros':    ['Efficiency optimization in manufacturing is permanently valuable','Simulation and digital twin skills are bridging IE to tech industry roles','Lean operations and supply chain design are globally recognized specializations'],
    'cons':    ['Factory floor time is required to build credibility — not desk-only work','Some traditional IE roles are being automated by smart factory systems'],
    'careers': ['Industrial Engineer','Supply Chain Optimization Specialist','Smart Manufacturing Consultant'],
    'stars': 3,
  },
  'Library & Info Management': {
    'pros':    ['Digital knowledge management, ontology design, and information architecture are growing areas','Government and university library systems provide stable public sector employment','Data governance and enterprise knowledge management are corporate equivalents'],
    'cons':    ['Traditional library roles are declining in headcount as digitalization advances','Salary is modest relative to education requirements in most roles'],
    'careers': ['Knowledge Management Specialist','Digital Archivist','Information Architecture Consultant'],
    'stars': 2,
  },
  'Logistics Management': {
    'pros':    ['Supply chain resilience is now a national security concern — sustained government attention','Cross-border logistics and cold chain management are specialist growth areas','Strong quantitative skills — route optimization, warehouse analytics — are genuinely valued'],
    'cons':    ['Autonomous vehicle and drone logistics will automate some operational roles over time','Shift work and physical coordination roles are demanding'],
    'careers': ['Supply Chain Manager','Logistics Analytics Specialist','Cross-Border Operations Director'],
    'stars': 3,
  },
  'Management Sci & Eng': {
    'pros':    ['Sits at the intersection of data analysis and organizational decision-making','Applicable in tech companies, consulting, and government policy equally','Strong quantitative training differentiates from pure management graduates'],
    'cons':    ['Title is unfamiliar to many employers — requires clear positioning in job search','Competition from both technical engineers and MBA graduates for similar roles'],
    'careers': ['Operations Research Analyst','Management Consultant','Data-Driven Strategy Manager'],
    'stars': 3,
  },
  'Public Administration': {
    'pros':    ['Civil service examination is the primary credential path — stable and structured','Government career progression is clear and protected from market forces','Policy implementation at local and national levels is an impactful and stable role'],
    'cons':    ['Private sector salary typically exceeds government pay at equivalent experience','Career advancement is slow and seniority-driven in Chinese bureaucracy'],
    'careers': ['Civil Servant','Urban Planning Official','Government Policy Manager'],
    'stars': 3,
  },
  'Tourism Management': {
    'pros':    ['Post-pandemic recovery is driving domestic and outbound tourism growth','Experiential travel, cultural tourism, and eco-tourism are premium growth segments','Hotel management and travel platform roles offer clear international career paths'],
    'cons':    ['Industry is highly cyclical and volatile to external shocks','Hospitality work often involves irregular hours and weekend shifts'],
    'careers': ['Hotel General Manager','Tourism Product Developer','Travel Platform Operations Manager'],
    'stars': 2,
  },

  # ── Agriculture ───────────────────────────────────────────────────
  'Animal Production': {
    'pros':    ['Precision livestock farming — sensor monitoring, AI feed optimization — is modernizing the industry','Food protein security is a permanent government concern','Veterinary science crossover skills increase career flexibility'],
    'cons':    ['Working conditions on production farms are physically demanding','Public perception of animal farming is increasingly scrutinized'],
    'careers': ['Livestock Production Manager','Animal Science Researcher','Precision Farming Specialist'],
    'stars': 3,
  },
  'Crop Production': {
    'pros':    ['Food security is a non-negotiable national priority — demand is floor-protected','Drone, GPS, and AI yield modeling are creating high-tech roles within agriculture','Seed technology and crop genetics are biotech-adjacent high-investment fields'],
    'cons':    ['Seasonal work cycles and rural postings are inherent to field roles','Salary lags urban technical equivalents significantly'],
    'careers': ['Crop Science Specialist','AgTech Field Agronomist','Precision Agriculture Data Analyst'],
    'stars': 3,
  },
  'Fisheries': {
    'pros':    ['Aquaculture supplies the majority of China\'s fish consumption — scale creates demand','Disease management and water quality monitoring are specialist skills with real scarcity value','Sustainable aquaculture certification is a growing export market requirement'],
    'cons':    ['Field work often involves remote coastal and offshore locations','Market consolidation is reducing the number of independent small-scale operators'],
    'careers': ['Aquaculture Manager','Fisheries Research Scientist','Water Quality Specialist'],
    'stars': 3,
  },
  'Forestry': {
    'pros':    ['Afforestation programs and carbon credit accounting are active government investment areas','Forest carbon monitoring using satellite data is an emerging tech-adjacent role','Sustainable timber certification creates international trade compliance roles'],
    'cons':    ['Career paths are largely public sector and rural-based','Salary is below comparable urban technical roles'],
    'careers': ['Forest Carbon Analyst','Ecological Restoration Specialist','Timber Certification Officer'],
    'stars': 3,
  },
  'Grassland Science': {
    'pros':    ['Desertification control and grassland restoration are long-term national ecological priorities','Carbon sequestration in grassland ecosystems is an emerging measurement specialty','Small cohort means genuine specialist status with limited competition'],
    'cons':    ['Highly niche field with limited career mobility outside government programs','Rural and remote postings are the norm'],
    'careers': ['Grassland Ecologist','Desertification Control Specialist','Rangeland Manager'],
    'stars': 2,
  },
  'Nature Conservation & Ecology': {
    'pros':    ['Biodiversity protection is receiving serious policy investment for the first time in Chinese history','International conservation NGOs actively recruit Chinese ecologists','Ecological services valuation and natural capital accounting are growing specialist areas'],
    'cons':    ['Academic research funding cycles can be unpredictable','Many roles require willingness to work in national parks and remote natural reserves'],
    'careers': ['Conservation Ecologist','Natural Capital Analyst','National Reserve Manager'],
    'stars': 3,
  },
  'Veterinary Medicine': {
    'pros':    ['Pet economy is booming — Chinese households are buying more pets than ever before','Clinical veterinary services are chronically understaffed in urban areas','Food animal inspection and disease control are government-backed stable roles'],
    'cons':    ['Long training path with clinical licensure requirements','Physical demands of large animal practice are significant'],
    'careers': ['Companion Animal Veterinarian','Food Safety Inspection Veterinarian','Animal Disease Control Officer'],
    'stars': 4,
  },

  # ── Philosophy ────────────────────────────────────────────────────
  'Philosophy': {
    'pros':    ['AI ethics, algorithmic fairness, and AI governance are genuine and growing career specializations','Technology companies are actively hiring ethicists and policy philosophers','Logical rigor from philosophy training is directly applicable in law, strategy, and research'],
    'cons':    ['Traditional academic philosophy positions are scarce and intensely competitive','Most philosophy graduates must translate their skills into adjacent roles to find stable income'],
    'careers': ['AI Ethics Researcher','Policy Analyst','Technology Governance Specialist'],
    'stars': 3,
  },
}

DEFAULT_SUBCAT = {
  'pros':    ['Focused expertise that creates genuine specialization value','Increasingly supported by AI tools that expand individual productivity','Clear credential pathway recognized by employers in the field'],
  'cons':    ['Competitive entry into top roles within this discipline','Continuous learning required to stay current as the field evolves'],
  'careers': ['Field Specialist','Technical Consultant','Research Analyst'],
  'stars':   3,
}

# ═══════════════════════════════════════════════════════════════════
# LAYER 3 — AI Verdict
# ═══════════════════════════════════════════════════════════════════
STAR_OPEN = {
  5: "This is one of the strongest bets you can make for 2029 and beyond.",
  4: "This major stands on solid ground and has genuine momentum heading into the AI era.",
  3: "This field offers a stable foundation, though the outcome will depend heavily on how you specialize.",
  2: "This major carries real risk in the current environment and demands a clear strategy to stand out.",
  1: "Entering this field today requires honest thought — the headwinds are strong and AI is reshaping the landscape fast.",
}

SUB_INSIGHT = {
  'Advanced Engineering':          "This interdisciplinary frontier sits at the edge of what's possible — quantum systems, AI-hardware co-design, and next-generation computing. The number of people who can work here is small, and so are the entry requirements for tolerance of ambiguity.",
  'Aerospace':                     "China is investing heavily in space infrastructure, satellite networks, and commercial aviation — making this one of the few engineering fields where domestic demand is accelerating independently of global trends.",
  'Agricultural Engineering':      "Precision farming, drone-based crop management, and AI-powered soil sensing are transforming this field from manual labor to tech-driven operation. The gap between what farms need and what graduates can deliver is still wide.",
  'Architecture':                  "Design is shifting fast: generative AI can draft a building in minutes. The architects who will thrive are those who learn to direct AI tools rather than compete with them — and who understand climate-responsive design.",
  'Automation':                    "Industry 4.0 is not a future concept in China — it is already the reality in manufacturing hubs. Automation engineers are the people making factories smarter, and demand is outpacing supply.",
  'Biomedical Engineering':        "China's aging population and healthcare reform are driving a decade-long expansion in medical devices and digital health. This field sits at the intersection of two of the most funded sectors in the country.",
  'Chem Engineering & Pharmacy':   "Battery chemistry, specialty materials, and API manufacturing are all in high national demand. This field is less glamorous than software but more recession-proof than most.",
  'Civil Engineering':             "BIM software and AI-assisted structural analysis are changing what civil engineers need to know. The construction market is maturing, but infrastructure maintenance and smart cities are opening new work.",
  'Computer Science':              "The most direct on-ramp to the AI economy. Competition for top roles is intense, but the ceiling is higher than almost any other discipline — and the floor is still well above the national graduate average.",
  'Electrical Engineering':        "The energy transition to solar, wind, and EVs runs on electrical engineers. Smart grid design, power electronics, and EV charging infrastructure are all areas where China is investing at scale.",
  'Electronic Information':        "Semiconductors are a national strategic priority after export controls forced China to accelerate domestic chip development. The government is backing this field with money, policies, and patience.",
  'Energy & Power':                "China's 2060 carbon neutrality target means this field will receive policy support and funding for the next 35 years. Nuclear, hydrogen, wind, and solar all need specialized graduates.",
  'Environmental Engineering':     "China's green economy transition is legally mandated — environmental standards are rising every year. This field has shifted from a regulatory burden to a genuine growth industry.",
  'Food Science & Engineering':    "Food safety is a politically sensitive national priority. Graduates who combine food science with data analytics and supply chain thinking are in real demand.",
  'Forestry Engineering':          "Ecological restoration projects and China's carbon credit market are creating new technical roles that didn't exist five years ago. The field is small but policy-protected.",
  'Geology Engineering':           "The global scramble for lithium, cobalt, and rare earths puts geological engineers at the center of the EV supply chain story. This is not the old extraction industry — it is a strategic resource field.",
  'Hydraulic Engineering':         "Water security is one of China's most serious long-term infrastructure challenges. Dam safety, flood control, and water allocation systems all require sustained engineering investment.",
  'Instrumentation':               "Precision measurement underpins advanced manufacturing, and China's push for self-sufficiency in high-end equipment means this niche field has more support than its small size suggests.",
  'Interdisciplinary Eng':         "These emerging cross-disciplinary programs are designed to fill gaps that traditional departments cannot. The upside is flexibility; the downside is that employers sometimes don't know what to do with you.",
  'Light Industry':                "Consumer goods manufacturing is shifting toward sustainable materials and premium positioning. Graduates who combine product knowledge with design and supply chain skills have real options.",
  'Materials Science':             "Battery materials, high-performance composites, and semiconductor substrates are national priority sectors. This may be the most quietly impactful field in Chinese engineering right now.",
  'Mechanical Engineering':        "The foundational manufacturing discipline is evolving — robotics integration and digital twins are replacing drafting tables. Graduates who adapt to smart manufacturing will remain essential.",
  'Mechanics':                     "A theoretical engineering foundation that feeds aerospace, civil, and mechanical research. Career paths are narrower than applied fields, but research positions remain stable.",
  'Mining':                        "Critical minerals for EVs and batteries have revived interest in mining engineering. Environmental compliance and sustainable extraction are now core skills, not optional.",
  'Nuclear Engineering':           "China is building more nuclear reactors than any other country. This is a small, specialized field with very high barriers to entry and very stable government-backed demand.",
  'Ocean Engineering':             "Offshore wind installation, deep-sea mining exploration, and marine data infrastructure are all expanding. China's Blue Economy policy is a real funding driver for this field.",
  'Ordnance':                      "Defense and military-industrial careers offer exceptional stability and competitive pay, but come with strict political requirements and limited career portability outside the sector.",
  'Public Security Tech':          "Smart surveillance, forensic technology, and emergency systems are government-funded priorities. Employment is largely within the public security apparatus, which offers stability with limited flexibility.",
  'Safety Engineering':            "Workplace safety compliance is legally required and enforcement is tightening. This field has historically been undervalued relative to the actual risk management work it involves.",
  'Surveying & Mapping':           "GIS, LiDAR, and satellite remote sensing have transformed this field from physical measurement to spatial intelligence. Smart city planning, autonomous driving, and disaster response all need this expertise.",
  'Textile':                       "China's textile sector is upgrading from volume to value — high-performance fabrics, wearable tech, and sustainable materials are where the growth is. Traditional garment production is moving elsewhere.",
  'Transportation':                "High-speed rail, smart highways, and urban transit systems represent decades of sustained infrastructure investment. Autonomous vehicle infrastructure is the next wave coming into this field.",
  'Basic Medical Sciences':        "This is the research foundation of medicine — graduate careers are primarily in academic research or pharmaceutical R&D. Clinical practice is not the path here, but scientific discovery is.",
  'Chinese Materia Medica':        "TCM herbal medicine is growing both domestically and internationally, with active WHO recognition efforts. AI is being applied to identify new active compounds, making this an unexpectedly tech-adjacent field.",
  'Clinical Medicine':             "The longest and hardest path in medicine, and also the most stable. No AI model is performing surgery or making final diagnoses independently — judgment and hands remain essential.",
  'Dental Medicine':               "China has a significant shortage of qualified dentists relative to its population and rising middle-class expectations. The income ceiling here is among the highest in medicine.",
  'Forensic Medicine':             "A niche but essential field that operates within the legal system. Career paths are almost entirely government-based — which means stability and limited variation.",
  'Integrative Medicine':          "Combining Western clinical medicine with TCM is a distinctly Chinese specialty that has real institutional support. The global interest in integrative approaches is growing.",
  'Medical Technology':            "Clinical laboratories, imaging technology, and diagnostic equipment are expanding rapidly as healthcare coverage deepens in China. These roles are critical but less visible than physicians.",
  'Nursing':                       "China faces a structural nursing shortage that is getting worse as the population ages. This is one of the few fields where job security is essentially guaranteed and demand increases every year.",
  'Pharmacy':                      "AI-assisted drug discovery is transforming pharmaceutical R&D, but clinical pharmacists and drug safety specialists remain human-essential roles in hospitals and regulatory agencies.",
  'Public Health':                 "The COVID pandemic fundamentally changed how governments fund and staff public health systems. Epidemiology, disease surveillance, and health policy have become genuinely valued skills.",
  'Trad. Chinese Medicine':        "Government support for TCM is embedded in national policy, and international interest is growing. The field blends traditional practice with modern research methods.",
  'Astronomy':                     "One of the most intellectually demanding and career-narrow fields in science. The paths are academic research or space agency roles — both highly competitive globally.",
  'Atmospheric Sciences':          "Climate modeling, weather forecasting, and extreme weather prediction are all areas receiving increased government investment. AI is transforming what atmospheric scientists can do with data.",
  'Biological Sciences':           "Genomics, synthetic biology, and cell therapy are reshaping medicine and agriculture. China is investing heavily in biotech, and biology graduates who can work with computational tools are in demand.",
  'Chemistry':                     "The foundational science for materials, pharmaceuticals, and energy storage. Graduate paths are wide but the field is competitive — specializing in battery chemistry or catalysis opens high-demand doors.",
  'Geographic Sciences':           "Spatial data, GIS, and remote sensing have moved from niche tools to essential infrastructure for smart cities, logistics, and climate monitoring. This field is more digital than most people realize.",
  'Geology':                       "Resource exploration for critical minerals is driving renewed interest in geology. This is field work combined with geospatial data analysis — less romantic than it sounds, more important than it used to be.",
  'Geophysics':                    "Seismic data analysis for oil and gas exploration, carbon storage site assessment, and earthquake prediction are the main application areas. AI is making interpretation faster and more accurate.",
  'Mathematics':                   "The AI era has made mathematics more valuable, not less. Machine learning, cryptography, optimization, and statistical modeling all run on mathematical foundations.",
  'Ocean Sciences':                "Offshore energy, deep-sea mining, and marine ecosystem monitoring are all expanding. China's maritime ambitions make this field strategically relevant and funded.",
  'Physics':                       "Quantum computing is China's most heavily funded scientific moonshot. Physics graduates who move into quantum information or semiconductor research are entering a field with genuine long-term potential.",
  'Psychology':                    "Mental health awareness is growing rapidly in Chinese society, and institutional support for psychological services is expanding. AI tools are augmenting therapists, not replacing them.",
  'Statistics':                    "Statistical thinking underlies all of data science, machine learning, and evidence-based policy. Statisticians who can communicate findings clearly are among the most practically useful graduates in any field.",
  'Economics':                     "A powerful analytical foundation but increasingly a launching pad rather than a destination. The graduates who win combine economic thinking with a second specialization in finance, policy, or technology.",
  'Finance':                       "Algorithmic trading and AI-driven credit scoring are automating the routine parts of finance. The roles that remain and grow require judgment under uncertainty — risk management, investment strategy, and client relationships.",
  'Intl Economics & Trade':        "Global supply chain reshaping and geopolitical realignment are simultaneously disrupting and creating trade careers. Graduates who understand both economics and regulatory compliance are finding new demand.",
  'Public Finance':                "Government budget management, fiscal policy, and tax administration are stable career paths that AI is supporting but not replacing. The ceiling is determined more by government rank than market forces.",
  'Education':                     "AI teaching tools are augmenting what teachers can deliver, not replacing the relationship at the heart of learning. Educators who adopt AI for lesson design and adaptive assessment will be more effective and more employable.",
  'Physical Education':            "The fitness and wellness industry in China is growing rapidly. PE graduates who build careers in sports medicine, performance analytics, or sports tech have expanding options beyond school teaching.",
  'History':                       "Historical analysis develops a rare capability: understanding how systems and societies change over time. In an era of rapid disruption, this perspective is genuinely valuable in policy, media, and strategic roles.",
  'Ethnology':                     "A highly specialized academic field with limited career paths outside of research institutions and government cultural policy roles. Meaningful work here requires acceptance of a narrow professional world.",
  'Law':                           "AI is handling legal document review, contract analysis, and precedent research with growing accuracy. The lawyers who will thrive are those handling judgment, negotiation, courtroom work, and client relationships.",
  'Marxist Theory':                "This field is politically valued in China's academic and government systems, making it a stable path for roles within the party and state apparatus. The scope is defined by that institutional context.",
  'Political Science':             "Policy analysis, international relations, and government affairs are career paths with genuine demand — in government and in the growing number of think tanks and international organizations.",
  'Public Security':               "A direct pipeline into police services, border control, and public safety agencies. Stable employment, clear career progression, and political reliability requirements define this field.",
  'Sociology':                     "Social research skills are growing in demand as organizations try to understand behavior, inequality, and community dynamics. The rise of social data and AI-assisted analysis is giving sociologists new quantitative tools.",
  'Chinese Language & Lit':        "Content creation, copywriting, and media careers are expanding in the digital economy — but AI writing tools are genuine competition. Graduates who develop a distinctive voice and editorial judgment will find demand.",
  'Foreign Languages':             "AI translation is improving rapidly and already handles most routine translation tasks. The language graduates with futures are those who develop domain expertise — legal, medical, technical translation.",
  'Journalism & Comm':             "The media industry is in structural transition, but demand for skilled communicators has not disappeared — it has moved to data journalism, video production, and brand content strategy.",
  'Agricultural Management':       "Rural revitalization policy and the professionalization of China's agricultural supply chains are creating demand for managers who understand both farming and business.",
  'Business Administration':       "The broadest management credential means the most competition and the least differentiation. Success comes from pairing this degree with deep industry knowledge or technical skills.",
  'E-Commerce':                    "China has the world's largest e-commerce market and its digital commerce infrastructure continues to evolve. Graduates who combine operations knowledge with data analytics skills are finding consistent demand.",
  'Industrial Engineering':        "Factory efficiency, supply chain optimization, and lean operations are fields where engineering thinking and management judgment together are genuinely valuable — and in shorter supply than demand suggests.",
  'Library & Info Management':     "Digitalization is transforming what libraries and information institutions do. The field is evolving toward knowledge management, digital preservation, and information architecture.",
  'Logistics Management':          "Supply chain resilience has become a national security concern after COVID disruptions. Logistics managers with cross-border operations experience and data skills are in growing demand.",
  'Management Sci & Eng':          "This field sits at the intersection of quantitative methods and organizational management — producing graduates who can build systems, analyze data, and communicate findings to decision-makers.",
  'Public Administration':         "Government service remains one of the most stable career paths in China, and public administration provides the direct credential for civil service. The work is shaped by policy priorities more than market forces.",
  'Tourism Management':            "Post-pandemic recovery and the experiential economy are driving tourism growth, but the industry remains cyclical. Graduates who move into hospitality technology or travel data analytics have more stability.",
  'Animal Production':             "Food protein security and animal welfare standards are both rising concerns. Graduates combining animal science with data monitoring and precision feeding technology are finding a field that is modernizing fast.",
  'Crop Production':               "Precision agriculture — GPS-guided planting, drone spraying, AI yield prediction — is transforming this field. The government's food security mandate ensures sustained investment regardless of market cycles.",
  'Fisheries':                     "Aquaculture supplies most of China's fish consumption and is growing. Sustainable aquaculture practices and disease management are specialized skills with real scarcity value.",
  'Forestry':                      "China's massive afforestation programs and carbon credit market are creating sustained demand for forestry professionals. The field has evolved from timber harvesting to ecosystem services.",
  'Grassland Science':             "Ecological restoration on China's degraded grasslands is a government priority for food security and carbon sequestration. A small, specialized field with reliable policy backing.",
  'Nature Conservation & Ecology': "Biodiversity protection and ecosystem services are receiving serious policy attention. International conservation work and domestic natural reserve management are both real career paths.",
  'Veterinary Medicine':           "China's pet economy is booming — more urban households own pets than ever before, and clinical veterinary services are chronically understaffed. This is one of the most reliable demand stories in the field.",
  'Philosophy':                    "AI ethics, algorithmic fairness, and the governance of intelligent systems have created a genuine demand for people who can think clearly about values and consequences. Philosophers with technical literacy are entering a field that didn't exist for their predecessors.",
}

# ═══════════════════════════════════════════════════════════════════
# CONTENT DEPTH — What is X? + Future Outlook (88 subcategories)
# ~150 words each → page word count 600 → 1000+
# ═══════════════════════════════════════════════════════════════════
WHAT_IS = {
  # ── Engineering ───────────────────────────────────────────────────
  'Advanced Engineering':
    "Advanced Engineering programs sit at the intersection of multiple disciplines, exploring frontier technologies such as quantum systems, AI hardware co-design, and next-generation computing architectures. Students develop rigorous theoretical and experimental skills across physics, materials science, and complex systems design. These programs are typically small in cohort size and highly selective, designed for students who want to work at the very edge of what engineering can currently achieve. Graduates are prepared for elite research roles in national laboratories, university research centers, and the handful of firms operating at this level of technical frontier.",

  'Aerospace':
    "Aerospace Engineering covers the design, development, and testing of aircraft, spacecraft, satellites, and propulsion systems. Students study aerodynamics, structural mechanics, orbital mechanics, and materials science with applications across commercial aviation, military systems, and space exploration. The curriculum combines deep physics foundations with hands-on systems engineering practice. China's rapidly expanding aerospace sector — spanning state programs, commercial launch companies, and a growing satellite industry — makes this one of the most strategically funded engineering disciplines available to Chinese students today.",

  'Agricultural Engineering':
    "Agricultural Engineering applies engineering principles to farming systems, rural infrastructure, and food production technology. Students study mechanization, irrigation design, agricultural machinery, soil-water management, and increasingly, precision farming technologies including drone systems, GPS-guided equipment, and AI-powered crop monitoring platforms. The field bridges traditional agricultural science with modern engineering practice. As China accelerates the modernization of its farming sector — both to improve food security and to reduce the rural-urban productivity gap — agricultural engineers are becoming central to that transformation.",

  'Architecture':
    "Architecture combines structural engineering knowledge with design thinking, environmental science, and urban planning theory. Students learn building systems, materials, construction methods, and spatial design principles alongside emerging skills in parametric modeling, building information modeling, and AI-assisted design tools. The field spans residential projects, commercial buildings, civic infrastructure, and large-scale urban masterplanning. With growing policy emphasis on green buildings, climate-resilient design, and sustainable urban development, architecture is evolving rapidly from a craft-based discipline into a data-informed practice.",

  'Automation':
    "Automation Engineering focuses on the design, integration, and control of automated systems — from industrial robots and programmable logic controllers to intelligent manufacturing lines and autonomous vehicles. Students study control theory, embedded systems, robotics, and systems programming. The discipline is central to China's transition toward advanced manufacturing, as factories replace manual assembly with precision automated systems. Graduates work across automotive, electronics, consumer goods, and logistics industries, designing and maintaining the intelligent infrastructure that defines modern production.",

  'Biomedical Engineering':
    "Biomedical Engineering applies engineering methods and principles to challenges in medicine and healthcare. Students study medical imaging systems, diagnostic devices, prosthetics, biosensors, biomechanics, and health information technology, developing skills that bridge clinical needs with engineering solutions. The field prepares graduates to work in medical device companies, hospital technology departments, and health AI startups. As China's healthcare system expands to serve an aging population, and as AI-powered diagnostics reshape clinical workflows, biomedical engineers are increasingly central to how care is delivered.",

  'Chem Engineering & Pharmacy':
    "Chemical Engineering and Pharmacy covers the industrial processes behind chemical production, pharmaceutical manufacturing, and advanced materials synthesis. Students study chemical reaction engineering, thermodynamics, process control, separation technology, and pharmaceutical formulation. The curriculum connects fundamental chemistry to large-scale industrial application. Graduates work in industries that are foundational to modern life — battery and specialty chemical manufacturing, pharmaceutical supply chains, food processing, and the materials companies producing the inputs that every other industry depends on.",

  'Civil Engineering':
    "Civil Engineering is responsible for the design, construction, and maintenance of the physical infrastructure of society — including roads, bridges, buildings, tunnels, dams, and water supply systems. Students study structural mechanics, soil engineering, hydraulics, transportation systems, and increasingly, digital tools such as building information modeling and AI-assisted structural analysis. The field underpins how cities and economies function at a fundamental level. While new construction is maturing in China's major cities, maintenance of existing infrastructure and smart city development continue to generate sustained demand for civil engineers.",

  'Computer Science':
    "Computer Science is the study of algorithms, data structures, programming languages, software systems, artificial intelligence, and the mathematical foundations of computing. Students develop skills in software engineering, machine learning, systems design, databases, networks, and human-computer interaction. The discipline is the intellectual foundation of the modern digital economy. In an era where software is embedded in healthcare, finance, manufacturing, and government, computer science graduates are among the most versatile and in-demand professionals globally — with career paths that range from product development to research to entrepreneurship.",

  'Electrical Engineering':
    "Electrical Engineering covers the generation, transmission, conversion, and application of electrical energy, alongside the design of electrical systems and components. Students study circuit theory, power electronics, electromagnetic fields, signal processing, and control systems. The field spans power generation, smart grid design, electric vehicle systems, and consumer electronics. China's energy transition — including the world's largest EV market and rapid renewable energy expansion — is creating sustained new demand for electrical engineers who can design the systems that move, store, and manage electricity efficiently.",

  'Electronic Information':
    "Electronic Information Engineering focuses on the design, testing, and application of electronic systems for communications, computing, and signal processing. Students study semiconductor physics, integrated circuit design, digital communications, microprocessor architecture, and embedded systems development. With China making semiconductor self-sufficiency a national strategic priority — backed by significant government investment and policy support — electronic information engineers are entering a field where domestic demand is being actively created at scale, independent of global market dynamics.",

  'Energy & Power':
    "Energy and Power Engineering covers the generation, conversion, storage, and distribution of energy from conventional and emerging sources including thermal, nuclear, wind, solar, and hydrogen systems. Students study thermodynamics, fluid mechanics, combustion engineering, power plant design, and energy system optimization. China's binding commitment to carbon neutrality by 2060 is driving decades of sustained transformation across the entire energy sector. This means nuclear construction, offshore wind installation, hydrogen infrastructure, and grid modernization will all require steady cohorts of energy engineers for the foreseeable future.",

  'Environmental Engineering':
    "Environmental Engineering applies scientific and engineering principles to the protection of air quality, water resources, and soil integrity, while managing the environmental impacts of industry and urban development. Students study water and wastewater treatment, air pollution control, solid waste management, environmental monitoring, and regulatory compliance systems. As China's environmental standards continue to rise and enforcement becomes more rigorous, environmental engineers are transitioning from peripheral compliance roles into genuinely strategic functions within major corporations, governments, and infrastructure projects.",

  'Food Science & Engineering':
    "Food Science and Engineering applies chemistry, biology, and engineering principles to the production, processing, packaging, preservation, and safety assurance of food products. Students study food chemistry, microbiology, food processing technology, packaging systems, and quality management. The field is directly connected to one of China's most politically sensitive policy areas — food safety — which has received significant regulatory and research investment following high-profile incidents. Graduates work across food manufacturing, supply chain management, regulatory agencies, and a growing functional food and nutrition innovation sector.",

  'Forestry Engineering':
    "Forestry Engineering combines forest science with engineering methods for the sustainable management, processing, and conservation of forest ecosystems. Students study silviculture, forest management systems, wood science and technology, forest road engineering, and increasingly, remote sensing technologies used for ecological monitoring and carbon accounting. China's major afforestation programs — planting billions of trees as part of its ecological restoration agenda — and the development of a domestic carbon credit market are creating new technical roles within a field that is evolving well beyond traditional timber production.",

  'Geology Engineering':
    "Geology Engineering applies geological knowledge to engineering site investigation, resource extraction, geohazard assessment, and environmental management. Students study rock mechanics, hydrogeology, geotechnical analysis, mineral exploration methods, and geospatial data interpretation. The global demand for lithium, cobalt, nickel, rare earths, and other critical minerals needed for electric vehicles and renewable energy systems has fundamentally repositioned geology engineering — from a declining extractive industry into a strategically essential field at the center of the clean energy transition.",

  'Hydraulic Engineering':
    "Hydraulic Engineering focuses on the science and technology of water resource management and hydraulic infrastructure — including dam design, reservoir management, irrigation systems, river engineering, and flood control networks. Students study fluid mechanics, hydrology, hydraulic structures, groundwater systems, and water resource policy. China manages some of the world's most complex river systems and faces significant long-term water security challenges. This combination of geographic need and national investment priority sustains consistent demand for hydraulic engineers across public water authorities and infrastructure project teams.",

  'Instrumentation':
    "Instrumentation Engineering covers the design, calibration, and application of measurement, sensing, and control devices used across scientific research, manufacturing quality control, and industrial process monitoring. Students study sensor technology, signal processing, measurement systems design, and precision calibration methods. While less visible than other engineering disciplines, instrumentation is foundational to advanced manufacturing — no precision production process operates without reliable measurement systems. China's push for self-sufficiency in high-end instrumentation, currently dominated by imported equipment, is creating targeted domestic investment in this field.",

  'Interdisciplinary Eng':
    "Interdisciplinary Engineering programs are designed to address problems that span traditional engineering boundaries. These programs combine elements from computer science, mechanical engineering, materials science, and AI system design into integrated curricula built around emerging fields — smart manufacturing, autonomous systems, quantum engineering, and human-machine interaction. Students develop flexible, cross-domain skill sets suited to roles that traditional single-discipline graduates struggle to fill. While these programs are newer and less familiar to some employers, they are often the most direct match to where industrial demand is actually growing.",

  'Light Industry':
    "Light Industry Engineering covers the technology and production processes behind consumer goods including paper products, plastics, rubber, printing systems, and packaging materials. Students study polymer engineering, production technology, quality control systems, packaging design, and materials characterization. While volume manufacturing of basic consumer goods is migrating toward lower-cost production regions, China's light industry sector is upgrading toward premium materials, sustainable packaging, and circular economy applications — areas where engineering knowledge and process innovation add significant commercial value.",

  'Materials Science':
    "Materials Science and Engineering studies the relationship between the structure, properties, processing, and performance of materials — including metals, ceramics, polymers, composites, semiconductors, and nanomaterials. Students learn materials characterization techniques, synthesis and fabrication methods, computational modeling, and failure analysis. Battery materials for EVs, semiconductor substrates, high-strength composites for aerospace, and biomedical implant materials are all named national strategic priorities in China. This convergence of demand makes materials science one of the most consistently well-funded engineering disciplines available.",

  'Mechanical Engineering':
    "Mechanical Engineering is one of the broadest engineering disciplines, covering the design, analysis, manufacturing, and operation of mechanical systems — from engines, turbines, and heat exchangers to robots, precision instruments, and complex machinery. Students study mechanics, thermodynamics, manufacturing processes, machine design, and increasingly, digital manufacturing tools such as CAD, simulation software, and digital twin systems. Mechanical engineering remains one of the largest engineering employers in China by absolute headcount, with applications spanning automotive, aerospace, energy, and consumer product manufacturing.",

  'Mechanics':
    "Engineering Mechanics is the theoretical discipline underpinning civil, mechanical, and aerospace engineering, providing the mathematical and physical foundations for analyzing forces, motion, deformation, and fluid behavior in engineering systems. Students study statics, dynamics, fluid mechanics, solid mechanics, and computational methods at a rigorous level. The field primarily prepares graduates for research careers in engineering science, advanced graduate study, or analytical roles in structural and aerospace engineering. Its value lies in providing the deepest analytical foundation — the kind that applied engineering programs build upon but rarely teach at this depth.",

  'Mining':
    "Mining Engineering covers the full lifecycle of mineral resource development — from exploration and site evaluation through extraction, processing, environmental management, and mine closure. Students study geomechanics, mine design, ventilation systems, blasting technology, mineral processing, and safety systems. The global transition to electric vehicles and renewable energy has dramatically increased demand for lithium, cobalt, copper, nickel, and rare earth minerals, repositioning mining engineering as a strategically important field and drawing new investment and government attention after more than a decade of relative decline.",

  'Nuclear Engineering':
    "Nuclear Engineering focuses on the design, operation, and safety of nuclear reactor systems, along with radiation protection, nuclear fuel cycle management, and the application of nuclear science in medicine and industry. Students study nuclear physics, reactor theory, thermal hydraulics, materials behavior under radiation, and regulatory compliance. China has one of the world's most active nuclear power construction programs, with dozens of reactors under construction or planned. This creates sustained domestic demand for nuclear engineers in both state energy companies and the research institutions that support them.",

  'Ocean Engineering':
    "Ocean Engineering covers the design, construction, and operation of structures and systems that function in marine environments — including offshore platforms, subsea pipelines, marine vessels, underwater robotics, and ocean energy systems. Students study fluid dynamics, structural mechanics, ocean wave theory, corrosion engineering, and marine systems integration. China's expanding offshore wind installation program along its coastline and growing interest in deep-sea resource exploration are creating real investment in a field that was previously small by comparison with land-based engineering disciplines.",

  'Ordnance':
    "Ordnance Engineering covers the scientific and engineering principles behind weapons systems, munitions, guidance technology, and defense equipment. Students study ballistics, explosives engineering, guidance and control systems, propulsion, and military systems design within a strictly controlled academic environment. Admission typically requires political reliability screening, and career paths are almost exclusively within China's defense industrial complex — state-owned defense enterprises, military research institutes, and weapons testing organizations. The trade-off is exceptional job security and competitive compensation within that closed system.",

  'Public Security Tech':
    "Public Security Technology applies engineering and information systems to law enforcement, public safety management, and emergency response. Students study surveillance systems, forensic science, cybercrime investigation, biometric identification, emergency communications, and disaster management technology. The field is growing rapidly as AI-powered monitoring, facial recognition, and smart city safety systems become embedded in Chinese urban infrastructure. Graduates work almost exclusively within the public security apparatus — police agencies, government technology bureaus, and state-contracted security technology companies.",

  'Safety Engineering':
    "Safety Engineering is concerned with the systematic identification, evaluation, and control of hazards in industrial workplaces, construction sites, transportation systems, and public environments. Students study risk assessment methodologies, safety management systems, hazardous materials handling, accident investigation techniques, and regulatory compliance frameworks. As Chinese workplace safety regulation becomes more rigorous and enforcement more consistent, safety engineers are evolving from compliance checkbox roles into genuine risk management functions within major industrial organizations — particularly in manufacturing, construction, and chemicals.",

  'Surveying & Mapping':
    "Surveying and Mapping Engineering covers the precise measurement, analysis, and digital representation of the Earth's surface using methods ranging from traditional field surveying to GPS satellite positioning, LiDAR scanning, and satellite remote sensing. Students develop skills in spatial data collection and processing, coordinate reference systems, digital cartography, and geographic information systems. The integration of this discipline with smart city planning, autonomous vehicle navigation, logistics optimization, and climate change monitoring has significantly expanded its commercial applications and career paths beyond traditional land surveying roles.",

  'Textile':
    "Textile Engineering covers the design, engineering, and production of fibers, yarns, fabrics, and finished textile products across the full value chain from raw material to finished goods. Students study fiber science, spinning, weaving and knitting technology, dyeing and finishing processes, and textile quality testing. While mass-market garment manufacturing is increasingly moving to lower-cost production regions, China's textile industry is investing significantly in high-performance technical textiles — materials engineered for medical, aerospace, protective, and smart wearable applications where engineering knowledge adds substantial value.",

  'Transportation':
    "Transportation Engineering covers the planning, design, construction, and operation of transportation systems including road networks, high-speed rail infrastructure, airports, ports, urban metro systems, and logistics networks. Students study traffic engineering, transportation demand modeling, infrastructure design, systems optimization, and increasingly, smart transportation technologies including connected vehicle systems and autonomous transport. China's extraordinary sustained investment in transportation infrastructure — including the world's largest high-speed rail network and ongoing urban metro expansion — has created consistent long-term demand for transportation engineers.",

  # ── Medicine ──────────────────────────────────────────────────────
  'Basic Medical Sciences':
    "Basic Medical Sciences is the research foundation of modern medicine, encompassing disciplines including anatomy, physiology, biochemistry, molecular biology, pathology, pharmacology, and immunology. Students develop a deep understanding of how the human body works at cellular and molecular levels — the essential foundation for medical research and pharmaceutical development. The field primarily prepares graduates for careers in academic research, pharmaceutical R&D, and graduate programs in medicine or life sciences. It is less directly connected to clinical practice and more connected to advancing the scientific understanding that underpins all of medical progress.",

  'Chinese Materia Medica':
    "Chinese Materia Medica is the scientific study of the natural substances — plants, minerals, and animal products — used in traditional Chinese medicine, along with the pharmacological mechanisms behind their therapeutic effects. Students study pharmacognosy, phytochemistry, drug extraction and processing, quality control, and the classical theories of TCM that guide their clinical application. The field is experiencing renewed interest as AI-powered compound screening identifies promising bioactive molecules within traditional formulas, and as international recognition of TCM grows through WHO integration and global wellness market expansion.",

  'Clinical Medicine':
    "Clinical Medicine is the core medical discipline that trains physicians to diagnose and treat disease in patients across all age groups and organ systems. Students undergo eight or more years of integrated study combining basic medical sciences with clinical training across internal medicine, surgery, gynecology, pediatrics, and other specialties, followed by residency programs. The training path is among the longest and most demanding in higher education. Clinical physicians occupy the center of the healthcare system — responsible for the patient relationship, diagnostic judgment, and treatment decisions that no AI system is currently authorized or equipped to make independently.",

  'Dental Medicine':
    "Dental Medicine trains dental surgeons to prevent, diagnose, and treat diseases of the teeth, gums, jaw, and oral tissues. Students complete a five-year program combining dental sciences — including oral anatomy, dental materials, radiology, and pharmacology — with clinical training across general dentistry, oral surgery, orthodontics, and periodontics. China's dental practitioner-to-population ratio remains significantly below comparable economies, creating a structural supply shortfall that private dental chains and hospital dental departments are actively trying to address. Cosmetic and orthodontic procedures are driving premium segment growth.",

  'Forensic Medicine':
    "Forensic Medicine applies medical and scientific knowledge to the legal system — primarily in the investigation of death, identification of injury causation, toxicological analysis, and the provision of expert medical testimony in criminal and civil proceedings. Students study forensic pathology, toxicology, forensic genetics, clinical forensic medicine, and the legal frameworks within which medical evidence is applied. Career paths are almost entirely within government institutions — public security bureaus, procuratorates, courts, and forensic identification centers — providing niche but stable professional employment.",

  'Integrative Medicine':
    "Integrative Medicine combines the clinical methods of Western biomedicine with the theories and therapies of traditional Chinese medicine into a unified practice approach. Students acquire competency in both biomedical diagnosis and TCM pattern differentiation, studying internal medicine, acupuncture, herbal pharmacology, and rehabilitation across an extended clinical training period. The field is a distinctly Chinese medical specialty with active government support and a clear institutional home in China's hospital system. International interest in evidence-based integrative approaches — particularly in oncology support, pain management, and rehabilitation — is gradually opening global research and practice pathways.",

  'Medical Technology':
    "Medical Technology trains clinical technologists to operate and interpret the results of diagnostic equipment and laboratory tests that underpin medical decision-making — including clinical laboratory analysis, medical imaging, pathology, and physiological measurement. Students develop specialized technical knowledge in laboratory science, imaging physics, equipment operation, and quality assurance systems. As China's healthcare coverage expands to serve a larger and older population, clinical laboratories and radiology departments are scaling up significantly. Medical technologists are essential to this expansion but often less visible than the physicians they support.",

  'Nursing':
    "Nursing trains professional nurses to provide direct clinical care, health education, rehabilitation support, and preventive health services to patients across hospital, community, and home settings. Students study nursing science, clinical medicine, pharmacology, anatomy, and develop practical clinical skills through extensive hospital placement training. China faces a structural nursing shortage — the country's nurse-to-patient ratios in many hospitals fall below international standards, and the demand for qualified nurses is growing as the population ages and as healthcare reform extends coverage. Nursing graduates enter one of the most reliably employed professions in the entire healthcare system.",

  'Pharmacy':
    "Pharmacy trains pharmacists to prepare, dispense, and counsel patients on the safe and effective use of medications, and to apply pharmaceutical science in drug development, quality control, and regulatory compliance. Students study pharmacology, pharmaceutical chemistry, pharmaceutical analysis, biopharmaceutics, and clinical pharmacy practice. The field spans two distinct but connected worlds — the clinical environment where pharmacists manage complex medication regimens, and the industrial environment where pharmaceutical scientists develop and test new drugs. AI is transforming drug discovery pipelines, creating new hybrid roles for pharmacists who combine chemical knowledge with computational methods.",

  'Public Health':
    "Public Health is the science and practice of protecting and improving the health of entire populations — through disease surveillance, epidemiological research, health policy development, environmental health management, and community health promotion. Students study epidemiology, biostatistics, health education, occupational health, social medicine, and public health management. The COVID-19 pandemic fundamentally elevated public health from a technical specialty to a recognized national priority, resulting in significantly increased government investment, expanded institutional capacity, and growing public awareness of the field's importance.",

  'Trad. Chinese Medicine':
    "Traditional Chinese Medicine is a comprehensive medical system rooted in thousands of years of clinical observation and theoretical development, encompassing acupuncture, herbal medicine, moxibustion, therapeutic massage, and dietary therapy. Students undergo a five-year program combining TCM theory — including yin-yang philosophy, five-element theory, and channel systems — with clinical training in diagnosis and treatment using TCM methods. Government policy explicitly mandates TCM integration throughout China's healthcare system, and international demand for TCM practitioners is growing alongside a global wellness industry that is increasingly open to evidence-informed traditional approaches.",

  # ── Science ───────────────────────────────────────────────────────
  'Astronomy':
    "Astronomy is the scientific study of celestial objects, phenomena, and the universe as a whole — encompassing observational astronomy, astrophysics, cosmology, and planetary science. Students develop expertise in physics, mathematics, computational modeling, and the operation of telescope and detector systems. China has made significant investments in astronomical infrastructure, including the world's largest single-dish radio telescope FAST and active participation in space telescope programs. Career paths are primarily academic and highly competitive globally. The computational skills developed through astronomy — data analysis, simulation, and modeling at scale — do translate to adjacent technology careers for those who pursue that route.",

  'Atmospheric Sciences':
    "Atmospheric Sciences is the study of Earth's atmosphere — its composition, structure, dynamics, and interactions with land, ocean, and human activity. Students study meteorology, climatology, atmospheric chemistry, cloud physics, and numerical weather prediction, developing strong mathematical and computational foundations. The field connects to some of the most pressing global challenges — including extreme weather forecasting, climate change attribution, and air quality management — that are receiving significant government and commercial investment. AI and machine learning are fundamentally changing what atmospheric scientists can accomplish with the enormous datasets generated by modern weather observation systems.",

  'Biological Sciences':
    "Biological Sciences is the study of living organisms — their structure, function, evolution, genetics, and ecological relationships. Students develop foundations in molecular biology, cell biology, genetics, biochemistry, ecology, and evolutionary theory, typically with significant laboratory training. The field is experiencing rapid transformation as genomic technologies, synthetic biology, and computational approaches combine to create new research capabilities and commercial applications in biotech, precision medicine, and agricultural biotechnology. China is investing significantly in life sciences research and the biotech industry cluster being built around it.",

  'Chemistry':
    "Chemistry is the fundamental scientific study of matter — its composition, structure, properties, and the reactions through which it transforms. Students study organic, inorganic, physical, analytical, and computational chemistry, developing both theoretical understanding and practical laboratory skills. The field is foundational to materials science, pharmaceutical research, energy storage, and environmental science. Battery chemistry for electric vehicles, catalyst development for clean energy, and specialty chemical synthesis for the semiconductor industry are all areas where chemistry graduates with the right specialization are finding strong and sustained demand.",

  'Geographic Sciences':
    "Geographic Sciences is the study of the spatial distribution of natural and human phenomena across Earth's surface — integrating physical geography, human geography, GIS technology, and remote sensing. Students develop skills in spatial data analysis, cartography, environmental systems, and the use of geographic information systems. The discipline has been transformed by satellite data, drone imagery, and machine learning — enabling applications from precision agriculture and logistics optimization to urban planning and climate monitoring. Graduates increasingly work in roles that would have been described as data science or spatial analytics a decade ago.",

  'Geology':
    "Geology is the scientific study of Earth — its composition, structure, history, and the processes that shape its surface and interior over geologic time. Students study mineralogy, petrology, stratigraphy, geomorphology, structural geology, and geochemistry, typically with significant field mapping training. The field connects to some of the most critical supply chain questions of the current decade: where are the lithium, cobalt, nickel, and rare earth deposits that will supply the electric vehicle and renewable energy industries? Geologists with exploration skills and geospatial data capabilities are at the center of answering that question.",

  'Geophysics':
    "Geophysics applies the principles of physics to the study of Earth — using seismic waves, gravitational fields, magnetic fields, and electrical properties to image the subsurface and understand Earth's interior. Students study seismology, exploration geophysics, well logging, electromagnetic methods, and increasingly, the computational methods used to interpret large geophysical datasets. The main industry application is in energy exploration — oil, gas, and geothermal — alongside earthquake hazard assessment and subsurface site investigation. AI and machine learning are making seismic interpretation significantly faster and more accurate, creating new roles for geophysicists who combine domain knowledge with computational skills.",

  'Mathematics':
    "Mathematics is the study of abstract structures — numbers, quantities, shapes, and the logical relationships between them — with applications extending across every field of human knowledge and industry. Students develop rigorous analytical and proof-writing skills through study of calculus, linear algebra, probability, statistics, abstract algebra, topology, and numerical methods. The AI era has substantially increased the practical demand for mathematical thinking: machine learning algorithms, cryptographic systems, optimization problems, and financial models all require deep mathematical foundations. Mathematics graduates who develop applied skills in programming and data analysis are among the most broadly employable graduates across industries.",

  'Ocean Sciences':
    "Ocean Sciences is the interdisciplinary study of the world's oceans — including physical oceanography, marine biology, marine chemistry, marine geology, and ocean-atmosphere interaction. Students develop skills in field sampling, oceanographic instrumentation, data analysis, and numerical modeling of ocean systems. The field connects to significant national interests: marine resource assessment, climate science, coastal hazard prediction, and the geopolitical importance of maritime territories. China's Blue Economy policy is actively investing in ocean research infrastructure and the commercial applications of marine science, creating a larger institutional base for ocean scientists than existed previously.",

  'Physics':
    "Physics is the fundamental science of matter, energy, space, and time — seeking to understand the deepest principles governing how the universe works. Students study classical mechanics, electromagnetism, quantum mechanics, thermodynamics, and statistical physics, developing the strongest analytical and mathematical foundation available in science. The field branches into areas ranging from particle physics to condensed matter, optics, and applied physics. Quantum computing — where China has made it one of the most heavily funded scientific investments in the country — is creating genuine new career paths for physics graduates with the right specialization, alongside longstanding opportunities in semiconductor research and photonics.",

  'Psychology':
    "Psychology is the scientific study of human behavior, mental processes, cognition, emotion, and social interaction. Students study research methods, neuroscience, developmental psychology, social psychology, clinical psychology, and organizational behavior — developing both empirical research skills and applied interpersonal competencies. Mental health awareness in China is rising rapidly, driven by urban stress, changing family structures, and generational shifts in how wellbeing is understood. This is creating genuine growth in demand for psychological services across clinical, educational, and corporate settings — a shift that is still in its early stages relative to comparable developed economies.",

  'Statistics':
    "Statistics is the science of collecting, analyzing, interpreting, and communicating data under conditions of uncertainty. Students study probability theory, statistical inference, regression modeling, experimental design, multivariate analysis, and computational statistics. The field is experiencing a renaissance driven by the data economy: every significant technology company, hospital system, financial institution, and government agency now depends on statistical thinking to make decisions. Statistics graduates who can combine mathematical rigor with programming skills and clear communication are among the most broadly in-demand analytical professionals across sectors.",

  # ── Economics ─────────────────────────────────────────────────────
  'Economics':
    "Economics is the study of how individuals, firms, and governments make decisions about the allocation of scarce resources — analyzing markets, prices, production, consumption, trade, and the forces that shape economic growth and distribution. Students develop rigorous analytical skills through study of microeconomics, macroeconomics, econometrics, and mathematical modeling. The discipline builds a powerful framework for understanding human behavior and system-level outcomes. Graduates who supplement economic foundations with quantitative skills, coding, or domain expertise in finance, policy, or technology find broad demand across consulting, government, development finance, and industry.",

  'Finance':
    "Finance is the study of how money, investment, and capital markets function — covering corporate finance, investment analysis, risk management, financial markets, and financial institutions. Students study financial theory, accounting, portfolio management, derivatives, and quantitative methods, developing both analytical skills and institutional knowledge of how capital is allocated in practice. Finance graduates enter one of the widest salary ranges of any discipline: entry-level roles are competitive but accessible, while senior roles in investment banking, asset management, and private equity offer among the highest compensation in the professional economy.",

  'Intl Economics & Trade':
    "International Economics and Trade covers the theory and practice of trade between nations — including trade policy, customs regulations, foreign exchange markets, international logistics, and the legal frameworks governing cross-border commercial transactions. Students study international trade theory, global supply chain management, trade law, customs compliance, and the business practices relevant to import-export operations. The field is navigating a period of significant disruption as geopolitical tensions reshape global supply chains, export control regimes tighten, and Belt and Road infrastructure creates new trade corridors requiring specialized commercial and compliance expertise.",

  'Public Finance':
    "Public Finance covers the financial management of government — including tax policy, government budgeting, public expenditure analysis, bond markets, and fiscal policy design. Students study public economics, taxation systems, government accounting, social security finance, and fiscal federalism. The field prepares graduates for careers in government finance departments, tax authorities, national audit institutions, and central bank and fiscal policy research roles. Public finance professionals operate at the intersection of economics and public administration, making decisions that affect the allocation of public resources at local, provincial, and national levels.",

  # ── Education ─────────────────────────────────────────────────────
  'Education':
    "Education as an academic discipline covers the theory and practice of teaching and learning across all levels — from early childhood development through higher education — including curriculum design, educational psychology, assessment methods, school management, and education policy. Students develop an integrated understanding of how learning happens, how it can be measured, and how educational systems can be designed to serve diverse students effectively. China's education system serves the world's largest student population, and the combination of government teacher employment guarantees with a rapidly expanding EdTech industry is creating a broader range of career paths than existed a generation ago.",

  'Physical Education':
    "Physical Education trains professionals in sports science, kinesiology, coaching methodology, sports medicine, and physical fitness instruction. Students study exercise physiology, sports biomechanics, sports psychology, athletic training, and the pedagogy of physical education in school settings. Beyond school teaching — the traditional career path — graduates are finding growing opportunities in China's expanding fitness and wellness industry, including personal training, sports rehabilitation, performance analytics, and sports technology roles. The domestic sports industry is professionalizing rapidly, and athletes, coaches, and sports health professionals are increasingly valued within that ecosystem.",

  # ── History ───────────────────────────────────────────────────────
  'History':
    "History is the scholarly study and interpretation of the human past — examining political, social, economic, cultural, and intellectual developments across civilizations and time periods. Students develop research skills in primary source analysis, historiographical method, critical writing, and the ability to construct evidence-based arguments from complex and incomplete information. The discipline trains a rare capacity: understanding how systems, institutions, and societies change over long time horizons. While direct commercial applications of history are narrow, the analytical and communication skills it develops are genuinely valued in policy research, media, cultural institutions, and strategic consulting roles.",

  # ── Law ───────────────────────────────────────────────────────────
  'Ethnology':
    "Ethnology is the comparative study of human cultures, ethnic groups, and the social structures, customs, beliefs, and practices that define them. Students study anthropological theory, ethnographic research methods, cultural analysis, minority studies, and the policy frameworks governing ethnic affairs in China. The field is one of the most niche in the Chinese university system, with career paths concentrated in academic research institutions, government cultural affairs departments, and the organizations responsible for implementing ethnic minority policy. Its value lies in developing deep cultural understanding and research skills that are rare and genuinely needed within those specialized contexts.",

  'Law':
    "Law is the study of legal systems, statutes, regulations, judicial processes, and the rights and obligations they create — covering civil law, criminal law, constitutional law, administrative law, commercial law, and international law. Students develop skills in legal research, argumentation, case analysis, and professional legal writing through a combination of doctrinal coursework and practical case study. Lawyers occupy a foundational role in every economy and society, and the growing regulatory complexity of China's domestic market — combined with expanding cross-border commercial activity — is creating sustained demand for legal professionals who combine technical expertise with sound judgment.",

  'Marxist Theory':
    "Marxist Theory is the academic study of Marxist philosophy, political economy, and political theory as a systematic intellectual tradition and the ideological foundation of the Chinese political system. Students study the works of Marx, Engels, Lenin, and Mao Zedong alongside Chinese socialist theory and the historical development of the Chinese Communist Party. The discipline occupies a unique institutional position: it is politically valued and systematically supported within China's academic system, providing stable employment pathways in party schools, government policy research, university political education departments, and ideological training institutions.",

  'Political Science':
    "Political Science is the systematic study of political institutions, government systems, public policy, political behavior, and international relations. Students study political theory, comparative politics, public administration, international relations, and policy analysis using empirical and theoretical methods. The field prepares graduates for careers in government agencies, diplomatic service, think tanks, international organizations, and policy research institutes. The complexity of China's domestic governance and its expanding global role in multilateral institutions and international development finance has created real professional demand for political scientists who combine analytical rigor with institutional knowledge.",

  'Public Security':
    "Public Security programs train law enforcement professionals and technical specialists for careers in police services, border security, criminal investigation, public order management, and the growing field of cybercrime and digital evidence. Students study criminal law, investigative techniques, forensic science, public safety management, and increasingly, the digital tools used in modern policing. Career paths are almost entirely within the public security system — police academies, provincial public security bureaus, border agencies, and national security institutions — providing stable government employment with clear rank-based career progression.",

  'Sociology':
    "Sociology is the scientific study of human society — examining social structures, institutions, inequalities, group behavior, cultural norms, and the forces that produce social change. Students develop quantitative and qualitative research skills including survey design, ethnographic methods, statistical analysis, and social data interpretation. The field is finding new relevance as organizations try to understand customer behavior, social media dynamics, community resilience, and the social impacts of technology — creating roles in corporate research, policy institutes, NGOs, and increasingly, the social data analytics teams that help governments and companies make sense of large-scale behavioral patterns.",

  # ── Literature ────────────────────────────────────────────────────
  'Chinese Language & Lit':
    "Chinese Language and Literature covers the history, theory, and practice of Chinese written and oral expression — spanning classical literature, modern fiction, poetry, linguistics, rhetoric, and cultural criticism. Students develop deep reading and writing skills alongside critical frameworks for interpreting literary and cultural texts. The field has historically prepared graduates for teaching, editing, and cultural institution roles. In the digital content economy, strong Chinese writing skills combined with media literacy and cultural knowledge create pathways into content strategy, screenwriting, brand communication, and the fast-growing cultural industries — though AI writing tools are increasingly competitive in this space.",

  'Foreign Languages':
    "Foreign Language programs train students in the linguistic, cultural, and professional competencies of specific non-Chinese languages — spanning major world languages including English, Japanese, Korean, French, German, Spanish, and Russian, alongside dozens of less commonly studied languages. Students develop speaking, listening, reading, and writing proficiency alongside cultural knowledge, translation theory, and in many programs, specialized vocabulary for legal, medical, or technical domains. The field is experiencing significant disruption from AI translation tools, which handle routine translation with growing accuracy. Graduates who develop specialized domain knowledge alongside their language skills — and who work at the intersection of language and another professional field — are best positioned to maintain competitive advantage.",

  'Journalism & Comm':
    "Journalism and Communication covers the theory and practice of gathering, producing, and distributing information and narrative across media platforms — including news reporting, broadcasting, digital media, public relations, advertising, and organizational communication. Students develop writing, storytelling, multimedia production, and media analysis skills alongside critical understanding of the media system's social and political role. Traditional media employment is contracting, but the demand for skilled communicators in digital platforms, data journalism, brand content, and corporate communications continues to generate career opportunities for graduates who adapt their skills to where audiences and attention have migrated.",

  # ── Management ────────────────────────────────────────────────────
  'Agricultural Management':
    "Agricultural Management combines business administration principles with agricultural production knowledge to prepare managers for roles in agribusiness, rural enterprise development, and agricultural supply chain coordination. Students study farm management, agricultural economics, rural development policy, supply chain management, and increasingly, digital agriculture systems. China's rural revitalization agenda — one of the central national policy priorities of the 2020s — is driving professionalization of the agricultural sector and creating demand for graduates who can manage the business side of modern farming enterprises and the rural development organizations supporting them.",

  'Business Administration':
    "Business Administration is the broad foundation of management education, covering accounting, marketing, operations, human resources, organizational behavior, strategic management, and entrepreneurship. Students develop general management competencies applicable across virtually every industry and type of organization. The credential's breadth is both its strength — it is recognized everywhere — and its limitation — it provides less differentiation than specialized degrees in a competitive graduate labor market. The graduates who succeed typically combine business administration foundations with either deep industry expertise, technical skills, or entrepreneurial execution.",

  'E-Commerce':
    "E-Commerce programs train professionals for careers in digital commerce — covering online retail operations, digital marketing, supply chain logistics, payment systems, platform economics, and data-driven customer behavior analysis. Students study e-commerce platforms, digital marketing tools, operations management, cross-border trade, and the data analytics that drive conversion and customer retention. China has built the world's most sophisticated e-commerce ecosystem, encompassing everything from domestic platforms to live commerce and cross-border trade channels. Graduates enter an industry that is still expanding but also evolving rapidly, requiring ongoing skill development to stay current with platform changes.",

  'Industrial Engineering':
    "Industrial Engineering is concerned with the design and optimization of complex systems combining people, machines, materials, information, and energy — with the goal of improving efficiency, quality, and productivity. Students study operations research, systems simulation, lean manufacturing, supply chain design, quality management, and human factors engineering. While rooted in manufacturing, the field's optimization principles apply across healthcare operations, logistics networks, service systems, and organizational design. Graduates who combine industrial engineering methods with data science skills are finding growing demand in both factory and non-factory environments.",

  'Library & Info Management':
    "Library and Information Management covers the organization, preservation, retrieval, and management of recorded knowledge — including digital information systems, archival science, knowledge management, and library science. Students study information architecture, database management, digital preservation, metadata systems, and increasingly, the management of organizational knowledge in corporate and government settings. The traditional library is being transformed by digitalization, shifting the field toward knowledge management systems, digital cultural heritage, information governance, and the design of the systems that help organizations find and use what they know.",

  'Logistics Management':
    "Logistics Management covers the planning, implementation, and control of the flow of goods, information, and resources from origin to consumption — encompassing warehousing, transportation, inventory management, supply chain design, and cross-border trade operations. Students study supply chain strategy, logistics systems, inventory optimization, transport economics, and operations management. China's dominant position in global manufacturing and its expanding cross-border e-commerce industry have made logistics one of the country's most economically critical sectors — and supply chain disruptions have elevated awareness of its strategic importance among governments and corporations globally.",

  'Management Sci & Eng':
    "Management Science and Engineering applies quantitative methods — including mathematical modeling, systems simulation, optimization algorithms, and data analysis — to management decision-making in complex organizations. Students study operations research, systems engineering, decision theory, project management, and information systems alongside foundational management coursework. The field sits at the productive intersection of analytical rigor and organizational application, preparing graduates to solve problems that are too complex for intuition alone but require management understanding to implement. This combination makes graduates competitive for roles in consulting, corporate strategy, government planning, and technology management.",

  'Public Administration':
    "Public Administration covers the management, policy implementation, and organizational design of government institutions at all levels — from local community services to national regulatory agencies. Students study public policy analysis, administrative law, public finance, organizational behavior in government, and the management of public service delivery. The field prepares graduates directly for civil service careers and for the examination processes that govern entry into China's public sector. Government employment at all levels offers stable income, defined benefits, and the opportunity to contribute to policy outcomes that affect millions of people.",

  'Tourism Management':
    "Tourism Management covers the planning, operation, and marketing of tourism services, hospitality businesses, and travel experiences — including hotels, resorts, travel agencies, tourism destinations, and event management. Students study hospitality operations, tourism economics, marketing strategy, cultural heritage management, and service quality systems. Post-pandemic recovery is restoring domestic and international tourism volumes, while a growing middle class with rising disposable income is creating premium demand for differentiated travel experiences. Graduates who position themselves in tourism technology platforms, cultural experience design, or sustainable tourism development have more resilient career paths than those focused only on traditional hotel and travel agency roles.",

  # ── Agriculture ───────────────────────────────────────────────────
  'Animal Production':
    "Animal Production covers the science and management of livestock and poultry farming — including animal nutrition, genetics and breeding, reproduction, disease management, housing systems, and production efficiency. Students study animal science, veterinary principles, feed formulation, and increasingly, precision livestock farming technologies that use sensors and AI to monitor animal health and optimize production. China's protein food supply depends heavily on domestic livestock production, making food security and animal welfare science genuine national priorities. Graduates work in production farms, feed companies, animal genetics businesses, and agricultural research institutions.",

  'Crop Production':
    "Crop Production covers the science and technology of growing agricultural crops — including soil science, plant physiology, genetics and breeding, crop protection, irrigation management, and precision farming. Students study agronomy, plant biology, pesticide science, agricultural meteorology, and the digital technologies transforming field management — from GPS-guided planting and drone-assisted spraying to AI-powered yield prediction and disease detection systems. Ensuring stable food production for 1.4 billion people is a permanent national priority in China, backing this field with consistent government investment in research, technology adoption support, and agricultural subsidy programs.",

  'Fisheries':
    "Fisheries Science covers the biology, management, and technology of fish and aquatic organism production — including aquaculture systems, capture fisheries management, fish disease, water quality, and sustainable production practices. Students study fish biology, aquaculture engineering, water quality management, fisheries economics, and aquatic ecology. China is the world's largest aquaculture producer, supplying the majority of its own fish consumption from farmed rather than wild-caught sources. The technical challenges of managing disease, water quality, and production efficiency at this scale create genuine demand for graduates who combine biological knowledge with systems management skills.",

  'Forestry':
    "Forestry Science covers the ecology, management, conservation, and utilization of forest ecosystems and the resources they provide — including timber, non-timber forest products, biodiversity, watershed protection, and carbon sequestration. Students study dendrology, silviculture, forest ecology, forest measurement, and wood science, with growing emphasis on remote sensing and GIS tools for forest monitoring. China's afforestation programs represent the largest tree-planting initiative in human history, and the development of voluntary carbon markets has created a new economic dimension to forest management that is generating genuinely new professional roles.",

  'Grassland Science':
    "Grassland Science is the study of grassland ecosystems — their ecology, management, conservation, and restoration — covering species composition, grazing management, desertification control, and grassland productivity. Students study plant ecology, soil science, rangeland management, and restoration ecology, often with field training in China's extensive northern and western grassland regions. China's grassland degradation — the result of decades of overgrazing and climate pressure — has made ecological restoration a policy priority, with funded programs to restore productivity and carbon sequestration capacity in degraded systems. It is a small but policy-backed field.",

  'Nature Conservation & Ecology':
    "Nature Conservation and Ecology covers the scientific study of biodiversity, ecosystem function, species conservation, and the management of protected areas and natural reserves. Students study ecology, conservation biology, wildlife management, environmental policy, and the use of remote sensing and GIS tools for habitat assessment. China has significantly expanded its protected area network and biodiversity conservation commitments in recent years, including major investments in national parks and ecological red line protections. This policy shift is creating new institutional roles for conservation professionals in both government agencies and the growing domestic environmental NGO sector.",

  'Veterinary Medicine':
    "Veterinary Medicine trains clinical veterinarians to prevent, diagnose, and treat diseases in animals — including companion animals, livestock, aquatic species, and wildlife. Students complete a five-year program combining veterinary basic sciences — anatomy, physiology, pharmacology, pathology — with clinical training across small animal, large animal, and exotic animal medicine. The rapid growth of China's pet ownership market, particularly in urban areas, has created significant and ongoing demand for companion animal veterinarians. Simultaneously, food animal inspection, disease surveillance, and zoonotic disease control are stable government-backed functions requiring qualified veterinary professionals.",

  # ── Philosophy ────────────────────────────────────────────────────
  'Philosophy':
    "Philosophy is the systematic study of fundamental questions about existence, knowledge, ethics, reason, and the nature of reality — encompassing logic, epistemology, metaphysics, ethics, political philosophy, and philosophy of mind. Students develop rigorous analytical and argumentative skills through engagement with canonical texts and contemporary philosophical problems. The field has traditionally prepared graduates for academic and teaching careers. The emergence of AI systems that make high-stakes decisions affecting human welfare has created genuine new demand for people who can reason clearly about values, ethics, governance, and the social implications of technology — a set of skills that philosophy uniquely develops.",
}

# Future Outlook — generated from star tier + AI impact + subcategory momentum
OUTLOOK_BY_STAR = {
  5: "The outlook for this field through 2029 is strong by most measures. Job demand is expanding, salary benchmarks are rising, and the field is benefiting from rather than being disrupted by AI adoption. Students who enter now will graduate into conditions that are better than today — assuming they invest in the technical and adaptive skills that the best employers in this area are already selecting for.",
  4: "The outlook for this field is solid heading into 2029. Demand is growing across most major employment sectors, and the combination of policy support and technological change is creating new roles faster than traditional ones are being eliminated. Graduates who stay current — building AI tool fluency alongside their core domain knowledge — will find a labor market that rewards their expertise.",
  3: "The outlook for this field through 2029 is stable but not uniformly positive. The employment floor is well-supported by institutional demand and, in many cases, government policy. But the ceiling is moving — the most valuable roles within this field will go to graduates who specialize intelligently and develop complementary skills rather than relying on the degree credential alone.",
  2: "The outlook for this field carries meaningful uncertainty through 2029. Some functions within it are being automated or consolidated, and the employment market is tighter than it was a decade ago. Graduates who succeed will be those who have identified a specific niche where their skills are genuinely scarce, rather than those who expect the general credential to open doors on its own.",
  1: "The outlook for this field is challenging over the 2025–2029 window. AI tools, shifting employer preferences, and market saturation in entry-level roles are all creating headwinds that graduates will need a clear plan to navigate. That plan should include either deep specialization within the field, a strong second skill that cross-applies the core training, or a willingness to work in non-obvious roles where the underlying knowledge transfers.",
}

DEFAULT_INSIGHT = "This is a specialized field where career outcomes depend heavily on the specific track you choose and the depth of expertise you develop."
AI_PICK_TEXT = " AI systems have specifically identified this major as one with above-average resilience and growth potential in the 2025–2029 window — a signal worth taking seriously when forming your own view."
NO_AI_TEXT   = " Form your own view by researching where alumni from this field actually end up five years out — the honest answer often differs from the official narrative."

# ── FAQ templates per category ────────────────────────────────────
# Q1: Is [name] a good major?
# Q2: How will AI affect [name] graduates?
# Q3: What jobs can [name] graduates get?

AI_IMPACT_BY_CAT = {
  'Engineering':  "AI is a tool, not a replacement. Engineers who use AI for simulation, design, and optimization will be significantly more productive. The demand is for engineers who understand both the domain and the AI tools.",
  'Medicine':     "AI assists diagnosis and drug discovery, but clinical judgment, patient relationships, and hands-on procedures remain irreplaceable. Medical graduates should learn to work with AI, not fear it.",
  'Science':      "AI is transforming scientific research — automating literature review, accelerating experimental design, and enabling analysis at scale. Scientists who embrace computational methods will have a major productivity advantage.",
  'Economics':    "Routine economic analysis is being automated. Economists who combine theoretical foundations with data science skills and clear communication are in demand. Specialization is increasingly important.",
  'Management':   "AI is handling scheduling, reporting, and routine analysis. Managers who provide judgment, stakeholder relationships, and strategic direction will remain essential. The minimum bar for managers is rising.",
  'Education':    "AI tools are expanding what individual educators can prepare and deliver. Teachers who adopt adaptive learning tools and AI-assisted assessment will be more effective — and more competitive in the market.",
  'Law':          "AI is handling document review, contract analysis, and precedent research efficiently. Lawyers who focus on courtroom advocacy, negotiation, and complex client judgment will see the least disruption.",
  'Literature':   "AI can generate generic content at scale. Writers and communicators who develop a distinctive voice, cultural depth, and editorial judgment will find AI accelerates rather than replaces their value.",
  'History':      "AI can retrieve and synthesize historical information quickly. The unique value of a history education is interpretive skill and long-term systemic thinking — something AI tools currently lack.",
  'Philosophy':   "AI cannot reason about ethics, values, and governance on its own. Philosophers are becoming essential collaborators in AI development, policy, and technology governance.",
  'Agriculture':  "AI, drones, and sensors are modernizing agriculture rapidly. Graduates who combine domain knowledge with technology literacy will lead the transformation of one of China's most important sectors.",
}

def slug(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def stars_html(n): return '★' * n + '☆' * (5 - n)

def build_verdict(major, rating, is_ai):
    sub      = major.get('sub', major['cat'])
    opening  = STAR_OPEN.get(rating, STAR_OPEN[3])
    insight  = SUB_INSIGHT.get(sub, DEFAULT_INSIGHT)
    modifier = AI_PICK_TEXT if is_ai else NO_AI_TEXT
    return f"{opening} {insight}{modifier}"

def build_faq(major, rating, is_ai):
    name = major['n']
    cat  = major['cat']
    sub  = major.get('sub', cat)
    d    = SUBCAT.get(sub, DEFAULT_SUBCAT)
    ai_q = AI_IMPACT_BY_CAT.get(cat, "AI is changing this field, but domain expertise and professional judgment remain valuable. Graduates who actively use AI tools will have a significant advantage over those who do not.")

    # Q1 varies by star rating
    if rating >= 4:
        a1 = f"{name} is considered a strong major for 2025–2029. The field has solid job demand, competitive salaries, and growing integration with AI and technology. Students entering now will graduate into a market that is expanding rather than contracting."
    elif rating == 3:
        a1 = f"{name} provides a stable career foundation, but outcomes depend significantly on specialization and the specific skills you develop alongside the core curriculum. The field is neither a guaranteed path nor a dead end — your choices within it matter a lot."
    else:
        a1 = f"{name} carries more uncertainty than most fields in the current environment. Students considering this major should carefully research where recent graduates actually work, what they earn, and how AI is affecting the sector before committing."

    # Q3 based on careers list
    career_str = ", ".join(d['careers'])

    return [
        {
            'q': f"Is {name} a good major to study in China in 2025?",
            'a': a1,
        },
        {
            'q': f"How will AI affect {name} graduates over the next 5 years?",
            'a': ai_q,
        },
        {
            'q': f"What jobs can {name} graduates get in China?",
            'a': f"Common career paths for {name} graduates include: {career_str}. The specific roles available vary by specialization, region, and whether you pursue graduate education. Top employers include both state-owned enterprises and private companies in this sector.",
        },
    ]

def page(major):
    code    = major['c']
    name    = major['n']
    cat     = major['cat']
    sub     = major.get('sub', cat)
    is_ai   = code in AIPICK
    d       = SUBCAT.get(sub, DEFAULT_SUBCAT)
    rating  = min(5, d['stars'] + (1 if is_ai else 0))
    field   = f"{cat} · {sub}" if sub != cat else cat
    verdict   = build_verdict(major, rating, is_ai)
    faq       = build_faq(major, rating, is_ai)
    what_is   = WHAT_IS.get(sub, f"{name} is a specialized discipline within {cat}, equipping students with knowledge and skills directly applicable to careers in this field. The curriculum combines theoretical foundations with practical training, preparing graduates for both employment and further academic study.")
    outlook_p = OUTLOOK_BY_STAR.get(rating, OUTLOOK_BY_STAR[3])

    ai_badge = ('<span style="background:rgba(245,158,11,.15);border:1px solid rgba(245,158,11,.4);'
                'border-radius:4px;padding:2px 8px;font-size:11px;color:#f59e0b;margin-left:8px;">🤖 AI Pick</span>'
                if is_ai else '')

    prompt  = (f'Analyze "{name}" ({sub or cat}, Chinese university major) for someone entering in 2025: '
               f'job prospects in 4 years, AI impact on this field, salary expectations, key skills, and main career paths.')
    px_url  = 'https://www.perplexity.ai/search?q=' + re.sub(
                r'[^A-Za-z0-9\-_.~]', lambda x: f'%{ord(x.group()):02X}', prompt)

    seo_desc = (f"Is {name} a good major in China? Expert AI analysis, career outlook 2025–2029, "
                f"pros & cons for {sub} students, and live community votes.")

    pros_html    = '\n'.join(f'<li><span class="ic g">✓</span>{p}</li>' for p in d['pros'])
    cons_html    = '\n'.join(f'<li><span class="ic r">✗</span>{c}</li>' for c in d['cons'])
    careers_html = '\n'.join(f'<li><span class="ic b">→</span><a href="/tools/careers/{slug(c)}.html" style="color:#60a5fa">{c}</a></li>' for c in d['careers'])

    # Tags come from a broader category-level set (keep them varied by having AI Pick override)
    base_tags = {
      'Engineering': ['Technical expertise','Industry demand'],
      'Medicine':    ['AI-resistant','High stability'],
      'Science':     ['Research foundation','AI collaboration'],
      'Economics':   ['Analytical skills','Policy relevance'],
      'Management':  ['Leadership skills','Entrepreneurship friendly'],
      'Education':   ['Social contribution','Job stability'],
      'Law':         ['Specialized expertise','Regulation growth'],
      'Literature':  ['Creative skills','Content economy'],
      'History':     ['Critical thinking','Cultural depth'],
      'Philosophy':  ['AI ethics demand','Big picture thinking'],
      'Agriculture': ['Food security priority','AgTech growth'],
    }
    tags = base_tags.get(cat, ['Specialized field'])
    tags_html = ''.join(f'<span class="tag">{t}</span>' for t in tags) + (
                '<span class="tag ai">🤖 AI Pick</span>' if is_ai else '')

    # FAQ JSON-LD
    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q['q'],
             "acceptedAnswer": {"@type": "Answer", "text": q['a']}}
            for q in faq
        ]
    }, ensure_ascii=False)

    faq_html = '\n'.join(
        f'''  <div class="faq-item">
    <div class="faq-q">{q['q']}</div>
    <div class="faq-a">{q['a']}</div>
  </div>''' for q in faq
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} Major in China — Career Outlook & AI Analysis 2025–2029</title>
<meta name="description" content="{seo_desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://ordinarymantrying.com/tools/majors/{slug(name)}.html">
<meta property="og:type"        content="article">
<meta property="og:title"       content="Is {name} Worth Studying? Career Outlook 2025–2029">
<meta property="og:description" content="{seo_desc}">
<meta property="og:url"         content="https://ordinarymantrying.com/tools/majors/{slug(name)}.html">
<meta property="og:site_name"   content="Ordinary Man Trying">
<meta name="twitter:card"       content="summary">
<meta name="twitter:title"      content="Is {name} Worth Studying? Career Outlook 2025–2029">
<meta name="twitter:description" content="{seo_desc}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article",
  "headline":"Is {name} Worth Studying in China? Career Outlook 2025–2029",
  "description":"{seo_desc}",
  "url":"https://ordinarymantrying.com/tools/majors/{slug(name)}.html",
  "author":{{"@type":"Person","name":"Ordinary Man Trying","url":"https://ordinarymantrying.com"}}}}
</script>
<script type="application/ld+json">{faq_schema}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:#0f172a;color:#e2e8f0;line-height:1.6;}}
a{{color:#60a5fa;text-decoration:none;}}
a:hover{{text-decoration:underline;}}
.hdr{{background:linear-gradient(160deg,#0d1b2e,#1a3560);padding:32px 20px 24px;
  border-bottom:1px solid #334155;}}
.back{{display:inline-flex;align-items:center;gap:6px;margin-bottom:20px;
  padding:10px 18px;background:rgba(255,255,255,.06);border:1px solid #334155;
  border-radius:10px;font-size:13px;font-weight:600;color:#cbd5e1;
  text-decoration:none;transition:all .15s;}}
.back:hover{{background:rgba(59,130,246,.15);border-color:rgba(59,130,246,.4);
  color:#60a5fa;text-decoration:none;}}
.cat{{font-size:11px;text-transform:uppercase;letter-spacing:.15em;color:#3b82f6;
  font-family:monospace;margin-bottom:8px;}}
h1{{font-size:clamp(22px,5vw,34px);font-weight:800;line-height:1.2;margin-bottom:8px;}}
.stars{{font-size:22px;letter-spacing:2px;margin:10px 0;}}
.tags{{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;}}
.tag{{background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.2);
  border-radius:20px;padding:4px 12px;font-size:12px;color:#93c5fd;}}
.tag.ai{{background:rgba(245,158,11,.1);border-color:rgba(245,158,11,.3);color:#f59e0b;}}
.page{{max-width:680px;margin:0 auto;padding:28px 18px 60px;}}
.card{{background:#1e293b;border:1px solid #334155;border-radius:12px;
  padding:20px;margin-bottom:16px;}}
.card h2{{font-size:12px;text-transform:uppercase;letter-spacing:.1em;
  color:#94a3b8;font-weight:700;margin-bottom:14px;}}
ul{{list-style:none;display:flex;flex-direction:column;gap:8px;}}
li{{font-size:14px;display:flex;gap:8px;align-items:flex-start;}}
.ic{{flex-shrink:0;font-weight:700;font-size:13px;margin-top:1px;}}
.ic.g{{color:#10b981;}}.ic.r{{color:#f87171;}}.ic.b{{color:#3b82f6;}}
.verdict{{background:linear-gradient(135deg,rgba(30,41,59,.9),rgba(15,23,42,.9));
  border:1px solid rgba(59,130,246,.3);border-radius:12px;padding:20px;
  margin-bottom:16px;position:relative;}}
.verdict::before{{content:"🤖 AI Verdict";display:block;font-size:10px;
  text-transform:uppercase;letter-spacing:.12em;color:#3b82f6;font-weight:700;
  margin-bottom:10px;}}
.verdict p{{font-size:14px;line-height:1.75;color:#cbd5e1;}}
.prose{{background:#1e293b;border:1px solid #334155;border-radius:12px;
  padding:20px;margin-bottom:16px;}}
.prose h2{{font-size:12px;text-transform:uppercase;letter-spacing:.1em;
  color:#94a3b8;font-weight:700;margin-bottom:12px;}}
.prose p{{font-size:14px;line-height:1.8;color:#cbd5e1;}}
.faq{{margin-bottom:16px;}}
.faq h2{{font-size:12px;text-transform:uppercase;letter-spacing:.1em;
  color:#94a3b8;font-weight:700;margin-bottom:12px;}}
.faq-item{{background:#1e293b;border:1px solid #334155;border-radius:10px;
  padding:16px;margin-bottom:10px;}}
.faq-q{{font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:8px;}}
.faq-a{{font-size:13px;color:#94a3b8;line-height:1.7;}}
.ask{{display:flex;align-items:center;justify-content:center;gap:8px;
  width:100%;padding:15px;background:#3b82f6;border:none;border-radius:12px;
  font-size:15px;font-weight:700;color:#fff;text-decoration:none;
  margin-bottom:12px;transition:background .15s;}}
.ask:hover{{background:#2563eb;text-decoration:none;}}
.vote-link{{display:block;text-align:center;padding:13px;
  background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);
  border-radius:12px;font-size:14px;font-weight:600;color:#60a5fa;
  transition:all .15s;margin-bottom:12px;}}
.vote-link:hover{{background:rgba(59,130,246,.18);text-decoration:none;}}
.blog-cta{{display:block;margin-bottom:16px;padding:20px 22px;
  background:linear-gradient(135deg,#1e3a5f,#0f172a);
  border:1px solid rgba(59,130,246,.35);border-radius:14px;
  text-decoration:none;transition:border-color .15s;}}
.blog-cta:hover{{border-color:rgba(59,130,246,.7);text-decoration:none;}}
.blog-cta-label{{font-size:11px;text-transform:uppercase;letter-spacing:.1em;
  color:#3b82f6;font-weight:700;margin-bottom:6px;}}
.blog-cta-title{{font-size:16px;font-weight:800;color:#e2e8f0;margin-bottom:4px;}}
.blog-cta-sub{{font-size:13px;color:#64748b;}}
.foot{{text-align:center;padding:20px;font-size:12px;color:#475569;
  border-top:1px solid #1e293b;}}
</style>
</head>
<body>
<div class="hdr">
  <a class="back" href="/tools/major-vote.html">← Back to All 757 Majors — Vote &amp; Compare</a>
  <div class="cat">{field}</div>
  <h1>{name}{ai_badge}</h1>
  <div class="stars">{stars_html(rating)}</div>
  <div style="font-size:13px;color:#94a3b8;">Future outlook rating · Part of a 5-year crowdsourced experiment</div>
  <div class="tags">{tags_html}</div>
</div>

<div class="page">

  <div class="prose">
    <h2>What is {sub}?</h2>
    <p>{what_is}</p>
  </div>

  <div class="verdict">
    <p>{verdict}</p>
  </div>

  <div class="prose">
    <h2>Future Outlook 2025–2029</h2>
    <p>{outlook_p}</p>
  </div>

  <div class="card">
    <h2>Pros</h2>
    <ul>{pros_html}</ul>
  </div>

  <div class="card">
    <h2>Cons</h2>
    <ul>{cons_html}</ul>
  </div>

  <div class="card">
    <h2>Related Careers</h2>
    <ul>{careers_html}</ul>
  </div>

  <div class="faq">
    <h2>Frequently Asked Questions</h2>
{faq_html}
  </div>

  <a class="ask" href="{px_url}" target="_blank" rel="noopener">
    🤖 Ask AI for deeper analysis →
  </a>

  <a class="vote-link" href="/tools/major-vote.html">
    ▲ Vote for {name} — see where it ranks among all 757 majors →
  </a>

  <a class="blog-cta" href="https://ordinarymantrying.com/building-in-public-experiment/" target="_blank" rel="noopener">
    <div class="blog-cta-label">📺 Building in Public — 5-Year Experiment</div>
    <div class="blog-cta-title">One ordinary person. No audience. No guarantee. Building this from scratch — with real numbers.</div>
    <div class="blog-cta-sub">Follow the journey → ordinarymantrying.com</div>
  </a>
</div>

<div class="foot">
  Data: Ministry of Education of China · Undergraduate Majors Directory 2024<br>
  Built by <a href="https://ordinarymantrying.com">Ordinary Man Trying</a>
</div>
</body>
</html>'''

# ── Generate ──────────────────────────────────────────────────────
out_dir = "ordinarymantrying.com/tools/majors"
os.makedirs(out_dir, exist_ok=True)

slugs_used = {}
count = 0
for major in ALL:
    s = slug(major['n'])
    if s in slugs_used:
        slugs_used[s] += 1
        s = f"{s}-{slugs_used[s]}"
    else:
        slugs_used[s] = 1

    with open(os.path.join(out_dir, f"{s}.html"), "w", encoding="utf-8") as f:
        f.write(page(major))
    count += 1
    if count % 100 == 0:
        print(f"  {count}/757...")

print(f"\n✓ {count} pages generated (Layer 1+2+3 + FAQ SEO)")

# Spot-check
ai_sample = [m for m in ALL if m['c'] in AIPICK][0]
plain_sample = ALL[50]
for m in [ai_sample, plain_sample]:
    sub = m.get('sub', m['cat'])
    d   = SUBCAT.get(sub, DEFAULT_SUBCAT)
    r   = min(5, d['stars'] + (1 if m['c'] in AIPICK else 0))
    print(f"\n  {m['n']} [{sub}] ★{r}")
    print(f"  Pros: {d['pros'][0][:60]}...")
    print(f"  Verdict: {build_verdict(m,r,m['c'] in AIPICK)[:80]}...")
