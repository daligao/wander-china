#!/usr/bin/env python3
"""
生成 259 个中文职业详情页 → tools/careers-cn/
纯工具页，含明显免责声明，链接到中文专业页
"""
import re, os, json, unicodedata, sys
sys.path.insert(0, os.path.dirname(__file__))
from cn_names import CN_MAJOR_NAMES

def slug(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def stars_html(n): return '★' * n + '☆' * (5 - n)

# ── 读取英文数据源 ──────────────────────────────────────────────────
with open("ordinarymantrying.com/tools/major-vote.html", encoding="utf-8") as f:
    mvh = f.read()
m = re.search(r'const ALL\s*=\s*(\[.*?\]);', mvh, re.DOTALL)
ALL = json.loads(m.group(1))
m2 = re.search(r'const AIPICK\s*=\s*new Set\(\[(.*?)\]\)', mvh)
AIPICK = set(x.strip().strip('"') for x in m2.group(1).split(','))

with open("generate_major_pages.py", encoding="utf-8") as f:
    gmp_src = f.read()
subcat_entries = re.findall(
    r"'([^']+)':\s*\{[^}]*'careers':\s*\[([^\]]+)\][^}]*'stars':\s*(\d)", gmp_src, re.DOTALL)
SUBCAT_MAP = {}
for sub, cars_raw, stars in subcat_entries:
    car_list = re.findall(r"'([^']+)'", cars_raw)
    SUBCAT_MAP[sub] = {'stars': int(stars), 'careers': car_list}
CAREER_SUBS = {}
for sub, data in SUBCAT_MAP.items():
    for c in data['careers']:
        CAREER_SUBS.setdefault(c, []).append(sub)

# 读取英文职业数据（工资+技能+ai_tag+简介）
with open("generate_career_pages.py", encoding="utf-8") as f:
    cp_src = f.read()
CAREER_DATA_RAW = {}
pattern = re.compile(
    r"'([^']+)':\s*\(\s*'((?:[^'\\]|\\.)*)',\s*\[(.*?)\],\s*'([^']+)',\s*'([^']+)'\s*\)",
    re.DOTALL)
for m in pattern.finditer(cp_src):
    name = m.group(1)
    if name in ('immune','resistant','augmented','at_risk'): continue
    intro = m.group(2).replace("\\'","'")
    skills_raw = re.findall(r"'([^']+)'", m.group(3))
    salary = m.group(4)
    ai_tag = m.group(5)
    CAREER_DATA_RAW[name] = (intro, skills_raw, salary, ai_tag)

# ── 职业中文名称对照表 ──────────────────────────────────────────────
CN_CAREER_NAMES = {
'Quantum Computing Researcher':'量子计算研究员',
'Photonics Engineer':'光子学工程师',
'Advanced Systems Scientist':'前沿系统科学家',
'Aerospace Engineer':'航空航天工程师',
'Propulsion Engineer':'推进系统工程师',
'Satellite Systems Specialist':'卫星系统专家',
'Aerospace Stress Analyst':'航空结构应力分析师',
'AgTech Field Agronomist':'农业科技田间农艺师',
'AgTech Product Developer':'农业科技产品研发工程师',
'Agribusiness Manager':'农业商务经理',
'Agricultural Supply Chain Director':'农业供应链总监',
'Animal Disease Control Officer':'动物疫病防控官员',
'Animal Science Researcher':'动物科学研究员',
'Aquaculture Manager':'水产养殖场经理',
'Architect':'注册建筑师',
'BIM Specialist':'BIM建筑信息模型专家',
'Urban Designer':'城市设计师',
'Astrophysicist':'天体物理学家',
'Space Agency Researcher':'国家航天科研人员',
'Data Scientist (from computational astronomy)':'数据科学家（天文方向）',
'Athletic Performance Coach':'运动表现教练',
'Sports Health Manager':'运动健康管理师',
'PE Teacher':'体育老师',
'Atmospheric Research Scientist':'大气科学研究员',
'Meteorologist':'气象预报员',
'Climate Data Scientist':'气候数据科学家',
'Automation Engineer':'自动化工程师',
'Robotics Systems Integrator':'机器人系统集成工程师',
'Industrial IoT Specialist':'工业物联网专家',
'Biomedical Researcher':'生物医学研究员',
'Medical AI Data Analyst':'医疗AI数据分析师',
'Pharmaceutical Scientist':'药学科学家',
'Battery Materials Researcher':'电池材料研究员',
'Biostatistician':'生物统计师',
'Biotech Research Scientist':'生物技术研究科学家',
'Genomics Data Analyst':'基因组学数据分析师',
'Cell Therapy Development Specialist':'细胞治疗研发专家',
'Brand Communications Manager':'品牌传播经理',
'Business Development Manager':'商务拓展经理',
'Operations Director':'运营总监',
'Entrepreneur / Startup Founder':'创业者/初创公司创始人',
'Carbon Accounting Specialist':'碳核算专家',
'Forestry Engineer':'林业工程师',
'Remote Sensing Analyst':'遥感数据分析师',
'Carbon Credit Analyst':'碳排放权分析师',
'Pharmaceutical Regulatory Affairs Manager':'药品注册法规事务经理',
'Clinical Pharmacist':'临床药师',
'Drug Safety Specialist':'药物警戒专家',
'Process Engineer':'工艺工程师',
'Pharmaceutical Chemist':'制药化学家',
'Energy Storage Researcher':'储能技术研究员',
'Materials Chemist':'材料化学家',
'Pharmaceutical Production Specialist':'制药生产专员',
'Civil Servant':'国家公务员',
'Infrastructure Planner':'基础设施规划师',
'Structural Engineer':'结构工程师',
'Project Manager':'项目经理',
'Corporate Lawyer':'企业法律顾问',
'International Arbitration Counsel':'国际仲裁律师',
'Legal Compliance Specialist':'法律合规专员',
'Content Strategist':'内容策略师',
'Content Strategy Director':'内容战略总监',
'Editor':'编辑',
'Screenwriter / Cultural Consultant':'编剧/文化顾问',
'Data Journalist':'数据新闻记者',
'EV Electrical Engineer':'新能源汽车电气工程师',
'Power Systems Engineer':'电力系统工程师',
'Smart Grid Specialist':'智能电网专家',
'Earthquake Risk Analyst':'地震风险分析师',
'Geophysicist':'地球物理学家',
'Seismic Data Interpreter':'地震数据解释师',
'Remote Sensing Specialist':'遥感技术专家',
'GIS Analyst':'GIS地理信息分析师',
'Urban Data Scientist':'城市大数据科学家',
'Exploration Geologist':'勘探地质学家',
'Environmental Site Assessor':'环境场地评估师',
'Hydrogeologist':'水文地质工程师',
'Geology Engineering':'地质工程师',
'Environmental Remediation Specialist':'环境修复专家',
'GIS Specialist':'GIS地理信息专家',
'Spatial Data Engineer':'空间数据工程师',
'Power Plant Engineer':'发电厂工程师',
'Nuclear Reactor Engineer':'核反应堆工程师',
'Nuclear Fuel Systems Analyst':'核燃料系统分析师',
'Radiation Safety Specialist':'辐射安全专家',
'Nuclear Systems Engineer':'核系统工程师',
'Marine Systems Engineer':'海洋系统工程师',
'Ocean Data Scientist':'海洋数据科学家',
'Offshore Structural Engineer':'海洋结构工程师',
'Oceanographer':'海洋学家',
'Marine Data Scientist':'海洋数据科学家',
'Offshore Resource Specialist':'海洋资源开发专家',
'Ordnance Engineer':'武器装备工程师',
'Military Equipment Analyst':'军事装备分析师',
'Weapons Systems Engineer':'武器系统工程师',
'Mine Safety Specialist':'矿山安全专家',
'Critical Minerals Analyst':'关键矿产分析师',
'Mining Engineer':'采矿工程师',
'Environmental Consultant':'环境咨询顾问',
'Pollution Control Engineer':'污染控制工程师',
'Conservation Ecologist':'保育生态学家',
'National Reserve Manager':'国家自然保护区管理员',
'Natural Capital Analyst':'自然资本评估分析师',
'Instrumentation Engineer':'仪器仪表工程师',
'Metrology Specialist':'计量专家',
'Quality Assurance Engineer':'质量保证工程师',
'Manufacturing Quality Manager':'制造品质经理',
'Packaging Technology Specialist':'包装技术专家',
'Product Design Engineer':'产品设计工程师',
'Technical Textile Engineer':'纺织技术工程师',
'Textile Process Manager':'纺织工艺经理',
'Sustainable Materials Specialist':'可持续材料专家',
'Mechanical Engineer':'机械工程师',
'Manufacturing Systems Manager':'制造系统经理',
'Robotics Design Engineer':'机器人设计工程师',
'Structural Mechanics Researcher':'结构力学研究员',
'Engineering R&D Specialist':'工程研发专家',
'Flood Control Specialist':'防洪减灾专家',
'Hydraulic Engineer':'水利工程师',
'Water Resource Planner':'水资源规划师',
'Food Safety Engineer':'食品安全工程师',
'R&D Food Scientist':'食品研发科学家',
'Supply Chain Quality Manager':'供应链品控经理',
'Forest Carbon Analyst':'森林碳汇分析师',
'Ecological Restoration Specialist':'生态修复专家',
'Timber Certification Officer':'木材认证官员',
'Crop Science Specialist':'作物科学专家',
'Precision Agriculture Data Analyst':'精准农业数据分析师',
'Livestock Production Manager':'畜牧生产经理',
'Precision Farming Specialist':'精准农业专家',
'Fisheries Research Scientist':'渔业科学研究员',
'Water Quality Specialist':'水质检测专家',
'Economic Policy Analyst':'经济政策分析师',
'Development Finance Specialist':'发展金融专家',
'Strategy Consultant':'战略咨询顾问',
'Investment Analyst':'投资分析师',
'Fintech Product Manager':'金融科技产品经理',
'Risk Manager':'风险管理师',
'Actuarial Scientist':'精算师',
'Quantitative Analyst':'量化分析师',
'Machine Learning Researcher':'机器学习研究员',
'Data Scientist':'数据科学家',
'Quantitative Risk Analyst':'量化风险分析师',
'Data-Driven Strategy Manager':'数据驱动战略经理',
'Operations Research Analyst':'运筹学分析师',
'Management Consultant':'管理咨询顾问',
'Smart Manufacturing Consultant':'智能制造顾问',
'Industrial Engineer':'工业工程师',
'Supply Chain Optimization Specialist':'供应链优化专家',
'International Business Manager':'国际商务经理',
'Language Technology Specialist':'语言技术专家',
'Technical / Legal Interpreter':'技术/法律口译员',
'Government Policy Researcher':'政府政策研究员',
'Party School Lecturer':'党校讲师',
'University Political Affairs Staff':'高校思政工作者',
'Diplomatic Affairs Officer':'外交事务官员',
'International Relations Researcher':'国际关系研究员',
'Policy Analyst':'政策分析师',
'AI Ethics Researcher':'AI伦理研究员',
'Technology Governance Specialist':'科技治理专家',
'Community Development Officer':'社区发展专员',
'Corporate Social Responsibility Specialist':'企业社会责任专员',
'Social Researcher':'社会学研究员',
'Epidemiologist':'流行病学家',
'Disease Surveillance Specialist':'疾病监测专家',
'Public Health Policy Analyst':'公共卫生政策分析师',
'Curriculum Developer':'课程研发专员',
'Teacher':'教师',
'EdTech Product Specialist':'教育科技产品专员',
'Historical Researcher':'历史学研究员',
'Museum Curator':'博物馆策展人',
'Policy Institute Analyst':'智库政策分析师',
'Ethnology Researcher':'民族学研究员',
'Minority Policy Analyst':'民族政策分析师',
'Cultural Affairs Officer':'文化事务官员',
'Hotel General Manager':'酒店总经理',
'Tourism Product Developer':'旅游产品策划师',
'Travel Platform Operations Manager':'旅游平台运营经理',
'Information Architecture Consultant':'信息架构咨询顾问',
'Digital Archivist':'数字档案师',
'Knowledge Management Specialist':'知识管理专员',
'E-Commerce Operations Manager':'电商运营经理',
'Cross-Border Trade Specialist':'跨境贸易专员',
'Digital Marketing Analyst':'数字营销分析师',
'Cross-Border Operations Director':'跨境运营总监',
'Supply Chain Manager':'供应链经理',
'Logistics Analytics Specialist':'物流数据分析师',
'Government Budget Analyst':'政府预算分析师',
'Fiscal Policy Advisor':'财政政策顾问',
'Tax Administration Specialist':'税务管理专员',
'Government Policy Manager':'政府政策管理专员',
'Urban Planning Official':'城市规划官员',
'Criminal Investigation Specialist':'刑事侦查专员',
'Cybercrime Investigator':'网络犯罪侦查员',
'Police Officer':'人民警察',
'Emergency Response Technologist':'应急响应技术员',
'Forensic Systems Specialist':'司法鉴定系统专家',
'Security Technology Engineer':'安防技术工程师',
'Forensic Pathologist':'法医病理学家',
'Forensic Toxicologist':'法医毒理学家',
'Legal Medicine Expert':'法医鉴定专家',
'Clinical Laboratory Technologist':'临床检验技师',
'Medical Imaging Specialist':'医学影像专家',
'Pathology Lab Manager':'病理实验室主任',
'Clinical Psychologist':'临床心理咨询师',
'Organizational Behavior Consultant':'组织行为顾问',
'UX Research Specialist':'用户体验研究专家',
'TCM Physician':'中医执业医师',
'Acupuncturist':'针灸师',
'TCM Product Developer':'中药产品研发师',
'Herbal Medicine Quality Analyst':'中药质量分析师',
'TCM Pharmacognosist':'生药学专家',
'Natural Product Researcher':'天然产物研究员',
'Integrative Medicine Physician':'中西医结合执业医师',
'Clinical TCM-Western Hybrid Specialist':'中西医临床专家',
'Integrative Health Researcher':'整合医学研究员',
'Physician':'临床执业医师',
'Medical Specialist':'专科主治医生',
'Clinical Department Director':'临床科室主任',
'Dentist':'口腔科执业医师',
'Dental Implant Surgeon':'口腔种植外科医生',
'Orthodontics Specialist':'正畸专科医生',
'Registered Nurse':'注册护士',
'Specialized Care Nurse':'专科护士',
'Community Health Practitioner':'社区卫生工作者',
'Medical Device Engineer':'医疗器械工程师',
'Health AI Product Manager':'医疗AI产品经理',
'Clinical Systems Analyst':'临床信息系统分析师',
'Software Engineer':'软件工程师',
'AI/ML Engineer':'AI/机器学习工程师',
'Cloud Architect':'云架构师',
'Embedded Systems Developer':'嵌入式系统开发工程师',
'IC Design Engineer':'集成电路设计工程师',
'RF Communications Engineer':'射频通信工程师',
'Semiconductor Physicist':'半导体物理学家',
'Semiconductor Process Engineer':'半导体工艺工程师',
'Scientific Instrument Engineer':'科学仪器工程师',
'Farm Automation Specialist':'农场自动化专家',
'Rural Development Officer':'乡村振兴专员',
'Desertification Control Specialist':'荒漠化治理专家',
'Grassland Ecologist':'草地生态学家',
'Rangeland Manager':'草地管理员',
'Defense Technology Researcher':'国防科技研究员',
'Companion Animal Veterinarian':'小动物（宠物）执业兽医',
'Food Safety Inspection Veterinarian':'食品安全检疫兽医',
'Export Control Consultant':'出口管制合规顾问',
'Industrial Hazard Consultant':'工业危害咨询顾问',
'International Market Analyst':'国际市场分析师',
'Precision Agriculture Engineer':'精准农业工程师',
'Renewable Energy Analyst':'可再生能源分析师',
'Risk Assessment Specialist':'风险评估专家',
'Safety Engineer':'安全工程师',
'Trade Compliance Specialist':'贸易合规专员',
'Cross-disciplinary R&D Researcher':'跨学科研发研究员',
'Emerging Tech Specialist':'新兴技术专家',
'Systems Integration Engineer':'系统集成工程师',
'Rail Infrastructure Specialist':'铁路基础设施专家',
'Traffic Data Analyst':'交通数据分析师',
'Transportation Systems Engineer':'交通系统工程师',
'Advanced Composites Specialist':'先进复合材料专家',
}

# ── AI影响分级（中文）──────────────────────────────────────────────
AI_IMPACT_CN = {
  'immune': {
    'label': '🛡️ AI高度安全',
    'desc': '该职业的核心工作内容是人际互动、临床判断或现场操作，AI目前几乎无法替代。具备该职业技能的毕业生工作稳定性强。',
    'color': '#10b981', 'border': 'rgba(16,185,129,.4)', 'bg': 'rgba(16,185,129,.05)',
  },
  'resistant': {
    'label': '🛡️ 较强AI抵御力',
    'desc': '该职业依赖专业判断、创意或人际沟通，AI工具可以辅助但难以全面替代。主动学习AI辅助工具将显著提升工作效率。',
    'color': '#3b82f6', 'border': 'rgba(59,130,246,.4)', 'bg': 'rgba(59,130,246,.05)',
  },
  'augmented': {
    'label': '⚡ AI赋能提升',
    'desc': 'AI工具将大幅提升该职业的工作效率，善于运用AI的从业者可以产出倍增。主动学习AI工具的毕业生将明显领先于同行。',
    'color': '#8b5cf6', 'border': 'rgba(139,92,246,.4)', 'bg': 'rgba(139,92,246,.05)',
  },
  'at_risk': {
    'label': '⚠️ 需关注AI影响',
    'desc': '该职业部分常规工作正在被AI工具替代。建议主动向更高价值的专业方向转型，并深耕AI难以取代的判断性、创造性技能。',
    'color': '#f59e0b', 'border': 'rgba(245,158,11,.4)', 'bg': 'rgba(245,158,11,.05)',
  },
}

# 职业星级 = 所在子类别星级
def get_career_stars(career_name):
    subs = CAREER_SUBS.get(career_name, [])
    if not subs: return 3
    return max(SUBCAT_MAP.get(s, {}).get('stars', 3) for s in subs)

# 找到该职业对应的专业（来自ALL数组）
def get_related_majors(career_name):
    """Find majors that mention this career via SUBCAT_MAP"""
    career_subs = CAREER_SUBS.get(career_name, [])
    result = []
    seen = set()
    for major in ALL:
        sub = major.get('sub', major.get('cat', ''))
        en = major.get('n', '')
        if sub in career_subs and en not in seen:
            seen.add(en)
            result.append(major)
    return result[:12]

DISCLAIMER = '''<div style="background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.4);
border-radius:10px;padding:14px 18px;margin:0 0 18px;font-size:13px;line-height:1.75;color:#fbbf24;">
⚠️ <strong>重要提示：</strong>高考填报志愿是人生大事，请谨慎决策。本页内容由人工智能生成，
数据仅供参考，不代表官方立场。薪资数据为市场参考范围，受地区、单位性质和个人能力影响较大。
填报专业请以各高校官方招生简章为准，并务必咨询专业升学指导老师。<strong>请勿将本页作为唯一填报依据。</strong>
</div>'''

def page_cn(en_name):
    cn_name = CN_CAREER_NAMES.get(en_name, en_name)
    data = CAREER_DATA_RAW.get(en_name)
    if not data:
        return None

    intro_en, skills_en, salary, ai_tag = data
    ai = AI_IMPACT_CN.get(ai_tag, AI_IMPACT_CN['augmented'])
    stars = get_career_stars(en_name)
    rel_majors = get_related_majors(en_name)

    star_str = stars_html(stars)
    star_label_map = {5:'就业前景极佳',4:'就业前景良好',3:'就业前景稳定',2:'需要谨慎规划',1:'面临较大挑战'}
    star_label = star_label_map.get(stars, '就业前景稳定')

    # 技能（直接展示英文+通用缩写，因为技术词汇全球通用）
    skills_html = ''.join(f'<span class="skill">{s}</span>' for s in skills_en)

    # 相关专业链接
    if rel_majors:
        major_links = '\n'.join(
            f'''<a class="major-link" href="/tools/majors-cn/{slug(m["n"])}.html">
  <span class="stars">{"★"*min(5,SUBCAT_MAP.get(m.get("sub",m["cat"]),{}).get("stars",3)+1) if m["c"] in AIPICK else "★"*SUBCAT_MAP.get(m.get("sub",m["cat"]),{}).get("stars",3)}{"☆"*(5-min(5,SUBCAT_MAP.get(m.get("sub",m["cat"]),{}).get("stars",3)))}</span>
  <span class="mname">{CN_MAJOR_NAMES.get(m["n"], m["n"])}</span>
  <span class="msub" style="font-size:11px;color:#64748b;">{m["n"]}</span>
</a>''' for m in rel_majors
        )
    else:
        major_links = '<p style="color:#64748b;font-size:13px;">该职业对应专业数据整理中</p>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cn_name} — 职业前景与薪资分析 2025 | 高考志愿参考</title>
<meta name="description" content="{cn_name}职业的薪资范围、技能要求、AI影响分析及对应大学专业，帮助高考生了解{cn_name}的就业前景。">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://ordinarymantrying.com/tools/careers-cn/{slug(en_name)}.html">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article",
  "headline":"{cn_name} — 职业前景与薪资分析 2025",
  "description":"{cn_name}职业的薪资范围、技能要求、AI影响分析及对应大学专业。",
  "url":"https://ordinarymantrying.com/tools/careers-cn/{slug(en_name)}.html",
  "inLanguage":"zh-CN"}}
