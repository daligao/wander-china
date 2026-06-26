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

## 当前文章状态（2026-06-26，第四次更新）

### 已发布（44篇）

**原创25篇（用户自述素材）：**
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
| — | 17-why-i-chose-hostinger-for-10-years.md | **Hostinger vs Bluehost for Bloggers Outside China**（**待发布**，等Hostinger联盟批准后填入链接）|
| 147 | 18-ai-helped-me-cool-my-rooftop.md | My Dad Said "Just Use the AC." I Asked AI Instead. ¥546 Later, I Barely Need It. |
| 166 | 19-xiaohongshu-banned-day-one.md | I Asked AI to Help Me Start a Side Hustle on China's Biggest App. My Account Was Banned Before I Got a Single Follower. |
| 174 | 20-ai-civil-service-exam-guide.md | My Niece Is Competing for One of China's Most Sought-After Jobs. I Used AI to Build Her a 30-Page Study Guide. It Took 20 Minutes. |
| 182 | 21-ai-home-server-openclaw-hermes.md | I Spent ¥340 on a Mini PC to Run a Local AI Agent. The AI Chose the Hardware. The Software Was Already Obsolete. |
| 195 | 22-ai-predict-gaokao-2026.md | 12 Million Students. One Exam. I Asked AI to Predict the Questions 6 Days Early. Here's the Verdict. |
| 197 | 23-ai-investment-handbook-second-opinion.md | I Asked AI to Read 10 Months of My Investment Conversations and Write a Second Opinion. |
| 199 | 24-ai-career-roadmap-45.md | I'm 45, I Work in IT, and I Asked AI to Plan My Next 5 Years. It Didn't Tell Me What I Wanted to Hear. |
| 308 | 25-worldcup-ai-prediction.md | I Made 6 AI Models Predict the World Cup. They Almost All Agreed. (Results: June 24) |
| 445 | 35-gaokao-major-ai.md | Gaokao Major AI（含Update段落） |
| 538 | draft-worldcup-part2.md | World Cup Part 2 |
| 574 | — | 手卷钢琴文章（含PageSpeed图+Hostinger联盟链接） |

**AI Generated工具配套文章（19篇，2026-06-26发布）：**
| ID | 文件 | 标题 |
|---|---|---|
| 597 | 26-life-simulators.md | I Built 10 Life Simulators… |
| 598 | 27-ai-replaced-my-sons-tutor.md | I Paid ¥3,840 for a Tutoring Class… |
| 599 | 28-buffett-7-decisions.md | Warren Buffett Made 7 Real Decisions… |
| 600 | 29-nelson-mandela-decisions.md | Nelson Mandela Was Offered Early Release… |
| 601 | 37-life-paper-900-squares.md | I Mapped 74 Famous Lives Into 900 Squares… |
| 602 | 38-life-a4.md | Your Entire Life Fits on One Sheet of A4 Paper… |
| 603 | 39-life-clock.md | What Percentage of Your Life Is a Black Hole?… |
| 604 | 40-buffett-value-screen.md | I Distilled Warren Buffett's Investing Criteria… |
| 605 | 41-investment-punch-card.md | Buffett Says You Only Get 20 Investment Punches… |
| 606 | 42-mandarin-flashcards.md | Offline Mandarin Flashcard App HSK 1–3 |
| 607 | 43-chinese-writing-toolkit.md | 11 Types of Chinese Letters… |
| 608 | 44-chinese-reading-lab.md | 10 Historical Decisions in Chinese HSK 4–6 |
| 609 | 45-chengyu-stories.md | 20 Chinese Idioms With 2,000-Year-Old Stories |
| 610 | 46-pinyin-annotator.md | Free Pinyin Annotator, No App |
| 611 | 47-china-career-database.md | 259 Chinese Career Paths |
| 612 | 48-major-rankings.md | 13 Ranking Lists for China's 757 Majors |
| 613 | 49-iq-challenge.md | 3 Lateral Thinking Traps |
| 614 | 50-shuangseqiu.md | Shuangseqiu Number Generator |
| 615 | 51-zhangxue-simulator.md | Zhang Xue Beat Ducati |

