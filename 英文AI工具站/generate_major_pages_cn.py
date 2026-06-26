#!/usr/bin/env python3
"""
生成 757 个中文专业详情页 → tools/majors-cn/
特点：纯工具页（无建站博客内容）+ 明显免责声明 + 中文权威内容
"""
import json, re, os, unicodedata, sys
sys.path.insert(0, os.path.dirname(__file__))
from cn_names import CN_MAJOR_NAMES, CN_SUBCAT

with open("ordinarymantrying.com/tools/major-vote.html", encoding="utf-8") as f:
    src = f.read()

m  = re.search(r'const ALL\s*=\s*(\[.*?\]);', src, re.DOTALL)
ALL = json.loads(m.group(1))
m2 = re.search(r'const AIPICK\s*=\s*new Set\(\[(.*?)\]\)', src)
AIPICK = set(x.strip().strip('"') for x in m2.group(1).split(','))

# ═══════════════════════════════════════════════════════════════════
# 每个子类别的中文典型职业方向（对应英文 SUBCAT careers）
# ═══════════════════════════════════════════════════════════════════
CN_CAREERS = {
  'Advanced Engineering': ['量子计算研究员','光子学工程师','前沿系统科学家'],
  'Aerospace': ['航空航天工程师','卫星系统专家','推进系统工程师'],
  'Agricultural Engineering': ['精准农业工程师','农业科技产品研发','农场自动化专家'],
  'Architecture': ['注册建筑师','城市设计师','BIM工程师'],
  'Automation': ['自动化工程师','机器人系统集成工程师','工业物联网专家'],
  'Biomedical Engineering': ['医疗器械研发工程师','临床系统分析师','医疗AI产品经理'],
  'Chem Engineering & Pharmacy': ['工艺工程师','制药生产专员','电池材料研究员'],
  'Civil Engineering': ['结构工程师','项目经理','基础设施规划师'],
  'Computer Science': ['软件工程师','AI/机器学习工程师','云架构师'],
  'Electrical Engineering': ['电力系统工程师','新能源汽车电气工程师','智能电网专家'],
  'Electronic Information': ['集成电路设计工程师','射频通信工程师','嵌入式系统开发工程师'],
  'Energy & Power': ['电厂工程师','新能源分析师','核电系统工程师'],
  'Environmental Engineering': ['环境咨询顾问','碳资产核查分析师','污染控制工程师'],
  'Food Science & Engineering': ['食品安全工程师','食品研发科学家','供应链品控经理'],
  'Forestry Engineering': ['林业工程师','碳汇计量专家','遥感分析师'],
  'Geology Engineering': ['勘探地质工程师','矿山现场工程师','环境修复专家'],
  'Hydraulic Engineering': ['水利工程师','水资源规划师','防洪减灾专家'],
  'Instrumentation': ['仪器仪表工程师','计量专家','品质保证工程师'],
  'Interdisciplinary Eng': ['系统集成工程师','新兴技术专家','跨学科研发研究员'],
  'Light Industry': ['产品设计工程师','包装技术专家','制造品质经理'],
  'Materials Science': ['电池材料研究员','半导体工艺工程师','先进复合材料专家'],
  'Mechanical Engineering': ['机械工程师','机器人设计工程师','制造系统经理'],
  'Mechanics': ['结构力学研究员','航空应力分析师','工程研发专家'],
  'Mining': ['采矿工程师','关键矿产分析师','矿山安全专家'],
  'Nuclear Engineering': ['核反应堆工程师','辐射安全专家','核燃料系统分析师'],
  'Ocean Engineering': ['海洋结构工程师','海洋系统工程师','海洋大数据科学家'],
  'Ordnance': ['武器系统工程师','国防技术研究员','军事装备分析师'],
  'Public Security Tech': ['安防技术工程师','司法鉴定系统专家','应急响应技术员'],
  'Safety Engineering': ['安全工程师','风险评估专家','工业危害咨询顾问'],
  'Semiconductor': ['集成电路设计工程师','工艺开发工程师','半导体材料科学家'],
  'Surveying & Mapping': ['测绘工程师','GIS数据分析师','遥感技术专家'],
  'Textile': ['纺织技术工程师','可持续材料科学家','服装供应链经理'],
  'Transportation': ['交通系统工程师','物流技术专家','智能驾驶工程师'],
  # Science
  'Astronomy': ['天文学研究员','射电望远镜工程师','空间数据科学家'],
  'Atmospheric Sciences': ['气象预报员','气候变化研究员','大气环境监测工程师'],
  'Biological Sciences': ['生物技术研究员','生物信息学分析师','生态系统研究员'],
  'Chemistry': ['化学研究员','材料分析工程师','精细化学品研发师'],
  'Geographic Sciences': ['自然地理研究员','城乡规划地理分析师','GIS工程师'],
  'Geology': ['地质勘查工程师','矿产资源分析师','地质灾害评估专家'],
  'Geophysics': ['地球物理勘探工程师','地震监测专家','油藏物理分析师'],
  'Marine Sciences': ['海洋生物研究员','海洋环境监测专家','深海资源调查员'],
  'Mathematics': ['数学研究员','量化金融分析师','数据科学家'],
  'Ocean Sciences': ['海洋学研究员','海洋气候分析师','深海探测技术员'],
  'Physics': ['物理学研究员','半导体物理工程师','量化分析师'],
  'Psychology': ['心理咨询师','用户研究分析师','企业心理健康顾问'],
  'Statistics': ['统计分析师','生物统计研究员','数据科学家'],
  # Agriculture
  'Agricultural Management': ['农业经济研究员','农业供应链经理','乡村振兴专员'],
  'Animal Production': ['畜牧技术员','饲料配方师','养殖场管理员'],
  'Crop Production': ['农艺师','育种研究员','农业生产技术员'],
  'Fisheries': ['水产养殖技术员','渔业资源评估师','水产品质检员'],
  'Forestry': ['林业工程师','生态修复专家','国家公园管理员'],
  'Grassland Science': ['草地生态修复师','草业技术员','荒漠化治理工程师'],
  'Nature Conservation & Ecology': ['自然保护区管理员','生物多样性监测员','生态系统服务评估师'],
  'Veterinary Medicine': ['执业兽医师','宠物科主治医生','动物防疫检疫员'],
  # Medicine
  'Basic Medical Sciences': ['基础医学研究员','生物医药研发科学家','医学教育工作者'],
  'Clinical Medicine': ['临床执业医师','专科主治医生','住院医师'],
  'Dental Medicine': ['执业口腔医师','口腔科主治医生','口腔修复技师'],
  'Forensic Medicine': ['法医学工作者','司法鉴定人','法医毒理专家'],
  'Integrative Medicine': ['中西医结合医师','综合医院中西医科大夫','临床研究员'],
  'Medical Technology': ['医学检验师','医学影像技师','康复治疗师'],
  'Nursing': ['注册护士','专科护士','护士长'],
  'Pharmacy': ['执业药师','药物研发科学家','医院临床药师'],
  'Public Health': ['公共卫生医师','流行病学调查员','卫生政策分析师'],
  'Trad. Chinese Medicine': ['中医执业医师','中医科主治医生','中药师'],
  # Economics
  'Economics': ['经济研究员','政策分析师','产业经济分析师'],
  'Finance': ['投资分析师','风险管理师','基金经理'],
  'Intl Economics & Trade': ['国际贸易专员','外贸业务员','贸易合规顾问'],
  'Public Finance': ['财政分析师','国有资产管理专员','政府审计员'],
  # Management
  'Business Administration': ['企业管理培训生','运营经理','战略分析师'],
  'E-Commerce': ['电商运营专员','跨境电商经理','新媒体营销专员'],
  'Industrial Engineering': ['工业工程师','精益生产顾问','供应链优化专家'],
  'Library & Info Management': ['图书馆员','知识管理专员','信息资源管理师'],
  'Logistics Management': ['物流规划师','仓储运营经理','供应链分析师'],
  'Management Sci & Eng': ['管理咨询顾问','数据驱动运营专家','项目管理师'],
  'Public Administration': ['公务员','政策研究员','政府项目管理专员'],
  'Tourism Management': ['酒店管理培训生','旅游产品经理','景区运营专员'],
  # Law / Education / Humanities
  'Education': ['中小学教师','教育技术产品经理','教育机构课程设计师'],
  'Ethnology': ['民族研究员','民族政策分析师','文化遗产保护专员'],
  'Foreign Languages': ['翻译或口译员','跨文化商务专员','外语教师'],
  'History': ['博物馆策展人','历史研究员','文化遗产保护工作者'],
  'Journalism & Comm': ['新媒体内容运营','记者或编辑','品牌传播专员'],
  'Law': ['律师','法律顾问','企业合规专员'],
  'Chinese Language & Lit': ['中文教师','媒体编辑','内容创作者'],
  'Marxist Theory': ['高校思政教师','党政研究员','社会治理分析师'],
  'Philosophy': ['AI伦理研究员','政策研究员','法律与哲学顾问'],
  'Physical Education': ['体育教师','运动康复师','体育产业运营'],
  'Political Science': ['政府公务员','国际事务研究员','国企政策岗'],
  'Public Security': ['公安民警','安全管理专员','网络安全执法员'],
  'Sociology': ['用户研究分析师','社会政策研究员','社会工作师'],
  'Agricultural Management (Mgmt)': ['农林经济分析师','乡村振兴专员','农业供应链经理'],
  'Chinese Materia Medica': ['中药师','中药研发研究员','中药质量检验师'],
}

