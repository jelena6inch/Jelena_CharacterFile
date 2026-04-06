"""
Jelena Jhang — Character File Generator (Windows Version)
========================================
已經幫你修正字型路徑與下載字體！
輸出：Jelena_CharacterFile.png（A4 直式，150dpi）
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ══════════════════════════════════════════════
# 路徑設定 (已修正為 Windows 專門路徑)
# ══════════════════════════════════════════════

FONT_DIR  = "./canvas-fonts"          # 英文字型資料夾
SYS_CJK   = "C:/Windows/Fonts/msjh.ttc"   # 中文字型 (微軟正黑體)
SYS_CJKB  = "C:/Windows/Fonts/msjhbd.ttc" # 中文粗體 (微軟正黑體粗體)
CHAR_IMG  = "./character.png"         # 角色圖 (我已經幫你準備好了！)
OUTPUT    = "./Jelena_CharacterFile.png"

# 如果沒有粗體字型，就直接用普通體
if not os.path.exists(SYS_CJKB):
    SYS_CJKB = SYS_CJK

# ══════════════════════════════════════════════
# 字型載入
# ══════════════════════════════════════════════

def F(size, bold=False, cjk=False):
    """JetBrainsMono（等寬英文）或 Noto Sans CJK（中文）"""
    if cjk:
        path = SYS_CJKB if bold else SYS_CJK
    else:
        name = "JetBrainsMono-Bold.ttf" if bold else "JetBrainsMono-Regular.ttf"
        path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def FI(size):
    """InstrumentSans — 內文用無襯線字型"""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, "InstrumentSans-Regular.ttf"), size)
    except:
        return ImageFont.load_default()

def FY(size):
    """YoungSerif — 標題用襯線字型"""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, "YoungSerif-Regular.ttf"), size)
    except:
        return ImageFont.load_default()

def FC(size):
    """CrimsonPro Italic — 引言/斜體用"""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, "CrimsonPro-Italic.ttf"), size)
    except:
        return ImageFont.load_default()

# ══════════════════════════════════════════════
# 色票
# ══════════════════════════════════════════════

BG        = "#F0EDE8"   # 暖米白背景
NAVY      = "#1E3560"   # 深藍（主色）
NAVY2     = "#2D4A7A"   # 中藍（次色）
GOLD      = "#C4973A"   # 金色（強調）
GOLD_L    = "#E8D4A0"   # 淺金（頭像框）
LIGHT_BG  = "#E8EDF5"   # 淺藍灰（能力條底色）
DIVIDER   = "#D0C8BE"   # 分隔線
WARM_G    = "#8A8070"   # 暖灰（副文字）
TEXT_D    = "#2C2825"   # 深棕（主文字）
TEXT_M    = "#4A4540"   # 中棕（內文）
TEXT_S    = "#6A6258"   # 淺棕（備註）
WHITE     = "#FFFFFF"

# ══════════════════════════════════════════════
# 畫布設定（A4 直式 @ 150dpi）
# ══════════════════════════════════════════════

W, H = 1240, 1754
img = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(img)

# ══════════════════════════════════════════════
# 工具函式
# ══════════════════════════════════════════════

def draw_wrapped(text, x, y, max_w, font, color=TEXT_M, lh=None):
    """自動換行繪製文字，回傳最終 y 座標"""
    words = []
    # 支援中文換行 (每個字都視為一個單元)
    for char in text:
        words.append(char)
        
    lines, cur = [], ""
    for w in words:
        t = (cur + w).strip()
        if d.textbbox((0, 0), t, font=font)[2] <= max_w:
            cur = cur + w
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
        
    _lh = lh or (d.textbbox((0, 0), "A", font=font)[3] + 8)
    for line in lines:
        d.text((x, y), line, font=font, fill=color)
        y += _lh
    return y

def section_title(x, y, title, col_w):
    """區塊標題：金色文字 + 深藍底線"""
    d.text((x, y), title, font=F(22, bold=True), fill=GOLD)
    d.rectangle([(x, y + 28), (x + col_w, y + 30)], fill=NAVY2)
    return y + 36

# ══════════════════════════════════════════════
# 背景細節
# ══════════════════════════════════════════════

# 細格紋
for gy in range(0, H, 36):
    d.line([(0, gy), (W, gy)], fill="#E8E4DC", width=1)
for gx in range(0, W, 36):
    d.line([(gx, 0), (gx, H)], fill="#ECE8E2", width=1)

# 外框：深藍粗框 + 金色細框
d.rectangle([(18, 18), (W - 18, H - 18)], outline=NAVY, width=3)
d.rectangle([(24, 24), (W - 24, H - 24)], outline=GOLD, width=1)

# 四角金點
for cx, cy in [(24, 24), (W - 24, 24), (24, H - 24), (W - 24, H - 24)]:
    d.ellipse([(cx - 5, cy - 5), (cx + 5, cy + 5)], fill=GOLD)

# ══════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════

d.rectangle([(18, 18), (W - 18, 148)], fill=NAVY)
d.rectangle([(18, 146), (W - 18, 150)], fill=GOLD)

d.text((48, 28),  "CHARACTER  FILE  —  No. 001", font=F(22),       fill="#7A99CC")
d.text((48, 56),  "Jelena Jhang",                font=FY(64),      fill=WHITE)
d.text((48, 124), "用語言理解世界，用工具讓工作更好。",               font=F(20, cjk=True), fill="#AABBD0")

# Keywords（右側標籤）
kws = ["Logistics", "Japanese", "AI Tools"]
kx = W - 48
for kw in reversed(kws):
    bb  = d.textbbox((0, 0), kw, font=F(20))
    kw_w = bb[2] - bb[0] + 20
    kx  -= kw_w
    # 使用半透明模擬色塊
    d.rectangle([(kx, 28), (kx + kw_w, 56)], fill="#335588")
    d.rectangle([(kx, 28), (kx + kw_w, 56)], outline="#5577AA", width=1)
    d.text((kx + 10, 32), kw, font=F(20), fill="#AABBD0")
    kx -= 10

# ══════════════════════════════════════════════
# 版面參數
# ══════════════════════════════════════════════

LX    = 40     # 左欄 x 起點
RX    = 520    # 右欄 x 起點
CW_L  = 460    # 左欄寬
CW_R  = W - RX - 40   # 右欄寬
START_Y = 168  # 內容起始 y

# ══════════════════════════════════════════════
# 左欄：頭像 + PROFILE + ABILITY STATS
# ══════════════════════════════════════════════

Y = START_Y

# ── 角色圖 ──
if os.path.exists(CHAR_IMG):
    char = Image.open(CHAR_IMG).convert("RGBA")
    # 如果已經是單張頭像，則調整大小即可
    ph     = 320
    pw     = int(char.size[0] * ph / char.size[1])
    char_r = char.resize((pw, ph), Image.LANCZOS)
    
    # 頭像框
    d.rectangle([(LX - 3, Y - 3), (LX + pw + 3, Y + ph + 3)], fill=NAVY)
    d.rectangle([(LX - 1, Y - 1), (LX + pw + 1, Y + ph + 1)], fill=GOLD_L)
    img.paste(char_r, (LX, Y), char_r)
    pw_final = pw
else:
    pw_final = 240 # 預留寬度

# 姓名資訊
NX = LX + pw_final + 16
d.text((NX, Y + 10),  "張  姵  涵",         font=FY(38), fill=NAVY)
d.text((NX, Y + 56),  "Logistics",          font=F(22, bold=True), fill=GOLD)
d.text((NX, Y + 84),  "Coordinator",        font=F(22, bold=True), fill=GOLD)
d.text((NX, Y + 120), "Taichung, Taiwan",   font=FI(20), fill=WARM_G)
d.text((NX, Y + 148), "JLPT N1  ★  2025",  font=F(20),  fill=NAVY2)

Y_after_portrait = Y + 320 + 20

# ── PROFILE ──
Y2 = section_title(LX, Y_after_portrait, "PROFILE", CW_L)

profile_items = [
    ("Role",  "物流業務助理（在職 3 年）"),
    ("Lang",  "中文 / 日文 N1 / English"),
    ("Study", "福岡短期交換研修"),
    ("Tools", "LINE Bot / AI辨識 / GAS"),
    ("Type",  "細心・溫柔・負責・耐心"),
]
for key, val in profile_items:
    d.text((LX,      Y2), key, font=F(20, bold=True),       fill=GOLD)
    d.text((LX + 68, Y2), val, font=F(20, cjk=True),        fill=TEXT_D)
    Y2 += 36

Y2 += 12

# ── ABILITY STATS ──
Y2 = section_title(LX, Y2, "ABILITY STATS", CW_L)

stats = [
    ("日語能力", "S",  "#C4973A", 0.96, "JLPT N1・福岡研修・日商書信"),
    ("物流實務", "A",  "#2D6A4A", 0.85, "訂單庫存交期協調 3yr+"),
    ("客戶溝通", "A",  "#2D4A7A", 0.90, "三語往來・細心溝通"),
    ("文件整理", "A",  "#5A3A7A", 0.88, "跨語言文件・帳單追蹤"),
    ("解決問題", "A+", "#8A2A2A", 0.92, "自製 3 個數位工具"),
]
BW = CW_L - 8  # 能力條總寬

for lbl, grade, gcol, val, note in stats:
    d.text((LX, Y2), lbl, font=F(20, cjk=True, bold=True), fill=TEXT_D)
    bb = d.textbbox((0, 0), grade, font=F(18, bold=True))
    gw = bb[2] - bb[0] + 16
    d.rectangle([(LX + CW_L - gw, Y2 - 1), (LX + CW_L, Y2 + 23)], fill=gcol)
    d.text((LX + CW_L - gw + 8, Y2 + 1), grade, font=F(18, bold=True), fill=WHITE)
    Y2 += 28
    d.rectangle([(LX, Y2), (LX + BW, Y2 + 10)], fill=LIGHT_BG)
    d.rectangle([(LX, Y2), (LX + int(BW * val) - 8, Y2 + 10)], fill=NAVY2)
    d.rectangle([(LX + int(BW * val) - 8, Y2), (LX + int(BW * val), Y2 + 10)], fill=gcol)
    Y2 += 14
    d.text((LX, Y2), note, font=F(17, cjk=True), fill=TEXT_S)
    Y2 += 30

# ══════════════════════════════════════════════
# 右欄：BACKSTORY + SPECIAL ABILITY + FUTURE QUEST
# ══════════════════════════════════════════════

RY = START_Y

# ── BACKSTORY ──
RY = section_title(RX, RY, "BACKSTORY", CW_R)

backstory_paras = [
    "她的日文不是為了考試而學的。大學三年級，因為喜歡日劇和動漫，開始一句一句地拆解這個語言。靠自學打底，畢業前取得 N2，赴日本福岡短期交換研修一個月，在全日文環境中獨立生活、上課、溝通——語感在那段時間變得更自然、更直覺。",
    "進入職場後，日文成了工作裡真實的工具：承接日本廠商的詢報價、交期確認、異常說明等書信往來；在涉及物流的會議場合，能以日文適時補充說明，確保資訊不因語言落差而失真；更擅長在會後整理重點、追蹤後續，讓溝通真正推進事情進展。2025 年，JLPT N1 正式合格。",
    "她習慣把眼睛放在「哪裡不順」。庫存查詢繁瑣→做了 LINE Bot；報價換算複雜→做了計算器；訂單格式混亂→開發 AI 辨識系統。這些工具不是為了展示技術，而是從真實的麻煩長出來的解法。她不只是執行工作的人，也是會主動讓工作變得更好的人。",
]
f_body = F(20, cjk=True)
for para in backstory_paras:
    RY = draw_wrapped(para, RX, RY, CW_R, f_body, color=TEXT_M, lh=34)
    RY += 16

RY += 8

# ── SPECIAL ABILITY ──
RY = section_title(RX, RY, "SPECIAL ABILITY", CW_R)

d.rectangle([(RX, RY), (RX + CW_R, RY + 80)], fill=NAVY)
d.rectangle([(RX, RY), (RX + 4,    RY + 80)], fill=GOLD)

RY2 = draw_wrapped(
    "語言力 × 實務力 × 自製工具力",
    RX + 14, RY + 8, CW_R - 20,
    F(22, bold=True, cjk=True), color=WHITE, lh=32
)
draw_wrapped(
    "遇到問題不只回報，而是想辦法解決它。",
    RX + 14, RY2 + 2, CW_R - 20,
    F(19, cjk=True), color="#AABBD0", lh=28
)
RY += 96

# ── FUTURE QUEST ──
RY = section_title(RX, RY, "FUTURE QUEST", CW_R)

d.rectangle([(RX, RY), (RX + CW_R, RY + 4)], fill=GOLD)
RY += 12
RY = draw_wrapped(
    "找到一個讓語言發光、讓細心被看見的地方，在穩定中持續累積、慢慢變強。",
    RX, RY, CW_R,
    FC(34), color=NAVY, lh=44
)

RY += 16

# ── Tag 標籤列 ──
tags = ["JLPT N1", "物流3年", "福岡研修", "日商往來", "AI工具", "台中在地"]
tx = RX
for tag in tags:
    bb = d.textbbox((0, 0), tag, font=F(18, cjk=True))
    tw = bb[2] - bb[0] + 20
    if tx + tw > RX + CW_R:
        tx  = RX
        RY += 38
    d.rectangle([(tx, RY), (tx + tw, RY + 32)], outline=NAVY2, width=1)
    d.text((tx + 10, RY + 6), tag, font=F(18, cjk=True), fill=NAVY2)
    tx += tw + 8
RY += 46

# ── 聯絡資訊 ──
d.rectangle([(RX, RY), (RX + CW_R, RY + 1)], fill=DIVIDER)
RY += 10
d.text((RX, RY), "jelena19961122@gmail.com   ·   0985-496781", font=FI(18), fill=WARM_G)

# ══════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════

d.rectangle([(18, H - 50), (W - 18, H - 18)], fill=NAVY)
footer_text = "Jelena Jhang  ·  Character File 2025  ·  Taichung, Taiwan"
bb = d.textbbox((0, 0), footer_text, font=F(18))
cx = (W - (bb[2] - bb[0])) // 2
d.text((cx, H - 40), footer_text, font=F(18), fill="#7A99CC")

# ══════════════════════════════════════════════
# 輸出
# ══════════════════════════════════════════════

img.save(OUTPUT, dpi=(150, 150))
print(f"✅ 完成！輸出至 {OUTPUT}，尺寸：{img.size}")