**素材来源：** 信息反馈/gemini对话.txt、gemini对话3.txt（含10个月投资学习对话记录）——文章10/11/12改编自此，去掉了全部个人信息，仅用投资框架和心理故事

---

## 变现状态与现实预期

| 渠道 | 状态 | 备注 |
|---|---|---|
| Hostinger 联盟 | **已申请，审核中** | 批准后替换文章17中 `YOUR_HOSTINGER_AFFILIATE_LINK_HERE` 占位符，再发布，一单 $65 |
| Bluehost 联盟 | **✅ 已批准** | 链接：https://bluehost.sjv.io/c/7436386/1376228/11352，已嵌入文章17，一单 $65 |
| Amazon Associates | 未申请 | associates.amazon.com，门槛低 |
| Google AdSense | **等 4-6 周后申请（约 2026-08）** | 44篇已达门槛，日期跨度需继续积累 |

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

### 坑6：Python f-string 里不能嵌套字典字面量
homepage 脚本 `tnode()` 函数里写了 `f'rgba({{"#34d399":"52,211,153",...}.get(clr,...)},0.25)'`，大括号转义和字典字面量冲突，报 `SyntaxError: single '}' is not allowed`。
**修复：** 把颜色RGB映射提取成普通变量，作为参数 `rgb` 传入函数，f-string 里只引用变量名。

### 坑7：文章封面图 URL 不要靠文件名猜，要用 API 查
给首页 Start Here 配图时，用了文章上传原始文件名 `15-late-night-ai-research-1024x538.jpg`，但 WP 实际存储的文件名是 `ai-parkinsons-research.jpeg`（upload 时重命名了），导致图片显示错误。
**正确做法：** `GET /wp-json/wp/v2/posts/{id}?_fields=featured_media` 拿 media ID，再 `GET /wp-json/wp/v2/media/{mid}` 拿 `source_url`，绝对准确。

### 坑8：大量文章分类是 Uncategorized 导致博客列表看不到
批量导入的文章没有设置分类，默认落在 Uncategorized。WP 博客页虽然不过滤分类，但 Yoast SEO 评分低，且用户浏览分类时找不到。
**修复（2026-06-25）：** 批量 PATCH `/wp-json/wp/v2/posts/{id}` 设置 `categories`，共修复 14 篇。分类逻辑：AI实验/工具类 → My AI Experiments(19)；副业/建站 → Side Hustle Diaries(4)；模拟器 → My AI Experiments(19)。

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

## FTP 直接上传工具（重要！以后用这个，不用手动登录 Hostinger）

**凭证文件：** `/Volumes/mg-ssd500/aifile/英文AI工具站/web-ftp-password.txt`（本地，不要上传到 GitHub）

```
FTP IP:   185.212.71.129
用户名:   u730818097
端口:     21
密码:     见 web-ftp-password.txt
```

**服务器工具目录路径：**
```
/domains/ordinarymantrying.com/public_html/tools/
```

**上传单个文件的命令（直接复制用）：**
```bash
FTP_USER="u730818097"
FTP_PASS=$(grep "Password:" /Volumes/mg-ssd500/aifile/英文AI工具站/web-ftp-password.txt | cut -d' ' -f2)
curl -s -T "本地文件路径" \
  "ftp://185.212.71.129/domains/ordinarymantrying.com/public_html/tools/文件名" \
  --user "$FTP_USER:$FTP_PASS" && echo "✓ 上传成功"
```

**批量上传多个文件：**
```bash
FTP_USER="u730818097"
FTP_PASS='见web-ftp-password.txt'
FTP_BASE="ftp://185.212.71.129/domains/ordinarymantrying.com/public_html/tools"

for file in 文件1.html 文件2.html 文件3.json; do
  curl -s -T "/本地路径/$file" "$FTP_BASE/$file" --user "$FTP_USER:$FTP_PASS" && echo "✓ $file"
done
```