DEFAULT_SUBCAT = {
  'pros': ['该专业具有稳定的社会需求','培养复合型专业知识与技能','毕业生就业方向多元'],
  'cons': ['竞争较为激烈，需要主动规划','薪资受细分方向影响差异较大'],
  'verdict': '该专业提供专业化的职业培养路径，具体发展前景取决于所选细分方向和个人技能积累。建议深入了解招生信息和毕业生就业情况后再做决策。',
}
DEFAULT_CAREERS = ['专业相关工程师或研究员','技术分析师','行业专家顾问']

STAR_OPEN_CN = {
  5: '综合来看，这是目前就业前景最强劲的专业方向之一。',
  4: '综合来看，这个专业在未来几年内具备较强的就业竞争力。',
  3: '综合来看，这个专业就业基础稳定，但未来发展空间取决于你的专业化选择。',
  2: '综合来看，这个专业面临一定的市场调整压力，选择时需要更谨慎的规划。',
  1: '综合来看，这个专业目前面临较大挑战，建议结合个人情况和市场现状慎重评估。',
}

AI_IMPACT_CN = {
  'Engineering':  'AI是工程师的助手，不是替代者。掌握AI辅助设计、仿真和优化工具的工程师，将比同行效率高出数倍。未来的需求是既懂专业领域、又能驾驭AI工具的复合型工程师。',
  'Medicine':     'AI在影像诊断和新药研发中发挥越来越大的作用，但临床判断、医患沟通和手术操作是AI难以取代的核心能力。医学生应主动学习AI辅助诊断工具，而不是担忧被替代。',
  'Science':      'AI正在加速科学研究——自动化文献综述、智能实验设计、大规模数据分析。主动拥抱计算科学工具的理科生，将在科研效率上远超同龄人。',
  'Economics':    '常规经济数据分析已逐步自动化。能结合经济理论与数据科学技能、并能清晰表达见解的经济学生，市场竞争力更强。细分专业化比通才化更重要。',
  'Management':   'AI正在接管排班、报表和常规分析。真正不可替代的管理人才，是能够提供判断力、建立利益相关方关系、把握战略方向的人。管理岗位的整体门槛在上移。',
  'Education':    'AI辅助工具正在提升个性化教学能力。善用AI备课、批改和学情分析的老师，将更有效率，也更有竞争力。但教育的核心仍是人与人之间的激励与关怀。',
  'Law':          'AI已能高效处理文件审查、合同分析和案例检索。专注于庭审辩护、谈判斡旋和复杂客户判断的律师，受自动化冲击最小。',
  'Literature':   'AI能批量生成通用内容，但真正有辨识度的声音、深刻的文化洞察和精准的编辑判断，是AI暂时无法替代的。掌握AI内容工具反而能让你的产出翻倍。',
  'History':      'AI能快速检索和整合历史信息，但诠释历史的能力——分析史料、识别系统性规律、评价历史影响——仍然是人类独有的高阶技能。',
  'Philosophy':   'AI本身无法独立推理伦理、价值和治理问题。哲学专业的学生正成为AI开发、政策制定和技术治理领域不可或缺的协作者。',
  'Agriculture':  'AI、无人机和物联网传感器正在快速改造农业生产方式。既懂农业专业知识、又掌握技术工具的毕业生，将引领中国农业现代化转型。',
}

