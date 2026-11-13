# site.json を作る（2026-11-13 新規サイト「はじめてのインスタ集客」）。見た目や順番を変えたい時はこれを直して再実行する。
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
steps = [("instagram-hajimekata", "アカウントを作る", "登録と最初の設定"),
         ("profile-kakikata", "プロフィールを書く", "名前・自己紹介・リンク"),
         ("pro-account-kirikae", "プロアカウントにする", "無料で数字が見える"),
         ("toukou-shurui-chigai", "投稿の種類を知る", "フィード・ストーリーズ・リール"),
         ("hajimete-toukou", "はじめて投稿する", "写真・文章・タグ付け"),
         ("hashtag-tsukekata", "ハッシュタグを付ける", "見つけてもらう入り口"),
         ("reel-tsukurikata", "リールを作る", "新しい人に届く動画"),
         ("story-tsukaikata", "ストーリーズで話す", "フォロワーと仲良くなる"),
         ("insight-mikata", "数字を見る", "インサイトで振り返る"),
         ("shukyaku-junban", "集客の順番を固める", "お店・サービスにつなげる")]
order = [s for s, _, _ in steps]
names = [t for _, t, _ in steps]
road = "".join('<li><a href="articles/%s.html"><span class="ig-n">%d</span><span class="ig-t"><b>%s</b><small>%s</small></span></a></li>' % (s, i + 1, t, d) for i, (s, t, d) in enumerate(steps))
rings = "".join('<a class="ig-ring" href="articles/%s.html"><span>%d</span><small>%s</small></a>' % (s, i + 1, t) for i, (s, t, d) in enumerate(steps))
hero = ('<section class="ig-hero">\n<p class="ig-eyebrow">はじめてのインスタ集客</p>\n'
        '<h1 class="ig-h1">インスタは、<br><em>順番どおり</em>なら迷わない。</h1>\n'
        '<p class="ig-lead">アカウント作りから、お店やサービスにお客さんが来るまで。やることを10のステップに並べました。上から順に読むだけで、今日やることが分かります。</p>\n'
        '<div class="ig-rings" aria-label="10のステップ">' + rings + '</div>\n'
        '<ol class="ig-road">' + road + '</ol>\n'
        '<p class="ig-count">いま読める記事：{N_ARTICLES}本 ・ <a href="articles/otehon-account.html">番外編：お手本アカウント11選を見る</a></p>\n</section>'
        '<script>(function(){try{var rd=JSON.parse(localStorage.getItem("ig-read")||"[]")}catch(e){return}'
        'document.querySelectorAll(".ig-road a,.ig-ring").forEach(function(a){var s=a.getAttribute("href").split("/").pop().replace(".html","");'
        'if(rd.indexOf(s)>=0)(a.closest("li")||a).classList.add("seen")})})()</script>')