**⚠️ 重要：密码里含特殊字符（`?.<}&%)`），curl `--user` 参数用单引号包裹整个 user:pass**

**列出服务器目录（验证上传）：**
```bash
curl -s "ftp://185.212.71.129/domains/ordinarymantrying.com/public_html/tools/" \
  --user "u730818097:密码" --list-only | grep "关键词"
```

---

## 中文学习工具（2026-06-23 上线）

### mandarin-flashcards（卡片+故事阅读）
- **网站完整版：** ordinarymantrying.com/tools/mandarin-flashcards.html（HSK1 150词，故事逐句阅读模式）
- **GitHub 公开版：** daligao.github.io/mandarin-flashcards/（同上，CC0）
- **本地文件：** `/Volumes/mg-ssd500/aifile/英文AI工具站/ordinarymantrying.com/tools/mandarin-flashcards.html`
- **GitHub repo：** `/Volumes/mg-ssd500/aifile/mandarin-flashcards/`
- **特色：** 点击任意汉字弹出拼音+释义，TTS 朗读，SRS 间隔复习

### chinese-writing-toolkit（中文写作练习）
- **网站完整版（11种）：** ordinarymantrying.com/tools/chinese-writing-toolkit.html
  - 包含：邀请信/感谢信/建议信/道歉信/申请信/通知/演讲稿/询问信/投诉信/求职信/自我介绍
  - 额外内容通过 fetch('cwt-extra.json') 加载——**cwt-extra.json 只存服务器，不在 GitHub**
- **GitHub 公开版（9种）：** daligao.github.io/chinese-writing-toolkit/（无求职信+自我介绍，CC0）
- **本地文件：** `/Volumes/mg-ssd500/aifile/英文AI工具站/ordinarymantrying.com/tools/chinese-writing-toolkit.html`
- **额外内容文件：** `/Volumes/mg-ssd500/aifile/英文AI工具站/ordinarymantrying.com/tools/cwt-extra.json`
- **GitHub repo：** `/Volumes/mg-ssd500/aifile/chinese-writing-toolkit/`
- **差异化策略：** 下载 HTML 到本地 → fetch 失败 → 9种+引流横幅；网站访问 → fetch 成功 → 11种完整版

**上传命令（网站版更新时）：**
```bash
FTP_USER="u730818097"; FTP_PASS='见凭证文件'
BASE="ftp://185.212.71.129/domains/ordinarymantrying.com/public_html/tools"
curl -s -T chinese-writing-toolkit.html "$BASE/chinese-writing-toolkit.html" --user "$FTP_USER:$FTP_PASS"
curl -s -T cwt-extra.json "$BASE/cwt-extra.json" --user "$FTP_USER:$FTP_PASS"
```

**注意：cwt-extra.json 不能 commit 到 GitHub（内含网站独家内容）**

---

## mandarin-flashcards HSK 扩展（2026-06-23 完成）

### 完成内容
- **HSK2 词库（126词）+ HSK3 词库（124词）** → 新文件 `mandarin-flashcards-hsk23.json`
  - 位置：`/Volumes/mg-ssd500/aifile/英文AI工具站/ordinarymantrying.com/tools/mandarin-flashcards-hsk23.json`
  - ⚠️ 此文件**只在服务器+本地**，不在 GitHub（同 cwt-extra.json 策略）
- **mandarin-flashcards.html 更新：**
  - 新增 Level 筛选器（All / HSK1 / HSK2 / HSK3）—— 网站版自动显示
  - fetch('mandarin-flashcards-hsk23.json') 成功时：加载 400+ 词，显示筛选器
  - fetch 失败时（GitHub/本地）：只显示 HSK1 150词 + 引流横幅
  - 已 FTP 上传到服务器
  - 已 git push 到 daligao/mandarin-flashcards（GitHub 版不含 JSON 文件）