STAR_LABEL_CN = {5:'强烈推荐', 4:'值得选择', 3:'稳中有变', 2:'谨慎考量', 1:'需充分规划'}

CAT_CN = {
  'Engineering':'工学','Medicine':'医学','Science':'理学','Economics':'经济学',
  'Management':'管理学','Education':'教育学','Law':'法学','Literature':'文学',
  'History':'历史学','Philosophy':'哲学','Agriculture':'农学',
}

DISCLAIMER = '''<div style="background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.4);
border-radius:10px;padding:14px 18px;margin:0 0 20px;font-size:13px;line-height:1.75;color:#fbbf24;">
⚠️ <strong>重要提示：</strong>高考填报志愿是人生大事，请谨慎决策。本页内容由人工智能生成，数据仅供参考，
不代表教育主管部门或高校官方立场。最终填报请以各高校官方招生简章为准，并务必咨询专业升学指导老师或招生顾问。
<strong>请勿将本页作为唯一填报依据。</strong>
</div>'''

def slug(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def stars_html(n): return '★' * n + '☆' * (5 - n)

def page_cn(major):
    code   = major['c']
    en_name = major['n']
    cn_name = CN_MAJOR_NAMES.get(en_name, en_name)
    cat    = major['cat']
    sub    = major.get('sub', cat)
    is_ai  = code in AIPICK

    d = CN_SUBCAT.get(sub, DEFAULT_SUBCAT)
    rating = min(5, (3 if 'verdict' in d else 3) + (1 if is_ai else 0))
    # Read stars from English SUBCAT to keep rating consistent
    # We'll compute from verdict keyword or default 3
    # Better: map from English stars
    rating_map = {
      'Advanced Engineering':5,'Aerospace':4,'Agricultural Engineering':3,'Architecture':3,
      'Automation':4,'Biomedical Engineering':4,'Chem Engineering & Pharmacy':3,'Civil Engineering':3,
      'Computer Science':5,'Electrical Engineering':4,'Electronic Information':5,'Energy & Power':4,
      'Environmental Engineering':3,'Food Science & Engineering':3,'Forestry Engineering':3,
      'Geology Engineering':3,'Hydraulic Engineering':3,'Instrumentation':3,'Interdisciplinary Eng':3,
      'Light Industry':3,'Materials Science':4,'Mechanical Engineering':3,'Mechanics':3,'Mining':3,
      'Nuclear Engineering':4,'Ocean Engineering':3,'Ordnance':3,'Public Security Tech':3,
      'Safety Engineering':3,'Semiconductor':5,'Surveying & Mapping':3,'Textile':2,'Transportation':3,
      'Philosophy':2,'Economics':3,'Finance':4,'Intl Economics & Trade / Public Finance':3,
      'Sociology':3,'Political Science':3,'Ethnology':2,'Marxist Theory':3,'Public Security':3,
      'Education':3,'Physical Education':3,'Chinese Language & Lit':3,'Foreign Languages':3,
      'Journalism & Comm':3,'History':2,'Mathematics':4,'Physics':4,'Chemistry':3,'Astronomy':3,
      'Geographic Sciences':3,'Atmospheric Sciences':3,'Marine Sciences':3,'Geophysics':3,
      'Geology':3,'Biological Sciences':3,'Psychology':3,'Statistics':4,
      'Agricultural Engineering':3,'Forestry Engineering':3,'Environmental Engineering':3,
      'Biomedical Engineering':4,'Food Science & Engineering':3,'Architecture':3,
      'Safety Engineering':3,'Biological Sciences (Eng)':3,'Public Security Tech':3,
      'Interdisciplinary Eng':3,'Crop Production':3,'Agricultural Management':3,'Animal Production':3,
      'Veterinary Medicine':4,'Forestry':3,'Fisheries':3,'Grassland Science':2,
      'Basic Medical Sciences':4,'Clinical Medicine':5,'Dental Medicine':5,'Public Health':3,
      'Trad. Chinese Medicine':3,'Integrative Medicine':4,'Pharmacy':4,
      'Chinese Materia Medica':3,'Forensic Medicine':3,'Medical Technology':3,'Nursing':4,
      'Management Sci & Eng':4,'Business Administration':3,'Agricultural Management (Mgmt)':3,
      'Public Administration':3,'Library & Info Management':3,'Logistics Management':3,
      'Industrial Engineering':3,'E-Commerce':3,'Tourism Management':3,
      'Ocean Sciences':3,'Nature Conservation & Ecology':3,
      'Intl Economics & Trade':3,'Public Finance':3,
      'Agricultural Management':3,
    }
    base_stars = rating_map.get(sub, 3)
    rating = min(5, base_stars + (1 if is_ai else 0))

    cat_cn = CAT_CN.get(cat, cat)
    sub_cn_map = {
      'Computer Science':'计算机类','Electronic Information':'电子信息类',
      'Electrical Engineering':'电气类','Automation':'自动化类',
      'Mechanical Engineering':'机械类','Materials Science':'材料类',
      'Civil Engineering':'土木类','Chemical Engineering':'化工与制药类',
      'Clinical Medicine':'临床医学类','Pharmacy':'药学类',
      'Finance':'金融学','Economics':'经济学',
      'Business Administration':'工商管理类','Public Administration':'公共管理类',
      'Law':'法学','Education':'教育学','History':'历史学','Philosophy':'哲学',
    }
    star_label = STAR_LABEL_CN.get(rating, '稳中有变')
    star_str   = stars_html(rating)
    ai_impact  = AI_IMPACT_CN.get(cat, 'AI正在改变各行各业的工作方式。主动掌握AI工具的毕业生，在效率和竞争力上将明显领先。')

    pros = d.get('pros', DEFAULT_SUBCAT['pros'])
    cons = d.get('cons', DEFAULT_SUBCAT['cons'])
    verdict = d.get('verdict', DEFAULT_SUBCAT['verdict'])
    cn_careers = CN_CAREERS.get(sub, DEFAULT_CAREERS)

    pros_html    = '\n'.join(f'<li><span class="ic g">✓</span>{p}</li>' for p in pros)
    cons_html    = '\n'.join(f'<li><span class="ic r">✗</span>{c}</li>' for c in cons)
    careers_html = '\n'.join(
        f'<li><span class="ic b">→</span>{c}</li>'
        for c in cn_careers
    )

    ai_badge = (
        '<span style="background:rgba(245,158,11,.15);border:1px solid rgba(245,158,11,.4);'
        'border-radius:4px;padding:2px 8px;font-size:11px;color:#f59e0b;margin-left:8px;">🤖 AI重点关注</span>'
        if is_ai else ''
    )

    opening = STAR_OPEN_CN.get(rating, STAR_OPEN_CN[3])

    # FAQ
    if rating >= 5:
        faq_a1 = f'根据教育部学科分类和市场就业数据，{cn_name}专业目前属于就业前景最好的专业方向之一，毕业生需求量大、薪资增长快，且所在行业受AI驱动而非被替代。考生可重点考虑。'
    elif rating == 4:
        faq_a1 = f'{cn_name}专业整体就业前景较好，用人单位需求稳定，薪资具有一定竞争力。建议结合自身兴趣和所在省市的招生情况综合判断。'
    elif rating == 3:
        faq_a1 = f'{cn_name}专业能提供稳定的就业基础，但发展潜力受专业方向选择影响较大。建议在报考前深入了解该专业的课程体系和毕业生就业情况。'
    else:
        faq_a1 = f'{cn_name}专业目前就业面临一定压力，考生在报考前应充分了解近年毕业生就业率和薪资水平，并明确适合自己的细分方向。'

    faq_html = f'''
  <div class="faq-item">
    <div class="faq-q">{cn_name}专业就业前景如何？</div>
    <div class="faq-a">{faq_a1}</div>
  </div>
  <div class="faq-item">
    <div class="faq-q">AI时代，{cn_name}专业会受到哪些影响？</div>
    <div class="faq-a">{ai_impact}</div>
  </div>
  <div class="faq-item">
    <div class="faq-q">{cn_name}专业毕业后能从事哪些职业？</div>
    <div class="faq-a">常见职业方向包括：{'、'.join(cn_careers)}。具体岗位因高校培养方向、地区和是否继续深造而有所不同，建议查阅目标院校的就业质量报告。</div>
  </div>'''

    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type":"Question","name":f"{cn_name}专业就业前景如何？",
             "acceptedAnswer":{"@type":"Answer","text":faq_a1}},
            {"@type":"Question","name":f"AI时代，{cn_name}专业会受到哪些影响？",
             "acceptedAnswer":{"@type":"Answer","text":ai_impact}},
            {"@type":"Question","name":f"{cn_name}专业毕业后能从事哪些职业？",
             "acceptedAnswer":{"@type":"Answer","text":f"常见职业方向包括：{'、'.join(cn_careers)}。"}},
        ]
    }, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cn_name}专业就业前景分析 2025-2029 — 高考志愿参考</title>