css = r'''
/* theme: story-gradient */
:root{--grad:linear-gradient(45deg,#f59f00,#e8590c 30%,#d6336c 55%,#ae3ec9 80%,#7048e8);--pk:#c2255c}
@media (prefers-color-scheme:dark){:root{--pk:#f783ac}}
body{font-family:"M PLUS Rounded 1c","Hiragino Sans","Noto Sans JP",sans-serif}
.logo span{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
header{border-bottom:0}
header:after{content:"";display:block;height:3px;background:var(--grad)}
.gnav a:hover,.gnav a.on{background:var(--grad);color:#fff}
.tag{background:var(--grad)}
article h2{border-left:0;position:relative;padding-left:22px}
article h2:before{content:"";position:absolute;left:0;top:0;bottom:0;width:6px;border-radius:4px 0 0 4px;background:var(--grad)}
.card{border-radius:18px}.thumb{border-radius:18px 18px 0 0}
.next{border-color:var(--pk)}
/* hero-base: */
.ig-hero{text-align:center;padding:26px 0 6px}
.ig-eyebrow{display:inline-block;font-size:13px;font-weight:800;letter-spacing:.08em;margin:0 0 10px;padding:3px 14px;border-radius:99px;color:#fff;background:var(--grad)}
.ig-h1{font-size:clamp(26px,5vw,38px);line-height:1.4;margin:0 0 12px}
.ig-h1 em{font-style:normal;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.ig-lead{max-width:640px;margin:0 auto 18px;color:var(--muted);font-size:15px}
.ig-rings{display:flex;gap:12px;overflow-x:auto;padding:8px 6px 12px;scrollbar-width:none}
.ig-rings::-webkit-scrollbar{display:none}
.ig-ring{flex:0 0 auto;width:76px;text-decoration:none;color:var(--fg);font-size:11px;line-height:1.35;position:relative;z-index:0}
.ig-ring span{display:flex;align-items:center;justify-content:center;width:62px;height:62px;margin:5px auto 6px;border-radius:50%;font-weight:900;font-size:22px;background:var(--card);border:3px solid var(--bg);position:relative;transition:transform .2s}
.ig-ring span:before{content:"";position:absolute;inset:-7px;border-radius:50%;background:var(--grad);z-index:-1}
.ig-ring:hover span{transform:scale(1.06)}
.ig-ring.seen span:before{background:var(--line)}
.ig-ring small{display:block}
.ig-road{list-style:none;padding:0;margin:8px auto 0;max-width:640px;text-align:left;position:relative}
.ig-road:before{content:"";position:absolute;left:21px;top:20px;bottom:20px;width:3px;border-radius:3px;background:var(--grad)}
.ig-road li{margin:0 0 10px;position:relative}
.ig-road a{display:flex;gap:14px;align-items:center;text-decoration:none;color:var(--fg);background:var(--card);border:1px solid var(--line);border-radius:16px;padding:10px 14px 10px 6px;transition:transform .15s,border-color .15s}
.ig-road a:hover{transform:translateX(4px);border-color:var(--pk)}
.ig-n{flex:0 0 32px;height:32px;border-radius:50%;background:var(--grad);color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center;position:relative;z-index:1}
.ig-t b{display:block;font-size:16px}.ig-t small{color:var(--muted);font-size:13px}
.ig-road li.seen .ig-n{background:var(--muted)}
.ig-road li.seen a:after{content:"読んだ";margin-left:auto;font-size:11px;color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:0 8px;white-space:nowrap}
.ig-count{font-size:13px;color:var(--muted);margin:10px 0 0}
/* article-base: */
.sec-img{margin:6px 0 18px;padding:0}
.sec-img img{display:block;width:100%;height:auto;aspect-ratio:1024/572;object-fit:cover;border-radius:18px;border:1px solid var(--line);background:var(--card)}
.ig-bar{position:fixed;left:0;top:0;height:4px;width:0;background:var(--grad);z-index:50}
.ig-step{display:inline-block;margin-left:8px;font-size:12px;font-weight:800;color:var(--pk);border:1.5px solid var(--pk);border-radius:99px;padding:0 10px;vertical-align:3px}
.ig-nav{display:flex;gap:10px;flex-wrap:wrap;margin:26px 0 6px}
.ig-nav a{flex:1 1 220px;text-decoration:none;color:var(--fg);background:var(--card);border:1px solid var(--line);border-radius:16px;padding:12px 16px;font-size:14px}
.ig-nav a small{display:block;color:var(--muted);font-size:12px}
.ig-nav a.nx{border:2px solid var(--pk)}
.ig-nav a.nx b:after{content:" →"}
.toc li.on>a{font-weight:800;color:var(--pk)}
/* category-base: */
.cx-head{text-align:center;padding:10px 0 4px}
.cx-eye{display:inline-block;font-size:12px;font-weight:800;color:#fff;background:var(--grad);border-radius:99px;padding:2px 12px}
.cx-head h1{font-size:26px;margin:10px 0 6px}.cx-head p{color:var(--muted);margin:0 0 6px;font-size:14px}
.cx-others{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:10px 0}
.cx-others a{font-size:13px;text-decoration:none;color:var(--fg);background:var(--soft);border-radius:99px;padding:4px 12px}
.cx-others small{margin-left:6px;color:var(--muted)}
'''

article_js = r'''<script>(function(O,N){
var slug=location.pathname.split("/").pop().replace(".html",""),i=O.indexOf(slug);
try{var rd=JSON.parse(localStorage.getItem("ig-read")||"[]");if(rd.indexOf(slug)<0){rd.push(slug);localStorage.setItem("ig-read",JSON.stringify(rd))}}catch(e){}
var bar=document.createElement("div");bar.className="ig-bar";document.body.appendChild(bar);
addEventListener("scroll",function(){var h=document.documentElement;bar.style.width=Math.min(100,100*h.scrollTop/((h.scrollHeight-h.clientHeight)||1))+"%"},{passive:true});
var hs=[].slice.call(document.querySelectorAll("article h2[id]")),ls=[].slice.call(document.querySelectorAll(".toc li"));
if(hs.length&&ls.length)addEventListener("scroll",function(){var k=-1;hs.forEach(function(h,j){if(h.getBoundingClientRect().top<120)k=j});ls.forEach(function(l,j){l.classList.toggle("on",j===k)})},{passive:true});
if(i<0)return;var h1=document.querySelector("article h1");if(h1){var s=document.createElement("span");s.className="ig-step";s.textContent="STEP "+(i+1)+" / "+O.length;h1.appendChild(s)}
var nv=document.createElement("div");nv.className="ig-nav";var x="";
if(i>0)x+='<a href="'+O[i-1]+'.html"><small>前のSTEP '+i+'</small><b>'+N[i-1]+'</b></a>';
if(i<O.length-1)x+='<a class="nx" href="'+O[i+1]+'.html"><small>次のSTEP '+(i+2)+'</small><b>'+N[i+1]+'</b></a>';
else x+='<a class="nx" href="../index.html"><small>10のステップ</small><b>はじめから見直す</b></a>';
nv.innerHTML=x;var nx=document.querySelector(".next");if(nx)nx.parentNode.insertBefore(nv,nx);
})(__O__,__N__)</script>'''.replace("__O__", json.dumps(order)).replace("__N__", json.dumps(names, ensure_ascii=False))

