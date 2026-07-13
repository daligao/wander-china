/* ---- Wander China — City Data File ---- */
/* All spot data is community-contributed. See CONTRIBUTING.md to add a city.
   Live demo with full data: https://ordinarymantrying.com/tools/wander-china/planner.html */

/* Spot schema:
   id       — snake_case, unique within city (also used as image filename: img/{city}/{id}.webp)
   nm       — English attraction name
   ic       — emoji icon
   cat      — landmark / culture / park / nature / history / food / shopping / entertainment
   dmin     — minimum visit duration (hours)
   dmax     — maximum visit duration (hours)
   pref     — 'day' / 'night' / 'both'
   cl       — closed day: 'Mon' / 'Tue' / ... / null
   hr       — hours string e.g. '09:00–17:00 (last entry 16:00)' — parsed by opening-hours filter
   price    — ticket price in ¥, integer (0 = free)
   pn       — human-readable price note e.g. '¥55 (students half)'
   metro    — metro directions e.g. 'Line 2, Wuyi Square Stn Exit 1'
   desc     — 2–3 sentence description from a local/foreigner perspective
   tip      — practical insider tip (must include at least one specific detail)

   tm field — NxN travel time matrix where N = spots.length
   tm[i][j] = [taxi_minutes, metro_minutes] from spot i to spot j
   Diagonal = [0,0]. See CONTRIBUTING.md for how to estimate this.
*/

const CITIES_DATA={
 changsha:{meta:{nm:'Changsha',nm_cn:'长沙',district:'Hunan · Star City',emoji:'🌶️'},
  spots:[
   {id:'orange_isle',nm:'Orange Isle',ic:'🍊',cat:'landmark',dmin:2,dmax:4,pref:'both',cl:null,
    hr:'07:00–22:00 (last entry 21:00)',price:0,pn:'Free (book 1–3 days ahead)',
    metro:'Line 2, Orange Isle Stn Exit 1/2',
    desc:'A 5km sandbar in the Xiang River crowned by a giant Mao Zedong sculpture. Golden hour here is the most iconic view in Changsha.',
    tip:'Reserve via WeChat 1–3 days ahead. Sightseeing train ¥40 round-trip saves the 1h walk. Best at sunset.'},
   /* Add more spots here — see CONTRIBUTING.md for full schema */
  ],
  tm:[
   [[0,0]] /* expand to NxN when you add more spots */
  ]},
 beijing:{meta:{nm:'Beijing',nm_cn:'北京',district:'The Northern Capital',emoji:'🏯'},spots:[],tm:[]},
 shanghai:{meta:{nm:'Shanghai',nm_cn:'上海',district:'Pearl of the Orient',emoji:'🌆'},spots:[],tm:[]},
 chengdu:{meta:{nm:'Chengdu',nm_cn:'成都',district:'Land of Abundance',emoji:'🐼'},spots:[],tm:[]},
 xian:{meta:{nm:"Xi'an",nm_cn:'西安',district:'The Eternal City',emoji:'⚔️'},spots:[],tm:[]},
 guangzhou:{meta:{nm:'Guangzhou',nm_cn:'广州',district:'City of Rams',emoji:'🍤'},spots:[],tm:[]},
 hangzhou:{meta:{nm:'Hangzhou',nm_cn:'杭州',district:'Paradise on Earth',emoji:'🍵'},spots:[],tm:[]},
 chongqing:{meta:{nm:'Chongqing',nm_cn:'重庆',district:'8D Magic Mountain City',emoji:'🌶️'},spots:[],tm:[]},
 kunming:{meta:{nm:'Kunming',nm_cn:'昆明',district:'Spring City',emoji:'🌸'},spots:[],tm:[]},
 harbin:{meta:{nm:'Harbin',nm_cn:'哈尔滨',district:'Ice City',emoji:'❄️'},spots:[],tm:[]},
 nanjing:{meta:{nm:'Nanjing',nm_cn:'南京',district:'Ancient Capital of Six Dynasties',emoji:'🦆'},spots:[],tm:[]},
 wuhan:{meta:{nm:'Wuhan',nm_cn:'武汉',district:'River City',emoji:'🌸'},spots:[],tm:[]},
 hohhot:{meta:{nm:'Hohhot',nm_cn:'呼和浩特',district:'Mongolian Heartland',emoji:'🐎'},spots:[],tm:[]},
 changchun:{meta:{nm:'Changchun',nm_cn:'长春',district:'Spring City of the North',emoji:'🌿'},spots:[],tm:[]},
 hefei:{meta:{nm:'Hefei',nm_cn:'合肥',district:'Green City of the East',emoji:'🌿'},spots:[],tm:[]},
 fuzhou:{meta:{nm:'Fuzhou',nm_cn:'福州',district:'Banyan City',emoji:'🌳'},spots:[],tm:[]},
 jinan:{meta:{nm:'Jinan',nm_cn:'济南',district:'City of Springs',emoji:'⛲'},spots:[],tm:[]},
 haikou:{meta:{nm:'Haikou',nm_cn:'海口',district:'Coconut City',emoji:'🌴'},spots:[],tm:[]},
 guiyang:{meta:{nm:'Guiyang',nm_cn:'贵阳',district:'Forest City',emoji:'🌲'},spots:[],tm:[]},
 lanzhou:{meta:{nm:'Lanzhou',nm_cn:'兰州',district:'Yellow River City',emoji:'🍜'},spots:[],tm:[]},
 nanchang:{meta:{nm:'Nanchang',nm_cn:'南昌',district:'The Hero City',emoji:'🦩'},spots:[],tm:[]},
 tianjin:{meta:{nm:'Tianjin',nm_cn:'天津',district:'The City of Concessions',emoji:'🎨'},spots:[],tm:[]},
 lhasa:{meta:{nm:'Lhasa',nm_cn:'拉萨',district:'Roof of the World',emoji:'🏔️'},spots:[],tm:[]},
 urumqi:{meta:{nm:'Urumqi',nm_cn:'乌鲁木齐',district:'The Heart of Asia',emoji:'🕌'},spots:[],tm:[]},
 shenyang:{meta:{nm:'Shenyang',nm_cn:'沈阳',district:'The Phoenix City',emoji:'🦅'},spots:[],tm:[]},
 zhengzhou:{meta:{nm:'Zhengzhou',nm_cn:'郑州',district:'Heart of China',emoji:'⚡'},spots:[],tm:[]},
 nanning:{meta:{nm:'Nanning',nm_cn:'南宁',district:'Green City',emoji:'🌿'},spots:[],tm:[]},
 xining:{meta:{nm:'Xining',nm_cn:'西宁',district:'Summer Capital',emoji:'🏔️'},spots:[],tm:[]},
 yinchuan:{meta:{nm:'Yinchuan',nm_cn:'银川',district:'Phoenix City of the West',emoji:'🦅'},spots:[],tm:[]},
 shijiazhuang:{meta:{nm:'Shijiazhuang',nm_cn:'石家庄',district:'Gateway to North China',emoji:'🌾'},spots:[],tm:[]},
 taiyuan:{meta:{nm:'Taiyuan',nm_cn:'太原',district:'Capital of Shanxi',emoji:'🏺'},spots:[],tm:[]},
};