### 文件更新命令（下次更新时用）
```bash
FTP_PASS=$(grep -i password /Volumes/mg-ssd500/aifile/英文AI工具站/web-ftp-password.txt | head -1 | awk '{print $NF}')
BASE="ftp://185.212.71.129/domains/ordinarymantrying.com/public_html/tools"
curl -s -T mandarin-flashcards.html "$BASE/mandarin-flashcards.html" --user "u730818097:$FTP_PASS"
curl -s -T mandarin-flashcards-hsk23.json "$BASE/mandarin-flashcards-hsk23.json" --user "u730818097:$FTP_PASS"
```

---

## GitHub 外链网络（2026-06-23 完成）

### 已建立的外链
所有操作均已 push 到 GitHub，无需用户额外操作。

| 仓库 | 操作 | 状态 |
|---|---|---|
| daligao/daligao（Profile README）| 新建，含全部工具链接 | ✅ 新建 |
| daligao/awesome-mandarin | 更新 Flashcards 为 HSK1-3 全版本；新增 Writing Toolkit | ✅ 更新 |
| daligao/awesome-chinese-learning | 更新 Flashcards；新增 Writing Toolkit；更新目录 | ✅ 更新 |
| daligao/awesome-no-login-web-apps | 新增 Flashcards + Writing Toolkit | ✅ 更新 |
| daligao/awesome-english | 新增博客链接（authentic English reading resource）| ✅ 更新 |
| daligao/gaokao-2026-english-exam | 新增 Related Tools 章节（链接4个工具）| ✅ 更新 |
| daligao/china-civil-service-challenge | 新增 Related Tools 章节 | ✅ 更新 |
| daligao/investment-punch-card | 新增 More Free Tools 章节 | ✅ 更新 |
| daligao/major-vote-cn-selector | 新增 More Free China Tools 章节 | ✅ 更新 |
| daligao/mandarin-flashcards | README 已有链接（上次更新）| ✅ 保持 |
| daligao/chinese-writing-toolkit | README 已有链接（上次更新）| ✅ 保持 |
| daligao/awesome-seo | 博客+文章链接（上次更新）| ✅ 保持 |
| daligao/awesome-indie | 博客链接（上次更新）| ✅ 保持 |

**外链覆盖总结：** ordinarymantrying.com 现在在 13 个 GitHub 仓库中有链接，涵盖工具首页、各工具页、博客文章。

---

## 下一步行动清单

**用户需要做：**
1. **2026-06-24**：拿到足彩结果，让Claude写Part 2博客并发布（Dev.to/Medium同步更新）
2. Hostinger 联盟审核通过后：更新文章17并发布（占位符：`YOUR_HOSTINGER_AFFILIATE_LINK_HERE`）
3. HN/Reddit：等账号成熟，继续评论积karma
4. Discord/Quora：有时间时发帖推广中文学习工具

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

---

## 夜间自动任务完成记录（2026-06-24 凌晨）

### 已完成
| 操作 | 结果 |
|---|---|
| 第26篇博客（Life Simulators）确认 | 已于2026-06-20发布为Post 336，URL: ordinarymantrying.com/life-simulator-legendary-decisions/ |
| IQ Challenge 加入 tools/index.html | ✅ 已添加，已FTP上传 |
| tools/sitemap.xml 加入 example-iq-challenge.html | ✅ 已添加（现29个URL），已FTP上传 |
| llms.txt 新增2条：Life Simulators文章 + IQ Challenge工具 | ✅ 已更新，已FTP上传 |
| IndexNow 推送 4 个 URL | ✅ 推送成功：life-simulator-legendary-decisions, example-iq-challenge.html, sitemap.xml, llms.txt |
| GitHub 宝库挖掘 | ✅ 完成，见 github-opportunities.md |

