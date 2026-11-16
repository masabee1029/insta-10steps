# -*- coding: utf-8 -*-
"""図解（assets/zukai/*.html）を作る。記事には [[zukai:名前]] の1行で入る。
2026-11-16 本人依頼「基本の投稿の仕方を図解して」→「ほかにも足す」。
手順・数字は、それぞれの記事に書いてあることだけを絵にする（新しい事実を足さない）。
toukou.html は手書き（このファイルでは作らない）。
"""
import os, html
ROOT = os.path.dirname(os.path.abspath(__file__))
E = html.escape

# ---------- スマホ画面の部品（viewBox 0 0 120 200） ----------
def T(x, y, s, cls="t", w=None, anchor=None):
    fs = ""
    if w:
        size = min(9.0, (w - 6) / max(1, len(s)))
        fs = ' style="font-size:%.1fpx"' % size
    a = ' text-anchor="start"' if anchor == "start" else ""
    return '<text class="%s" x="%s" y="%s"%s%s>%s</text>' % (cls, x, y, fs, a, E(s))

def bars(x, y, ws, gap=10, h=5):
    return "".join('<rect class="s" x="%d" y="%d" width="%d" height="%d" rx="2"/>' % (x, y + i * gap, w, h) for i, w in enumerate(ws))

def grid(y, rows=2, hi=None):
    o = ""
    for r in range(rows):
        for c in range(3):
            o += '<rect class="p" x="%d" y="%d" width="30" height="30" rx="3"/>' % (12 + c * 33, y + r * 33)
    if hi is not None:
        r, c = divmod(hi, 3)
        o += '<rect class="sel" x="%d" y="%d" width="30" height="30" rx="3"/>' % (12 + c * 33, y + r * 33)
    return o

def navbar(hit=None):
    """下のボタンの並び。hit='plus' / 'search' で光らせる"""
    o = '<line class="ln" x1="0" y1="170" x2="120" y2="170"/>'
    xs = [20, 40, 60, 80, 100]
    for x in xs:
        if x == 60:
            o += '<text class="big%s" x="60" y="190">＋</text>' % ("" if hit == "plus" else " dim")
        elif x == 40:
            o += '<circle class="ic%s" cx="39" cy="183" r="4.5"/><line class="ic%s" x1="42.5" y1="186.5" x2="46" y2="190"/>' % (("", "") if hit == "search" else (" dim", " dim"))
        else:
            o += '<circle class="s" cx="%d" cy="185" r="5"/>' % x
    if hit == "plus":
        o += '<circle class="hit" cx="60" cy="185" r="12"/>'
    if hit == "search":
        o += '<circle class="hit" cx="41" cy="185" r="11"/>'
    return o