site = {
    "logo_html": "はじめての<span>インスタ集客</span>",
    "colors": {"ACCENT_L": "#c2255c", "ACCENT2_L": "#6741d9", "ACCENT_D": "#f783ac", "ACCENT2_D": "#b197fc"},
    "hero_title": "インスタは、順番どおりなら迷わない。",
    "hero_text": "アカウント作りから集客まで、やることを10のステップに並べました。",
    "home_description": "Instagram（インスタ）の使い方と集客のやり方を、はじめての人向けに10のステップで順番に解説。アカウント作成、プロフィール、プロアカウント、投稿、ハッシュタグ、リール、ストーリーズ、インサイト、集客の流れまで、公式ヘルプで確かめた情報で紹介します。",
    "home_picks_title": "", "picks_title_short": "", "picks_title_long": "",
    "about_html": "<p>数ある情報の中から、このサイトを見つけてくださり、ありがとうございます。</p>"
                  "<p>「はじめてのインスタ集客」は、Instagram（インスタ）をこれから始める人や、お店・サービスのお客さんを増やしたい人に向けて、使い方と集客のやり方を<strong>やる順番どおり</strong>に並べたサイトです。機能や数字は Instagram の公式ヘルプなどで確かめ、記事ごとに確認日を書いています。</p>"
                  "<p>このサイトは Instagram（Meta）の公式サイトではありません。個人が運営する非公式の解説サイトです。Instagram は Meta Platforms, Inc. の商標です。</p>"
                  "<p>アプリの画面や機能は、ときどき変わります。記事と画面が違う時は、公式ヘルプもあわせて見てみてください。</p>",
    "picks": {}, "default_picks": [],
    "category_slugs": {"はじめる": "start", "投稿する": "post", "集客する": "grow"},
    "og": {"line1": "はじめての", "line2": "インスタ集客", "sub": "10のステップで順番に", "rings": ["#f59f00", "#d6336c", "#ae3ec9", "#7048e8"], "style": "frame", "card_sub": "10のステップで順番に"},
    "images": {"motif": "rings", "bg": "#2a0f24", "colors": ["#f59f00", "#e8590c", "#d6336c", "#ae3ec9", "#7048e8"], "header_image": "assets/header.jpg"},
    "header_ai": True,
    "profile_name": "まさび",
    "profile_html": "大手印刷会社で約20年、製造・品質管理・営業支援を担当したのち、グラフィックデザイナーとして独立。いまは広告・ブランド相談の会社を運営しながら、自分でもインスタやSNSで発信しています。はじめての人がつまずきやすいところを、順番どおりに分かりやすくお伝えします。",
    "next_step_html": "<p>最後まで読んでくださり、ありがとうございました。</p><p>まずは、この記事のステップを1つだけ、今日のうちにやってみませんか。5分でできることから始めると、次のステップが楽になります。</p><p>あなたのインスタで、いちばん届けたい相手はどんな人ですか？</p>",
    "refs": {"_label": "人気"},
    "featured": order[:5],
    "hero_html": hero,
    "extra_css": css,
    "font_import": '@import url("https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@500;700;800;900&display=swap");\n',
    "article_js": article_js,
    "category_head_html": '<header class="cx-head"><span class="cx-eye">PART {NO} ・ {N}本</span><h1>{CAT}</h1><p>{INTRO}</p><div class="cx-others">{OTHERS}</div></header>',
    "category_intros": {"はじめる": "アカウントを作って、プロフィールを整えて、プロアカウントにするまで。STEP 1〜3です。",
                        "投稿する": "投稿の種類、はじめての投稿、ハッシュタグ、リール。STEP 4〜7です。",
                        "集客する": "ストーリーズ、数字の見方、お店やサービスにつなげる順番。STEP 8〜10です。"},
    "category_order": ["はじめる", "投稿する", "集客する"],
    "vc_ads": [], "a8_ads": [],
}
json.dump(site, open(os.path.join(ROOT, "site.json"), "w"), ensure_ascii=False, indent=1)
json.dump({"amazon_tag": "", "rakuten_affiliate_id": "", "contact_url": "", "ga_measurement_id": "G-EHWF25C1RB",
           "site_url": "https://masabee1029.github.io/insta-10steps/", "site_name": "はじめてのインスタ集客"},
          open(os.path.join(ROOT, "config.json"), "w"), ensure_ascii=False, indent=1)
print("site.json written")