### GitHub 挖掘报告
**文件：** `/Volumes/mg-ssd500/aifile/英文AI工具站/github-opportunities.md`

核心发现（100条，分10类）：
- **A区**：35个 Awesome List 外链机会（提 PR 即得外链）
- **B区**：5个中国开发者社区（提 Issue 比 PR 更简单）
- **C区**：5个非GitHub产品目录（BetaList/Altern/AlternativeTo等）
- **D区**：27个新工具创意（FSRS算法、Anki导出、更多模拟器人物…）
- **E-J区**：28个开源贡献/技术优化/社区/文章创意

**立即可做的（5分钟内）：**
1. XiaomingX/1000-chinese-independent-developer-plus → 开 Issue 中文提交（最简单）
2. iAmCorey/awesome-indie-hacker-tools → 找同行中国开发者联系
3. lappemic/awesome-ai-built-games → Life Simulators PR（完美匹配）

**新工具优先级建议：**
1. Anki 牌组导出功能（Mandarin Flashcards 加 .apkg 下载）
2. 认知偏差扩展版（IQ Challenge 从3题扩展到20题）
3. 甘地 / 林肯 Life Simulator

---

## 首页当前结构（2026-06-25 最终版）

脚本：`/tmp/update_homepage.py`（每次改首页都用这个，改完 `python3 /tmp/update_homepage.py` 推送）

| 区块 | 内容 | 背景色 |
|---|---|---|
| HERO | "I Bet 5 Years on AI. Watch It Happen." + 视频背景 | 深色 |
| WHAT | 30+ Articles / 20+ Free AI Tools + 统计栏 | #0b1120 深色 |
| TIMELINE | 5个里程碑节点（Jun16-21）+ 渐变连接线 | #0b1120 深色 |
| ARTICLES | Recently Published 5篇（最新排序） | #f0f4f8 浅色 |
| FEATURED_TOOLS | Life A4 横幅 + Major Vote + AQ Kids | #0f172a 深色 |
| FREE_TOOLS | Gaokao考题 + 3个工具卡片 | #0d141a 深色 |
| START_HERE | "An Ordinary Man Using AI to Change His Life" + 3张卡 | #f0f4f8 浅色 |
| WHO_I_AM | 个人故事 + 两张桌面照片 | #0f172a 深色 |

**Start Here 三张卡（2026-06-25 更新）：**
- s1：帕金森病（I Used AI to Research Parkinson's Disease…）
- s2：屋顶隔热（My Dad Said "Just Use the AC."…）
- s3：zhangxue（My Son Asked a Normal Question…）图片更好放尾位

---

## 2026-06-25 完成记录

### tools/index.html 全面重做
- 旧版：71个文件平铺，无分类
- 新版：5个分类 + 顶部粘性导航锚点直达
  - 🤖 AI Tools（9个）
  - 📈 Investing（8个）
  - 🀄 Learn Chinese（4个）
  - 🌱 Life Tools（2个）
  - 🎭 Life Simulators（11个）
- 暗色风格不变，卡片hover动效，响应式
- 文件：`/Volumes/mg-ssd500/aifile/英文AI工具站/ordinarymantrying.com/tools/index.html`
- FTP上传成功（见坑9）

### Post 330（张雪那篇）深度强化
URL: ordinarymantrying.com/my-son-asked-a-normal-question-i-tried-to-answer-it-with-ai-i-aimed-too-high-the-ai-wont-let-me-quit/

新增内容（按文章末尾顺序）：
1. **2006年采访视频** embed（YouTube: TAHbQ7KrHlY，18分钟原版）
2. **座右铭大字**："Chase your dreams. / Because I was brave, my life became extraordinary."（黄色高亮）
3. **张雪现状图**（zhangxue-now.png，Media ID: 545）+ Valentin Debise末圈逆转夺赛季第三冠
4. **模拟器大按钮** "Start the Simulator →"（蓝色渐变）
5. 删除了乱入的 Buffett/Grassroots 投资工具链接