</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  background:#0f172a;color:#e2e8f0;line-height:1.7;}}
a{{color:#60a5fa;text-decoration:none;}}
a:hover{{text-decoration:underline;}}
.hdr{{background:linear-gradient(160deg,#0d1b2e,#1a3560);padding:28px 20px 22px;
  border-bottom:1px solid #334155;}}
.back{{display:inline-flex;align-items:center;gap:6px;margin-bottom:16px;
  padding:8px 16px;background:rgba(255,255,255,.06);border:1px solid #334155;
  border-radius:8px;font-size:13px;font-weight:600;color:#cbd5e1;text-decoration:none;}}
.back:hover{{background:rgba(59,130,246,.12);color:#60a5fa;text-decoration:none;}}
.badge{{font-size:11px;text-transform:uppercase;letter-spacing:.12em;
  color:#3b82f6;font-family:monospace;margin-bottom:8px;}}
h1{{font-size:clamp(22px,5vw,32px);font-weight:800;line-height:1.2;margin-bottom:6px;}}
.meta{{font-size:13px;color:#64748b;margin-top:4px;}}
.page{{max-width:700px;margin:0 auto;padding:22px 18px 60px;}}
.card{{background:#1e293b;border:1px solid #334155;border-radius:12px;
  padding:18px 20px;margin-bottom:14px;}}
.card h2{{font-size:15px;font-weight:700;margin-bottom:10px;color:#e2e8f0;}}
.card p{{font-size:14px;color:#cbd5e1;line-height:1.8;}}
.salary-big{{font-size:24px;font-weight:800;color:#10b981;}}
.salary-note{{font-size:12px;color:#64748b;margin-top:6px;}}
.ai-card{{border-radius:12px;padding:16px 20px;margin-bottom:14px;border:1px solid;}}
.ai-label{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px;}}
.skills{{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;}}
.skill{{padding:4px 12px;background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);
  border-radius:20px;font-size:12px;color:#93c5fd;}}
.stage{{margin-bottom:12px;}}
.stage strong{{color:#e2e8f0;font-size:14px;}}
.stage p{{font-size:13px;color:#94a3b8;margin-top:4px;}}
.major-link{{display:flex;align-items:center;gap:10px;padding:10px 14px;
  background:#1e293b;border:1px solid #334155;border-radius:8px;
  margin-bottom:6px;text-decoration:none;color:inherit;}}
.major-link:hover{{border-color:rgba(59,130,246,.5);text-decoration:none;}}
.stars{{color:#f59e0b;font-size:12px;flex-shrink:0;}}
.mname{{font-size:13px;font-weight:600;color:#e2e8f0;flex:1;}}
.cta{{display:block;text-align:center;padding:14px;margin:20px 0 12px;
  background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);
  border-radius:10px;font-size:14px;font-weight:600;color:#60a5fa;}}
.cta:hover{{background:rgba(59,130,246,.15);text-decoration:none;}}
.foot{{text-align:center;padding:20px;font-size:12px;color:#475569;
  border-top:1px solid #1e293b;line-height:2;}}
</style>
</head>
<body>
<div class="hdr">
  <a class="back" href="/tools/careers-cn/">← 返回所有职业列表</a>
  <div class="badge">职业前景分析 · 2025-2029</div>
  <h1>{cn_name}</h1>
  <div class="meta">英文名：{en_name} &nbsp;·&nbsp; 综合评级：{star_str} {star_label}</div>
</div>

<div class="page">
{DISCLAIMER}

<div class="card">
  <h2>职业简介</h2>
  <p>{intro_en}</p>
  <p style="margin-top:8px;font-size:13px;color:#64748b;">注：职业描述基于市场通用岗位职能，实际工作内容因单位和部门有所不同。</p>
</div>

<div class="card">
  <h2>💰 薪资参考范围</h2>
  <div class="salary-big">{salary}</div>
  <p class="salary-note">月薪（税前）· 受地区、单位性质和个人能力影响较大<br>
  北京、上海、深圳等一线城市薪资通常高于全国平均水平 20–40%<br>
  国有企业稳定性强，私营和外资企业薪资弹性较大</p>
</div>

<div class="ai-card" style="border-color:{ai['border']};background:{ai['bg']};">
  <div class="ai-label" style="color:{ai['color']}">{ai['label']}</div>
  <p style="font-size:13px;color:#cbd5e1;line-height:1.8;">{ai['desc']}</p>
</div>

<div class="card">
  <h2>🔑 核心技能要求</h2>
  <div class="skills">{skills_html}</div>
  <p style="font-size:12px;color:#64748b;margin-top:10px;">技术技能名称保留英文（行业通用表达），面试和实际工作中均以此为准。</p>
</div>

<div class="card">
  <h2>📈 职业发展阶段</h2>
  <div class="stage">
    <strong>入职 1–3 年（初级）</strong>
    <p>在导师或上级指导下熟悉业务体系，建立专业知识框架。通常需要 3–6 个月内开始独立承担项目模块。</p>
  </div>
  <div class="stage">
    <strong>3–6 年（中级）</strong>
    <p>独立主导项目或业务模块，开始带领初级成员，逐步建立行业内的专业声誉和人脉网络。</p>
  </div>
  <div class="stage">
    <strong>6 年以上（高级/管理）</strong>
    <p>负责重大项目或部门管理，参与战略决策，薪资上限显著提升。高级岗位通常需要丰富的项目记录或专业认证。</p>
  </div>
</div>

<div style="font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#94a3b8;
  font-weight:700;margin:20px 0 10px;">通往此职业的推荐大学专业</div>
{major_links}

<a class="cta" href="/tools/major-vote-cn.html">← 返回757个专业对比工具</a>

</div>
<div class="foot">
  数据参考：高校就业质量报告 · 市场薪资调研 · 教育部学科目录<br>
  ⚠️ 本站由AI辅助生成，内容仅供参考，请以官方信息为准<br>
  <a href="/tools/careers-cn/">所有职业列表</a> &nbsp;|&nbsp;
  <a href="/tools/major-vote-cn.html">专业对比工具</a>
</div>
</body></html>'''

# ═══════════════════════════════════════════════════════════════════
# INDEX PAGE
# ═══════════════════════════════════════════════════════════════════
def build_index(career_names):
    # Group by AI tag
    groups = {'immune':[],'resistant':[],'augmented':[],'at_risk':[]}
    cn_group = {
        'immune':'🛡️ AI高度安全型职业',
        'resistant':'🛡️ AI较强抵御力职业',
        'augmented':'⚡ AI赋能提升型职业',
        'at_risk':'⚠️ 需关注AI影响的职业',
    }
    for en in career_names:
        data = CAREER_DATA_RAW.get(en)
        if data:
            groups[data[3]].append(en)
        else:
            groups['augmented'].append(en)

    sections = ''
    for tag in ('immune','resistant','augmented','at_risk'):
        careers = groups[tag]
        if not careers: continue
        rows = ''.join(
            f'<a href="/tools/careers-cn/{slug(c)}.html" class="clink">'
            f'{CN_CAREER_NAMES.get(c, c)}'
            f'<span class="cen">{c}</span></a>\n'
            for c in sorted(careers, key=lambda x: CN_CAREER_NAMES.get(x, x))
        )
        ai = AI_IMPACT_CN[tag]
        sections += f'''<div class="grp-section">
<h2 class="grp-h" style="color:{ai["color"]}">{cn_group[tag]} <span class="cnt">({len(careers)})</span></h2>
<div class="clist">{rows}</div>
</div>\n'''

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>259个职业前景分析 — AI时代哪些工作最安全？| 高考志愿参考</title>
<meta name="description" content="按AI影响程度分类的259个职业前景分析，帮助高考生了解选择专业后的职业发展前景和薪资待遇。">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://ordinarymantrying.com/tools/careers-cn/">
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  background:#0f172a;color:#e2e8f0;line-height:1.7;}}
a{{color:#60a5fa;text-decoration:none;}}
.hdr{{background:linear-gradient(160deg,#0d1b2e,#1a3560);padding:32px 20px 28px;
  border-bottom:1px solid #334155;text-align:center;}}
h1{{font-size:clamp(20px,4vw,30px);font-weight:800;margin-bottom:8px;}}
.sub{{font-size:14px;color:#64748b;}}
.warn{{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.4);
  border-radius:10px;padding:14px 18px;margin:20px auto;max-width:700px;
  font-size:13px;color:#fbbf24;line-height:1.75;}}
.page{{max-width:700px;margin:0 auto;padding:20px 18px 60px;}}
.grp-section{{margin-bottom:28px;}}
.grp-h{{font-size:14px;font-weight:700;margin-bottom:10px;}}
.cnt{{color:#475569;font-size:12px;}}
.clist{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:6px;}}
.clink{{display:block;padding:8px 12px;background:#1e293b;border:1px solid #334155;
  border-radius:8px;font-size:13px;font-weight:600;color:#e2e8f0;}}
.clink:hover{{border-color:rgba(59,130,246,.5);color:#60a5fa;text-decoration:none;}}
.cen{{display:block;font-size:11px;color:#64748b;font-weight:400;margin-top:2px;}}
.back-btn{{display:block;text-align:center;padding:12px;margin-bottom:20px;
  background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);
  border-radius:10px;font-size:14px;font-weight:600;color:#60a5fa;}}
.foot{{text-align:center;padding:20px;font-size:12px;color:#475569;border-top:1px solid #1e293b;}}
</style>
</head>
<body>
<div class="hdr">
  <h1>💼 259个职业前景分析</h1>
  <div class="sub">按AI影响程度分类 · 高考志愿参考工具</div>
</div>

<div class="page">
<div class="warn">
⚠️ 本站内容由人工智能生成，仅供参考，不代表官方立场。
职业发展受个人能力、地区和市场环境影响显著。高考填报请咨询专业老师。
</div>

<a class="back-btn" href="/tools/major-vote-cn.html">🗳️ 返回专业投票与对比工具</a>

{sections}

</div>
<div class="foot">
  数据参考：高校就业质量报告 · 市场薪资调研<br>
  ⚠️ 本站由AI辅助生成，内容仅供参考
</div>
</body></html>'''

# ═══════════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════════
out_dir = 'ordinarymantrying.com/tools/careers-cn'
os.makedirs(out_dir, exist_ok=True)

# Use the same career names as the English site
career_names_to_generate = list(CAREER_DATA_RAW.keys())

ok = skip = 0
for en_name in career_names_to_generate:
    html = page_cn(en_name)
    if html is None:
        skip += 1; continue
    fname = os.path.join(out_dir, f'{slug(en_name)}.html')
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    ok += 1

with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(build_index(career_names_to_generate))

print(f'✅ 生成 {ok} 个中文职业页面（跳过 {skip}）→ {out_dir}/')
