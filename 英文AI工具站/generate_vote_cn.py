#!/usr/bin/env python3
"""生成 major-vote-cn.html — 中文版专业投票工具（纯工具，无建站内容）"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from cn_names import CN_MAJOR_NAMES

with open("ordinarymantrying.com/tools/major-vote.html", encoding="utf-8") as f:
    src = f.read()

m = re.search(r'const ALL\s*=\s*(\[.*?\]);', src, re.DOTALL)
ALL = json.loads(m.group(1))
m2 = re.search(r'const AIPICK\s*=\s*new Set\(\[(.*?)\]\)', src)
AIPICK_LIST = [x.strip().strip('"') for x in m2.group(1).split(',')]
m3 = re.search(r'const SEED\s*=\s*(\{.*?\});', src)
SEED = json.loads(m3.group(1))

# 嵌入中文名称到 ALL 数组
ALL_CN = []
for major in ALL:
    cn = CN_MAJOR_NAMES.get(major['n'], major['n'])
    ALL_CN.append({**major, 'cn': cn})

ALL_JSON = json.dumps(ALL_CN, ensure_ascii=False)
AIPICK_JSON = json.dumps(AIPICK_LIST)
SEED_JSON = json.dumps(SEED)

# 中文学科门类映射
CN_CATS_JS = json.dumps({
    'Engineering':'工学','Medicine':'医学','Science':'理学',
    'Agriculture':'农学','Economics':'经济学','Management':'管理学',
    'Law':'法学','Literature':'文学','History':'历史学',
    'Education':'教育学','Philosophy':'哲学',
}, ensure_ascii=False)

# 中文专业分析数据（CAT_ANALYSIS）
CN_CAT_ANALYSIS = {
  'Engineering': {
    'tags': ['需求旺盛','AI赋能','全球化机遇','高薪'],
    'pros': ['未来十年就业市场强劲','起薪高，发展上限大','技能可跨行业迁移'],
    'cons': ['竞争持续加剧，需要持续学习','技术迭代快，不学则淘汰'],
    'careers': ['软件工程师','AI工程师','产品经理'],
    'stars': 4
  },
  'Science': {
    'tags': ['科研导向','AI协作','创新基础'],
    'pros': ['分析能力强，就业路径多元','可走科研或产业双轨','国际化机会多'],
    'cons': ['学术路径周期长','转入产业需主动补强'],
    'careers': ['科研人员','数据分析师','生物科技专家'],
    'stars': 4
  },
  'Medicine': {
    'tags': ['AI高稳定性','就业保障','社会价值','高薪'],
    'pros': ['AI时代最稳定的专业之一','受人尊重且不可或缺','AI辅助诊断，不替代临床判断'],
    'cons': ['培养周期极长，经济回报慢','学业和临床压力都很大'],
    'careers': ['临床医师','医学研究员','医疗AI专家'],
    'stars': 5
  },
  'Economics': {
    'tags': ['商科基础','分析能力','政策相关'],
    'pros': ['就业面广，覆盖金融和政策领域','量化训练扎实','国际机构认可度高'],
    'cons': ['需要细分方向才能脱颖而出','初级岗位竞争激烈'],
    'careers': ['金融分析师','政策顾问','管理咨询顾问'],
    'stars': 3
  },
  'Management': {
    'tags': ['领导力','跨行业灵活','适合创业'],
    'pros': ['适用于所有行业','领导力和软技能培养','支持创业路径'],
    'cons': ['技术深度不如工科','毕业生竞争同质化较严重'],
    'careers': ['运营经理','商务总监','创业者'],
    'stars': 3
  },
  'Education': {
    'tags': ['编制稳定','社会价值','AI工具助力'],
    'pros': ['政府背书，就业稳定性强','有意义的长期职业','AI辅助工具提升教学效率'],
    'cons': ['薪资天花板低于市场化行业','AI正在快速改变课堂形态'],
    'careers': ['中小学教师','教育技术专员','课程研发师'],
    'stars': 3
  },
  'Law': {
    'tags': ['专业壁垒','合规需求','AI辅助研究'],
    'pros': ['专业判断价值高，AI难以完全替代','监管环境扩张带来持续需求','AI辅助法律检索，判断力仍是人类'],
    'cons': ['从业资质路径长','部分基础法律工作面临AI冲击'],
    'careers': ['律师','法律顾问','合规专员'],
    'stars': 3
  },
  'Literature': {
    'tags': ['创意经济','内容时代','人文叙事'],
    'pros': ['人类独特的创造力仍有价值','内容经济持续增长','可迁移到UX、传媒和营销'],
    'cons': ['AI写作工具竞争直接','多数路径起薪偏低'],
    'careers': ['内容创作者','用户体验文案','媒体专家'],
    'stars': 2
  },
  'History': {
    'tags': ['批判性思维','深度研究','文化洞察'],
    'pros': ['培养深厚的分析和研究能力','长期系统思维独特视角','在政策和文化领域有价值'],
    'cons': ['直接就业路径较窄','与技术专业相比行业需求有限'],
    'careers': ['研究员','政策分析师','博物馆策展人'],
    'stars': 2
  },
  'Philosophy': {
    'tags': ['AI伦理需求','逻辑基础','大局思维'],
    'pros': ['AI伦理是快速增长的细分领域','独特的问题解决方式在科技领域受重视','法律、政策、战略的优质基础'],
    'cons': ['传统职业路径窄','向雇主量化价值难度较大'],
    'careers': ['AI伦理研究员','政策顾问','战略咨询顾问'],
    'stars': 3
  },
  'Agriculture': {
    'tags': ['粮食安全优先','农业科技增长','政策扶持'],
    'pros': ['国家战略重点，政府持续投入','AI、无人机和生物技术深度融合','粮食需求刚性，就业稳定'],
    'cons': ['城市薪资预期偏低','社会认知度和吸引力有待提升'],
    'careers': ['农业科技专家','食品安全工程师','乡村振兴专员'],
    'stars': 3
  }
}

CN_CAT_ANALYSIS_JSON = json.dumps(CN_CAT_ANALYSIS, ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>高考志愿填报参考 — 757个本科专业前景对比 | 哪个专业4年后最有价值？</title>
<meta name="description" content="覆盖教育部全部757个普通本科专业，AI评分+网友投票，帮助高考生和家长科学填报志愿。专业前景、职业方向、薪资参考一站查询。">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://ordinarymantrying.com/tools/major-vote-cn.html">
<meta property="og:type" content="website">
<meta property="og:title" content="高考志愿填报参考 — 757个专业前景对比">
<meta property="og:description" content="覆盖教育部全部757个普通本科专业，帮助高考生科学填报志愿。">
<meta property="og:url" content="https://ordinarymantrying.com/tools/major-vote-cn.html">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebApplication",
  "name":"高考志愿参考工具 — 757个专业前景对比",
  "description":"覆盖教育部全部757个普通本科专业，帮助高考生填报志愿。",
  "url":"https://ordinarymantrying.com/tools/major-vote-cn.html",
  "applicationCategory":"EducationApplication",
  "inLanguage":"zh-CN",
  "offers":{{"@type":"Offer","price":"0","priceCurrency":"CNY"}}}}
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DBR2PMLR61"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-DBR2PMLR61');</script>
<style>
:root{{
  --bg:#0f172a;--card:#1e293b;--ink:#e2e8f0;--muted:#94a3b8;--line:#334155;
  --ac:#3b82f6;--ac-bg:rgba(59,130,246,.1);
  --gold:#f59e0b;--green:#10b981;--green-bg:rgba(16,185,129,.08);
  --sans:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  --mono:ui-monospace,"SF Mono",Consolas,monospace;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:var(--sans);background:var(--bg);color:var(--ink);line-height:1.5;}}
a{{color:#60a5fa;text-decoration:none;}}
a:hover{{text-decoration:underline;}}
.hdr{{text-align:center;padding:28px 20px 20px;border-bottom:1px solid var(--line);
  background:linear-gradient(160deg,#0d1b2e 0%,#1a3560 100%);}}
.tag{{font-family:var(--mono);font-size:10px;letter-spacing:.15em;text-transform:uppercase;
  color:var(--ac);margin-bottom:8px;}}
h1{{font-size:clamp(18px,4.5vw,28px);font-weight:800;line-height:1.25;margin-bottom:8px;}}
.hint{{font-size:13px;color:var(--muted);max-width:480px;margin:0 auto 14px;}}
.hint b{{color:var(--ink);}}
.ctr{{display:flex;gap:6px;justify-content:center;align-items:center;flex-wrap:wrap;
  font-family:var(--mono);font-size:12px;color:var(--muted);}}
.ctr .big{{font-size:22px;font-weight:800;color:var(--ac);}}
.warn-bar{{background:rgba(245,158,11,.08);border-bottom:1px solid rgba(245,158,11,.3);
  padding:10px 16px;font-size:12px;color:#fbbf24;line-height:1.6;text-align:center;}}
.lb-strip{{position:sticky;top:0;z-index:100;background:var(--card);
  border-bottom:2px solid var(--line);overflow-x:auto;}}
.lb-table{{width:100%;min-width:400px;border-collapse:collapse;font-size:12px;}}
.lb-table thead tr{{background:#162032;}}
.lb-table thead th{{padding:7px 12px;text-align:left;font-family:var(--mono);
  font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);
  font-weight:600;border-bottom:1px solid var(--line);white-space:nowrap;}}
.lb-table thead th:first-child{{width:40px;text-align:center;}}
.lb-table thead th:last-child{{width:80px;text-align:right;}}
.lb-table tbody tr{{border-bottom:1px solid rgba(51,65,85,.5);transition:background .12s;}}
.lb-table tbody tr:hover{{background:rgba(255,255,255,.03);}}
.lb-rank{{font-family:var(--mono);font-size:11px;font-weight:700;text-align:center;}}
.lb-rank.r1{{color:var(--gold);}}.lb-rank.r2{{color:#c0c0c0;}}.lb-rank.r3{{color:#cd7f32;}}
.lb-nm{{font-weight:600;color:var(--ink);max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}}
.lb-sub{{color:var(--muted);font-size:11px;}}
.lb-vc{{font-family:var(--mono);font-weight:700;color:var(--ac);text-align:right;white-space:nowrap;}}
.page{{max-width:700px;margin:0 auto;padding:20px 14px 60px;}}
.sec-hdr{{display:flex;align-items:center;gap:8px;margin-bottom:12px;}}
.sec-hdr h2{{font-size:14px;font-weight:700;}}
.sec-hdr .badge{{font-size:10px;background:rgba(245,158,11,.12);color:var(--gold);
  border:1px solid rgba(245,158,11,.3);border-radius:4px;padding:1px 7px;}}
.sec-note{{font-size:12px;color:var(--muted);margin-bottom:12px;margin-top:-6px;}}
.mc{{display:flex;flex-direction:column;background:var(--card);
  border:1px solid var(--line);border-radius:10px;padding:12px 14px;
  margin-bottom:8px;transition:border-color .15s;}}
.mc:hover{{border-color:#475569;}}
.mc.ai{{border-left:3px solid var(--gold);}}
.mc.voted{{background:var(--green-bg);border-color:var(--green);}}
.mc-top{{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:10px;}}
.mc-info{{flex:1;min-width:0;}}
.mc-name{{font-size:14px;font-weight:600;line-height:1.35;}}
.mc-en{{font-size:11px;color:#475569;margin-top:2px;}}
.mc-meta{{font-size:11px;color:var(--muted);margin-top:3px;display:flex;gap:6px;flex-wrap:wrap;}}
.ai-dot{{color:var(--gold);}}
.mc-vc{{font-family:var(--mono);font-size:12px;font-weight:700;color:var(--ac);
  flex-shrink:0;padding-top:2px;}}
.vbtn{{appearance:none;cursor:pointer;width:100%;height:44px;border-radius:9px;
  font-size:15px;font-weight:700;font-family:var(--sans);
  border:2px solid var(--ac);background:var(--ac-bg);color:var(--ac);
  display:flex;align-items:center;justify-content:center;gap:6px;
  transition:all .15s;}}
.vbtn:hover:not(:disabled){{background:var(--ac);color:#fff;}}
.vbtn.done{{border-color:var(--green);background:var(--green-bg);color:var(--green);cursor:default;}}
.vbtn:disabled:not(.done){{opacity:.4;cursor:default;}}
.id-bar{{margin:0 0 20px;padding:14px 16px;background:rgba(255,255,255,.03);
  border:1px solid var(--line);border-radius:10px;}}
.id-label{{font-size:11px;color:var(--muted);text-transform:uppercase;
  letter-spacing:.08em;font-weight:600;margin-bottom:8px;}}
.id-pills{{display:flex;flex-wrap:wrap;gap:6px;}}
.id-pill{{background:rgba(255,255,255,.05);border:1px solid var(--line);
  border-radius:20px;padding:5px 13px;font-size:12px;font-weight:600;
  color:var(--muted);cursor:pointer;transition:all .15s;user-select:none;}}
.id-pill:hover{{border-color:#475569;color:var(--ink);}}
.id-pill.sel{{background:rgba(59,130,246,.15);border-color:var(--ac);color:var(--ac);}}
.id-note{{font-size:11px;color:var(--muted);margin-top:8px;}}
.browse-bar{{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap;}}
.browse-bar select,
.browse-bar input{{
  appearance:none;background:var(--card);border:1px solid var(--line);color:var(--ink);
  border-radius:8px;padding:8px 12px;font-size:13px;font-family:var(--sans);
  outline:none;transition:border-color .15s;}}
.browse-bar select{{flex:1;min-width:120px;cursor:pointer;}}
.browse-bar input{{flex:2;min-width:160px;}}
.browse-bar select:focus,.browse-bar input:focus{{border-color:var(--ac);}}
#browse-list{{display:flex;flex-direction:column;gap:6px;}}
.more-note{{text-align:center;font-size:12px;color:var(--muted);padding:10px;}}
.divider{{height:1px;background:var(--line);margin:24px 0;}}
.rank-strip{{background:#0d1b2e;border-bottom:1px solid var(--line);padding:10px 14px;}}
.rank-strip-label{{font-size:10px;font-family:var(--mono);text-transform:uppercase;
  letter-spacing:.1em;color:var(--muted);margin-bottom:7px;}}
.rank-pills{{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px;
  scrollbar-width:none;}}
.rank-pills::-webkit-scrollbar{{display:none;}}
.rank-pill{{flex-shrink:0;padding:5px 12px;background:rgba(255,255,255,.04);
  border:1px solid var(--line);border-radius:20px;font-size:12px;color:var(--muted);
  text-decoration:none;white-space:nowrap;transition:all .15s;}}
.rank-pill:hover{{border-color:var(--ac);color:#e2e8f0;background:rgba(59,130,246,.08);text-decoration:none;}}
.rank-pill.hot{{border-color:rgba(245,158,11,.4);color:#f59e0b;background:rgba(245,158,11,.06);}}
.ap-overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.65);
  z-index:300;align-items:flex-end;justify-content:center;}}
.ap-overlay.open{{display:flex;}}
.ap-panel{{background:#1e293b;border-radius:20px 20px 0 0;
  padding:20px 20px 36px;width:100%;max-width:600px;
  max-height:88vh;overflow-y:auto;position:relative;
  animation:apUp .22s ease;}}
@keyframes apUp{{from{{transform:translateY(100%)}}to{{transform:translateY(0)}}}}
.ap-close{{position:absolute;top:14px;right:16px;background:none;border:none;
  color:var(--muted);font-size:20px;cursor:pointer;line-height:1;padding:4px 8px;}}
.ap-close:hover{{color:var(--ink);}}
.ap-handle{{width:40px;height:4px;background:var(--line);border-radius:2px;margin:0 auto 16px;}}
.ap-title{{font-size:18px;font-weight:800;margin-bottom:2px;}}
.ap-sub{{font-size:12px;color:var(--muted);margin-bottom:14px;}}
.ap-stars{{font-size:24px;letter-spacing:3px;margin-bottom:14px;}}
.ap-tags{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px;}}
.ap-tag{{background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.2);
  border-radius:20px;padding:4px 12px;font-size:12px;color:#93c5fd;}}
.ap-tag.ai{{background:rgba(245,158,11,.1);border-color:rgba(245,158,11,.3);color:var(--gold);}}
.ap-sec{{margin-bottom:16px;}}
.ap-sec h3{{font-size:10px;text-transform:uppercase;letter-spacing:.1em;
  color:var(--muted);font-weight:700;margin-bottom:8px;}}
.ap-list{{list-style:none;padding:0;display:flex;flex-direction:column;gap:5px;}}
.ap-list li{{font-size:13px;display:flex;gap:8px;align-items:flex-start;}}
.ap-list li .ic{{flex-shrink:0;font-size:12px;margin-top:1px;}}
.ap-list.pros li .ic{{color:var(--green);}}.ap-list.cons li .ic{{color:#f87171;}}
.ap-list.careers li .ic{{color:var(--ac);}}
.ap-divider{{border:none;border-top:1px solid var(--line);margin:16px 0;}}
.ap-action{{display:block;width:100%;padding:14px;background:rgba(59,130,246,.08);
  border:1px solid rgba(59,130,246,.25);border-radius:12px;font-size:14px;
  font-weight:700;color:#60a5fa;cursor:pointer;text-decoration:none;
  text-align:center;transition:all .15s;margin-bottom:8px;}}
.ap-action:hover{{background:rgba(59,130,246,.18);text-decoration:none;}}
.foot{{text-align:center;font-size:11px;color:var(--muted);padding:0 14px 30px;line-height:1.8;}}
.foot a{{color:var(--ac);}}
.disclaimer{{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.3);
  border-radius:10px;padding:12px 16px;margin-bottom:20px;
  font-size:12px;color:#fbbf24;line-height:1.7;}}
.en-link{{display:block;text-align:center;padding:10px;margin-bottom:18px;
  background:rgba(59,130,246,.06);border:1px solid rgba(59,130,246,.2);
  border-radius:8px;font-size:12px;color:#64748b;}}
</style>
</head>
<body>

<!-- 免责声明横幅 -->
<div class="warn-bar">
⚠️ 本工具由AI辅助生成，数据仅供参考。<strong>高考志愿是人生大事，请务必咨询专业升学老师，勿将本页作为唯一填报依据。</strong>
</div>

<div class="hdr">
  <div class="tag">高考志愿参考工具 · 2026</div>
  <h1>中国有757个本科专业<br>哪个专业4年后最有价值？</h1>
  <p class="hint">覆盖教育部全部普通本科专业。<b>为你认为有价值的专业投票，支持多选。</b>帮助更多考生做参考。</p>
  <div class="ctr">
    <span class="big" id="s-total">0</span>
    <span>票已投出（跨757个专业）</span>
  </div>
</div>

<!-- 导航快速链接 -->
<div class="rank-strip">
  <div class="rank-strip-label">📊 快速导航</div>
  <div class="rank-pills">
    <a class="rank-pill hot" href="/tools/majors-cn/">📚 757个专业详情</a>
    <a class="rank-pill hot" href="/tools/careers-cn/">💼 259个职业前景</a>
    <a class="rank-pill" href="/tools/major-vote.html">🌐 English Version</a>
  </div>
</div>

<!-- 排行榜（吸顶）-->
<div class="lb-strip">
  <table class="lb-table">
    <thead>
      <tr>
        <th>#</th>
        <th>专业名称</th>
        <th>学科</th>
        <th>票数</th>
      </tr>
    </thead>
    <tbody id="lb"></tbody>
  </table>
</div>

<div class="page">

  <!-- 免责说明 -->
  <div class="disclaimer">
    ⚠️ <strong>重要提示：</strong>本工具内容由人工智能生成，专业分析和职业数据仅供参考，不代表教育主管部门或高校官方立场。
    高考填报志愿请以各高校官方招生简章为准，并务必咨询专业升学指导老师。<strong>切勿将本页作为唯一填报依据。</strong>
  </div>

  <!-- 英文版链接 -->
  <a class="en-link" href="/tools/major-vote.html">This tool also has an English version for international comparison →</a>

  <!-- 身份选择 -->
  <div class="id-bar" id="id-bar">
    <div class="id-label">你的身份（可选）</div>
    <div class="id-pills">
      <div class="id-pill" data-id="student" onclick="setIdentity('student')">📚 学生/高考生</div>
      <div class="id-pill" data-id="parent"  onclick="setIdentity('parent')">👨‍👩‍👧 家长</div>
      <div class="id-pill" data-id="tech"    onclick="setIdentity('tech')">💻 IT/互联网</div>
      <div class="id-pill" data-id="health"  onclick="setIdentity('health')">🏥 医疗</div>
      <div class="id-pill" data-id="finance" onclick="setIdentity('finance')">📈 金融/商业</div>
      <div class="id-pill" data-id="edu"     onclick="setIdentity('edu')">🎓 教育</div>
      <div class="id-pill" data-id="other"   onclick="setIdentity('other')">👤 其他</div>
    </div>
    <div class="id-note" id="id-note">可选 — 帮助我们了解不同背景人群的判断差异。</div>
  </div>

  <!-- AI推荐专业 -->
  <div class="sec-hdr"><h2>🤖 AI重点关注专业</h2><span class="badge">投票</span></div>
  <p class="sec-note">这13个专业在AI评估中得分最高，认为是未来4年最有价值的方向。可先从这里开始，也可直接浏览全部专业。</p>
  <div id="featured-list"></div>

  <div class="divider"></div>

  <!-- 浏览全部专业 -->
  <div class="sec-hdr"><h2>🔍 浏览全部757个专业</h2></div>
  <div class="browse-bar">
    <select id="cat-sel">
      <option value="">全部学科门类</option>
    </select>
    <input id="search" type="text" placeholder="搜索专业名称..." oninput="renderBrowse()">
  </div>
  <div id="browse-list"></div>

</div>

<div class="foot">
  数据来源：教育部普通高等学校本科专业目录（2024）·  AI分析仅供参考<br>
  ⚠️ 本工具由AI辅助生成，内容不代表官方立场，请以高校招生简章为准<br>
  <a href="/tools/major-vote.html">English Version</a> ·
  <a href="/tools/majors-cn/">757个专业详情</a> ·
  <a href="/tools/careers-cn/">259个职业前景</a>
</div>

<script>
const ALL = {ALL_JSON};
const AIPICK = new Set({AIPICK_JSON});
const SEED = {SEED_JSON};
const CN_CATS = {CN_CATS_JS};
const CAT_ANALYSIS = {CN_CAT_ANALYSIS_JSON};
const CATS = ["Agriculture","Economics","Education","Engineering","History","Law","Literature","Management","Medicine","Philosophy","Science"];
const LS_V   = 'mjv4cn_votes';
const LS_MY  = 'mjv4cn_mine';
const LS_ID  = 'mjv4cn_id';
const WP     = '/tools/votes.php';
const BROWSE_MAX = 60;

let votes = {{}};
let myVotes = new Set();
let userIdentity = null;

function initVotes() {{
  Object.assign(votes, SEED);
  try {{
    const lv = JSON.parse(localStorage.getItem(LS_V)||'{{}}');
    for (const [k,v] of Object.entries(lv)) votes[k] = Math.max(votes[k]||0,v);
    myVotes = new Set(JSON.parse(localStorage.getItem(LS_MY)||'[]'));
  }} catch(e) {{}}
}}
function persist() {{
  try {{
    localStorage.setItem(LS_V, JSON.stringify(votes));
    localStorage.setItem(LS_MY, JSON.stringify([...myVotes]));
  }} catch(e) {{}}
}}
function initIdentity() {{
  try {{ userIdentity = localStorage.getItem(LS_ID)||null; }} catch(e) {{}}
}}
function setIdentity(id) {{
  userIdentity = (userIdentity === id) ? null : id;
  try {{
    if (userIdentity) localStorage.setItem(LS_ID, userIdentity);
    else localStorage.removeItem(LS_ID);
  }} catch(e) {{}}
  renderIdentity();
}}
function renderIdentity() {{
  const bar = document.getElementById('id-bar');
  if (!bar) return;
  bar.querySelectorAll('.id-pill').forEach(p => {{
    p.classList.toggle('sel', p.dataset.id === userIdentity);
  }});
  const note = document.getElementById('id-note');
  if (note) note.textContent = userIdentity
    ? '✓ 身份已保存 — 帮助对比不同背景的投票差异。'
    : '可选 — 帮助我们了解不同背景人群的判断差异。';
}}

function doVote(code) {{
  if (myVotes.has(code)) return;
  votes[code] = (votes[code]||0) + 1;
  myVotes.add(code);
  persist();
  document.querySelectorAll('#r-'+code).forEach(row => {{
    row.classList.add('voted');
    const btn = row.querySelector('.vbtn');
    const vc  = document.getElementById('v-'+code);
    if (btn) {{ btn.innerHTML='✓ 已支持'; btn.classList.add('done'); btn.disabled=true; }}
    if (vc) vc.textContent = votes[code];
  }});
  renderLB();
  document.getElementById('s-total').textContent =
    Object.values(votes).reduce((a,b)=>a+b,0);
  if (typeof gtag !== 'undefined') gtag('event','vote',{{event_category:'major_cn',event_label:code}});
  fetch(WP,{{method:'POST',headers:{{'Content-Type':'application/json'}},
    body:JSON.stringify({{code, identity: 'cn_'+userIdentity}})}}).catch(()=>{{}});
}}

function slugify(n) {{
  return n.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
}}

function makeCard(m) {{
  const voted = myVotes.has(m.c);
  const ai    = AIPICK.has(m.c);
  const vc    = votes[m.c]||0;
  const div   = document.createElement('div');
  div.className = 'mc' + (ai?' ai':'') + (voted?' voted':'');
  div.id = 'r-'+m.c;
  div.innerHTML = `
    <div class="mc-top">
      <div class="mc-info">
        <div class="mc-name">${{m.cn||m.n}}</div>
        <div class="mc-en">${{m.n}}</div>
        <div class="mc-meta">
          ${{ai?'<span class="ai-dot">🤖 AI重点关注</span>':''}}
          <span>${{CN_CATS[m.cat]||m.cat}}</span>
        </div>
      </div>
      <div class="mc-vc" id="v-${{m.c}}">${{vc>0?vc:''}}</div>
    </div>
    <button class="vbtn ${{voted?'done':''}}" ${{voted?'disabled':''}}
      onclick="doVote('${{m.c}}')">${{voted?'✓ 已支持':'▲ 我支持这个专业'}}</button>
    <button class="ap-btn" style="width:100%;margin-top:8px;padding:8px;background:transparent;
      border:1px solid var(--line);border-radius:8px;font-size:12px;font-weight:600;
      color:var(--muted);cursor:pointer;transition:all .15s;"
      onmouseover="this.style.borderColor='var(--ac)';this.style.color='var(--ac)'"
      onmouseout="this.style.borderColor='var(--line)';this.style.color='var(--muted)'"
      onclick="showAnalysis('${{m.c}}')">📊 查看专业分析</button>
    <a style="display:block;text-align:center;margin-top:6px;font-size:11px;
      color:var(--muted);text-decoration:none;padding:4px;"
      href="/tools/majors-cn/${{slugify(m.n)}}.html"
      onmouseover="this.style.color='var(--ac)'"
      onmouseout="this.style.color='var(--muted)'">🔗 查看完整职业前景分析 →</a>`;
  return div;
}}

const DEFAULT_ANALYSIS = {{
  tags:['专业领域','就业潜力'],
  pros:['专业技能扎实','就业路径明确','可借助AI工具提升效率'],
  cons:['竞争激烈','需要持续学习'],
  careers:['专业工程师/研究员','技术顾问','行业分析师'],
  stars:3
}};

function showAnalysis(code) {{
  const m = codeIdx[code];
  if (!m) return;
  const base = CAT_ANALYSIS[m.cat] || DEFAULT_ANALYSIS;
  const isAI = AIPICK.has(code);
  const stars = Math.min(5, base.stars + (isAI ? 1 : 0));
  const starStr = '★'.repeat(stars) + '☆'.repeat(5 - stars);

  document.getElementById('ap-name').textContent  = m.cn||m.n;
  document.getElementById('ap-ename').textContent = m.n;
  document.getElementById('ap-field').textContent = (CN_CATS[m.cat]||m.cat) + (m.sub&&m.sub!==m.cat?' · '+m.sub:'');
  document.getElementById('ap-stars').textContent = starStr;
  document.getElementById('ap-tags').innerHTML = base.tags
    .map(t => `<span class="ap-tag">${{t}}</span>`).join('') +
    (isAI ? '<span class="ap-tag ai">🤖 AI重点关注</span>' : '');
  document.getElementById('ap-pros').innerHTML = base.pros
    .map(p => `<li><span class="ic">✓</span>${{p}}</li>`).join('');
  document.getElementById('ap-cons').innerHTML = base.cons
    .map(c => `<li><span class="ic">✗</span>${{c}}</li>`).join('');
  document.getElementById('ap-careers').innerHTML = base.careers
    .map(c => `<li><span class="ic">→</span>${{c}}</li>`).join('');
  document.getElementById('ap-detail').href = `/tools/majors-cn/${{slugify(m.n)}}.html`;

  const ov = document.getElementById('ap-overlay');
  ov.classList.add('open');
  document.body.style.overflow = 'hidden';
}}
function closeAnalysis() {{
  document.getElementById('ap-overlay').classList.remove('open');
  document.body.style.overflow = '';
}}

const codeIdx = {{}};
for (const m of ALL) codeIdx[m.c] = m;

function renderLB() {{
  const top = Object.entries(votes).filter(([,v])=>v>0)
    .sort((a,b)=>b[1]-a[1]).slice(0,10);
  const lb = document.getElementById('lb');
  if (!top.length) {{
    lb.innerHTML='<tr><td colspan="4" style="padding:8px 12px;font-size:12px;color:var(--muted)">暂无投票 — 成为第一个投票的人。</td></tr>';
    return;
  }}
  lb.innerHTML = top.map(([code,cnt],i) => {{
    const m = codeIdx[code]||{{}};
    const rc = i===0?'r1':i===1?'r2':i===2?'r3':'';
    return `<tr>
      <td class="lb-rank ${{rc}}">#${{i+1}}</td>
      <td class="lb-nm">${{m.cn||m.n||code}}</td>
      <td class="lb-sub">${{CN_CATS[m.cat]||m.cat||''}}</td>
      <td class="lb-vc">${{cnt}} 票</td>
    </tr>`;
  }}).join('');
}}

const FEAT = ALL.filter(m => AIPICK.has(m.c));
function renderFeatured() {{
  const el = document.getElementById('featured-list');
  el.innerHTML = '';
  FEAT.forEach(m => el.appendChild(makeCard(m)));
}}

function renderBrowse() {{
  const cat = document.getElementById('cat-sel').value;
  const q   = document.getElementById('search').value.trim().toLowerCase();
  let filtered = ALL.filter(m =>
    (!cat || m.cat === cat) &&
    (!q   || m.n.toLowerCase().includes(q) || (m.cn&&m.cn.includes(q)) || (m.sub&&m.sub.toLowerCase().includes(q)))
  );
  const el = document.getElementById('browse-list');
  el.innerHTML = '';
  const shown = filtered.slice(0, BROWSE_MAX);
  shown.forEach(m => el.appendChild(makeCard(m)));
  if (filtered.length > BROWSE_MAX) {{
    const note = document.createElement('p');
    note.className = 'more-note';
    note.textContent = `显示 ${{BROWSE_MAX}} / ${{filtered.length}} 个专业 — 输入更多关键词缩小范围。`;
    el.appendChild(note);
  }}
  if (!shown.length) {{
    el.innerHTML = '<p class="more-note">没有找到匹配的专业。</p>';
  }}
}}

function buildCatSel() {{
  const sel = document.getElementById('cat-sel');
  CATS.forEach(c => {{
    const o = document.createElement('option');
    o.value = c; o.textContent = CN_CATS[c]||c;
    sel.appendChild(o);
  }});
  sel.addEventListener('change', renderBrowse);
}}

// Boot
initVotes();
initIdentity();
buildCatSel();
renderLB();
renderFeatured();
renderIdentity();
renderBrowse();
document.getElementById('s-total').textContent =
  Object.values(votes).reduce((a,b)=>a+b,0);

fetch(WP).then(r=>r.ok?r.json():null).then(d=>{{
  if(!d)return;
  let changed=false;
  for(const [k,v] of Object.entries(d)){{
    const nv=(SEED[k]||0)+v;
    if(nv>(votes[k]||0)){{votes[k]=nv;changed=true;}}
  }}
  if(changed){{renderLB();renderFeatured();renderBrowse();
    document.getElementById('s-total').textContent=Object.values(votes).reduce((a,b)=>a+b,0);}}
}}).catch(()=>{{}});
</script>

<!-- 分析面板 -->
<div class="ap-overlay" id="ap-overlay" onclick="if(event.target===this)closeAnalysis()">
  <div class="ap-panel">
    <button class="ap-close" onclick="closeAnalysis()">✕</button>
    <div class="ap-handle"></div>
    <div class="ap-title" id="ap-name"></div>
    <div style="font-size:12px;color:#64748b;margin-bottom:4px;" id="ap-ename"></div>
    <div class="ap-sub" id="ap-field"></div>
    <div class="ap-stars" id="ap-stars"></div>
    <div class="ap-tags" id="ap-tags"></div>
    <div class="ap-sec">
      <h3>专业优势</h3>
      <ul class="ap-list pros" id="ap-pros"></ul>
    </div>
    <div class="ap-sec">
      <h3>注意事项</h3>
      <ul class="ap-list cons" id="ap-cons"></ul>
    </div>
    <div class="ap-sec">
      <h3>典型职业方向</h3>
      <ul class="ap-list careers" id="ap-careers"></ul>
    </div>
    <hr class="ap-divider">
    <a class="ap-action" id="ap-detail" href="#" target="_blank">📄 查看完整职业前景分析 →</a>
    <div style="font-size:12px;color:#475569;text-align:center;margin-top:8px;">
      ⚠️ 以上分析由AI生成，仅供参考，请结合实际情况综合判断
    </div>
  </div>
</div>
</body></html>'''

out_path = "ordinarymantrying.com/tools/major-vote-cn.html"
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ 生成 {out_path}")
print(f"   ALL array: {len(ALL)} 个专业（含中文名称）")
print(f"   AI重点关注: {len(AIPICK_LIST)} 个专业")