情绪弧线：2006穷小子 → 座右铭 → 今日夺冠 → 你来试试 → Related Reading

### 坑9：FTP hostname 失效，改用 IP
- `ftp.ordinarymantrying.com` DNS 解析失败（[Errno 8]）
- 改用 IP 直连：`185.212.71.129`，用户名：`u730818097`
- 密码文件：`/Volumes/mg-ssd500/aifile/英文AI工具站/web-ftp-password.txt`

**Recently Published 5篇（已定稿）：**
- c1 大卡：Kids Quiz（Jun 23，最新）
- c2 大卡：Buffett Punch Card（Jun 22）
- c3：GitHub 外链（Jun 22）
- c4：WeChat vs Blog（Jun 21）
- c5：Major Vote（Jun 21）

### life-a4 工具 v4.0 上线（2026-06-25 凌晨）

**文件：** `ordinarymantrying.com/tools/life-a4/index.html`（82,624 bytes）

**三大新功能：**

1. **时间通货膨胀（Time Inflation）**
   - 工具栏新增"Calendar Time / Felt Time"切换按钮
   - Felt Time 模式：格子高度随年龄变化（0-20岁 16px，20-40岁 12px，40-50岁 10px，50-60岁 8px，60+岁 4px）
   - 直观感受"童年觉得很长，老来觉得很短"的时间体验
   - 模式切换调用 `setTimeMode('subjective'/'objective')`

2. **黑洞格子（Black Hole Squares）**
   - 点击任意已过去的灰色格子 → 标记为"被遗忘的月份"（黑色 + 🕳️）
   - 再次点击取消标记
   - 第5个统计数字实时显示"黑洞占比%"
   - 黑洞卡片（blackHoleCard）显示警告文字：≥30% 触发强烈警示
   - 数据持久化：localStorage `lifeA4_bh`

3. **概率云（Probability Cloud）**
   - 里程碑设置区增加"Confidence"下拉（Certain / ±1年 / ±2年 / ±3年 / ±5年 / Rough idea ±8年）
   - 置信范围内的格子用渐变色光晕显示（颜色强度随距离中心衰减）
   - 让用户看到"我大概在几岁结婚"而不是一个精确的点

**技术细节：**
- 所有新状态变量：`blackHoles=new Set()`, `timeMode='objective'`, `milestoneConf={}`
- `renderGrid()` 末尾自动调用 `applySubjectiveHeights()`（若处于subjective模式）
- `reveal()` 调用 `restoreBlackHoles()` + `updateBlackHoleStats()`
- 本地预览：`/Volumes/mg-ssd500/aifile/英文AI工具站/life-a4-preview.html`

---

## 下一步行动清单（更新至 2026-06-26，第二次）

---

### ✅ FTP上传完成（2026-06-26）

14个文件已通过 Python ftplib 直接上传到 `/domains/ordinarymantrying.com/public_html/tools/`，无需hPanel。

- `major-vote-cn.html`（PK血条）
- `major-vote.html`（英文PK血条）
- `shuangseqiu-generator.html`（新工具）
- `value-investing-calculator.html`、`10x-stock-screener.html`、`sell-signal-checklist.html`、`investment-punch-card.html`（投资内循环）
- `life-a4/index.html`、`life-clock/index.html`、`life-paper/index.html`（Life三部曲内循环）
- `mandarin-flashcards.html`、`pinyin-annotator.html`、`chinese-reading-lab.html`、`chengyu-stories.html`（中文学习链）

---

### ⏳ 等待外部事件

| 事项 | 触发条件 | 动作 |
|---|---|---|
| 文章17发布 | Hostinger联盟审批通过 | 替换 `YOUR_HOSTINGER_AFFILIATE_LINK_HERE` → 发布 |
| AdSense申请 | 等到 2026-08 初 | 申请 AdSense，44篇文章已达内容量 |
| 世界杯Part 3 | 准决赛开踢 | 复用Part 1/2框架再做预测实验 |

