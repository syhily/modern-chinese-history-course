#!/usr/bin/env python3
"""生成《中国近现代史》EPUB 封面 assets/cover.jpg。

以同系列《中国古代史教程》封面（assets 版式来源）为基底：几何布局完全沿用
（黑色书名横带位置、左右分栏、社标与系列徽标位置均从模板封面实测），
配色改为本书封面的蓝灰色系（自原书封面扫描页采样），文字替换为本书内容。

用法：
    python3 make_cover.py \
        --base ../ancient-chinese-history-course/assets/cover.jpg \
        --out  ../assets/cover.jpg

依赖：Pillow（pip install pillow）。字体使用 macOS 系统自带的
Songti.ttc（宋体）与 HelveticaNeue.ttc。
"""
import argparse

from PIL import Image, ImageDraw, ImageFont

# ---- 版式几何（自模板封面 1080x1440 实测） ----
W, H = 1080, 1440
BAND_X0, BAND_X1 = 319, 1080      # 黑色书名横带左右界
BAND_Y0, BAND_Y1 = 406, 578       # 黑色书名横带上下界
EMBLEM_BOX = (38, 28, 118, 110)   # 左上角「文」系列徽标裁切区（模板坐标）
PUBLOGO_BOX = (70, 1310, 305, 1395)  # 左下角出版社标志裁切区（模板坐标）

# ---- 本书配色（自原书封面扫描页采样，数字化后略提纯） ----
C_LIGHT = (143, 166, 206)    # 上部浅色
C_LIGHT2 = (118, 127, 166)   # 下部左栏
C_BLOCK = (103, 119, 152)    # 下部右侧深色块
C_BAND = (22, 22, 25)        # 书名横带
C_DARK_TEXT = (42, 46, 56)   # 深色文字（系列名、主编）
C_EN_TITLE = (198, 210, 228) # 英文书名（原书为低对比度白）
C_INTRO = (220, 226, 236)    # 简介文字（深色块上的浅色字）


def font(path, index, size):
    return ImageFont.truetype(path, size, index=index)


def pick_songti(size, want_bold=False):
    """在 Songti.ttc 中寻找宋体：粗体取 Songti SC Black，正文取 STSong Regular。"""
    path = "/System/Library/Fonts/Supplemental/Songti.ttc"
    fonts = {}
    for i in range(8):
        try:
            f = ImageFont.truetype(path, size, index=i)
        except Exception:
            break
        fonts[" ".join(f.getname())] = f
    if want_bold:
        for name in ("Songti SC Black", "Songti SC Bold"):
            if name in fonts:
                return fonts[name]
    else:
        for name in ("STSong Regular", "Songti SC Light"):
            if name in fonts:
                return fonts[name]
    return next(iter(fonts.values()))


def draw_spaced(draw, xy, text, fnt, fill, x1):
    """从 xy 起把 text 逐字均匀排到 x1（两端对齐的字距）。"""
    x0, y = xy
    widths = []
    for ch in text:
        bb = draw.textbbox((0, 0), ch, font=fnt)
        widths.append(bb[2] - bb[0])
    total = sum(widths)
    gaps = len(text) - 1
    step = (x1 - x0 - total) / gaps if gaps else 0
    x = x0
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + step


def color_key_paste(canvas, crop, box, bg):
    """把 crop 贴到 canvas 的 box 位置，把接近 bg（模板底色）的像素抠为透明。"""
    crop = crop.convert("RGB")
    px = crop.load()
    mask = Image.new("L", crop.size, 0)
    mp = mask.load()
    for yy in range(crop.size[1]):
        for xx in range(crop.size[0]):
            p = px[xx, yy]
            d = sum((a - b) ** 2 for a, b in zip(p, bg)) ** 0.5
            mp[xx, yy] = max(0, min(255, int((d - 12) * 9)))
    canvas.paste(crop, (box[0], box[1]), mask)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="模板封面 cover.jpg 路径")
    ap.add_argument("--out", required=True, help="输出 cover.jpg 路径")
    args = ap.parse_args()

    tpl = Image.open(args.base).convert("RGB")
    assert tpl.size == (W, H), f"模板封面尺寸应为 {W}x{H}，实为 {tpl.size}"

    img = Image.new("RGB", (W, H), C_LIGHT)
    dr = ImageDraw.Draw(img)

    # 下部：横带以下左栏浅色、右侧深色块（与模板同版式）
    dr.rectangle([0, BAND_Y1, BAND_X0, H], fill=C_LIGHT2)
    dr.rectangle([BAND_X0, BAND_Y1, W, H], fill=C_BLOCK)
    # 黑色书名横带
    dr.rectangle([BAND_X0, BAND_Y0, W, BAND_Y1], fill=C_BAND)

    # 徽标与社标：从模板封面抠图移植（二者完全一致）
    for box in (EMBLEM_BOX, PUBLOGO_BOX):
        crop = tpl.crop(box)
        color_key_paste(img, crop, box, crop.getpixel((2, 2)))  # 以裁切区角落像素为底色

    song = pick_songti(40)
    song_bold = pick_songti(118, want_bold=True)
    try:
        en = font("/System/Library/Fonts/HelveticaNeue.ttc", 1, 48)
    except Exception:
        en = font("/System/Library/Fonts/Helvetica.ttc", 1, 48)

    # 顶部系列名：本书为「高等院校文科教材·史学系列」，通栏均排
    draw_spaced(dr, (150, 46), "高等院校文科教材·史学系列", song, C_DARK_TEXT, 1015)

    # 英文书名（原书为低对比度白，两行）
    dr.text((70, 165), "Modern and Contemporary History", font=en, fill=C_EN_TITLE)
    dr.text((70, 232), "of China", font=en, fill=C_EN_TITLE)

    # 横带书名：白色宋体加粗，带内居中
    title = "中国近现代史"
    bb = dr.textbbox((0, 0), title, font=song_bold)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    dr.text(((BAND_X0 + W - tw) / 2 - bb[0], (BAND_Y0 + BAND_Y1 - th) / 2 - bb[1]),
            title, font=song_bold, fill=(255, 255, 255))

    # 横带左侧：主编一行（本书为主编二人一行，与模板的两行不同）
    ed_font = pick_songti(34)
    ed_text = "章开沅朱英主编"
    bb = dr.textbbox((0, 0), ed_text, font=ed_font)
    draw_spaced(dr, (30, (BAND_Y0 + BAND_Y1) / 2 - (bb[3] - bb[1]) / 2 - bb[1]),
                ed_text, ed_font, C_DARK_TEXT, BAND_X0 - 30)

    # 深色块内简介（首行缩进两字，手动分行）
    intro_font = pick_songti(24)
    intro = "本书以新的史学教材编写理念，运用新的编写体例，诠释了中国近现代史这一漫长历史时期的波澜壮阔。书中大量的历史新知识、新观点、研究新理论、新方法，有助于读者全面了解史学界新近相关的研究动态，激发思考和研究兴趣，从而以全新的视角认识中国近现代史。"
    lines = ["　　" + intro[i:i + 24] if i == 0 else intro[i:i + 24]
             for i in range(0, len(intro), 24)]
    y = 890
    for ln in lines:
        dr.text((425, y), ln, font=intro_font, fill=C_INTRO)
        y += 42

    img.save(args.out, quality=92)
    print("written:", args.out)


if __name__ == "__main__":
    main()