def pill(x, y, w, label, hit=True, h=18):
    o = '<rect class="%s" x="%d" y="%d" width="%d" height="%d" rx="%d"/>' % ("hit2" if hit else "pl", x, y, w, h, h // 2)
    return o + T(x + w / 2, y + h / 2 + 3.2, label, "t on" if hit else "t", w=w)

def topnext(label="次へ"):
    return pill(80, 8, 34, label)

def rows(y, labels, hit=None, h=22, gap=4):
    o = ""
    for i, s in enumerate(labels):
        yy = y + i * (h + gap)
        on = (i == hit)
        o += '<rect class="%s" x="8" y="%d" width="104" height="%d" rx="7"/>' % ("hit2" if on else "row", yy, h)
        o += T(15, yy + h / 2 + 3.2, s, "t l on" if on else "t l", w=96, anchor="start")
    return o

def field(y, label, val_w=60, hit=True):
    o = T(12, y - 4, label, "t l", w=100, anchor="start")
    o += '<rect class="%s" x="10" y="%d" width="100" height="20" rx="5"/>' % ("field" if hit else "row", y)
    o += '<rect class="s" x="16" y="%d" width="%d" height="5" rx="2"/>' % (y + 8, val_w)
    return o

def bigbtn(y, label, hit=True):
    o = '<rect class="go" x="10" y="%d" width="100" height="22" rx="8"/>' % y + T(60, y + 14.5, label, "t w", w=100)
    if hit:
        o += '<rect class="ring" x="6" y="%d" width="108" height="30" rx="11"/>' % (y - 4)
    return o

def keyboard():
    o = '<rect class="kb" x="0" y="124" width="120" height="76"/><g class="keys">'
    for r in range(2):
        for c in range(5):
            o += '<rect x="%d" y="%d" width="16" height="13" rx="2"/>' % (6 + c * 20, 131 + r * 18)
    return o + '<rect x="26" y="167" width="56" height="13" rx="2"/></g>'

def profile_head(hamb=False, edit=False):
    o = '<circle class="s" cx="28" cy="36" r="14"/>' + bars(50, 28, [52, 36])
    o += bars(12, 58, [80, 64, 72], gap=9)
    if edit:
        o += pill(10, 88, 100, "プロフィールを編集")
    else:
        o += '<rect class="row" x="10" y="88" width="100" height="16" rx="6"/>'
    if hamb:
        o += '<g class="ic"><line x1="99" y1="10" x2="111" y2="10"/><line x1="99" y1="14" x2="111" y2="14"/><line x1="99" y1="18" x2="111" y2="18"/></g><circle class="hit" cx="105" cy="14" r="9"/>'
    return o

def tabs(sel):
    labs = ["投稿", "ストーリーズ", "リール"]
    xs = [21, 63, 104]
    o = ""
    for i, (s, x) in enumerate(zip(labs, xs)):
        cls = ("t on" + (" sm" if len(s) > 3 else "")) if i == sel else "t sm"
        o += T(x, 179, s, cls)
    hx = {0: (6, 30), 1: (38, 50), 2: (90, 28)}[sel]
    o += '<rect class="hit2" x="%d" y="166" width="%d" height="20" rx="10"/>' % hx
    return o

def photo(x=12, y=24, w=96, h=110, sun=True):
    o = '<rect class="p" x="%d" y="%d" width="%d" height="%d" rx="4"/>' % (x, y, w, h)
    if sun:
        o += '<circle class="sun" cx="%d" cy="%d" r="10"/>' % (x + w * 0.7, y + h * 0.3)
        o += '<path class="hill" d="M%d %d l%d %d l%d %d l%d %d z"/>' % (x, y + h, w * 0.35, -h * 0.45, w * 0.3, h * 0.3, w * 0.35, h * 0.15)
    return o

def check(cx, cy):
    return '<circle class="chk" cx="%d" cy="%d" r="5"/>' % (cx, cy)

def phone(svg):
    return '<div class="zk-ph"><svg viewBox="0 0 120 200" aria-hidden="true">%s</svg></div>' % svg

def steps_fig(title, sub, frames, note=None, done=None):
    li = ""
    for i, (svg, cap) in enumerate(frames, 1):
        li += '<li>%s<p><span class="zk-n">%d</span>%s</p></li>' % (phone(svg), i, cap)
    if done:
        li += '<li class="zk-done">%s<p><span class="zk-n">✓</span>%s</p></li>' % (phone(done[0]), done[1])
    nt = note or "画面は分かりやすく描いた絵です。ボタンの位置や形は、アプリの新しさで少し変わることがあります。"
    return ('<figure class="zk" aria-label="図解：%s">\n<figcaption class="zk-h"><b>図解：%s</b><small>%s</small></figcaption>\n<ol class="zk-steps">\n%s\n</ol>\n<p class="zk-note">%s</p>\n</figure>\n'
            % (E(title), E(title), E(sub), li, E(nt)))

def b(s):
    """キャプションの「」の中を太字に"""
    import re
    return re.sub(r"「(.+?)」", r"<b>「\1」</b>", E(s))

SUB = "ピンクの枠のところを押します"

# ---------- 1. アカウントの作り方（STEP 1） ----------
def z_hajimekata():
    store = '<rect class="field" x="10" y="16" width="100" height="18" rx="9"/><circle class="ic" cx="20" cy="25" r="4"/>' + bars(28, 23, [50])
    f = [
        ('<rect class="hit2" x="34" y="60" width="52" height="52" rx="12"/><rect class="p" x="40" y="66" width="40" height="40" rx="9"/>' + bars(30, 124, [60, 44]) + '<g class="app"><rect x="14" y="150" width="22" height="22" rx="6"/><rect x="49" y="150" width="22" height="22" rx="6"/><rect x="84" y="150" width="22" height="22" rx="6"/></g>',
         "「App Store」か「Google Play」を開く"),
        (store + '<rect class="p" x="10" y="44" width="28" height="28" rx="7"/>' + bars(44, 50, [44, 30]) + pill(78, 50, 34, "入手") + '<rect class="p" x="10" y="84" width="100" height="70" rx="5"/>',
         "「Instagram」と検索して入れる"),
        ('<rect class="p" x="42" y="40" width="36" height="36" rx="9"/>' + bars(30, 92, [60]) + pill(10, 130, 100, "新しいアカウントを作成", h=22) + bars(34, 168, [52]),
         "「新しいアカウントを作成」を押す"),
        (field(30, "メールか電話番号") + keyboard() + pill(10, 66, 100, "次へ", hit=False, h=20), "メールアドレスか電話番号を入れる"),
        (field(30, "認証コード", 36) + '<g class="code"><rect x="14" y="62" width="14" height="18" rx="3"/><rect x="31" y="62" width="14" height="18" rx="3"/><rect x="48" y="62" width="14" height="18" rx="3"/><rect x="65" y="62" width="14" height="18" rx="3"/><rect x="82" y="62" width="14" height="18" rx="3"/></g>' + keyboard(), "届いた認証コードを入れる"),
        (field(30, "パスワード", 0) + '<g class="dots">' + "".join('<circle cx="%d" cy="40" r="2.5"/>' % (18 + i * 8) for i in range(8)) + '</g>' + keyboard(), "パスワードを決めて入れる"),
        ('<rect class="hit2" x="10" y="24" width="100" height="20" rx="5"/>' + bars(16, 32, [60]) + '<g class="wheel"><rect x="10" y="60" width="100" height="56" rx="6"/></g><rect class="pl" x="10" y="80" width="100" height="16" rx="4"/>' + bars(20, 68, [24, 24, 24], gap=17), "あなた自身の誕生日を入れる"),
        (field(30, "名前", 50) + keyboard(), "名前を入れる"),
        (field(30, "ユーザーネーム（@）", 44) + '<circle class="okc" cx="102" cy="40" r="5"/>' + keyboard(), "ユーザーネーム（@から始まるID）を決める"),
        (bars(12, 24, [96, 90, 96, 80, 92, 70], gap=11) + '<rect class="row" x="10" y="94" width="100" height="48" rx="5"/>' + bars(16, 102, [80, 70, 76], gap=11) + bigbtn(160, "同意する"), "利用規約などを確認して同意する"),
    ]
    done = (profile_head() + grid(112, 2), "自分のプロフィールができたら完成")
    return steps_fig("アカウントの作り方（10の手順）", SUB, [(s, b(c)) for s, c in f], done=done)

# ---------- 2. プロアカウントへの切り替え（STEP 3） ----------
def z_pro():
    f = [
        (profile_head() + grid(112, 2) + navbar() + '<circle class="hit" cx="100" cy="185" r="11"/>', "自分のプロフィール画面を開く"),
        (profile_head(hamb=True) + grid(112, 2), "右上のメニュー（三本線）を押す"),
        (rows(24, ["設定とアクティビティ", "アーカイブ", "QRコード", "保存済み"], hit=0), "「設定とアクティビティ」を押す"),
        (T(12, 30, "プロフェッショナル向け", "t l", anchor="start", w=100) + rows(38, ["アカウントの種類とツール", "", ""], hit=0) + bars(12, 130, [70, 50]), "「アカウントの種類とツール」を押す"),
        (rows(24, ["", ""]) + pill(10, 90, 100, "プロアカウントに切り替える", h=22), "「プロアカウントに切り替える」を押す"),
        (T(12, 22, "カテゴリ", "t l", anchor="start") + rows(30, ["カフェ", "美容室", "パン屋", "教室"], hit=0), "お店に合うカテゴリを選ぶ"),
        (topnext() + rows(40, ["ビジネス", "クリエイター"], hit=0, h=34, gap=10) + check(100, 57), "「ビジネス」か「クリエイター」を選んで「次へ」"),
    ]
    done = (profile_head() + '<rect class="new" x="10" y="108" width="100" height="16" rx="6"/>' + bars(20, 113, [80]) + grid(132, 1), "プロフィールにお店向けの機能が出たら完成")
    return steps_fig("プロアカウントへの切り替え方（7つの手順）", SUB, [(s, b(c)) for s, c in f], done=done,
                     note="切り替えは無料で、あとから個人アカウントに戻せます。画面は分かりやすく描いた絵です。ボタンの位置や名前は、アプリの新しさで少し変わることがあります。")

# ---------- 3. プロフィールの各部分（STEP 2） ----------
def z_profile():
    # 1枚の大きな画面に、番号つきの説明
    svg = ('<svg viewBox="0 0 300 250" aria-hidden="true" class="zk-big">'
           '<rect class="frame" x="70" y="6" width="160" height="238" rx="18"/>'
           '<circle class="s" cx="104" cy="44" r="18"/><circle class="hit" cx="104" cy="44" r="21"/>'
           '<rect class="s" x="132" y="34" width="56" height="7" rx="3"/><rect class="s" x="132" y="47" width="40" height="7" rx="3"/>'
           '<rect class="hit2" x="82" y="70" width="80" height="12" rx="4"/><rect class="s" x="86" y="73" width="54" height="6" rx="3"/>'
           '<rect class="hit2" x="82" y="86" width="136" height="38" rx="4"/>' + bars(86, 90, [120, 110, 100], gap=10, h=5) +
           '<rect class="hit2" x="82" y="128" width="92" height="12" rx="4"/><rect class="lk" x="86" y="131" width="60" height="6" rx="3"/>' +
           '<rect class="row" x="82" y="148" width="136" height="16" rx="6"/>' +
           "".join('<rect class="p" x="%d" y="%d" width="42" height="34" rx="3"/>' % (82 + c * 47, 172 + r * 37) for r in range(2) for c in range(3)) +
           '<g class="callout">'
           '<line x1="83" y1="44" x2="40" y2="30"/><circle cx="30" cy="30" r="10"/><text x="30" y="34">1</text>'
           '<line x1="82" y1="76" x2="40" y2="76"/><circle cx="30" cy="76" r="10"/><text x="30" y="80">2</text>'
           '<line x1="218" y1="105" x2="262" y2="105"/><circle cx="272" cy="105" r="10"/><text x="272" y="109">3</text>'
           '<line x1="82" y1="134" x2="40" y2="134"/><circle cx="30" cy="134" r="10"/><text x="30" y="138">4</text>'
           '<line x1="188" y1="40" x2="262" y2="40"/><circle cx="272" cy="40" r="10"/><text x="272" y="44">5</text>'
           '</g></svg>')
    items = [
        ("プロフィール写真", "丸く表示される。ひと目で見分けてもらう"),
        ("名前", "検索の対象になる。「何のお店か」が分かる言葉を入れる"),
        ("自己紹介", "150文字まで。誰の何のアカウントか・良さ・信頼できる理由・次にしてほしいこと"),
        ("リンク", "5つまで。予約・ホームページ・地図へつなぐ"),
        ("ユーザーネーム", "@から始まるID。ほかの人と同じものは使えない"),
    ]
    dl = "".join('<li><span class="zk-n">%d</span><b>%s</b>：%s</li>' % (i, E(a), E(c)) for i, (a, c) in enumerate(items, 1))
    return ('<figure class="zk" aria-label="図解：プロフィールの5つの欄">\n<figcaption class="zk-h"><b>図解：プロフィールの5つの欄</b><small>番号は下の説明と同じです</small></figcaption>\n'
            '<div class="zk-one">%s<ol class="zk-legend">%s</ol></div>\n<p class="zk-note">画面は分かりやすく描いた絵です。欄の並び方は、アプリの新しさで少し変わることがあります。</p>\n</figure>\n' % (svg, dl))

# ---------- 4. 投稿の種類（STEP 4） ----------
def z_shurui():
    def card(svg, name, what, life, reach, keep=True):
        return ('<li>%s<p><b>%s</b><br><small>%s</small></p><p class="zk-tags"><span class="%s">%s</span><span class="%s">%s</span></p></li>'
                % (phone(svg), E(name), E(what), "ok" if keep else "ng", E(life), "hot" if "以外" in reach else "", E(reach)))
    feed = profile_head() + grid(112, 2, hi=0)
    caro = '<rect class="p" x="12" y="30" width="96" height="110" rx="4"/><rect class="p" x="100" y="36" width="20" height="98" rx="4" opacity=".6"/><circle class="chk" cx="54" cy="150" r="3"/><circle class="s" cx="62" cy="150" r="3"/><circle class="s" cx="70" cy="150" r="3"/><path class="ic" d="M88 85 l8 0 m-3 -3 l3 3 l-3 3"/>'
    reel = '<rect class="p" x="0" y="0" width="120" height="200"/><circle class="playc" cx="60" cy="95" r="16"/><path class="play" d="M55 86 l13 9 l-13 9 z"/>' + bars(10, 160, [70, 50]) + '<circle class="s" cx="106" cy="120" r="5"/><circle class="s" cx="106" cy="138" r="5"/><circle class="s" cx="106" cy="156" r="5"/>'
    story = '<rect class="p" x="0" y="0" width="120" height="200"/><rect class="prog" x="6" y="6" width="108" height="3" rx="1.5"/><rect class="progon" x="6" y="6" width="60" height="3" rx="1.5"/><circle class="s" cx="14" cy="20" r="6"/><circle class="sun" cx="78" cy="70" r="12"/><rect class="sticker" x="30" y="120" width="60" height="26" rx="8"/>'
    hl = profile_head() + "".join('<circle class="hlc" cx="%d" cy="122" r="11"/>' % x for x in (24, 52, 80)) + grid(142, 1)
    li = "".join([
        card(feed, "フィード投稿", "写真や動画。プロフィールに並ぶ", "残る", "フォロワー"),
        card(caro, "カルーセル", "1つの投稿に何枚も入れる", "残る", "フォロワー"),
        card(reel, "リール", "縦長の短い動画", "残る", "フォロワー以外にも"),
        card(story, "ストーリーズ", "画面いっぱいの写真・動画", "24時間で消える", "フォロワー", keep=False),
        card(hl, "ハイライト", "ストーリーズをプロフィールに残す", "残る", "プロフィールを見た人"),
    ])
    return ('<figure class="zk zk-types" aria-label="図解：投稿の種類5つ">\n<figcaption class="zk-h"><b>図解：投稿の種類5つ</b><small>上が「残るか消えるか」、下が「主に届く相手」</small></figcaption>\n<ul class="zk-steps">%s</ul>\n'
            '<p class="zk-note">画面は分かりやすく描いた絵です。「フォロワー以外にも」届きやすいのは、リールだけです。</p>\n</figure>\n' % li)

# ---------- 5. タグの言葉の見つけ方（STEP 6） ----------
def z_hashtag():
    srch = '<rect class="field" x="10" y="14" width="100" height="18" rx="9"/><circle class="ic" cx="20" cy="23" r="4"/>'
    f = [
        (grid(20, 3) + navbar("search"), "下の虫めがねのマークを押す"),
        (srch + bars(28, 21, [40]) + '<line class="cur" x1="70" y1="18" x2="70" y2="28"/>' + keyboard(), "上の検索欄に言葉を入れる"),
        (srch + bars(28, 21, [40]) + rows(42, ["#　　　　　", "#　　　　", "#　　　　　　"], hit=1), "候補からお店に合うものを選ぶ"),
        ('<circle class="hash" cx="30" cy="34" r="16"/><text class="big" x="30" y="40">#</text>' + bars(54, 28, [50, 34]) + grid(66, 3, hi=4), "タグのページで、似たお店の投稿か見る"),
    ]
    return steps_fig("ハッシュタグの言葉の見つけ方（4つの手順）", SUB, [(s, b(c)) for s, c in f],
                     note="1つの投稿に付けられるハッシュタグは5個までです。画面は分かりやすく描いた絵です。")

# ---------- 6. ストーリーズの出し方（STEP 7） ----------
def z_story():
    f = [
        (grid(20, 3) + navbar("plus"), "画面の下の「＋」を押す"),
        ('<rect class="p" x="12" y="18" width="96" height="120" rx="4"/>' + tabs(1), "「ストーリーズ」を選ぶ"),
        ('<rect class="p" x="12" y="18" width="96" height="96" rx="4"/>' + grid(120, 1, hi=1) + '<circle class="shut" cx="60" cy="172" r="12"/>', "その場で撮るか、写真・動画を選ぶ"),
        ('<rect class="p" x="0" y="0" width="120" height="200"/><circle class="sun" cx="80" cy="60" r="12"/><rect class="hit2" x="94" y="10" width="20" height="20" rx="6"/><text class="t on" x="104" y="24">Aa</text><rect class="sticker" x="28" y="110" width="64" height="28" rx="8"/><rect class="hit2" x="24" y="106" width="72" height="36" rx="10"/>', "必要なら文字やスタンプを付ける"),
        ('<rect class="p" x="0" y="0" width="120" height="150"/>' + pill(6, 166, 52, "ストーリーズ") + pill(62, 166, 52, "親しい友達", hit=False), "「ストーリーズ」か「親しい友達」を選ぶ"),
    ]
    done = ('<circle class="ringg" cx="28" cy="36" r="17"/><circle class="s" cx="28" cy="36" r="13"/>' + bars(50, 28, [52, 36]) + bars(12, 60, [80, 64]) + grid(84, 3), "選んだほうでシェアすると、24時間見られる")
    return steps_fig("ストーリーズの出し方（6つの手順）", SUB, [(s, b(c)) for s, c in f], done=done)

# ---------- 7. リールの作り方（STEP 8） ----------
def z_reel():
    vid = '<rect class="p" x="0" y="0" width="120" height="200"/><circle class="playc" cx="60" cy="90" r="14"/><path class="play" d="M55 82 l12 8 l-12 8 z"/>'
    f = [
        (grid(20, 3) + navbar("plus"), "画面の下の「＋」を押す"),
        ('<rect class="p" x="12" y="18" width="96" height="120" rx="4"/>' + tabs(2), "「リール」を選ぶ"),
        (grid(20, 3, hi=3) + '<circle class="shut" cx="60" cy="172" r="12"/>', "その場で撮るか、動画を選ぶ"),
        (vid + '<rect class="kb" x="0" y="150" width="120" height="50"/><rect class="trim" x="10" y="160" width="100" height="24" rx="4"/><rect class="hit2" x="30" y="158" width="56" height="28" rx="5"/>', "必要なら動画を短く切る"),
        (vid + '<rect class="hit2" x="94" y="10" width="20" height="20" rx="6"/><text class="t on" x="104" y="24">Aa</text><rect class="tx" x="24" y="132" width="72" height="14" rx="4"/>', "必要なら文字を入れる"),
        (vid + '<rect class="hit2" x="10" y="160" width="100" height="22" rx="8"/><path class="ic" d="M20 176 v-10 l8 -2 v10"/><circle class="ic" cx="18" cy="176" r="2.5"/><circle class="ic" cx="26" cy="174" r="2.5"/>' + bars(36, 168, [56]), "必要なら音楽を付ける"),
        ('<rect class="p" x="34" y="20" width="52" height="92" rx="4"/><rect class="sel" x="34" y="20" width="52" height="92" rx="4"/>' + "".join('<rect class="p" x="%d" y="130" width="16" height="26" rx="2"/>' % (10 + i * 20) for i in range(5)) + '<rect class="sel" x="30" y="128" width="20" height="30" rx="3"/>', "カバー画像（表紙）を選ぶ"),
        ('<rect class="p" x="12" y="18" width="30" height="48" rx="3"/><rect class="field" x="48" y="18" width="62" height="48" rx="4"/>' + bars(53, 25, [48, 40, 30]) + keyboard(), "キャプション（説明文）を書く"),
        ('<rect class="p" x="12" y="18" width="30" height="48" rx="3"/>' + bars(48, 22, [56, 44]) + '<rect class="hit2" x="46" y="44" width="66" height="18" rx="5"/><text class="t on" x="79" y="56"># # # # #</text>' + rows(84, ["", ""]), "ハッシュタグを付ける（5個まで）"),
        ('<rect class="p" x="12" y="18" width="30" height="48" rx="3"/>' + bars(48, 22, [56, 44, 50]) + rows(84, ["", ""]) + bigbtn(164, "シェア"), "「シェア」を押すと投稿される"),
    ]
    return steps_fig("リールの作り方（10の手順）", SUB, [(s, b(c)) for s, c in f])

# ---------- 8. 集客の3つの段階（STEP 10） ----------
def z_junban():
    st = [
        ("知ってもらう", "「こんなお店があるんだ」", "リール・ハッシュタグ・発見タブ", "w1"),
        ("好きになってもらう", "「この人、いいな」「また見たい」", "フィード投稿・ストーリーズ・コメント", "w2"),
        ("行動してもらう", "「行ってみたい」「頼んでみたい」", "プロフィールのリンク・DM・予約ボタン", "w3"),
    ]
    li = "".join('<li class="%s"><span class="zk-n">%d</span><b>%s</b><q>%s</q><small>使う機能：%s</small></li>' % (c, i, E(a), E(q), E(f)) for i, (a, q, f, c) in enumerate(st, 1))
    return ('<figure class="zk" aria-label="図解：集客の3つの段階">\n<figcaption class="zk-h"><b>図解：集客の3つの段階</b><small>上から下へ、お客さんの気持ちが進みます</small></figcaption>\n'
            '<ol class="zk-funnel">%s</ol>\n<p class="zk-note">「何を投稿すればいい？」と迷った時は、お客さんがいまどの段階にいるかを考えると、次にやることが決まります。</p>\n</figure>\n' % li)

# ---------- 9. 月1回の振り返り（STEP 9） ----------
def z_insight():
    st = ["期間を「30日」にする", "「閲覧者」と「新規フォロワー」を見る", "閲覧者がいちばん多かった投稿を1つ選ぶ",
          "その投稿の「フォロワー以外」の割合を見る", "良かった理由を、1つだけ考える", "次の月は、その理由を取り入れて投稿"]
    li = "".join('<li><span class="zk-n">%d</span>%s</li>' % (i, b(s)) for i, s in enumerate(st, 1))
    return ('<figure class="zk" aria-label="図解：月1回の振り返り">\n<figcaption class="zk-h"><b>図解：月1回の振り返り（6つの手順）</b><small>6まで行ったら、次の月にまた1から</small></figcaption>\n'
            '<ol class="zk-cycle">%s</ol>\n<p class="zk-note">大切なのは、良かった理由を1つにしぼることです。いくつも一度に変えると、何が効いたのか分からなくなります。</p>\n</figure>\n' % li)

OUT = {
    "hajimekata": z_hajimekata, "pro": z_pro, "profile": z_profile, "shurui": z_shurui,
    "hashtag": z_hashtag, "story": z_story, "reel": z_reel, "junban": z_junban, "insight": z_insight,
}

if __name__ == "__main__":
    d = os.path.join(ROOT, "assets", "zukai"); os.makedirs(d, exist_ok=True)
    for k, fn in OUT.items():
        open(os.path.join(d, k + ".html"), "w", encoding="utf-8").write(fn())
    print("zukai:", ", ".join(OUT))