---

### 📋 可选下一步（Claude可以帮做）

1. **博客文章内链**：每篇已发布文章末尾加"Related Tools"区块，指向对应工具（如文章12末尾加Supermarket Test链接）
2. **X.com 社交账号**：首页和footer加 @TuanVan66095Get 链接（WordPress theme social settings）
3. **Awesome List PR**：按 github-opportunities.md 的"极高优先级"逐条提交
4. **Amazon Associates申请**：低门槛，工具27（家教文章）已有Amazon链接占位符 `[YOUR AMAZON AFFILIATE LINK HERE]`
5. **LiteSpeed 性能优化**：WPCode 加两个代码片段（font-display:swap + JS defer），手机端从74→85+
6. **life-clock 添加生命三部曲入口**：在 Life Clock 顶部加 A4/Paper/Clock 三个工具横向导航标签

---

### ✅ 本轮已完成（2026-06-26）

**文章（19篇）：**
- 写了 15 篇新工具配套文章（articles/37-51）
- 更新4篇旧草稿标题（26-29，加Note说明）
- 全部推送并发布（Post 597–615）
- 批量去掉所有 (AI Generated) 标题标签
- 4篇模拟器文章（597/599/600/615）开头加了 Note 说明

**工具内循环网络（11个文件）：**
- 投资工具链（5个节点闭环）：Supermarket→10×→ValueCalc→PunchCard→Supermarket
- Life三部曲（A4→Clock→Paper→Simulators）
- 中文学习链闭环（Flashcards→Pinyin→ReadingLab→Chengyu→Flashcards）

**变现：**
- 文章17改写为 Hostinger vs Bluehost 对比文章
- Bluehost联盟链接已嵌入：`https://bluehost.sjv.io/c/7436386/1376228/11352`

**中文工具：**
- major-vote-cn.html PK 血条设计完成（HTML/CSS/JS 对齐英文版）

### life-paper（900 Squares）v5.0 上线（2026-06-25）

**URL：** `ordinarymantrying.com/tools/life-paper/`（67,589 bytes）

**核心定位：零隐私 · 全通用 · 强冲击** — 不输入任何个人数据，7个视角看人类共同的命运。

**7个模式：**
1. **📖 Famous Lives（英雄功能）** — 10位名人的完整A4纸，含褚时健/姜子牙/摩西奶奶/山德士/摩西/刘邦/王德顺/J.K.罗琳/任正非/乔布斯，每人有事件时间线+扎心金句+最后一击文字。内置"年龄对比器"：输入你的年龄，自动生成"褚时健X岁的时候，他的褚橙时刻还在前面"的个性化文字。
2. **🎲 Random Life** — 骰子摇出随机人生，看别人的纸，认出自己的影子
3. **🌍 Generation** — 80后/90后/00后平均A4纸，输入年龄看你在哪里
4. **🎭 Role Swap** — 父母年轻时/未来孩子/职场强人/ICU护士，4个视角
5. **⚖️ Life Exchange** — 选择人生套餐（996/躺平/孝子/丁克等），格子实时变化
6. **🕯️ Memorial** — 集体悼念墙，每个年龄段的人类共同感受（10万人说了什么）
7. **🎰 Fate Machine** — 命运老虎机，3个滚轮：年代×家庭背景×人生事件

**配色：** 琥珀金/烛光（与 life-a4 靛蓝、life-clock 熔岩红完全不同）

**tools/index.html 同步更新：** Life Tools 区块从2个增至5个，三工具都有入口

---

## 2026-06-26 完成记录（第十五次）

### careers-cn 批量更新 + FTP 上传

**改动内容（262个页面）：**
- 每个职业详情页末尾加入「报考需求问卷」蓝色推广块，引流至 `/tools/cn/baokao/gaokao-choice-questionnaire.html`
- footer 新增问卷链接
- 部分专业名称修正（如"数学与物理学基础" → "数理基础科学"）

