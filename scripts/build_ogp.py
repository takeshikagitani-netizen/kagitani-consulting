# -*- coding: utf-8 -*-
"""OGP画像生成 (1200x630)
左：profile.png をネイビー背景に配置
右：サイトタイトル＋キャッチ＋数字訴求
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / 'images'
OUT = IMAGES / 'ogp.jpg'

NAVY = (17, 32, 80)        # #112050
NAVY2 = (25, 44, 96)
GOLD = (201, 151, 61)      # #c9973d
GOLD2 = (212, 170, 82)
WHITE = (255, 255, 255)
GREY = (200, 210, 230)

W, H = 1200, 630

# キャンバス（ネイビー背景）
img = Image.new('RGB', (W, H), NAVY)
draw = ImageDraw.Draw(img)

# 左側に縦の薄いネイビーグラデ風帯
for x in range(0, 600):
    r = NAVY[0] + int((NAVY2[0] - NAVY[0]) * x / 600)
    g = NAVY[1] + int((NAVY2[1] - NAVY[1]) * x / 600)
    b = NAVY[2] + int((NAVY2[2] - NAVY[2]) * x / 600)
    draw.line([(x, 0), (x, H)], fill=(r, g, b))

# プロフィール写真：円形マスクで配置
profile = Image.open(IMAGES / 'profile.png').convert('RGBA')
P_SIZE = 380
profile_resized = profile.resize((P_SIZE, P_SIZE), Image.LANCZOS)

# 円形マスク
mask = Image.new('L', (P_SIZE, P_SIZE), 0)
mdraw = ImageDraw.Draw(mask)
mdraw.ellipse((0, 0, P_SIZE, P_SIZE), fill=255)

# ゴールドの細い縁取り
ring_size = P_SIZE + 12
ring = Image.new('RGBA', (ring_size, ring_size), (0, 0, 0, 0))
rdraw = ImageDraw.Draw(ring)
rdraw.ellipse((0, 0, ring_size, ring_size), fill=GOLD + (255,))

px = (600 - ring_size) // 2
py = (H - ring_size) // 2
img.paste(ring, (px, py), ring)
img.paste(profile_resized, (px + 6, py + 6), mask)

# 右テキストブロック開始位置
TX = 640

# フォント探索
def get_font(size):
    candidates = [
        r'C:\Windows\Fonts\YuGothB.ttc',     # 游ゴシック Bold
        r'C:\Windows\Fonts\meiryob.ttc',     # メイリオ Bold
        r'C:\Windows\Fonts\msgothic.ttc',
        r'C:\Windows\Fonts\YuGothM.ttc',
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()

font_big = get_font(56)
font_med = get_font(34)
font_small = get_font(26)
font_num = get_font(72)

# 上：肩書ラベル（ゴールド）
draw.text((TX, 70), '後継社長専門の、幹部づくり屋。', font=font_small, fill=GOLD2)

# サイト名（大）
draw.text((TX, 110), '鍵谷 健', font=font_big, fill=WHITE)

# 区切り線
draw.line([(TX, 200), (TX + 380, 200)], fill=GOLD, width=3)

# ひとことコンセプト（2026-10-13確定の2行・言い換えない）
draw.text((TX, 225), '現場に入る経営参謀', font=font_med, fill=WHITE)
draw.text((TX, 275), '社長を不要とする会社づくり', font=font_med, fill=WHITE)

# 数字訴求
draw.text((TX, 375), '累計売上', font=font_small, fill=GREY)
draw.text((TX, 410), '600億円弱', font=font_num, fill=GOLD2)
draw.text((TX, 520), '29事業を、私が抜けても回る形に', font=font_small, fill=GREY)

# 保存（OGPは2MB未満が望ましい、JPG品質90）
img.save(OUT, 'JPEG', quality=90, optimize=True)
print(f'saved: {OUT} ({OUT.stat().st_size/1024:.1f} KB)')
