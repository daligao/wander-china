# China Major & Career Decision Database

**定位**：AI时代中国大学专业与职业决策数据库
**URL**：ordinarymantrying.com/tools/

---

## 已上线

### major-vote.html — 主工具页
- 757个教育部官方专业，5年众包投票实验（2025–2029）
- 身份选择器（6种背景）
- AI Analysis 底部弹窗（pros/cons/careers + Perplexity深度分析）
- Rally分享按钮（X/Twitter）
- Building-in-public 博客引流 CTA
- localStorage: `mjv4_votes` `mjv4_mine` `mjv4_id`

### majors/[slug].html — 757个专业详情页
- Layer 1：独立 title/meta/canonical/OG/JSON-LD
- Layer 2：88个子类各自的 pros/cons/careers/stars
- Layer 3：AI Verdict（子类见解 × 5星级语气 × AI Pick修饰词）
- FAQ：3题独特问答 + FAQ JSON-LD schema
- 生成脚本：`generate_major_pages.py`
- Sitemap：`majors/sitemap.xml`（已提交 Google Search Console）

---

## 路线图

### P1 — 内容厚度（本周）
**目标**：每个专业页从 ~600词 → ~1000词，Google 更愿意收录

每页新增两个段落：
- `What is [Sub]?` — 该子类是什么、学什么、培养什么技能（~150词）
- `Future Outlook` — 该领域未来趋势，结合AI影响（~150词）

更新 `generate_major_pages.py` → 重新生成全部757页 → 重新上传 majors/

---

### P2 — 排行榜页面 ✅ 已完成（13页）
**目标**：高搜索量入口词，天然容易被引用传播

已生成13个页面（`generate_ranking_pages.py`）：
- `best-majors-china-2025.html` — Top 50 按星级排名
- `ai-picks-majors-china.html` — AI标记的13个专业
- `ai-resistant-majors-china.html` — 医学/法律/哲学（AI抵抗型）
- 分类页 × 10：engineering / medicine / science / economics / management / law / literature / agriculture / education / history-philosophy

Sitemap已更新（758 + 13 = 771 URLs）

---

### P3 — 职业数据库（下个月）
**目标**：专业 → 职业 → 薪资 → 增长 完整链条

架构：
```
/tools/careers/software-engineer.html
/tools/careers/ai-engineer.html
/tools/careers/clinical-medicine-physician.html
...
```

起点：88个子类已有 careers 字段（3个/子类），共约 200 个不重复职业
每个职业页包含：
- 职业简介
- 所需专业背景
- 薪资范围（初级/中级/高级）
- AI影响程度
- 关联专业链接（内链网络）

内链逻辑：
```
专业页 → 职业页 → 其他相关专业页
```
形成知识图谱，对 SEO 和用户体验都有复利效应

---

### P4 — 数据持久化（未来）
WordPress PHP 后端：`/wp-json/major-votes/v1/`
- 投票存数据库（当前只存 localStorage）
- 支持按身份/行业分析投票分布
- WPCode Lite 插件实现（代码已规划，未部署）

---

### Phase 2 — 其他国家版本（长期）
- 美国：CIP code 体系
- 英国：UCAS subject 体系
- 印度：UGC 体系
- 框架相同，数据替换，形成多语言/多国家 SEO 矩阵