**新增上传：**
- `cn/baokao/gaokao-choice-questionnaire.html`（28.7K）——首次上传服务器

**FTP 结果：** 262 + 1 文件全部成功，0 失败

---

### GitHub 外链推广进度（2026-06-26）

**今日新增：**
- `XiaomingX/1000-chinese-independent-developer-plus` Issue #69（中文提交，最快见效）

**已积累的待审 PR（8个仓库）：**

| 仓库 | PR | 内容 | Stars |
|---|---|---|---|
| mezod/awesome-indie | #170 | 博客 Building in Public | **11,498** |
| yrgo/awesome-educational-games | #26, #27 | Mandarin Flashcards + Simulators | 1,129 |
| iAmCorey/awesome-indie-hacker-tools | — | 未提（格式不匹配） | 1,372 |
| lappemic/awesome-ai-built-games | #32 | Life Simulators | 28 |
| thomashirtz/awesome-chinese-learning | #6, #7 | 中文学习工具 | 70 |
| learner-long-life/awesome-value-investing | #3 | Buffett 工具 | 8 |
| davidpelayo/awesome-parenting | #4 | AQ Kids | 53 |
| AdrienLemaire/awesome-mental-models | #7 | IQ Challenge | 157 |
| maehr/awesome-digital-history | #354 | Life Simulators（CI报错但非我们问题） | — |

**优先级说明：** mezod/awesome-indie PR #170 影响最大（11k stars），其次 yrgo（1.1k stars）。CI 报错的 maehr 那个等人工审核即可，不用管。

---

### 下一步等待清单（更新）

| 事项 | 触发条件 | 动作 |
|---|---|---|
| 文章17发布 | Hostinger联盟审批通过 | 替换 `YOUR_HOSTINGER_AFFILIATE_LINK_HERE` → 发布 |
| AdSense申请 | 等到 2026-08 初（44篇已达量） | 申请 AdSense |
| 世界杯Part 3 | 准决赛开踢 | 复用Part 1/2框架再做预测实验 |
| Awesome List PR 合并 | 等各仓库 maintainer 审核 | 合并后带来 DoFollow 外链 |

---

## 旧项目处置记录（不是重点，了解即可）

**重点永远是 ordinarymantrying.com（英文站），以下旧项目不再投入精力。**

### rolluppiano.net（手卷钢琴，已关闭）
- 曾是C2C电子钢琴销售站，Wix建站$276，Fiverr视频$50，Facebook广告$100，卖出几个后疫情停了
- 域名已到期未续，Wix站已关闭
- 内容已迁移：Post 574 https://ordinarymantrying.com/roll-up-piano-beginner-zero-experience/
  - 嵌入了YouTube Shorts演示视频（https://www.youtube.com/shorts/9uO-0tsMCFY）
  - 嵌入了Fiverr专业视频（YouTube: uItxQLMtZuI）
  - 含Amazon联盟链接（amzn.to/4gFa13A，base64加密）
- 实物库存仍在家中，留1个拍内容，其余可eBay/FB Marketplace处置
- **不需要续域名，不需要重建站**

### zfuye.org（副业资源站，已停更）
- 中文副业内容站，1502篇文章（绝大多数"网上收集"搬运，非原创），WordPress + DUX主题
- 香港小主机（慢），无Google Analytics，流量未知但估计极低
- 已在 gheader 侧边栏添加 block-35 Widget，指向 ordinarymantrying.com/tools/（CDN延迟，次日生效）
- 不续费、不维护，让它自然吸引一点点同类受众导流过来
- 若想出售：闲鱼挂¥200-300，标注1502篇内容+WordPress+副业赛道
- **不需要再投入时间**

---

*最后更新：2026-06-26（第十五次），Claude Sonnet 4.6 整理*
