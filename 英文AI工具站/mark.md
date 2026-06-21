# 英文博客 ordinarymantrying.com · 项目全貌记录

> 这个文件是给下一个 Claude 看的，也是给我自己看的。
> 目标：让任何一个新 Claude 打开这个文件后，5分钟内就能理解这个项目的来龙去脉，直接上手帮忙。

---

## 用户背景（重要，影响所有决策）

- IT行业从业者，非金融专业背景
- 儿子刚上高一，是做这件事的重要情感动机之一
- 学习价值投资约10个月，主要用AI（Gemini/Claude）自学，有一位实践经验丰富的线上朋友作为参照
- 有过多次副业尝试，都没成功：枸杞站（mjy-shop.com）做了6年没赚钱、手卷钢琴亏钱、还有一个因为愧疚放弃的副业（文章05里有写）
- 投入了约700元（域名+主机），希望能赚回来；赚不到也可以接受，因为有股票投资兜底

---

## 为什么会有这个博客（用户自述）

1. 老师说价值投资要"选好股，多去赚钱攒股" → 需要副业收入来源
2. 怕失业 → 想用副业分散风险
3. 和 Claude 沟通后，从"AI工具测评"转向"创业/投资/AI折腾记录"博客（测评不在行，但有多次失败副业经历可以写）
4. 想**写真东西**，以后给儿子毕业时看——这个动机很耐久，不依赖外部收入反馈
5. 变现路径：广告费（AdSense）+ 联盟营销（Hostinger等）

---

## 四个项目的全貌

用户同时在推进4个项目。这是一个关键背景，帮助理解内容选题的来源。

| 项目 | 平台 | 状态 | 优先级 |
|---|---|---|---|
| 英文个人博客 | ordinarymantrying.com | 活跃进行中 | ⭐⭐⭐⭐⭐ 最高 |
| 小红书价值投资账号「用AI挖护城河」| 小红书 | 已发1篇，60篇内容就绪 | ⭐⭐⭐⭐ 高 |
| 小红书信息差账号「外网副业情报站」| 小红书 | 进行中，翻译Reddit/IndieHackers故事 | ⭐⭐⭐ 中 |
| 闲鱼二手 | 闲鱼 | 还未启动 | ⭐⭐ 低（最耗运营精力） |

**项目协同逻辑：** 价值投资账号深化投资思考 → 信息差账号锻炼内容生产 → 英文博客把两者综合为全球受众叙述。不是完全分裂的。

---

## 英文博客基础信息

| 项目 | 内容 |
|---|---|
| 网址 | https://ordinarymantrying.com |
| WP 后台 | https://ordinarymantrying.com/wp-admin |
| 域名注册 | Namecheap，$11.28/年，到期 2027-06-15 |
| 主机 | Hostinger 美国节点，24个月 ¥542 |
| 主题 | Astra（免费版） |
| 插件 | Yoast SEO、LiteSpeed Cache |
| WordPress 登录用户名 | love0972@outlook.com |
| Application Password | MQgZ LdsN BECb sfLY fqzB sGBn（名称: claude-import） |
| 凭证文件 | wp_credentials.json（已加 .gitignore，不可提交！） |
| API 接入 | REST API + Application Password，Python脚本 import_to_wp.py 推草稿 |

---

## 博客定位与内容规则

**定位：** 一个中国普通人，用AI折腾创业和投资，真实记录每一步——包括失败。

**四个内容支柱：**
1. My AI Experiments（AI实验记录）
2. Side Hustle Diaries（副业日记）
3. Lessons from Failure（失败课）
4. AI + Investing（AI+投资）

**写作铁律（不能破）：**
- 第一人称，真实，不卖课，不画饼，不承诺结果
- 具体数字、具体时间、具体失败——越具体越好
- 英文由AI辅助写，但必须是自然英文，不是翻译腔
- 价值投资类文章：不给股票推荐、不给价格目标、不承诺回报——写框架和过程，不写结论
- 不追热点，只写亲身经历

**差异化核心：** 中国人视角 + 多次失败的真实经历 + 正在进行时（不是回头看成功）

