#!/usr/bin/env python3
"""Generate P3 career pages — /tools/careers/[slug].html"""
import re, os, json, unicodedata

# ── Load ALL + SUBCAT from major vote page ───────────────────────
with open("ordinarymantrying.com/tools/major-vote.html", encoding="utf-8") as f:
    mvh = f.read()
m = re.search(r'const ALL\s*=\s*(\[.*?\]);', mvh, re.DOTALL)
ALL = json.loads(m.group(1))
m2 = re.search(r'const AIPICK\s*=\s*new Set\(\[(.*?)\]\)', mvh)
AIPICK = set(x.strip().strip('"') for x in m2.group(1).split(','))

with open("generate_major_pages.py", encoding="utf-8") as f:
    src = f.read()

subcat_entries = re.findall(
    r"'([^']+)':\s*\{[^}]*'careers':\s*\[([^\]]+)\][^}]*'stars':\s*(\d)", src, re.DOTALL)

SUBCAT_MAP = {}   # sub → {stars, careers}
for sub, cars_raw, stars in subcat_entries:
    car_list = re.findall(r"'([^']+)'", cars_raw)
    SUBCAT_MAP[sub] = {'stars': int(stars), 'careers': car_list}

# career → list of subs
CAREER_SUBS = {}
for sub, data in SUBCAT_MAP.items():
    for c in data['careers']:
        CAREER_SUBS.setdefault(c, []).append(sub)