<meta name="description" content="{cn_name}专业前景、薪资待遇、优缺点及典型职业方向全面分析，帮助高考生和家长了解{cat_cn}{cn_name}专业的就业情况。">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://ordinarymantrying.com/tools/majors-cn/{slug(en_name)}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{cn_name}专业就业前景 2025 — 高考志愿参考">
<meta property="og:url" content="https://ordinarymantrying.com/tools/majors-cn/{slug(en_name)}.html">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article",
  "headline":"{cn_name}专业就业前景分析 2025-2029",
  "description":"{cn_name}专业前景、薪资待遇、优缺点及典型职业方向。",
  "url":"https://ordinarymantrying.com/tools/majors-cn/{slug(en_name)}.html",
  "inLanguage":"zh-CN",
  "author":{{"@type":"Organization","name":"Ordinary Man Trying"}}}}
</script>
<script type="application/ld+json">{faq_schema}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  background:#0f172a;color:#e2e8f0;line-height:1.7;}}
a{{color:#60a5fa;text-decoration:none;}}
a:hover{{text-decoration:underline;}}
.hdr{{background:linear-gradient(160deg,#0d1b2e,#1a3560);padding:28px 20px 22px;
  border-bottom:1px solid #334155;}}
.back{{display:inline-flex;align-items:center;gap:6px;margin-bottom:18px;
  padding:8px 16px;background:rgba(255,255,255,.06);border:1px solid #334155;
  border-radius:8px;font-size:13px;font-weight:600;color:#cbd5e1;text-decoration:none;}}
.back:hover{{background:rgba(59,130,246,.12);border-color:rgba(59,130,246,.4);
  color:#60a5fa;text-decoration:none;}}
.cat-badge{{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:#3b82f6;
  font-family:monospace;margin-bottom:8px;}}
h1{{font-size:clamp(24px,5vw,36px);font-weight:800;line-height:1.2;margin-bottom:6px;}}
.meta{{font-size:13px;color:#64748b;margin-top:6px;}}
.page{{max-width:700px;margin:0 auto;padding:24px 18px 60px;}}
.card{{background:#1e293b;border:1px solid #334155;border-radius:12px;
  padding:18px 20px;margin-bottom:14px;}}
.card h2{{font-size:15px;font-weight:700;margin-bottom:10px;color:#e2e8f0;}}
.card p{{font-size:14px;color:#cbd5e1;line-height:1.8;}}
.stars-row{{display:flex;align-items:center;gap:10px;margin-bottom:10px;}}
.star-val{{font-size:20px;color:#f59e0b;letter-spacing:2px;}}
.star-label{{font-size:13px;font-weight:700;color:#e2e8f0;}}
ul.pros-cons{{list-style:none;padding:0;}}
ul.pros-cons li{{display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;
  font-size:14px;color:#cbd5e1;}}
.ic{{flex-shrink:0;font-weight:700;font-size:14px;margin-top:1px;}}
.ic.g{{color:#10b981;}}.ic.r{{color:#f87171;}}.ic.b{{color:#60a5fa;}}
.verdict-box{{background:rgba(59,130,246,.06);border:1px solid rgba(59,130,246,.25);
  border-radius:10px;padding:14px 18px;margin-bottom:14px;font-size:14px;
  color:#cbd5e1;line-height:1.8;}}
.ai-card{{border-radius:12px;padding:16px 20px;margin-bottom:14px;border:1px solid;}}
.faq-item{{margin-bottom:14px;}}
.faq-q{{font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:4px;}}
.faq-a{{font-size:13px;color:#94a3b8;line-height:1.8;}}
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
  <a class="back" href="/tools/major-vote-cn.html">← 返回757个专业对比</a>
  <div class="cat-badge">{cat_cn} · 高考志愿参考</div>
  <h1>{cn_name}{ai_badge}</h1>
  <div class="meta">综合评分：{star_str} {star_label} &nbsp;·&nbsp; 英文名：{en_name}</div>
</div>

<div class="page">
{DISCLAIMER}

<div class="card">
  <h2>综合评估</h2>
  <div class="stars-row">
    <span class="star-val">{star_str}</span>
    <span class="star-label">{star_label}（{rating}/5）</span>
  </div>
  <p>{opening}{verdict}</p>
</div>

<div class="card">
  <h2>✅ 专业优势</h2>
  <ul class="pros-cons">{pros_html}</ul>
</div>

<div class="card">
  <h2>⚠️ 注意事项</h2>
  <ul class="pros-cons">{cons_html}</ul>
</div>

<div class="card">
  <h2>💼 典型职业方向</h2>
  <ul class="pros-cons">{careers_html}</ul>
  <p style="font-size:12px;color:#64748b;margin-top:10px;">以上职业方向为参考，实际就业情况因院校层次、地区和个人能力有所不同。</p>
</div>

<div class="ai-card" style="border-color:rgba(99,102,241,.4);background:rgba(99,102,241,.04);">
  <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;
    color:#818cf8;margin-bottom:6px;">🤖 AI时代影响分析</div>
  <p style="font-size:13px;color:#cbd5e1;line-height:1.8;">{ai_impact}</p>
</div>

<div class="card">
  <h2>❓ 常见问题</h2>
  {faq_html}
</div>

<a class="cta" href="/tools/major-vote-cn.html">← 返回757专业总览，对比更多方向</a>

<div style="background:linear-gradient(135deg,#1e3a5f,#1e40af);border-radius:12px;
  padding:20px 24px;margin:24px 0 8px;text-align:center;">
  <div style="font-size:15px;font-weight:700;color:#fff;margin-bottom:6px;">📋 还没想好报什么专业？</div>
  <div style="font-size:13px;color:#93c5fd;margin-bottom:14px;">
    填写你的情况（分数、兴趣、城市偏好……），生成一段话直接问 AI 或升学规划老师
  </div>
  <a href="/tools/cn/baokao/gaokao-choice-questionnaire.html" target="_blank"
     style="display:inline-block;background:#fff;color:#1e3a5f;font-weight:700;
            font-size:14px;padding:10px 28px;border-radius:8px;text-decoration:none;
            transition:opacity .15s;">
    填写报考需求问卷 →
  </a>
</div>

</div>
<div class="foot">
  数据参考：教育部学科专业目录 · 高校就业质量报告 · 市场薪资调研<br>
  ⚠️ 本站由AI辅助生成，内容仅供参考，请以各高校官方信息为准<br>
  <a href="/tools/major-vote-cn.html">专业对比工具</a> &nbsp;|&nbsp;
  <a href="/tools/majors-cn/">所有专业列表</a> &nbsp;|&nbsp;
  <a href="/tools/cn/baokao/gaokao-choice-questionnaire.html">报考需求问卷</a>
</div>
</body></html>'''

# ═══════════════════════════════════════════════════════════════════
# INDEX PAGE
# ═══════════════════════════════════════════════════════════════════
def build_index(all_majors):
    rows_by_cat = {}
    for m in all_majors:
        cat = m['cat']
        rows_by_cat.setdefault(cat, []).append(m)

    sections = ''
    cat_order = ['Engineering','Medicine','Science','Agriculture','Economics',
                 'Management','Law','Literature','History','Education','Philosophy']
    for cat in cat_order:
        mlist = rows_by_cat.get(cat, [])
        if not mlist: continue
        cat_cn = CAT_CN.get(cat, cat)
        rows = ''
        for maj in sorted(mlist, key=lambda x: x['n']):
            en = maj['n']
            cn = CN_MAJOR_NAMES.get(en, en)
            s = slug(en)
            rows += f'<a href="/tools/majors-cn/{s}.html" class="mlink">{cn}<span class="en">{en}</span></a>\n'
        sections += f'''<div class="cat-section">
<h2 class="cat-h">{cat_cn} <span class="cnt">({len(mlist)})</span></h2>
<div class="mlist">{rows}</div>
</div>\n'''

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>757个大学专业就业前景一览 — 高考志愿参考工具</title>
<meta name="description" content="覆盖教育部全部普通本科专业，按学科门类分类，提供就业前景、优缺点和职业方向分析，帮助高考生和家长科学填报志愿。">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://ordinarymantrying.com/tools/majors-cn/">
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  background:#0f172a;color:#e2e8f0;line-height:1.7;}}
a{{color:#60a5fa;text-decoration:none;}}
.hdr{{background:linear-gradient(160deg,#0d1b2e,#1a3560);padding:32px 20px 28px;
  border-bottom:1px solid #334155;text-align:center;}}
h1{{font-size:clamp(22px,5vw,32px);font-weight:800;margin-bottom:8px;}}
.sub{{font-size:14px;color:#64748b;}}
.warn{{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.4);
  border-radius:10px;padding:14px 18px;margin:20px auto;max-width:700px;
  font-size:13px;color:#fbbf24;line-height:1.75;}}
.page{{max-width:700px;margin:0 auto;padding:20px 18px 60px;}}
.cat-section{{margin-bottom:28px;}}
.cat-h{{font-size:14px;font-weight:700;color:#3b82f6;margin-bottom:10px;
  text-transform:uppercase;letter-spacing:.1em;}}
.cnt{{color:#475569;font-size:12px;}}
.mlist{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:6px;}}
.mlink{{display:block;padding:8px 12px;background:#1e293b;border:1px solid #334155;
  border-radius:8px;font-size:13px;font-weight:600;color:#e2e8f0;}}
.mlink:hover{{border-color:rgba(59,130,246,.5);color:#60a5fa;text-decoration:none;}}
.en{{display:block;font-size:11px;color:#64748b;font-weight:400;margin-top:2px;}}
.back-btn{{display:block;text-align:center;padding:12px;margin-bottom:20px;
  background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);
  border-radius:10px;font-size:14px;font-weight:600;color:#60a5fa;}}
.foot{{text-align:center;padding:20px;font-size:12px;color:#475569;
  border-top:1px solid #1e293b;}}
</style>
</head>
<body>
<div class="hdr">
  <h1>🎓 757个大学专业前景分析</h1>
  <div class="sub">覆盖教育部全部普通本科专业 · 高考志愿参考工具</div>
</div>

<div class="page">
<div class="warn">
⚠️ 本站内容由人工智能生成，数据仅供参考，不代表官方立场。
高考填报志愿请以各高校招生简章为准，并务必咨询专业升学老师。
</div>

<a class="back-btn" href="/tools/major-vote-cn.html">🗳️ 返回专业投票与对比工具</a>

{sections}

<div style="background:linear-gradient(135deg,#1e3a5f,#1e40af);border-radius:12px;
  padding:20px 24px;margin:24px 0 8px;text-align:center;">
  <div style="font-size:15px;font-weight:700;color:#fff;margin-bottom:6px;">📋 还没想好报什么专业？</div>
  <div style="font-size:13px;color:#93c5fd;margin-bottom:14px;">
    填写你的情况，生成一段话直接问 AI 或升学规划老师
  </div>
  <a href="/tools/cn/baokao/gaokao-choice-questionnaire.html" target="_blank"
     style="display:inline-block;background:#fff;color:#1e3a5f;font-weight:700;
            font-size:14px;padding:10px 28px;border-radius:8px;text-decoration:none;">
    填写报考需求问卷 →
  </a>
</div>

</div>
<div class="foot">
  数据参考：教育部学科专业目录 · 高校就业质量报告<br>
  ⚠️ 本站由AI辅助生成，内容仅供参考，请以各高校官方信息为准<br>
  <a href="/tools/cn/baokao/gaokao-choice-questionnaire.html" style="color:#60a5fa;">报考需求问卷</a>
</div>
</body></html>'''

# ═══════════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════════
out_dir = 'ordinarymantrying.com/tools/majors-cn'
os.makedirs(out_dir, exist_ok=True)

ok = skip = 0
for major in ALL:
    en_name = major.get('n','')
    if not en_name:
        skip += 1; continue
    fname = os.path.join(out_dir, f'{slug(en_name)}.html')
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(page_cn(major))
    ok += 1

with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(build_index(ALL))

print(f'✅ 生成 {ok} 个中文专业页面（跳过 {skip}）→ {out_dir}/')
if skip: print(f'  跳过条目（无专业名称）: {skip}')