---

## 当前文章状态（2026-06-17，第三次更新）

### 已发布（25篇）
| ID | 文件 | 标题 |
|---|---|---|
| 27 | 01-my-story.md | I'm an Ordinary Chinese Guy Trying to Make Money Online with AI |
| 32 | 02-goji-berry-6-years.md | My Goji Berry Website Ran for 6 Years and Never Made Money |
| 70 | 03-ai-60-posts-one-day.md | I Used AI to Create 60 Social Media Posts in One Day |
| 71 | 04-analyze-stocks-with-claude.md | How I Analyze Chinese Stocks with Claude Every Morning |
| 72 | 05-side-hustle-i-quit.md | The Side Hustle I Quit Because I Felt Guilty |
| 73 | 06-week1-reality-check.md | Week 1 of Running This Blog: Expectations vs. Reality |
| 74 | 07-ai-said-buy-i-hesitated.md | AI Told Me to Buy. I Hesitated. It Tripled. |
| 75 | 08-the-side-hustle-i-never-mentioned.md | The Side Hustle I Run in Chinese That I've Never Mentioned Here |
| 76 | 09-value-investing-account-native-language.md | I Also Started a Value-Investing Account — In My Native Language First |
| 77 | 10-what-makes-a-10x-company.md | What Makes a Stock a 10x Candidate? I Asked AI to Help Me Build a Filter |
| 78 | 11-two-stocks-i-held-too-long.md | The Two Stocks I Held for Years That I Should Have Sold Much Earlier |
| 79 | 12-grassroots-research-supermarket-test.md | Before I Buy a Stock, I Go to the Supermarket |
| 80 | 13-how-i-built-this-blog-700rmb.md | How I Built This Blog for ¥700 and What I'd Do Differently |
| 81 | 14-when-i-fell-in-love-with-a-stock.md | When I Fell in Love With a Stock (And Why That's Dangerous) |
| 82 | 15-ai-helped-me-become-a-better-advocate.md | I Used AI to Research My Dad's Parkinson's Disease |
| 102 | 16-i-fed-20-reports-to-ai.md | I Fed 20 Financial Reports to AI. It Ignored My Question and Found a Better One. |
| — | 17-why-i-chose-hostinger-for-10-years.md | Why I'm Hosting This Blog Outside China（**待发布**，等Hostinger联盟链接审批通过） |
| 147 | 18-ai-helped-me-cool-my-rooftop.md | My Dad Said "Just Use the AC." I Asked AI Instead. ¥546 Later, I Barely Need It. |
| 166 | 19-xiaohongshu-banned-day-one.md | I Asked AI to Help Me Start a Side Hustle on China's Biggest App. My Account Was Banned Before I Got a Single Follower. |
| 174 | 20-ai-civil-service-exam-guide.md | My Niece Is Competing for One of China's Most Sought-After Jobs. I Used AI to Build Her a 30-Page Study Guide. It Took 20 Minutes. |
| 182 | 21-ai-home-server-openclaw-hermes.md | I Spent ¥340 on a Mini PC to Run a Local AI Agent. The AI Chose the Hardware. The Software Was Already Obsolete. |
| 195 | 22-ai-predict-gaokao-2026.md | 12 Million Students. One Exam. I Asked AI to Predict the Questions 6 Days Early. Here's the Verdict. |
| 197 | 23-ai-investment-handbook-second-opinion.md | I Asked AI to Read 10 Months of My Investment Conversations and Write a Second Opinion. |
| 199 | 24-ai-career-roadmap-45.md | I'm 45, I Work in IT, and I Asked AI to Plan My Next 5 Years. It Didn't Tell Me What I Wanted to Hear. |
| 308 | 25-worldcup-ai-prediction.md | I Made 6 AI Models Predict the World Cup. They Almost All Agreed. (Results: June 24) |

**图片配置清单：** articles/image-briefs.md（每篇文章有图片方向、搜索关键词、alt文字）

**素材来源：** 信息反馈/gemini对话.txt、gemini对话3.txt（含10个月投资学习对话记录）——文章10/11/12改编自此，去掉了全部个人信息，仅用投资框架和心理故事

---

## 变现状态与现实预期

| 渠道 | 状态 | 备注 |
|---|---|---|
| Hostinger 联盟 | **已申请，审核中** | 通过后在文章17嵌入链接再发布，一单 $65 |
| Amazon Associates | 未申请 | associates.amazon.com，门槛低 |
| Google AdSense | **等 4-6 周后申请（约 2026-08）** | 21篇已达门槛，但全部发布于3天内，需等日期"熟化"避免内容农场嫌疑 |

**重要时间线认知（给用户和 Claude 都要记住）：**
- Google 自然流量：通常需要 6-18 个月才有实质增长，前3个月基本是零
- 正确期望：**12个月后评估值不值**，中间只看文章数量和质量，不看收入
- 最快的钱：Hostinger 联盟，写一篇建站文章嵌入链接，一次转化=$65

---

## 技术基础设施

- **Python 导入脚本：** `import_to_wp.py`
  - 用法：把新 .md 文件名加入 ARTICLES 列表，`python3 import_to_wp.py` 推草稿
  - 格式：首行 `# 标题`，第二行 `*Category: xxx | ~xxx words*`，`---` 分隔，正文，`---` 结尾，closing 问句
- **凭证文件：** `wp_credentials.json`（含真实密码，已 .gitignore，**绝对不能 git commit**）
- **Hostinger/LiteSpeed 坑：** `.htaccess` 需要加 Authorization 头透传规则（已加），否则 API 401
- **About Me 页面：** 已通过 API 重做（Cover块+头像+正文），不再依赖 Site Editor Title 块

### Footer 编辑方法

Footer 是 FSE（Full Site Editing）主题的 template part，**不是** widget。

```python
# 读取
GET /wp-json/wp/v2/template-parts/hostinger-ai-theme//footer?context=edit

# 修改后写回
POST /wp-json/wp/v2/template-parts/hostinger-ai-theme//footer
{"content": raw_content}
```

- Footer 结构：3列（Menu / Contacts / Newsletter）+ 底部版权栏
- "Menu" 列引用 Navigation Block ID 11（同时也是 header 导航）
- **不要在 WP Site Editor 里保存 footer**（同首页风险）

---

### ⚠️ 首页（Page ID 8）编辑禁区

**绝对不要在 WordPress 后台用可视化编辑器或代码编辑器打开首页后保存！**

- WordPress 编辑器会自动注入 `<!-- wp:post-content -->` 模板块，导致整个首页内容渲染两遍
- 此 bug 已触发两次（2026-06），每次要用 Python 脚本修复
- **首页只能通过 Python API 脚本修改**
- 若不小心打开了，直接关标签页，不要点保存/更新

**修复脚本（每次出问题都用这个逻辑）：**
```python
# 找到第一个 <!-- /wp:post-content --> 截断
raw = page['content']['raw']
cut = raw.find('<!-- /wp:post-content -->')
clean = raw[:cut]
# 验证正常值：wp:cover=1, My Tools出现2次(标题+按钮), Who I Am=1, wp:post-content=0
# POST 到 /wp-json/wp/v2/pages/8
```

---

## 已完成的网站页面

| Page | URL | ID |
|---|---|---|
| 首页 | ordinarymantrying.com | 8 |
| Blog列表 | /blog/ | 9 |
| About Me | /about-me/ | 24 |
| Tools | /tools/ | — |
| Privacy Policy | /privacy-policy/ | 184 |
| Contact | /contact/ | 185 |

- 首页含：工具区块、About 区块、最新文章入口
- About Me 含 aboutme.png 卡通头像 Tim（200×280px）
- Privacy Policy 覆盖：Cookie / AdSense / 联盟链接披露 / GDPR
- Contact 含联系邮箱，footer "Contacts" 栏指向此页（不直接暴露邮箱）

---

## 内容选题建议（下一批文章方向）

**最值得写的（有具体个人故事支撑）：**
- 更多副业失败故事——每一次失败都可以是一篇独立文章
- 价值投资学习的10个月：AI作为老师是什么感受，买错了股票怎么处理
- 如果闲鱼启动了：实时记录摆摊、定价、第一单的过程
- 儿子视角：如果有一天他问我钱是怎么来的……（情感共鸣强）

**谨慎写的（竞争激烈，需要有差异化内容）：**
- 技巧类/测评类——除非有自己的真实数字截图，否则同质化严重

**来自 Gemini 对话文件的更多可写方向（信息反馈文件夹）：**
- "炒股"到"攒股"的心态转变（把市场下跌看成买入机会，不是灾难）
- 十六字方针：如何给自己设置不碰融资的纪律规则
- 如何比较同行业两家公司（安琪vs梅花，东阿vs片仔癀）——AI作为思维陪练
- 管理层研究：我为什么去研究一个CEO有没有"野心"
- 仓位管理：凯利公式的普通人版本——赔率和胜率怎么决定我押多少

**已写过的选题（不要重复）：**
见上方草稿列表中的12个标题。

---

## 踩坑记录（给下一个 Claude 避坑）

### 坑1：Python 脚本里中文弯引号导致 SyntaxError
文章内容含中文弯引号 `"..."` 嵌套在 Python 双引号字符串时，`"` (U+201C) 被解析器当作字符串结束符。
**修复：** 外层 Python 字符串改用单引号 `'...'` 包裹含弯引号的文本。

### 坑2：Privacy Policy slug 被 WP 默认草稿占用
WordPress 安装时自动创建 ID 3 的 draft "Privacy Policy" 占用了 `privacy-policy` slug，新建页面变成 `privacy-policy-2`。
**修复：** `DELETE /wp-json/wp/v2/pages/3`，再 `POST /wp-json/wp/v2/pages/184` `{"slug":"privacy-policy"}`。

### 坑3：AdSense 内容农场嫌疑
21篇文章全部在 2026-06-15 至 2026-06-17 三天内发布，AdSense 审核系统识别为内容农场模式。
**对策：** 继续写新文章，让日期自然向后延伸；等 4-6 周后再申请 AdSense（目标：2026-08 初）。

### 坑4：Footer 暴露了 WP 管理员邮箱
Hostinger AI 主题 footer 的 "Contacts" 栏默认填入了 WP 管理员邮箱 `love0972@outlook.com`。
**修复：** 通过 template-parts API 替换为 Contact 页面链接，邮箱不再公开暴露。

### 坑5：Widget API 对 FSE 主题无效
主题使用 Full Site Editing，`/wp-json/wp/v2/sidebars` 只返回 `wp_inactive_widgets`。
Footer 内容在 template part 里，用 `/wp-json/wp/v2/template-parts/hostinger-ai-theme//footer` 操作。

---

## ⚠️ 发新文章必做：评论区模板

**Astra 主题全局评论开关无效**，每篇文章必须手动在内容末尾追加评论块。
用 import_to_wp.py 推草稿后，再用以下 Python 片段追加（或在 `append_comments.py` 中复用）：

```python
COMMENT_BLOCK = '''<!-- wp:html -->
<div style="margin-top:40px;padding-top:24px;border-top:1px solid #e5e5e5">
  <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#999;margin:0 0 28px">Share your experience or thoughts below.</p>
</div>
<style>
.wp-block-post-comments .commentlist .comment{padding-left:0!important}
.wp-block-post-comments .commentlist .comment p{margin:.15em 0!important}
.wp-block-avatar,.wp-block-avatar img{display:none!important}
.wp-block-comment-author-name{margin:0 0 2px!important}
.wp-block-comment-date{margin:0 0 6px!important}
.wp-block-comment-content{margin:0 0 6px!important}
.wp-block-comment-reply-link{margin:0!important}
.wp-block-comment-author-name a,.wp-block-comment-author-name{font-family:-apple-system,sans-serif;font-size:14px;font-weight:700;color:#1a1a1a;text-decoration:none}
.wp-block-comment-date a,.wp-block-comment-date{font-family:-apple-system,sans-serif;font-size:12px;color:#aaa;text-decoration:none}
.wp-block-comment-content p{font-family:Georgia,serif;font-size:16px;color:#333;line-height:1.7}
.wp-block-comment-reply-link a{font-family:-apple-system,sans-serif;font-size:12px;color:#888;text-decoration:none}
.comment-reply-title{font-family:Georgia,serif;font-size:20px;font-weight:700;color:#1a1a1a;margin-bottom:16px}
.comment-notes,.comment-form label{font-family:-apple-system,sans-serif;font-size:13px;color:#555}
.comment-form label{display:block;margin-bottom:5px;font-weight:600}
.comment-form textarea,.comment-form input[type="text"],.comment-form input[type="email"],.comment-form input[type="url"]{width:100%;border:1px solid #e0e0e0;border-radius:5px;padding:10px 13px;font-family:Georgia,serif;font-size:15px;color:#1a1a1a;background:#fafafa;box-sizing:border-box}
.comment-form textarea:focus,.comment-form input:focus{outline:none;border-color:#1a1a2e;background:#fff}
.comment-form textarea{min-height:110px}
.comment-form-comment,.comment-form-author,.comment-form-email,.comment-form-url{margin-bottom:14px}
.form-submit .submit{background:#1a1a2e;color:#fff;border:none;border-radius:5px;padding:11px 26px;font-family:-apple-system,sans-serif;font-size:14px;font-weight:700;cursor:pointer}
.form-submit .submit:hover{background:#2d2d50}
</style>
<!-- /wp:html -->

<!-- wp:comments -->
<div class="wp-block-comments"><!-- wp:comment-template -->
<!-- wp:group {"style":{"spacing":{"margin":{"top":"1.2em","bottom":"1.2em"},"padding":{"bottom":"1.2em"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group" style="margin-top:1.2em;margin-bottom:1.2em;padding-bottom:1.2em;border-bottom:1px solid #f0f0f0">
<!-- wp:comment-author-name {"fontSize":"small"} /-->
<!-- wp:comment-date {"fontSize":"small"} /-->
<!-- wp:comment-content /-->
<!-- wp:comment-reply-link {"fontSize":"small"} /-->
</div>
<!-- /wp:group -->
<!-- /wp:comment-template -->
<!-- wp:comments-pagination -->
<!-- wp:comments-pagination-previous /-->
<!-- wp:comments-pagination-numbers /-->
<!-- wp:comments-pagination-next /-->
<!-- /wp:comments-pagination -->
<!-- wp:post-comments-form /--></div>
<!-- /wp:comments -->'''

# 追加到文章末尾
POST_ID = ???  # 填入文章 ID
url = f'{SITE}/wp-json/wp/v2/posts/{POST_ID}?context=edit&_fields=content'
# ... 读取 raw，追加 COMMENT_BLOCK，POST 回去
```

---

## 高考志愿填报工具（2026-06-21 上线）

**主工具页：** ordinarymantrying.com/tools/major-vote.html
**详情页：** ordinarymantrying.com/tools/majors/[slug].html × 757页
**排行榜/分类页：** × 13页（见下）
**投票后端：** ordinarymantrying.com/tools/votes.php（PHP，IP限速，JSON持久化）
**总页面数：** 771页

生成脚本：
- `generate_major_pages.py` → 757个专业详情页
- `generate_ranking_pages.py` → 13个排行榜/分类页

13个排行榜页（均在 /tools/ 目录）：
- best-majors-china-2025.html（Top 50）
- ai-picks-majors-china.html（13个AI标记专业）
- ai-resistant-majors-china.html（医学/法律/哲学）
- engineering / medicine / science / economics / management / law / literature / agriculture / education / history-philosophy × 10个分类页

SEO：sitemap.xml 771个URL，已提交 Google GSC + Bing IndexNow
主工具页新增排行榜导航栏（横向滚动13个标签）

配套博客文章：Post 445（已更新含Update段落+2张截图）
building-in-public 页：Post 339（Timeline已更新，高考志愿工具上线记录）

---

## 工具页 11个人生模拟器（2026-06-21 更新）

**已上线：** ordinarymantrying.com/tools/（工具页显示全部21张卡片：10个工具 + 11个模拟器）

**11个模拟器：**
- zhangxue / disney / honda / curie / jobs / rowling / oprah / musk / mandela / buffett
- **hawking-simulator.html**（2026-06-21新增，7个决策，简单英语，含《时间简史》Amazon联盟链接 amzn.to/4eT7gKG）

**配套博客文章：** 26-life-simulators.md（已写好，待发布至WP）

---

## 文章25「世界杯AI预测实验」进度（2026-06-19）

**核心实验：** 让3个中国AI（Kimi/豆包/千问）+ 3个美国AI（ChatGPT/Gemini/Claude）预测足彩26087期14场比赛，买了两张真票各¥2。

**关键发现：**
- 14场中12场6个AI预测完全一致
- 唯一中美分歧：场次9挪威vs塞内加尔——中国AI全押挪威赢，美国AI全押平局
- 结果出炉时间：**2026-06-24**

**发布状态：**
- ✅ 博客已发布：https://ordinarymantrying.com/6-ai-models-predict-world-cup-china-vs-us/（Post ID 308）
- ✅ X（Twitter）已发（1次曝光，0点击）
- ✅ Dev.to已发：https://dev.to/vn_tunl_09a36fcbda701/i-pitted-3-chinese-ai-models-against-3-american-ones-on-14-world-cup-matches-363c
- ✅ Medium已发：https://medium.com/@levantuann002/...（含canonical link指回博客）
- ❌ Hacker News：新账号无法提交
- ❌ Reddit r/ChatGPT：账号需满4个月才能发帖，u/Remote_Weakness7905 需等待至2026-10月

**Part 2计划（6月24日开奖后）：**
- 填入14场实际结果，计算每个AI准确率
- 宣布中美AI谁赢（核心：挪威vs塞内加尔谁对）
- 发布博客Part 2，更新Reddit评论区

**草稿：** articles/draft-worldcup-ai-prediction-part1.md（Part 1参考）
**Part 2模板：** articles/draft-worldcup-part2.md（框架已写好，24日填数据即可发布）

---

## Wuying MCP（阿里云无影云桌面）

- **Server名称：** wuying_mcp_server
- **Key：** akm-d3faa052-559e-49d6-bbeb-0277d0aec172（免费key，过期前抓紧用）
- **端点：** https://agentbay.wuying.aliyuncs.com/v2/mcp（HTTP transport，Ubuntu 22.04）
- **状态：** ✓ Connected，但tools需**重启Claude Code**后才能使用
- **用途：** 云端真实Ubuntu浏览器，可操作任何网站

配置命令（key失效时重新配）：
```bash
claude mcp add wuying_mcp_server \
  --transport http \
  "https://agentbay.wuying.aliyuncs.com/v2/mcp?APIKEY=YOUR_KEY&IMAGEID=computer-use-ubuntu-2204"
```

---

## 下一步行动清单

**用户需要做：**
1. **2026-06-24**：拿到足彩结果，让Claude写Part 2博客并发布（Dev.to/Medium同步更新）
2. Hostinger 联盟审核通过后：更新文章17并发布（占位符：`YOUR_HOSTINGER_AFFILIATE_LINK_HERE`）
3. HN/Reddit：等账号成熟，继续评论积karma
4. 设备温度监控Python：用户在研究，回来找Claude写代码

**Claude 下次继续帮忙时：**
1. 高考志愿填报文章：草稿在 articles/35-gaokao-major-ai.md，等用户确认发布
2. 世界杯Part 2：草稿在 articles/draft-worldcup-part2.md，24日填数据发布
3. 文章17 Hostinger联盟：等审核通过

**已发布文章（2026-06-21新增）：**
- Post 436：I Tried to Promote My AI Experiment — and Got Blocked Everywhere（含3张截图）
  URL: https://ordinarymantrying.com/blocked-everywhere-trying-to-promote-ai-experiment/

**已修复（2026-06-21）：**
- goji-berry tag（ID 13）已删除，不再产生404空页面

---

*最后更新：2026-06-21（第七次），Claude Sonnet 4.6 整理*