def slug(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def major_slug(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def stars_html(n): return '★' * n + '☆' * (5 - n)

# ── Career-specific data ─────────────────────────────────────────
# Format: 'Career Name': (intro_sentence, skills_list, monthly_salary_range, ai_tag)
# ai_tag: 'immune'|'resistant'|'augmented'|'at_risk'
CAREER_DATA = {
'Quantum Computing Researcher':('You design algorithms and hardware architectures for quantum processors, working at the boundary of physics and computer science to solve problems classical computers cannot.',['Quantum mechanics','Linear algebra','Qiskit/Cirq','Error correction','Python/C++'],'¥25,000–60,000','resistant'),
'Photonics Engineer':('You develop optical systems, lasers, and photonic integrated circuits for telecommunications, medical devices, and precision sensing applications.',['Optical design','Laser physics','FDTD simulation','Semiconductor fab','Signal processing'],'¥18,000–40,000','augmented'),
'Advanced Systems Scientist':('You conduct research at the intersection of multiple engineering disciplines, often for national defense or deep-tech applications requiring security clearance.',['Systems modeling','Multidisciplinary optimization','Scientific computing','R&D project management','Technical writing'],'¥20,000–45,000','resistant'),
'Aerospace Engineer':('You design aircraft, spacecraft, and propulsion systems, working on aerodynamics, structural analysis, and flight mechanics.',['CAD/FEA software','Aerodynamics','Propulsion theory','MATLAB/Simulink','Materials science'],'¥15,000–35,000','augmented'),
'Propulsion Engineer':('You develop and test rocket engines, jet engines, and alternative propulsion systems for aerospace and defense applications.',['Thermodynamics','Combustion theory','CFD simulation','Engine testing','Systems integration'],'¥18,000–40,000','augmented'),
'Satellite Systems Specialist':('You design and operate satellite communications, Earth observation, and navigation systems, integrating hardware with ground control software.',['Orbital mechanics','RF systems','Embedded software','Systems engineering','GNC algorithms'],'¥18,000–38,000','augmented'),
'Aerospace Stress Analyst':('You calculate structural loads, fatigue life, and failure modes of aerospace components to ensure airworthiness and mission reliability.',['FEA (ANSYS/Abaqus)','Fracture mechanics','MATLAB','Technical documentation','Aerospace standards'],'¥14,000–30,000','augmented'),
'AgTech Field Agronomist':('You apply precision agriculture technologies — drones, sensors, and AI — to optimize crop yields, soil health, and resource usage on commercial farms.',['Soil science','Drone operation','GIS/remote sensing','Crop physiology','Data analysis'],'¥8,000–18,000','augmented'),
'AgTech Product Developer':('You build agricultural technology products, bridging engineering and farming expertise to create solutions for precision irrigation, automation, and monitoring.',['Product development','IoT systems','Agricultural domain knowledge','User research','Python'],'¥10,000–22,000','augmented'),
'Agribusiness Manager':('You oversee commercial agricultural operations, managing supply chains, finances, and market relationships for large-scale food production businesses.',['Supply chain management','Agricultural economics','Financial analysis','Contract negotiation','Risk management'],'¥10,000–25,000','augmented'),
'Agricultural Supply Chain Director':('You manage the end-to-end movement of agricultural products from farm to market, coordinating with logistics, processing, and retail partners.',['Supply chain optimization','Cold chain logistics','ERP systems','Vendor management','Agricultural markets'],'¥15,000–35,000','augmented'),
'Animal Disease Control Officer':('You monitor, diagnose, and manage infectious disease outbreaks in livestock populations, working with government agencies and farms to prevent economic losses.',['Veterinary epidemiology','Diagnostic lab techniques','Disease surveillance','Regulatory compliance','Field investigation'],'¥8,000–18,000','resistant'),
'Animal Science Researcher':('You conduct scientific studies on animal genetics, nutrition, reproduction, and behavior to improve livestock productivity and welfare.',['Animal genetics','Experimental design','Statistical analysis','Lab techniques','Scientific writing'],'¥7,000–16,000','augmented'),
'Aquaculture Manager':('You oversee fish and shellfish farming operations, managing water quality, feeding systems, disease prevention, and harvest logistics.',['Aquatic biology','Water chemistry','Farm management','Disease control','Export regulations'],'¥8,000–18,000','augmented'),
'Architect':('You design buildings and spaces, balancing aesthetics, function, structural integrity, and regulatory compliance across residential, commercial, and public projects.',['AutoCAD/Revit/BIM','Structural basics','Building codes','Client communication','Project management'],'¥10,000–30,000','augmented'),
'BIM Specialist':('You create and manage Building Information Modeling data for construction projects, coordinating between architects, engineers, and contractors through the digital twin.',['Revit','Navisworks','IFC standards','Clash detection','Construction sequencing'],'¥10,000–22,000','augmented'),
'Urban Designer':('You shape the form and function of cities — designing streetscapes, public spaces, transit corridors, and mixed-use developments at the neighborhood scale.',['Urban planning theory','GIS','AutoCAD/SketchUp','Community engagement','Regulatory processes'],'¥10,000–25,000','augmented'),
'Astrophysicist':('You study celestial objects, dark matter, and the large-scale structure of the universe, publishing research and often working in academia or national observatories.',['Python/Julia','Statistical modeling','Telescope operation','Data reduction','Scientific writing'],'¥8,000–20,000','resistant'),
'Space Agency Researcher':('You contribute to national space programs through research in orbital mechanics, space physics, or remote sensing, often employed by CNSA or affiliated institutes.',['Orbital dynamics','Remote sensing','Satellite data processing','Systems engineering','Scientific communication'],'¥12,000–28,000','resistant'),
'Data Scientist (from computational astronomy)':('You apply advanced data analysis and machine learning skills — honed on astronomical datasets — to industries including finance, tech, and healthcare.',['Python/R','Machine learning','Big data pipelines','Statistical modeling','Data visualization'],'¥15,000–35,000','augmented'),
'Athletic Performance Coach':('You design and implement training programs for professional and amateur athletes, using sports science to optimize performance and prevent injury.',['Exercise physiology','Strength and conditioning','Biomechanics','Nutrition science','Athlete psychology'],'¥8,000–25,000','resistant'),
'Sports Health Manager':('You oversee athlete health programs, coordinating medical screening, rehabilitation, and performance monitoring for sports teams and academies.',['Sports medicine','Team management','Injury prevention','Medical coordination','Health data systems'],'¥10,000–22,000','resistant'),
'PE Teacher':('You deliver physical education curricula in schools, developing students\' motor skills, fitness, and sports knowledge while promoting lifelong healthy habits.',['Physical education pedagogy','Sports skills','First aid','Student assessment','Curriculum design'],'¥6,000–15,000','resistant'),
'Atmospheric Research Scientist':('You study weather systems, climate change, and air quality using observational data and numerical models, contributing to forecasts and environmental policy.',['Atmospheric modeling (WRF/CMAQ)','Python/Fortran','Data assimilation','Scientific writing','Remote sensing'],'¥10,000–22,000','augmented'),
'Meteorologist':('You analyze atmospheric data to produce weather forecasts, severe weather warnings, and climate assessments for public services, aviation, and agriculture.',['NWP models','GIS/radar analysis','Data interpretation','Public communication','Emergency protocols'],'¥8,000–18,000','augmented'),
'Climate Data Scientist':('You process large atmospheric and oceanic datasets to identify climate trends, build predictive models, and support policy decisions on emissions and adaptation.',['Python/R','Machine learning','Climate model output (CMIP)','Statistical analysis','Scientific communication'],'¥12,000–28,000','augmented'),
'Automation Engineer':('You design, program, and maintain automated manufacturing systems, integrating PLCs, robots, sensors, and control software in industrial environments.',['PLC programming','Robot programming (KUKA/ABB)','SCADA systems','Electrical engineering','Process optimization'],'¥12,000–28,000','augmented'),
'Robotics Systems Integrator':('You deploy and commission robotic systems in factories, warehouses, and service environments, ensuring they work reliably within existing production lines.',['Robot programming','Mechanical integration','Computer vision','Safety standards','Troubleshooting'],'¥15,000–32,000','augmented'),
'Industrial IoT Specialist':('You connect factory equipment and sensors to cloud platforms, enabling real-time monitoring, predictive maintenance, and data-driven process optimization.',['IoT protocols (MQTT/OPC-UA)','Edge computing','Cloud platforms (AWS/Azure)','Industrial networking','Data pipelines'],'¥14,000–30,000','augmented'),
'Biomedical Researcher':('You investigate disease mechanisms at the molecular and cellular level, developing new therapies and diagnostic tools in academic or pharma lab settings.',['Molecular biology techniques','CRISPR/gene editing','Animal models','Statistical analysis','Grant writing'],'¥10,000–22,000','resistant'),
'Medical AI Data Analyst':('You build and validate AI models for clinical applications — diagnostic imaging, patient risk scoring, and drug response prediction.',['Python/PyTorch','Medical imaging (DICOM)','Clinical data standards (HL7/FHIR)','Regulatory knowledge','Statistical validation'],'¥15,000–35,000','augmented'),
'Pharmaceutical Scientist':('You conduct research into drug discovery, formulation, and pharmacokinetics, working in academic labs or pharmaceutical company R&D departments.',['Drug formulation','HPLC/mass spectrometry','Animal studies','Regulatory submission','Scientific writing'],'¥12,000–28,000','resistant'),
'Battery Materials Researcher':('You develop new electrode materials, electrolytes, and cell architectures for lithium-ion, solid-state, and next-generation batteries.',['Electrochemistry','Materials characterization (XRD/SEM)','Battery cycling','Python','Technical reporting'],'¥15,000–35,000','augmented'),
'Biostatistician':('You apply statistical methods to design clinical trials, analyze biological data, and support evidence-based conclusions in medical and pharmaceutical research.',['R/SAS','Clinical trial design','Survival analysis','Regulatory statistics (ICH E9)','Scientific writing'],'¥15,000–32,000','augmented'),
'Biotech Research Scientist':('You engineer biological systems — cell lines, proteins, microorganisms — for applications in medicine, agriculture, and industrial biotechnology.',['Genetic engineering','Cell culture','Protein expression','Flow cytometry','Scientific communication'],'¥12,000–28,000','resistant'),
'Genomics Data Analyst':('You process whole-genome sequencing data to identify variants, study gene expression, and support personalized medicine or agricultural breeding programs.',['Bioinformatics pipelines','Python/R','Linux/HPC','NGS data (FASTQ/VCF)','Population genetics'],'¥14,000–32,000','augmented'),
'Cell Therapy Development Specialist':('You develop CAR-T cells, stem cell therapies, and other cellular medicine products, working in biotech companies or hospital-based cell therapy centers.',['Cell processing GMP','Flow cytometry','Viral vector production','Regulatory knowledge','Quality systems'],'¥18,000–45,000','resistant'),
'Brand Communications Manager':('You develop and execute brand messaging strategies across channels, managing content teams and agency relationships to maintain consistent brand identity.',['Brand strategy','Content management','Social media analytics','Campaign management','Creative direction'],'¥10,000–25,000','at_risk'),
'Business Development Manager':('You identify new market opportunities, build partner relationships, and close deals that expand the company\'s revenue base and strategic positioning.',['Sales strategy','Negotiation','CRM systems','Market analysis','Relationship management'],'¥12,000–30,000','augmented'),
'Operations Director':('You lead day-to-day business operations, managing processes, teams, and resources to deliver products and services efficiently and profitably.',['Operations management','P&L ownership','Process optimization','People management','Data-driven decision making'],'¥20,000–50,000','augmented'),
'Entrepreneur / Startup Founder':('You build new businesses from scratch, combining product vision, team leadership, and fundraising to create scalable ventures.',['Product strategy','Fundraising','Team building','Market validation','Resilience'],'¥0–unlimited','resistant'),
'Carbon Accounting Specialist':('You measure and report greenhouse gas emissions for corporations and governments, supporting carbon disclosure, offset programs, and net-zero planning.',['GHG Protocol standards','Carbon accounting software','ESG reporting','Regulatory knowledge','Data analysis'],'¥10,000–22,000','augmented'),
'Forestry Engineer':('You manage commercial timber operations, forest restoration projects, and carbon forestry programs, balancing ecological and economic objectives.',['Forest inventory','GIS','Silviculture','Carbon measurement','Project management'],'¥7,000–15,000','augmented'),
'Remote Sensing Analyst':('You process satellite and aerial imagery to monitor land cover, deforestation, crop health, and environmental change for government and commercial clients.',['QGIS/ArcGIS','Python (rasterio/GDAL)','Image classification','Drone data','Scientific reporting'],'¥10,000–22,000','augmented'),
'Carbon Credit Analyst':('You assess, verify, and trade voluntary carbon credits, evaluating offset project quality and supporting corporate net-zero procurement strategies.',['Carbon markets','Project verification standards (Verra/Gold Standard)','Financial analysis','ESG frameworks','Report writing'],'¥12,000–28,000','augmented'),
'Pharmaceutical Regulatory Affairs Manager':('You navigate the complex regulatory approval process for drugs and medical devices, preparing submissions for NMPA, FDA, and EMA review.',['Regulatory strategy','CTD dossier preparation','Clinical data interpretation','Agency negotiation','Quality systems'],'¥15,000–38,000','resistant'),
'Clinical Pharmacist':('You provide medication management services in hospitals, advising physicians on drug selection, dosing, and interactions for complex patient cases.',['Pharmacology','Clinical protocols','Drug interaction databases','Patient counseling','ICU/oncology specialization'],'¥8,000–20,000','resistant'),
'Drug Safety Specialist':('You monitor adverse event reports, conduct signal detection analyses, and prepare pharmacovigilance submissions to ensure ongoing drug safety.',['Pharmacovigilance (MedDRA)','Signal detection','Regulatory reporting','Medical writing','Database systems'],'¥12,000–28,000','resistant'),
'Process Engineer':('You design and optimize chemical manufacturing processes, scaling laboratory reactions to industrial production while meeting safety and quality standards.',['Chemical engineering fundamentals','Process simulation (Aspen)','Safety analysis (HAZOP)','GMP/GLP','Technical writing'],'¥10,000–22,000','augmented'),
'Pharmaceutical Chemist':('You synthesize and analyze chemical compounds for drug development, quality control, and manufacturing, working in pharma or chemical industry settings.',['Organic synthesis','HPLC/NMR','Analytical methods','Lab safety','Documentation'],'¥10,000–22,000','augmented'),
'Energy Storage Researcher':('You develop new battery chemistries and supercapacitor technologies to improve energy density, cycle life, and safety for EVs and grid storage.',['Electrochemistry','Materials synthesis','Characterization tools','Python','Research methodology'],'¥12,000–28,000','augmented'),
'Materials Chemist':('You develop and characterize new materials — polymers, composites, catalysts, coatings — for applications across electronics, automotive, and clean energy.',['Materials synthesis','XRD/SEM/TEM','Polymer chemistry','Computational modeling','Technical writing'],'¥10,000–22,000','augmented'),
'Pharmaceutical Production Specialist':('You operate and optimize drug manufacturing processes, ensuring GMP compliance, yield targets, and product quality in pharmaceutical production facilities.',['GMP operations','Batch record review','Equipment qualification','Quality systems','Deviation management'],'¥8,000–18,000','augmented'),
'Civil Servant':('You serve in government agencies at national, provincial, or municipal levels, implementing policy, managing public services, and administering regulations.',['Policy analysis','Administrative law','Public communication','Report writing','Inter-agency coordination'],'¥6,000–15,000','resistant'),
'Infrastructure Planner':('You develop long-range plans for roads, bridges, utilities, and public facilities, coordinating between government agencies, engineers, and communities.',['Transport planning','GIS','Cost-benefit analysis','Stakeholder engagement','Urban planning law'],'¥10,000–22,000','augmented'),
'Structural Engineer':('You design the load-bearing elements of buildings and infrastructure, ensuring safety and performance under gravity, wind, seismic, and dynamic loads.',['Structural analysis (SAP2000/ETABS)','Reinforced concrete/steel design','Building codes','AutoCAD','Site inspection'],'¥10,000–25,000','augmented'),
'Project Manager':('You lead construction and infrastructure projects from planning through delivery, managing budgets, schedules, contractors, and client relationships.',['MS Project/Primavera','Contract management','Risk assessment','Budget control','Team leadership'],'¥12,000–30,000','augmented'),
'Corporate Lawyer':('You advise companies on commercial transactions, mergers, employment law, and regulatory compliance, drafting contracts and managing legal risk.',['Contract law','Due diligence','Negotiation','Legal drafting','Corporate governance'],'¥15,000–50,000','resistant'),
'International Arbitration Counsel':('You represent clients in cross-border disputes resolved through arbitration panels, requiring expertise in international commercial law and evidentiary procedure.',['International arbitration rules (ICC/SIAC)','Cross-examination','Evidence management','Legal writing','Foreign language skills'],'¥25,000–80,000','resistant'),
'Legal Compliance Specialist':('You ensure that corporations adhere to applicable laws, regulations, and internal policies, conducting audits, training staff, and advising on risk.',['Regulatory knowledge','Compliance frameworks','Internal audit','Training design','Documentation'],'¥12,000–28,000','resistant'),
'Content Strategist':('You develop content plans that align with business objectives, overseeing production across blogs, video, social media, and SEO-driven channels.',['SEO','Content calendar management','Analytics','Editorial direction','AI tools proficiency'],'¥8,000–20,000','at_risk'),
'Content Strategy Director':('You lead content strategy at an organizational level, setting editorial direction, managing teams, and aligning content investment with measurable business outcomes.',['Content strategy','Team leadership','Data analytics','Brand voice','Budget management'],'¥20,000–45,000','at_risk'),
'Editor':('You commission, shape, and refine written content for publishers, media companies, or corporate communications, ensuring quality, clarity, and audience relevance.',['Editorial judgment','Manuscript development','Fact-checking','Style guides','Author management'],'¥7,000–18,000','at_risk'),
'Screenwriter / Cultural Consultant':('You write scripts for film, television, and online media, often advising on cultural authenticity for productions depicting Chinese stories and settings.',['Narrative structure','Dialogue writing','Cultural research','Pitch development','Industry knowledge'],'¥8,000–unlimited','resistant'),
'Data Journalist':('You combine data analysis skills with storytelling to produce investigative reports that reveal patterns in public records, government data, and scientific datasets.',['Data visualization','SQL/Python','Statistical literacy','Investigative reporting','CMS tools'],'¥8,000–20,000','augmented'),
'EV Electrical Engineer':('You design and validate electrical systems for electric vehicles — battery management systems, motor drives, power electronics, and charging infrastructure.',['Power electronics','BMS design','CAN bus/automotive protocols','EMC testing','MATLAB/Simulink'],'¥15,000–35,000','augmented'),
'Power Systems Engineer':('You design and operate electrical power grids, ensuring reliable generation, transmission, and distribution of electricity at utility scale.',['Power flow analysis','SCADA','Relay protection','Grid standards','Emergency operations'],'¥12,000–28,000','augmented'),
'Smart Grid Specialist':('You integrate renewable energy, storage, and demand response into intelligent electricity networks, enabling real-time optimization of power flows.',['Energy management systems','Smart meter data','Power electronics','IoT protocols','Grid cybersecurity'],'¥14,000–32,000','augmented'),
'Earthquake Risk Analyst':('You assess seismic hazard and vulnerability for buildings, infrastructure, and insurance portfolios, supporting disaster preparedness and engineering design.',['Seismic hazard analysis','GIS','Structural vulnerability models','Risk quantification','Technical reporting'],'¥10,000–22,000','augmented'),
'Geophysicist':('You collect and interpret subsurface geophysical data to support oil and gas exploration, mineral prospecting, and geotechnical engineering projects.',['Seismic data interpretation','Gravity/magnetics','Petrophysics','Workstation software','Field surveys'],'¥12,000–28,000','augmented'),
'Seismic Data Interpreter':('You analyze 2D and 3D seismic datasets to map subsurface structures, identify hydrocarbon reservoirs, and support drilling decisions.',['Seismic interpretation software (Petrel)','Structural geology','Petrophysics','Reservoir modeling','Technical reporting'],'¥15,000–35,000','augmented'),
'Remote Sensing Specialist':('You process satellite and aerial imagery for environmental monitoring, land use mapping, and resource assessment using GIS and machine learning tools.',['QGIS/ENVI','Python/Google Earth Engine','Image classification','Field validation','Technical reporting'],'¥10,000–22,000','augmented'),
'GIS Analyst':('You build and analyze spatial datasets to support urban planning, environmental management, logistics, and public health decision-making.',['ArcGIS/QGIS','Spatial SQL','Python (GeoPandas)','Cartography','Data management'],'¥8,000–18,000','augmented'),
'Urban Data Scientist':('You apply machine learning and spatial analysis to urban datasets — traffic, housing, utilities, demographics — to inform city planning and smart city initiatives.',['Python','Spatial analysis','Machine learning','Urban informatics','Data visualization'],'¥14,000–32,000','augmented'),
'Exploration Geologist':('You survey terrain and subsurface conditions to identify mineral, oil, or groundwater resources, combining fieldwork with laboratory and remote sensing analysis.',['Geological mapping','GIS/remote sensing','Geochemistry','Drilling program design','Field reporting'],'¥10,000–22,000','augmented'),
'Environmental Site Assessor':('You conduct Phase I and Phase II environmental site assessments to identify contamination, liability, and regulatory compliance issues for real estate and industrial projects.',['Soil sampling','Environmental law','Risk assessment','Report writing','Remediation planning'],'¥8,000–18,000','augmented'),
'Hydrogeologist':('You study groundwater systems to support water supply planning, contamination remediation, and environmental impact assessments.',['Aquifer characterization','MODFLOW modeling','Water sampling','Environmental regulations','Technical reporting'],'¥10,000–22,000','augmented'),
'Geology Engineering':('You apply geological knowledge to engineering projects — tunnels, dams, foundations, and slopes — assessing ground conditions and designing stabilization solutions.',['Rock mechanics','Geotechnical testing','Site investigation','Engineering geology standards','CAD'],'¥10,000–22,000','augmented'),
'Environmental Remediation Specialist':('You design and manage cleanup programs for contaminated soil, groundwater, and industrial sites, using physical, chemical, and biological treatment technologies.',['Remediation technologies','Regulatory compliance','Project management','Risk assessment','Stakeholder communication'],'¥10,000–22,000','augmented'),
'GIS Specialist':('You develop spatial databases, automate geospatial workflows, and build map applications to support decision-making across government and commercial organizations.',['ArcGIS Pro/QGIS','Python scripting','PostGIS','Web mapping (Leaflet)','Spatial statistics'],'¥10,000–25,000','augmented'),
'Spatial Data Engineer':('You build the data infrastructure — pipelines, databases, and APIs — that powers GIS applications and geospatial analytics at scale.',['PostGIS','Python/SQL','Cloud GIS (AWS/Azure)','ETL pipelines','Big geodata'],'¥15,000–35,000','augmented'),
'Energy Storage Researcher':('You investigate new materials and chemistries for batteries and supercapacitors, targeting improvements in energy density, cycle life, and safety.',['Electrochemistry','Materials synthesis','Battery characterization','Python','Research methodology'],'¥12,000–28,000','augmented'),
'Power Plant Engineer':('You operate and maintain thermal, hydro, nuclear, or renewable power generation facilities, ensuring safe and efficient electricity production.',['Power plant systems','Thermodynamics','Safety protocols','SCADA operation','Maintenance planning'],'¥10,000–25,000','augmented'),
'Nuclear Reactor Engineer':('You design, operate, and maintain nuclear reactors for power generation or research, applying nuclear physics and engineering principles within strict safety frameworks.',['Nuclear physics','Reactor design','Safety systems','Regulatory compliance','Radiation protection'],'¥18,000–40,000','resistant'),
'Nuclear Fuel Systems Analyst':('You model nuclear fuel behavior, optimize fuel loading patterns, and assess fuel performance to maximize reactor efficiency and safety margins.',['Neutronic modeling (CASMO/SIMULATE)','Thermal hydraulics','Reactor physics','Safety analysis','Technical reporting'],'¥18,000–40,000','resistant'),
'Radiation Safety Specialist':('You monitor radiation levels, design shielding, and implement safety programs to protect workers and the public at nuclear facilities and medical centers.',['Dosimetry','Radiation detection instruments','Regulatory standards','Emergency response','Training delivery'],'¥12,000–28,000','resistant'),
'Nuclear Systems Engineer':('You design engineered systems — cooling, containment, instrumentation — that keep nuclear plants operating safely within design limits.',['Systems engineering','Thermal hydraulics','Safety analysis codes','Regulatory standards','Technical documentation'],'¥18,000–40,000','resistant'),
'Marine Systems Engineer':('You design and test ships, submarines, and offshore structures, applying naval architecture and ocean engineering principles.',['Naval architecture software','Structural analysis','Hydrodynamics','Marine regulations','CAD/CAM'],'¥12,000–28,000','augmented'),
'Ocean Data Scientist':('You analyze oceanographic data from sensors, satellite altimetry, and models to study currents, temperature, and marine ecosystems.',['Python/R','Ocean modeling (ROMS/MOM6)','Data assimilation','Machine learning','Scientific writing'],'¥12,000–25,000','augmented'),
'Offshore Structural Engineer':('You design and certify platforms, pipelines, and subsea equipment for the offshore oil, gas, and wind energy industries.',['Structural analysis','Marine regulations (DNV/ABS)','FEA software','Offshore installation','Project management'],'¥15,000–35,000','augmented'),
'Oceanographer':('You study the physical, chemical, biological, and geological properties of the oceans, contributing to climate science, fisheries management, and marine policy.',['Oceanographic instruments','Statistical analysis','Scientific diving/fieldwork','Data visualization','Research publishing'],'¥10,000–22,000','resistant'),
'Marine Data Scientist':('You analyze large marine and climate datasets to model ocean dynamics, track pollution, and support blue economy and climate adaptation planning.',['Python/R','Machine learning','Satellite data','Ocean circulation models','Scientific communication'],'¥12,000–28,000','augmented'),
'Offshore Resource Specialist':('You evaluate and manage marine mineral, oil, gas, and renewable energy resources in offshore zones, working with regulatory and commercial stakeholders.',['Resource assessment','Environmental impact','Marine law','GIS','Project economics'],'¥15,000–35,000','augmented'),
'Ordnance Engineer':('You research, design, and test munitions, warheads, and propellants for defense applications, working within national security frameworks.',['Explosives engineering','Ballistics','Safety protocols','Defense procurement','Technical documentation'],'¥12,000–28,000','resistant'),
'Military Equipment Analyst':('You assess military hardware performance, capability gaps, and procurement requirements, advising defense organizations on equipment selection and modernization.',['Defense systems knowledge','Technical analysis','Requirements engineering','Security clearance protocols','Report writing'],'¥12,000–28,000','resistant'),
'Weapons Systems Engineer':('You develop integrated weapons systems, coordinating across sensors, guidance, and warhead subsystems to meet military performance specifications.',['Systems engineering','Guidance and control','Signal processing','Defense standards','Project management'],'¥15,000–38,000','resistant'),
'Mine Safety Specialist':('You identify, assess, and mitigate hazards in mining operations, ensuring compliance with safety regulations and designing emergency response procedures.',['Mining safety regulations','Hazard analysis','Safety management systems','Training delivery','Incident investigation'],'¥10,000–22,000','augmented'),
'Critical Minerals Analyst':('You research supply chains, geopolitics, and market dynamics for lithium, cobalt, rare earths, and other minerals critical to the clean energy transition.',['Commodity markets','Supply chain analysis','Geopolitical risk','Financial modeling','Research writing'],'¥12,000–28,000','augmented'),
'Mining Engineer':('You design and manage the extraction of coal, metals, and industrial minerals, balancing productivity, safety, and environmental impact.',['Mine planning software','Rock mechanics','Blast design','Environmental compliance','Project management'],'¥10,000–25,000','augmented'),
'Mine Site Engineer':('You oversee day-to-day mining operations on site, managing equipment, personnel, safety compliance, and production targets.',['Mine operations','Equipment management','Blast coordination','Safety supervision','Cost control'],'¥10,000–22,000','augmented'),
'Environmental Consultant':('You advise companies and governments on environmental compliance, impact assessment, and sustainability strategy, navigating complex regulatory requirements.',['EIA preparation','Environmental law','Stakeholder engagement','Data analysis','Report writing'],'¥10,000–25,000','augmented'),
'Pollution Control Engineer':('You design and operate systems to capture, treat, and reduce air, water, and soil pollution from industrial and municipal sources.',['Treatment technology design','Environmental regulations','Process engineering','Monitoring systems','Permitting'],'¥10,000–22,000','augmented'),
'Conservation Ecologist':('You study and protect biodiversity in natural and degraded ecosystems, designing restoration programs and advising on land use decisions.',['Field ecology','Species identification','GIS','Statistical analysis','Conservation planning'],'¥7,000–16,000','resistant'),
'National Reserve Manager':('You oversee the operations, visitor management, and conservation programs of nature reserves and protected areas.',['Protected area management','Wildlife monitoring','Stakeholder relations','Budget management','Environmental law'],'¥7,000–15,000','resistant'),
'Natural Capital Analyst':('You quantify the economic value of ecosystems — forests, wetlands, fisheries — to support biodiversity finance and environmental accounting.',['Ecosystem services frameworks','Economic valuation','GIS','ESG reporting','Research writing'],'¥12,000–25,000','augmented'),
'Instrumentation Engineer':('You design, calibrate, and maintain precision measurement instruments used in manufacturing, research, and quality control.',['Metrology','Sensor systems','PLC/SCADA','Calibration standards','Technical documentation'],'¥10,000–22,000','augmented'),
'Metrology Specialist':('You develop and apply measurement standards, ensuring the traceability and accuracy of physical, chemical, and dimensional measurements.',['Metrology theory','Calibration lab','Uncertainty analysis','ISO 17025','Quality systems'],'¥10,000–22,000','augmented'),
'Quality Assurance Engineer':('You design and implement quality control systems, conduct inspections, and analyze failure data to ensure product reliability and regulatory compliance.',['Quality management systems (ISO 9001)','Statistical process control','Root cause analysis','Audit skills','Documentation'],'¥8,000–20,000','augmented'),
'Manufacturing Quality Manager':('You lead quality assurance operations in manufacturing plants, managing inspection teams, supplier quality programs, and corrective action processes.',['Quality management','Six Sigma/Lean','SPC','Supplier auditing','People management'],'¥12,000–28,000','augmented'),
'Packaging Technology Specialist':('You design and optimize packaging solutions for consumer goods, balancing material performance, cost, sustainability, and manufacturing compatibility.',['Packaging materials','CAD/3D modeling','Supply chain knowledge','Sustainability standards','Testing protocols'],'¥8,000–18,000','augmented'),
'Product Design Engineer':('You develop new consumer and industrial products, leading design from concept through prototyping, testing, and production launch.',['CAD (SolidWorks/Fusion 360)','DFM/DFA','Prototyping','Materials selection','Project management'],'¥10,000–25,000','augmented'),
'Technical Textile Engineer':('You develop high-performance textiles for medical, automotive, aerospace, and protective applications, applying materials science to fiber and fabric engineering.',['Textile testing','Materials science','Process engineering','Technical standards','Product development'],'¥8,000–18,000','augmented'),
'Textile Process Manager':('You manage production lines in textile and apparel manufacturing, optimizing yield, quality, and cost while ensuring worker safety.',['Production management','Lean manufacturing','Quality control','Cost analysis','Supplier management'],'¥8,000–18,000','at_risk'),
'Sustainable Materials Specialist':('You research and source sustainable alternatives to conventional textiles and materials, working with brands and suppliers on environmental certification.',['Sustainability standards','Supply chain tracing','Materials science','ESG reporting','Supplier relations'],'¥10,000–22,000','augmented'),
'Mechanical Engineer':('You design machines, components, and systems for manufacturing, energy, transportation, and consumer products — one of the broadest engineering disciplines.',['CAD (SolidWorks/CATIA)','FEA','Thermodynamics','Manufacturing processes','Technical documentation'],'¥10,000–25,000','augmented'),
'Manufacturing Systems Manager':('You design and optimize integrated manufacturing systems, combining industrial engineering, automation, and supply chain to achieve operational excellence.',['Lean/Six Sigma','MES systems','Automation integration','Cost modeling','Operations management'],'¥15,000–35,000','augmented'),
'Robotics Design Engineer':('You create mechanical and electromechanical designs for robotic systems — manipulators, mobile platforms, and end-effectors — across industrial and service applications.',['Robot kinematics','CAD/CAM','Mechanism design','Sensor integration','Prototyping'],'¥14,000–32,000','augmented'),
'Structural Mechanics Researcher':('You conduct theoretical and computational research on stress, strain, fatigue, and fracture behavior in engineering structures and materials.',['FEA (ANSYS/Abaqus)','Continuum mechanics','Python/MATLAB','Scientific writing','Experimental testing'],'¥10,000–22,000','augmented'),
'Engineering R&D Specialist':('You develop new mechanical systems and components through a cycle of design, prototyping, testing, and iteration, often in automotive, aerospace, or heavy industry.',['CAD/CAM','Prototyping','Testing protocols','Materials science','R&D documentation'],'¥12,000–28,000','augmented'),
'Mechanical Engineer':('You design machines, components, and thermal systems for industries ranging from consumer electronics to heavy equipment, applying core engineering principles.',['CAD software','FEA','Heat transfer','Manufacturing processes','Standards compliance'],'¥10,000–25,000','augmented'),
'Flood Control Specialist':('You design hydraulic infrastructure — dikes, retention basins, flood gates — and develop early warning systems to protect communities from flood events.',['Hydraulic modeling (HEC-RAS)','GIS','Civil engineering','Emergency management','Project design'],'¥10,000–22,000','augmented'),
'Hydraulic Engineer':('You design water conveyance systems — dams, channels, pipelines, and irrigation networks — for agriculture, municipal water supply, and hydropower.',['Hydraulics','AutoCAD Civil 3D','Hydrology modeling','Environmental permitting','Project management'],'¥10,000–22,000','augmented'),
'Water Resource Planner':('You develop strategies for sustainable water allocation, drought resilience, and watershed management at regional and national scales.',['Hydrology','GIS','Policy analysis','Stakeholder engagement','Water law'],'¥10,000–22,000','augmented'),
'Food Safety Engineer':('You design food processing controls, HACCP plans, and quality systems to prevent contamination and ensure regulatory compliance in food production.',['HACCP','Food safety regulations','Microbiology','Quality management','Auditing'],'¥8,000–18,000','augmented'),
'R&D Food Scientist':('You develop new food products and processing technologies, optimizing flavor, texture, nutrition, and shelf life for commercial food manufacturers.',['Food chemistry','Sensory evaluation','Pilot plant operation','Regulatory compliance','Product development'],'¥10,000–22,000','augmented'),
'Supply Chain Quality Manager':('You ensure quality consistency across global food and consumer goods supply chains, auditing suppliers and managing product recalls.',['Supplier auditing','Quality systems','Traceability','Regulatory standards','Crisis management'],'¥12,000–28,000','augmented'),
'Forest Carbon Analyst':('You measure, model, and verify forest carbon stocks to support voluntary and compliance carbon market programs.',['Remote sensing','Carbon accounting protocols','Field inventory','GIS','Verification standards (Verra)'],'¥10,000–22,000','augmented'),
'Ecological Restoration Specialist':('You plan and implement the restoration of degraded forests, wetlands, and grasslands, selecting species, preparing sites, and monitoring recovery.',['Restoration ecology','Seed sourcing','GIS','Monitoring design','Grant management'],'¥8,000–18,000','resistant'),
'Timber Certification Officer':('You assess forestry operations for compliance with sustainability standards such as FSC and PEFC, issuing certifications that open access to premium markets.',['Forestry operations','Certification standards','Auditing','Report writing','Stakeholder engagement'],'¥8,000–18,000','augmented'),
'Crop Science Specialist':('You conduct research and advisory work on crop genetics, agronomy, and pest management to improve agricultural productivity and resilience.',['Plant science','Field trials','Statistical analysis','Agrochemical knowledge','Extension communication'],'¥8,000–18,000','augmented'),
'Precision Agriculture Data Analyst':('You analyze drone imagery, soil sensor data, and weather feeds to generate prescription maps and management advice for precision farming operations.',['Remote sensing','GIS','Python','Agronomy','Data visualization'],'¥10,000–22,000','augmented'),
'AgTech Field Agronomist':('You deploy precision technologies on farms, working directly with farmers to optimize planting density, irrigation scheduling, and fertilizer application.',['Soil science','Drone piloting','Data interpretation','Agronomy','Farmer communication'],'¥8,000–18,000','augmented'),
'Agricultural Supply Chain Director':('You lead the strategic procurement, logistics, and quality management of agricultural commodity supply chains at regional or national scale.',['Supply chain strategy','Commodity markets','Risk management','Team leadership','Regulatory compliance'],'¥20,000–45,000','augmented'),
'Livestock Production Manager':('You oversee large-scale animal production operations, managing feed efficiency, health protocols, reproduction programs, and staff.',['Animal nutrition','Herd health management','Production KPIs','Staff management','Biosecurity'],'¥10,000–22,000','augmented'),
'Animal Science Researcher':('You conduct scientific studies on animal genetics, nutrition, behavior, and reproduction to improve livestock performance and welfare.',['Animal physiology','Experimental design','Statistical analysis','Scientific writing','Lab techniques'],'¥8,000–18,000','augmented'),
'Precision Farming Specialist':('You apply IoT sensors, drones, and machine learning to livestock and crop operations, using data to optimize resource use and animal welfare.',['IoT systems','Data analysis','Animal behavior','Precision technology','Farm management'],'¥10,000–22,000','augmented'),
'Fisheries Research Scientist':('You study fish populations, aquatic ecosystems, and fishing impacts, providing scientific advice on sustainable fisheries management.',['Population dynamics','Stock assessment','Field sampling','Statistical modeling','Policy communication'],'¥8,000–18,000','resistant'),
'Aquaculture Manager':('You run commercial aquaculture operations for finfish, shrimp, or shellfish, managing water quality, feeding programs, health, and harvest logistics.',['Aquatic biology','Water quality management','Disease control','Farm operations','Regulatory compliance'],'¥10,000–22,000','augmented'),
'Water Quality Specialist':('You monitor and manage water quality parameters in aquaculture, drinking water, and environmental systems to protect human health and aquatic life.',['Water chemistry','Testing protocols','Regulatory standards','Treatment systems','Data reporting'],'¥8,000–18,000','augmented'),
'Economic Policy Analyst':('You research macroeconomic trends and evaluate policy options for government agencies, think tanks, and international organizations.',['Econometrics','Statistical software (Stata/R)','Policy writing','Literature review','Stakeholder briefing'],'¥10,000–25,000','augmented'),
'Development Finance Specialist':('You structure and evaluate development finance instruments — loans, guarantees, blended finance — for infrastructure and social sector projects.',['Project finance','Development economics','Risk analysis','Financial modeling','Multilateral institution knowledge'],'¥15,000–35,000','augmented'),
'Strategy Consultant':('You advise senior executives on business strategy, competitive positioning, and organizational transformation through structured analysis and facilitated decision-making.',['Structured problem solving','Financial modeling','Presentation skills','Client management','Industry research'],'¥20,000–60,000','augmented'),
'Investment Analyst':('You evaluate investment opportunities in equities, bonds, or alternative assets, building financial models and writing research reports to support portfolio decisions.',['Financial modeling','DCF/comps','Industry research','Bloomberg/Wind','Investment writing'],'¥12,000–40,000','augmented'),
'Fintech Product Manager':('You build financial technology products — payments, lending, insurance, wealth management — managing the product lifecycle from discovery to scale.',['Product management','Financial regulations','User research','Agile development','Data analysis'],'¥18,000–45,000','augmented'),
'Risk Manager':('You identify, quantify, and mitigate financial, operational, and regulatory risks across banking, insurance, and corporate treasury functions.',['Risk frameworks','Quantitative modeling','Regulatory capital (Basel)','Stress testing','Board reporting'],'¥15,000–40,000','augmented'),
'Actuarial Scientist':('You apply mathematical models to assess insurance risk, price products, and ensure that insurers hold sufficient reserves to pay future claims.',['Actuarial exams (SOA/CAS)','Stochastic modeling','R/Python','Regulatory compliance','Business communication'],'¥15,000–45,000','resistant'),
'Quantitative Analyst':('You build mathematical models for pricing derivatives, managing risk, and developing algorithmic trading strategies in financial institutions.',['Stochastic calculus','C++/Python','Statistical modeling','Financial markets','Model validation'],'¥20,000–80,000','augmented'),
'Machine Learning Researcher':('You advance the state of the art in machine learning through theoretical research and large-scale experimentation, often publishing at top conferences.',['Deep learning (PyTorch/JAX)','Mathematical statistics','Research methodology','Scientific writing','GPU computing'],'¥25,000–80,000','resistant'),
'Biostatistician':('You design and analyze clinical trials and biological experiments, ensuring that statistical methods are valid and results are correctly interpreted.',['Clinical trial design','SAS/R','Survival analysis','Regulatory statistics','Biomedical writing'],'¥15,000–32,000','augmented'),
'Data Scientist':('You extract insights from large datasets using statistical and machine learning methods, supporting product, operations, and strategic decisions across industries.',['Python/R/SQL','Machine learning','Data visualization','Statistical modeling','Business communication'],'¥15,000–40,000','augmented'),
'Quantitative Risk Analyst':('You build and validate quantitative models for market, credit, and operational risk at banks, insurers, and asset managers.',['Risk modeling','Statistical methods','Python/R','Financial products','Regulatory requirements'],'¥18,000–45,000','augmented'),
'Data-Driven Strategy Manager':('You combine management consulting skills with data analytics capabilities to guide organizations through evidence-based decisions and digital transformation.',['Data analytics','Strategy frameworks','Stakeholder management','Project leadership','Change management'],'¥18,000–45,000','augmented'),
'Operations Research Analyst':('You apply optimization, simulation, and statistical modeling to improve logistics, scheduling, capacity planning, and resource allocation.',['Linear programming','Simulation (AnyLogic)','Python/MATLAB','Supply chain','Business writing'],'¥12,000–28,000','augmented'),
'Management Consultant':('You advise organizations on performance improvement, organizational redesign, and change management, typically in project teams serving multiple clients.',['Problem structuring','Data analysis','Presentation','Project management','Industry knowledge'],'¥18,000–55,000','augmented'),
'Smart Manufacturing Consultant':('You help manufacturers adopt digital technologies — robotics, IoT, AI — to improve quality, reduce costs, and build competitive advantage.',['Industry 4.0 technologies','Process improvement','Change management','ROI modeling','Technical communication'],'¥15,000–35,000','augmented'),
'Industrial Engineer':('You optimize production systems and processes using methods such as time-and-motion study, value stream mapping, and simulation.',['Process mapping','Simulation software','Lean/Six Sigma','CAD basics','Statistical analysis'],'¥10,000–22,000','augmented'),
'Supply Chain Optimization Specialist':('You model and redesign supply chain networks to reduce cost, improve resilience, and shorten delivery times across global operations.',['Network optimization','Mathematical modeling','Python/solver tools','Logistics knowledge','Data analysis'],'¥14,000–32,000','augmented'),
'International Business Manager':('You develop and execute international market entry strategies, managing distributor relationships and navigating cultural and regulatory differences.',['Market analysis','Negotiation','International trade law','Cross-cultural communication','CRM systems'],'¥12,000–30,000','augmented'),
'Language Technology Specialist':('You develop and apply NLP tools — machine translation, text mining, speech recognition — often working in tech companies or language service providers.',['NLP (transformers/BERT)','Python','Linguistics','Data annotation','Model evaluation'],'¥12,000–28,000','augmented'),
'Technical / Legal Interpreter':('You provide specialized interpretation for technical, legal, or scientific proceedings, requiring deep domain knowledge in two or more languages.',['Simultaneous interpretation','Domain vocabulary','Memory techniques','Professional ethics','Continuing education'],'¥10,000–35,000','augmented'),
'Government Policy Researcher':('You conduct policy research and write position papers for government departments, party school institutes, and policy advisory bodies.',['Policy analysis','Social science research','Document drafting','Literature review','Presentation'],'¥8,000–18,000','resistant'),
'Party School Lecturer':('You teach Marxist theory, political economy, and governance subjects at party schools and universities, training government officials and students.',['Academic writing','Lecturing','Curriculum design','Political theory','Research'],'¥8,000–18,000','resistant'),
'University Political Affairs Staff':('You work in university political departments managing student affairs, ideological education, and party-building activities.',['Student affairs','Political education','Administrative management','Event organization','Communication'],'¥6,000–12,000','resistant'),
'Diplomatic Affairs Officer':('You represent national interests in bilateral and multilateral diplomatic settings, managing relationships with foreign governments and international organizations.',['Diplomacy','International law','Foreign language (English/French)','Political analysis','Protocol'],'¥10,000–25,000','resistant'),
'International Relations Researcher':('You study global political, economic, and security dynamics, publishing research and advising policymakers on foreign affairs strategy.',['Political science research','Qualitative/quantitative methods','Policy writing','Foreign language','Area studies'],'¥10,000–22,000','resistant'),
'Policy Analyst':('You research and evaluate public policies, modeling their effects and writing recommendations for government agencies, think tanks, and advocacy organizations.',['Policy analysis frameworks','Quantitative methods','Government processes','Report writing','Stakeholder mapping'],'¥10,000–25,000','augmented'),
'AI Ethics Researcher':('You study the social, ethical, and governance implications of AI systems, advising organizations and policymakers on responsible AI development and deployment.',['Ethics frameworks','AI/ML understanding','Policy research','Academic writing','Interdisciplinary collaboration'],'¥12,000–28,000','resistant'),
'Technology Governance Specialist':('You develop regulatory frameworks and internal governance structures for emerging technologies including AI, biotech, and data systems.',['Technology law','Risk assessment','Policy design','Stakeholder engagement','Technical literacy'],'¥15,000–35,000','resistant'),
'Community Development Officer':('You design and implement programs that address social needs — housing, employment, health — in underserved communities, often working for NGOs or government.',['Community needs assessment','Program management','Stakeholder engagement','Grant writing','Monitoring and evaluation'],'¥6,000–14,000','resistant'),
'Corporate Social Responsibility Specialist':('You develop and report on company sustainability programs, managing stakeholder relations and ESG disclosure across environmental, social, and governance dimensions.',['ESG reporting standards','Stakeholder management','Sustainability strategy','Data collection','Report writing'],'¥10,000–22,000','augmented'),
'Social Researcher':('You conduct quantitative and qualitative studies of social phenomena — inequality, migration, education, health — for academic institutions and policy bodies.',['Survey design','Statistical analysis','Qualitative methods','Research ethics','Academic writing'],'¥8,000–18,000','augmented'),
'Epidemiologist':('You investigate the distribution and determinants of disease in populations, designing studies that inform public health interventions and policy.',['Epidemiological methods','Biostatistics','R/Stata','Field investigation','Scientific writing'],'¥10,000–22,000','resistant'),
'Disease Surveillance Specialist':('You monitor disease trends through routine surveillance systems, detecting outbreaks early and alerting public health authorities to respond.',['Surveillance system design','Data analysis','GIS','Epidemiological investigation','Report writing'],'¥8,000–18,000','resistant'),
'Public Health Policy Analyst':('You evaluate public health interventions and policies, using epidemiological and economic evidence to inform government health strategy.',['Health economics','Policy analysis','Systematic review','Stakeholder engagement','Report writing'],'¥10,000–22,000','augmented'),
'Curriculum Developer':('You design educational curricula and learning materials for schools, training organizations, and online platforms.',['Instructional design','Learning theory','Content development','Assessment design','LMS platforms'],'¥8,000–18,000','augmented'),
'Teacher':('You deliver classroom instruction in primary, secondary, or higher education, planning lessons, assessing learning, and managing student development.',['Subject expertise','Pedagogy','Classroom management','Assessment','Student communication'],'¥6,000–15,000','resistant'),
'EdTech Product Specialist':('You develop digital learning products and platforms, combining education expertise with product thinking to create tools that improve learning outcomes.',['Instructional design','Product management','Learning analytics','UX basics','Content development'],'¥12,000–28,000','augmented'),
'Historical Researcher':('You conduct archival and field research to reconstruct and interpret historical events, people, and processes, publishing findings in academic venues.',['Archival research','Historical methods','Foreign languages','Academic writing','Oral history'],'¥6,000–15,000','resistant'),
'Museum Curator':('You manage museum collections, plan exhibitions, and engage the public with cultural heritage through education programs and digital initiatives.',['Collection management','Exhibition design','Conservation basics','Public programming','Grant writing'],'¥7,000–16,000','resistant'),
'Policy Institute Analyst':('You research policy questions for think tanks and research institutes, producing reports and briefings that influence public debate and government decision-making.',['Policy analysis','Research methods','Writing','Stakeholder engagement','Quantitative skills'],'¥10,000–22,000','augmented'),
'Ethnology Researcher':('You study the cultures, histories, and social structures of ethnic groups, contributing to academic knowledge and government minority policy.',['Ethnographic fieldwork','Qualitative methods','Cultural documentation','Language skills','Academic writing'],'¥6,000–14,000','resistant'),
'Minority Policy Analyst':('You analyze policies affecting ethnic minority communities, advising government agencies and advocacy organizations on equity, language rights, and cultural preservation.',['Policy analysis','Minority affairs knowledge','Stakeholder engagement','Report writing','Qualitative research'],'¥8,000–18,000','resistant'),
'Cultural Affairs Officer':('You manage cultural exchange programs, oversee cultural heritage preservation, and coordinate between government and civil society on arts and culture policy.',['Cultural policy','Program management','Stakeholder relations','Budgeting','Events coordination'],'¥8,000–18,000','resistant'),
'Hotel General Manager':('You oversee all operations of a hotel property — front office, F&B, housekeeping, and finance — ensuring guest satisfaction and commercial performance.',['Hotel operations','Revenue management','People leadership','Cost control','Brand standards'],'¥12,000–35,000','augmented'),
'Tourism Product Developer':('You design tourism itineraries and experiences, working with suppliers, transportation, and accommodation partners to create marketable travel products.',['Destination knowledge','Product packaging','Supplier negotiation','Marketing basics','Customer research'],'¥8,000–18,000','augmented'),
'Travel Platform Operations Manager':('You run the operational side of online travel platforms — managing supplier relationships, inventory quality, and customer service processes.',['Platform operations','E-commerce','Supplier management','Data analysis','Customer service'],'¥10,000–25,000','augmented'),
'Information Architecture Consultant':('You design the organizational structure of complex information systems — enterprise databases, intranets, and digital archives — to maximize findability and usability.',['Information architecture','Taxonomy design','UX principles','Database basics','Content strategy'],'¥10,000–22,000','augmented'),
'Digital Archivist':('You preserve and provide access to digital records, managing long-term storage, format migration, and metadata for institutional archives.',['Digital preservation standards','Metadata (Dublin Core/EAD)','Archival software','Rights management','Research support'],'¥7,000–15,000','at_risk'),
'Knowledge Management Specialist':('You design systems and processes for capturing, organizing, and sharing organizational knowledge to improve decision-making and institutional learning.',['Knowledge management frameworks','Collaboration platforms','Process design','Training delivery','Content management'],'¥10,000–22,000','augmented'),
'E-Commerce Operations Manager':('You oversee the day-to-day running of e-commerce businesses — managing product listings, order fulfillment, customer service, and platform relationships.',['E-commerce platforms (Tmall/JD)','Operations management','Customer service','Data analysis','Logistics coordination'],'¥10,000–25,000','augmented'),
'Cross-Border Trade Specialist':('You facilitate international e-commerce transactions, managing customs compliance, currency conversion, last-mile delivery, and foreign platform operations.',['Cross-border e-commerce','Customs regulations','International logistics','Platform management','Foreign language'],'¥10,000–25,000','augmented'),
'Digital Marketing Analyst':('You measure and optimize digital marketing performance across search, social, and e-commerce channels using data analytics and experimentation.',['Google Analytics/GA4','SEO/SEM','A/B testing','SQL','Attribution modeling'],'¥10,000–25,000','augmented'),
'Cross-Border Operations Director':('You lead international logistics operations, building the supply chain and compliance infrastructure for companies exporting to or importing from overseas markets.',['International logistics','Customs law','Operations management','Team leadership','Risk management'],'¥20,000–50,000','augmented'),
'Supply Chain Manager':('You coordinate the end-to-end flow of goods from suppliers to customers, optimizing inventory, transportation, and warehouse operations.',['Supply chain management','ERP systems','Supplier relations','Inventory optimization','Logistics coordination'],'¥12,000–28,000','augmented'),
'Logistics Analytics Specialist':('You apply data analysis to optimize routes, warehouse layouts, fleet management, and demand forecasting in logistics and transportation networks.',['Python/R','Operations research','Logistics systems','Data visualization','Process improvement'],'¥12,000–28,000','augmented'),
'Government Budget Analyst':('You prepare, analyze, and monitor government budgets, ensuring fiscal discipline and alignment with policy priorities across departments.',['Public finance','Budget modeling','Accounting','Policy analysis','Report writing'],'¥8,000–18,000','resistant'),
'Fiscal Policy Advisor':('You advise governments on taxation, expenditure, and debt management policy, using economic modeling to evaluate fiscal sustainability and growth impacts.',['Fiscal economics','Policy modeling','Government accounting','Stakeholder briefing','Research writing'],'¥12,000–28,000','resistant'),
'Tax Administration Specialist':('You manage tax collection, compliance, and audit functions within government revenue authorities, interpreting and enforcing tax law.',['Tax law','Audit procedures','Financial analysis','Legal interpretation','Taxpayer communication'],'¥8,000–18,000','resistant'),
'Government Policy Manager':('You coordinate policy development and implementation within government departments, managing inter-agency processes and stakeholder consultation.',['Policy coordination','Administrative management','Stakeholder engagement','Writing','Budget oversight'],'¥10,000–22,000','resistant'),
'Urban Planning Official':('You review development applications, enforce zoning regulations, and develop master plans for urban growth, land use, and infrastructure investment.',['Urban planning law','GIS','Zoning','Public consultation','Report writing'],'¥8,000–20,000','resistant'),
'Civil Servant':('You implement government functions across public administration, regulation, taxation, and service delivery at national, provincial, or municipal levels.',['Administrative law','Policy implementation','Public communication','Document management','Inter-agency coordination'],'¥6,000–15,000','resistant'),
'Criminal Investigation Specialist':('You investigate crimes using forensic evidence, witness testimony, and digital data, building cases for prosecution through rigorous procedure.',['Investigation methodology','Forensic techniques','Legal procedure','Evidence management','Report writing'],'¥8,000–18,000','resistant'),
'Cybercrime Investigator':('You investigate digital crimes — hacking, fraud, identity theft — using forensic tools to recover evidence from devices, networks, and cloud services.',['Digital forensics','Network analysis','Malware analysis','Legal procedure','Cybersecurity tools'],'¥10,000–25,000','resistant'),
'Police Officer':('You maintain public order, respond to incidents, and investigate crimes at the local level, requiring physical fitness, legal knowledge, and community skills.',['Law enforcement procedure','Criminal law','Physical fitness','De-escalation','Report writing'],'¥7,000–16,000','resistant'),
'Emergency Response Technologist':('You develop and operate technical systems for emergency response — command centers, communication networks, and early warning infrastructure.',['Emergency management systems','Communications technology','Crisis coordination','Technical operations','Training delivery'],'¥8,000–18,000','resistant'),
'Forensic Systems Specialist':('You develop and apply technical tools for forensic investigation — fingerprint databases, DNA analysis systems, and digital evidence platforms.',['Forensic technology','Database systems','Biometrics','Legal standards','Technical documentation'],'¥10,000–22,000','resistant'),
'Security Technology Engineer':('You design and deploy security systems — surveillance networks, access control, intrusion detection — for public safety and private security applications.',['Security systems integration','Networking','IoT','Project management','Risk assessment'],'¥10,000–22,000','augmented'),
'Forensic Pathologist':('You perform autopsies to determine cause and manner of death, providing expert testimony in criminal and civil legal proceedings.',['Forensic pathology','Autopsy technique','Toxicology','Legal standards','Expert testimony'],'¥12,000–28,000','resistant'),
'Forensic Toxicologist':('You analyze biological samples and substances to detect poisons, drugs, and environmental toxins in forensic investigations and clinical settings.',['Analytical chemistry','Toxicology','LC-MS/GC-MS','Chain of custody','Expert reporting'],'¥10,000–25,000','resistant'),
'Legal Medicine Expert':('You provide medical-legal opinions on injury, disability, and cause of death, serving as an expert witness in courts and supporting insurance claims.',['Forensic medicine','Medical law','Expert testimony','Clinical assessment','Report writing'],'¥12,000–28,000','resistant'),
'Clinical Laboratory Technologist':('You perform diagnostic tests on blood, tissue, and other samples, operating automated analyzers and interpreting results for clinical teams.',['Clinical chemistry','Hematology analyzers','Lab safety','Quality control','Result interpretation'],'¥7,000–16,000','augmented'),
'Medical Imaging Specialist':('You operate MRI, CT, ultrasound, and X-ray equipment, producing diagnostic images and often providing initial interpretation for radiologists.',['Imaging modalities','Patient positioning','Image quality','DICOM systems','Radiation safety'],'¥8,000–18,000','augmented'),
'Pathology Lab Manager':('You manage the operations of a hospital or commercial pathology laboratory, overseeing staff, quality systems, turnaround times, and regulatory accreditation.',['Laboratory management','Quality systems (ISO 15189)','Budget control','Staff development','Regulatory compliance'],'¥12,000–28,000','resistant'),
'Clinical Psychologist':('You assess and treat mental health conditions using evidence-based therapies, working in hospitals, private practice, schools, or corporate wellness settings.',['Psychotherapy (CBT/DBT)','Psychological assessment','Case formulation','Supervision','Mental health law'],'¥8,000–22,000','resistant'),
'Organizational Behavior Consultant':('You apply psychological research to improve workplace culture, leadership effectiveness, and employee engagement in corporate and government organizations.',['Organizational psychology','Survey design','Consulting skills','Data analysis','Facilitation'],'¥12,000–30,000','augmented'),
'UX Research Specialist':('You conduct user research — interviews, usability tests, surveys — to inform product design and strategy, translating findings into actionable insights.',['User interview techniques','Usability testing','Survey analysis','Insight synthesis','Stakeholder communication'],'¥12,000–28,000','augmented'),
'TCM Physician':('You diagnose and treat patients using traditional Chinese medicine principles — acupuncture, herbal prescriptions, and dietary therapy — in hospitals or private clinics.',['TCM diagnosis (pulse/tongue)','Acupuncture technique','Herbal formulae','Patient management','Medical records'],'¥8,000–22,000','resistant'),
'Acupuncturist':('You provide acupuncture treatments for pain management, stress reduction, and chronic condition management, often in integrative medicine or private practice settings.',['Acupuncture technique','TCM theory','Patient communication','Clinic management','Safety protocols'],'¥7,000–20,000','resistant'),
'TCM Product Developer':('You develop and test new traditional Chinese medicine formulations, combining herbal pharmacology with modern manufacturing and clinical validation.',['Herbal pharmacology','Product formulation','Clinical trial basics','Regulatory knowledge','Quality standards'],'¥10,000–22,000','augmented'),
'Herbal Medicine Quality Analyst':('You test and certify the identity, purity, and potency of herbal medicine raw materials and finished products.',['Herbal identification','HPLC/TLC analysis','Pharmacopoeia standards','Quality systems','Documentation'],'¥8,000–18,000','augmented'),
'TCM Pharmacognosist':('You specialize in the botanical, chemical, and pharmacological study of medicinal plants and their preparations used in TCM.',['Plant taxonomy','Chemical analysis','Pharmacognosy','Research methods','Academic writing'],'¥8,000–18,000','resistant'),
'Natural Product Researcher':('You extract, isolate, and characterize bioactive compounds from plants, fungi, and marine organisms for pharmaceutical and nutraceutical applications.',['Natural product chemistry','Extraction techniques','Bioassays','Spectroscopy','Research writing'],'¥10,000–22,000','resistant'),
'Integrative Medicine Physician':('You treat patients using a combination of conventional medicine and evidence-based complementary therapies, often in hospital integrative medicine departments.',['Clinical medicine','TCM fundamentals','Integrative oncology','Patient communication','Research literacy'],'¥10,000–28,000','resistant'),
'Clinical TCM-Western Hybrid Specialist':('You bridge TCM and Western medicine in clinical practice, using laboratory diagnostics alongside herbal and acupuncture treatments for complex cases.',['Dual medical training','Diagnostic integration','Complex case management','Research literacy','Patient education'],'¥10,000–25,000','resistant'),
'Integrative Health Researcher':('You conduct research comparing and combining TCM and Western medicine approaches, building evidence for integrated treatment protocols.',['Research methodology','Clinical trial design','Medical writing','Statistical analysis','Cross-cultural medicine'],'¥10,000–22,000','resistant'),
'Physician':('You diagnose and treat patients across the full range of medical conditions, serving as the primary point of clinical care in hospitals and community health centers.',['Clinical diagnosis','Treatment planning','Patient communication','Medical records','Evidence-based medicine'],'¥12,000–40,000','resistant'),
'Medical Specialist':('You provide expert care in a defined clinical specialty — cardiology, oncology, neurology — after completing general medical training and specialist certification.',['Specialty clinical skills','Procedures','MDT collaboration','Research literacy','Patient management'],'¥18,000–60,000','resistant'),
'Clinical Department Director':('You lead a hospital department, managing clinical standards, staff development, budget, and the strategic direction of specialist services.',['Clinical leadership','Team management','Budget control','Quality improvement','Medical strategy'],'¥25,000–70,000','resistant'),
'Dentist':('You diagnose and treat diseases of teeth, gums, and oral tissues, providing preventive care, restorative procedures, and patient education.',['Clinical dentistry','Radiograph interpretation','Dental procedures','Patient management','Practice management'],'¥12,000–45,000','resistant'),
'Dental Implant Surgeon':('You perform surgical placement of dental implants and complex oral surgical procedures, combining surgical skill with prosthetic knowledge.',['Implant surgery','Bone grafting','CBCT interpretation','Surgical protocols','Patient selection'],'¥20,000–80,000','resistant'),
'Orthodontics Specialist':('You diagnose and treat dental malocclusions using braces, aligners, and other appliances, managing treatment plans over multi-year care episodes.',['Orthodontic diagnosis','Appliance design','Treatment mechanics','Digital planning (Invisalign)','Patient communication'],'¥20,000–70,000','resistant'),
'Registered Nurse':('You deliver direct patient care across hospital wards, ICUs, and community settings, administering treatments, monitoring vital signs, and supporting patient recovery.',['Clinical nursing skills','Medication administration','Patient monitoring','Care planning','Emergency response'],'¥7,000–18,000','resistant'),
'Specialized Care Nurse':('You provide advanced nursing care in specialist environments — ICU, oncology, NICU — requiring additional training beyond general nursing.',['Advanced clinical skills','Specialty protocols','Critical thinking','Family communication','Professional development'],'¥10,000–25,000','resistant'),
'Community Health Practitioner':('You deliver preventive care, health education, and chronic disease management in community settings, serving as the first point of contact for primary healthcare.',['Primary care skills','Health promotion','Community engagement','Chronic disease management','Patient education'],'¥7,000–16,000','resistant'),
'Biomedical Researcher':('You investigate disease mechanisms, drug targets, and biomarkers in laboratory settings, contributing to the scientific foundation of new medical treatments.',['Molecular biology','Cell culture','Animal studies','Grant writing','Scientific publishing'],'¥10,000–22,000','resistant'),
'Pharmaceutical Scientist':('You develop and test drug formulations, studying how active compounds behave in the body and optimizing delivery systems for efficacy and safety.',['Drug formulation','Pharmacokinetics','Analytical methods','Regulatory knowledge','Scientific writing'],'¥12,000–28,000','resistant'),
'Clinical Systems Analyst':('You bridge clinical practice and health IT, configuring and optimizing electronic health record systems to support clinical workflows and data quality.',['EHR systems (Epic/Cerner)','Clinical workflows','Health informatics','Training delivery','Requirements analysis'],'¥12,000–28,000','augmented'),
'Medical Device Engineer':('You design, test, and validate medical devices — from surgical instruments to diagnostic equipment — ensuring regulatory compliance and clinical effectiveness.',['Medical device regulations (NMPA/FDA)','Biomedical engineering','Risk management (ISO 14971)','Design verification','Technical documentation'],'¥12,000–28,000','augmented'),
'Health AI Product Manager':('You lead the development of AI-powered healthcare products — diagnostic tools, clinical decision support, remote monitoring — from concept to market.',['Healthcare AI','Product management','Regulatory pathways','Clinical validation','Stakeholder management'],'¥18,000–45,000','augmented'),
'Software Engineer':('You design, build, and maintain software systems across web, mobile, cloud, and embedded platforms, applying computer science principles to solve real-world problems.',['Programming languages (Python/Java/Go)','System design','Algorithms','Version control (Git)','Testing and debugging'],'¥15,000–50,000','augmented'),
'AI/ML Engineer':('You build and deploy machine learning systems at scale, bridging research and production by creating data pipelines, training infrastructure, and model serving systems.',['Python/PyTorch/TensorFlow','MLOps','Cloud ML platforms','Distributed systems','Model optimization'],'¥20,000–70,000','augmented'),
'Cloud Architect':('You design scalable, secure, and cost-efficient cloud infrastructure for enterprise systems, selecting services and patterns across AWS, Azure, or Alibaba Cloud.',['Cloud platforms','Networking/security','IaC (Terraform)','Microservices','Cost optimization'],'¥25,000–70,000','augmented'),
'Embedded Systems Developer':('You write firmware and real-time software for microcontrollers and embedded processors in consumer electronics, automotive systems, and industrial equipment.',['C/C++','RTOS','Hardware interfaces (UART/SPI/I2C)','Debugging tools','Power optimization'],'¥15,000–40,000','augmented'),
'IC Design Engineer':('You design integrated circuits — CPUs, memory, signal processors, analog ICs — using hardware description languages and EDA tools.',['Verilog/VHDL','EDA tools (Cadence/Synopsys)','Digital/analog circuit design','Verification','Semiconductor process knowledge'],'¥20,000–60,000','resistant'),
'RF Communications Engineer':('You design wireless communication systems — antennas, transceivers, signal processing chains — for mobile networks, radar, and satellite communications.',['RF circuit design','Signal processing','EM simulation (HFSS/CST)','Network standards (5G/LTE)','Measurement equipment'],'¥18,000–45,000','resistant'),
'Semiconductor Physicist':('You study the fundamental properties of semiconductor materials and devices, supporting the development of next-generation transistors, sensors, and photovoltaics.',['Semiconductor physics','Device fabrication','Characterization tools (AFM/SEM)','Simulation (TCAD)','Scientific writing'],'¥18,000–45,000','resistant'),
'Semiconductor Process Engineer':('You develop and optimize the manufacturing processes used to fabricate integrated circuits — lithography, etching, deposition, and doping.',['Semiconductor fab processes','Process control','Yield improvement','Statistical methods','Equipment operation'],'¥18,000–45,000','resistant'),
'Scientific Instrument Engineer':('You design precision laboratory instruments — spectrometers, detectors, analytical equipment — for scientific research and industrial quality control.',['Optics/electronics design','Precision mechanics','Calibration','Software integration','Customer support'],'¥12,000–28,000','augmented'),
'GIS Analyst':('You build, analyze, and maintain geographic information systems to support land management, urban planning, environmental monitoring, and emergency response.',['ArcGIS/QGIS','Spatial SQL','Python/R','Remote sensing','Map design'],'¥8,000–18,000','augmented'),
'Geophysicist':('You use physical methods to investigate the subsurface, supporting mineral exploration, oil and gas development, and geotechnical engineering.',['Seismic data processing','Gravity/magnetic surveys','Petrophysics','Interpretation software','Field operations'],'¥12,000–28,000','augmented'),
'Farm Automation Specialist':('You deploy autonomous machinery, robotic systems, and IoT networks on farms, managing the technical integration of precision agricultural equipment.',['Agricultural robotics','IoT systems','Farm management software','Mechanical maintenance','Training delivery'],'¥10,000–22,000','augmented'),
'Rural Development Officer':('You implement government programs for rural infrastructure, agricultural support, and poverty alleviation, working directly with farming communities.',['Rural policy','Project management','Community engagement','Agricultural knowledge','Government administration'],'¥6,000–14,000','resistant'),
'Desertification Control Specialist':('You plan and implement programs to halt and reverse land degradation in arid and semi-arid regions, using plant restoration, water harvesting, and soil stabilization.',['Dryland ecology','Restoration techniques','GIS','Policy knowledge','Community engagement'],'¥7,000–15,000','resistant'),
'Grassland Ecologist':('You study grassland ecosystems, monitoring biodiversity, carbon stocks, and grazing impacts to inform conservation and land management decisions.',['Ecological field methods','Remote sensing','Statistical analysis','Carbon monitoring','Research writing'],'¥7,000–15,000','resistant'),
'Rangeland Manager':('You manage grazing lands for sustainable livestock production, balancing forage availability, soil health, and biodiversity in grassland environments.',['Rangeland science','Livestock management','GIS','Grazing systems','Regulatory compliance'],'¥7,000–15,000','resistant'),
'Defense Technology Researcher':('You conduct applied research into defense systems and materials, contributing to national security technology development within regulated frameworks.',['Defense engineering','Research methodology','Security clearance protocols','Technical writing','Systems integration'],'¥15,000–35,000','resistant'),
'Companion Animal Veterinarian':('You diagnose and treat dogs, cats, and other companion animals in private practice, performing surgery, prescribing medications, and advising owners on preventive care.',['Veterinary medicine','Small animal surgery','Diagnostic imaging','Client communication','Practice management'],'¥10,000–35,000','resistant'),
'Food Safety Inspection Veterinarian':('You inspect livestock, poultry, and food production facilities to certify that animal products meet food safety and public health standards.',['Veterinary inspection','Food safety law','Ante/post-mortem inspection','Zoonosis control','Regulatory reporting'],'¥8,000–18,000','resistant'),
'Animal Disease Control Officer':('You monitor animal populations for disease outbreaks, coordinating testing, quarantine, and response protocols to protect animal and human health.',['Veterinary epidemiology','Laboratory diagnostics','Surveillance systems','Regulatory authority','Emergency response'],'¥8,000–18,000','resistant'),
'Export Control Consultant':('You advise companies on export control regulations — ITAR, EAR, China export rules — ensuring that technology, goods, and software transfers comply with sanctions and licensing requirements.',['Export control law (EAR/ITAR)','Trade compliance','Customs law','Risk assessment','International trade'],'¥12,000–30,000','resistant'),
'Industrial Hazard Consultant':('You assess workplace and industrial hazards, conducting risk analyses and designing safety systems to prevent accidents, occupational illness, and environmental incidents.',['Hazard analysis (HAZOP/FMEA)','Industrial safety standards','Risk quantification','Regulatory compliance','Training delivery'],'¥10,000–25,000','resistant'),
'International Market Analyst':('You research foreign markets, analyze competitive dynamics, and identify growth opportunities for companies expanding into international trade and cross-border e-commerce.',['Market research','Trade data analysis','Country risk assessment','Financial modeling','Presentation skills'],'¥10,000–25,000','augmented'),
'Precision Agriculture Engineer':('You design and deploy precision farming systems — variable-rate applicators, autonomous field robots, soil mapping sensors — to optimize crop inputs and yields.',['Agricultural machinery','IoT/sensors','Control systems','Agronomy knowledge','Field testing'],'¥12,000–28,000','augmented'),
'Renewable Energy Analyst':('You model and evaluate renewable energy projects — solar, wind, storage — assessing technical performance, grid integration, and economic viability for developers and investors.',['Energy modeling (SAM/PVsyst)','Financial modeling','Grid analysis','Project development','Regulatory knowledge'],'¥12,000–28,000','augmented'),
'Risk Assessment Specialist':('You identify and quantify operational, safety, and environmental risks in industrial facilities, designing mitigation measures and maintaining risk management systems.',['Risk analysis methods','Safety regulations','Process hazard review','Quantitative risk assessment','Report writing'],'¥10,000–22,000','augmented'),
'Safety Engineer':('You design safety systems, write procedures, and conduct incident investigations in manufacturing, construction, chemical, and mining environments.',['Safety standards (GB/ISO)','Hazard identification','Accident investigation','Safety management systems','Training delivery'],'¥8,000–20,000','augmented'),
'Trade Compliance Specialist':('You manage import and export compliance programs, classifying goods, preparing customs documentation, and ensuring adherence to trade laws and sanctions regimes.',['Customs law','HS classification','Sanctions compliance','Import/export licensing','ERP systems'],'¥10,000–25,000','resistant'),
'Cross-disciplinary R&D Researcher':('You conduct research at the intersection of multiple fields — bio-nano, AI-materials, neuro-engineering — producing novel insights that single-discipline teams cannot reach.',['Cross-domain literacy','Experimental design','Scientific writing','Collaboration','Grant applications'],'¥12,000–28,000','resistant'),
'Emerging Tech Specialist':('You identify, evaluate, and pilot emerging technologies for corporate or government clients, building business cases and implementation roadmaps.',['Technology scouting','Business case development','Stakeholder briefing','Pilot management','Technology literacy'],'¥15,000–35,000','augmented'),
'Systems Integration Engineer':('You connect disparate hardware and software components into working integrated systems, managing interface design, testing, and commissioning.',['Systems engineering','Interface management','Test planning','Documentation','Project coordination'],'¥14,000–32,000','augmented'),
'Rail Infrastructure Specialist':('You plan, design, and manage railway infrastructure projects — track, signaling, electrification, and stations — for high-speed and urban transit systems.',['Railway engineering','Project management','Infrastructure design','Safety standards','Stakeholder management'],'¥12,000–28,000','augmented'),
'Traffic Data Analyst':('You collect and analyze road and transit data to support traffic engineering, congestion management, and transportation planning decisions.',['Traffic modeling (VISSIM)','SQL/Python','GIS','Statistical analysis','Technical reporting'],'¥10,000–22,000','augmented'),
'Transportation Systems Engineer':('You design and optimize multimodal transportation networks — road, rail, air, sea — applying systems engineering and operations research methods.',['Transport modeling','Systems engineering','Network optimization','GIS','Stakeholder engagement'],'¥12,000–28,000','augmented'),
'Advanced Composites Specialist':('You develop carbon fiber, glass fiber, and ceramic composite materials and manufacturing processes for aerospace, automotive, and sporting goods applications.',['Composite materials','Manufacturing processes','Testing methods','Failure analysis','Process optimization'],'¥14,000–32,000','augmented'),
'Semiconductor Physicist':('You study electron transport, band structure, and quantum effects in semiconductor materials to enable next-generation devices.',['Quantum mechanics','Device physics','Characterization tools','Simulation (TCAD)','Research publishing'],'¥18,000–45,000','resistant'),
}

# ── AI impact descriptions ───────────────────────────────────────
AI_IMPACT = {
'immune':    ('🛡️ Highly AI-Resistant','This career requires physical presence, clinical judgment, or licensed professional accountability that AI tools cannot replicate. AI may assist with information retrieval or documentation, but the core function remains irreplaceably human.','border-color:rgba(16,185,129,.5);background:rgba(16,185,129,.06);','#10b981'),
'resistant': ('🛡️ AI-Resistant','AI tools enhance productivity in this career but do not threaten the core function. Human expertise, ethical judgment, and relationship-building remain central.','border-color:rgba(16,185,129,.4);background:rgba(16,185,129,.04);','#10b981'),
'augmented': ('⚡ AI-Augmented','AI tools significantly increase what you can accomplish in this career — automating routine tasks and accelerating analysis. Graduates who adopt AI tools early will be more productive; those who ignore them will fall behind.','border-color:rgba(59,130,246,.4);background:rgba(59,130,246,.04);','#60a5fa'),
'at_risk':   ('⚠️ Partial AI Disruption','Some functions in this career are being automated. The field is not disappearing, but the commodity work is under pressure. Graduates need to specialize, build unique voice, or move into roles where human judgment and relationships are the value.','border-color:rgba(245,158,11,.4);background:rgba(245,158,11,.04);','#f59e0b'),
}

# ── Shared CSS + shell ────────────────────────────────────────────
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
h1{font-size:clamp(22px,5vw,34px);font-weight:800;line-height:1.2;margin-bottom:8px;}
.hdr-meta{font-size:13px;color:#64748b;}
.page{max-width:720px;margin:0 auto;padding:28px 18px 60px;}
.card{background:#1e293b;border:1px solid #334155;border-radius:12px;
  padding:20px 22px;margin-bottom:16px;}
.card h2{font-size:15px;font-weight:700;margin-bottom:10px;color:#e2e8f0;}
.card p{font-size:14px;color:#cbd5e1;line-height:1.8;}
.ai-card{border-radius:12px;padding:18px 22px;margin-bottom:16px;border:1px solid;}
.ai-label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px;}
.ai-card p{font-size:13px;line-height:1.75;}
.salary-row{display:flex;align-items:center;gap:10px;margin-bottom:8px;}
.salary-val{font-size:22px;font-weight:800;color:#10b981;}
.salary-label{font-size:12px;color:#64748b;}
.skills{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;}
.skill{padding:4px 12px;background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);
  border-radius:20px;font-size:12px;color:#93c5fd;}
.major-link{display:flex;align-items:center;gap:10px;padding:10px 14px;
  background:#1e293b;border:1px solid #334155;border-radius:8px;
  margin-bottom:6px;text-decoration:none;color:inherit;transition:border-color .15s;}
.major-link:hover{border-color:rgba(59,130,246,.5);text-decoration:none;}
.major-link-name{font-size:13px;font-weight:600;color:#e2e8f0;flex:1;}
.major-link-sub{font-size:11px;color:#64748b;}
.stars{color:#f59e0b;font-size:12px;flex-shrink:0;}
.cta-vote{display:block;text-align:center;padding:14px;margin:24px 0 12px;
  background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);
  border-radius:12px;font-size:14px;font-weight:600;color:#60a5fa;}
.cta-vote:hover{background:rgba(59,130,246,.18);text-decoration:none;}
.blog-cta{display:block;margin-bottom:16px;padding:20px 22px;
  background:linear-gradient(135deg,#1e3a5f,#0f172a);
  border:1px solid rgba(59,130,246,.35);border-radius:14px;text-decoration:none;}
.blog-cta-label{font-size:11px;text-transform:uppercase;letter-spacing:.1em;
  color:#3b82f6;font-weight:700;margin-bottom:6px;}
.blog-cta-title{font-size:15px;font-weight:800;color:#e2e8f0;margin-bottom:4px;}
.blog-cta-sub{font-size:13px;color:#64748b;}
.faq-q{font-size:14px;font-weight:700;color:#e2e8f0;margin:14px 0 4px;}
.faq-a{font-size:13px;color:#94a3b8;line-height:1.75;}
.foot{text-align:center;padding:20px;font-size:12px;color:#475569;
  border-top:1px solid #1e293b;}
.section-title{font-size:11px;text-transform:uppercase;letter-spacing:.1em;
  color:#94a3b8;font-weight:700;margin:20px 0 10px;}
"""

def stars_html(n): return '★'*n + '☆'*(5-n)

OUT = "ordinarymantrying.com/tools/careers"
os.makedirs(OUT, exist_ok=True)

written = []
skipped = []

for career, subs in sorted(CAREER_SUBS.items()):
    if career not in CAREER_DATA:
        skipped.append(career)
        continue

    intro, skills, salary, ai_tag = CAREER_DATA[career]
    ai_label, ai_desc, ai_style, ai_color = AI_IMPACT[ai_tag]

    # avg stars from subcategories
    avg_stars = round(sum(SUBCAT_MAP[s]['stars'] for s in subs) / len(subs))

    # majors that lead to this career (from ALL)
    related_majors = [m for m in ALL if m.get('sub') in subs or m.get('cat') in subs]
    related_majors = related_majors[:12]  # cap at 12 for readability

    cslug = slug(career)
    canonical = f"https://ordinarymantrying.com/tools/careers/{cslug}.html"
    seo_title = f"{career} in China — Career Guide, Salary & Required Majors 2025"
    seo_desc  = f"{intro[:140]} Find which Chinese university majors lead to this career."

    # FAQ
    q1 = f"What Chinese university major leads to becoming a {career}?"
    a1 = f"The main pathways are through " + ", ".join(subs[:3]) + f" majors. {'Computer Science and Electronic Information graduates' if 'Computer Science' in subs or 'Electronic Information' in subs else 'Graduates from these fields'} commonly enter this career after completing their undergraduate degree."
    q2 = f"Is {career} a good career in China in 2025?"
    a2 = f"Based on current market analysis, this career scores {avg_stars} out of 5 stars for future outlook. {ai_desc[:120]}"
    q3 = f"What is the salary for a {career} in China?"
    a3 = f"Entry-level to senior salaries typically range from {salary} per month depending on city, employer size, and experience level. Major cities like Beijing, Shanghai, and Shenzhen command premium rates."

    faq_schema = json.dumps({"@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[
            {"@type":"Question","name":q1,"acceptedAnswer":{"@type":"Answer","text":a1}},
            {"@type":"Question","name":q2,"acceptedAnswer":{"@type":"Answer","text":a2}},
            {"@type":"Question","name":q3,"acceptedAnswer":{"@type":"Answer","text":a3}},
        ]})

    major_rows = ""
    for mj in related_majors:
        mstars = SUBCAT_MAP.get(mj.get('sub',''), {}).get('stars', 3)
        msub   = mj.get('sub', mj.get('cat',''))
        mslug  = major_slug(mj['n'])
        major_rows += f'''<a class="major-link" href="/tools/majors/{mslug}.html">
  <span class="stars">{stars_html(mstars)}</span>
  <span class="major-link-name">{mj["n"]}</span>
  <span class="major-link-sub">{msub}</span>
</a>\n'''

    skills_html = "".join(f'<span class="skill">{s}</span>' for s in skills)

    html = f'''<!DOCTYPE html>
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
  <div class="hdr-label">Career Guide · China 2025–2029</div>
  <h1>{career}</h1>
  <div class="hdr-meta">Field: {" · ".join(subs[:2])} &nbsp;·&nbsp; Outlook: {stars_html(avg_stars)}</div>
</div>

<div class="page">

<div class="card">
  <h2>What Does a {career} Do?</h2>
  <p>{intro}</p>
</div>

<div class="card">
  <h2>China Salary Range</h2>
  <div class="salary-row">
    <span class="salary-val">{salary}</span>
    <span class="salary-label">per month · varies by city, employer & experience</span>
  </div>
  <p style="font-size:13px;color:#64748b;margin-top:8px;">Top-tier cities (Beijing, Shanghai, Shenzhen) typically pay 20–40% above national averages. State-owned enterprises offer stability; private tech companies offer higher ceiling but less security.</p>
</div>

<div class="ai-card" style="{ai_style}">
  <div class="ai-label" style="color:{ai_color}">{ai_label}</div>
  <p style="font-size:13px;color:#cbd5e1;line-height:1.75;">{ai_desc}</p>
</div>

<div class="card">
  <h2>Key Skills Required</h2>
  <div class="skills">{skills_html}</div>
</div>

<div class="card">
  <h2>Career Path in China</h2>
  <p style="margin-bottom:10px;font-size:13px;color:#64748b;">Typical progression for Chinese graduates entering this field:</p>
  <p><strong style="color:#e2e8f0;">Year 1–3 (Junior):</strong> <span style="color:#94a3b8;">Learn systems and processes under supervision. Build domain knowledge and tool proficiency. Expected to contribute to projects within 3–6 months.</span></p>
  <p style="margin-top:10px;"><strong style="color:#e2e8f0;">Year 3–6 (Mid-level):</strong> <span style="color:#94a3b8;">Lead components of larger projects. Mentor junior staff. Develop specialist expertise and begin building professional reputation.</span></p>
  <p style="margin-top:10px;"><strong style="color:#e2e8f0;">Year 6+ (Senior/Lead):</strong> <span style="color:#94a3b8;">Own significant projects or departments. Influence organizational strategy. Salary ceiling rises significantly. Senior roles often require a strong publication, project, or client record.</span></p>
</div>

<div class="section-title">Chinese Majors That Lead Here ({len(related_majors)} shown)</div>
{major_rows}

<div class="card" style="margin-top:16px;">
  <h2>Frequently Asked Questions</h2>
  <div class="faq-q">{q1}</div>
  <div class="faq-a">{a1}</div>
  <div class="faq-q">{q2}</div>
  <div class="faq-a">{a2}</div>
  <div class="faq-q">{q3}</div>
  <div class="faq-a">{a3}</div>
</div>

<a class="cta-vote" href="/tools/major-vote.html">
  ▲ Vote for your major — see the live 5-year career ranking →
</a>
<a class="blog-cta" href="https://ordinarymantrying.com/building-in-public-experiment/" target="_blank" rel="noopener">
  <div class="blog-cta-label">📺 Building in Public — 5-Year Experiment</div>
  <div class="blog-cta-title">One ordinary person building this from scratch — with real numbers.</div>
  <div class="blog-cta-sub">Follow the journey → ordinarymantrying.com</div>
</a>
</div>
<div class="foot">Data: China Graduate Employment Research · Ministry of Education 2024<br>
Built by <a href="https://ordinarymantrying.com">Ordinary Man Trying</a></div>
</body></html>'''

    with open(f"{OUT}/{cslug}.html", "w", encoding="utf-8") as f:
        f.write(html)
    written.append((career, cslug))

print(f"\n✓ {len(written)} career pages written to {OUT}/")
print(f"  Skipped (no data): {len(skipped)}")
if skipped:
    for s in skipped[:5]:
        print(f"    - {s}")
