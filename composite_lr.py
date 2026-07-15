from PIL import Image, ImageDraw, ImageFont
import os

IMG = '/Users/chensijing/WorkBuddy/2026-07-15-17-02-13/img'
OUT = os.path.join(IMG, 'composite_lr.png')

F = '/System/Library/Fonts/STHeiti Light.ttc'
F_TOP  = ImageFont.truetype(F, 38, index=0)
F_SUBS = ImageFont.truetype(F, 22, index=0)
F_COL  = ImageFont.truetype(F, 30, index=0)
F_NUM  = ImageFont.truetype(F, 26, index=0)
F_SUB  = ImageFont.truetype(F, 20, index=0)
F_TAG  = ImageFont.truetype(F, 20, index=0)

BG   = (14, 10, 28)
PINK = (255, 46, 136)
CYAN = (25, 230, 255)
GOLD = (255, 210, 74)
WHITE= (245, 240, 255)
MUT  = (160, 148, 205)
CARD = (28, 22, 48)

PAD = 46
COL_W = 540
GAP = 40
TOP_H = 130
COL_TITLE_H = 74

main_mods = [
    ("mod_01_kv.png",      "KV 主视觉 · 活动名/日期/标语"),
    ("mod_02_banner.png",  "轮播 Banner 686×200 · 宣发位"),
    ("mod_03_intro.png",   "活动介绍 · 官宣视频+图文"),
    ("mod_04_roster.png",  "艺人阵容 · DAY1/DAY2 头像墙"),
    ("mod_05_ticket.png",  "购票通道 · 单日/双日/VIP"),
    ("mod_06_coin.png",    "金币面板 · 我的金币/已消耗"),
    ("mod_07_artistlist.png","艺人解锁进度 · 终极混战总榜"),
    ("mod_08_lottery.png", "九宫格抽奖 · 1000金币/次"),
]

def wrap(draw, text, font, max_w):
    lines = []
    for para in text.split('\n'):
        cur = ''
        for ch in para:
            t = cur + ch
            if draw.textlength(t, font=font) <= max_w:
                cur = t
            else:
                lines.append(cur); cur = ch
        lines.append(cur)
    return lines

# ---- 拼主页面（mod_01~08 纵向拼接，每块带小标签）----
def build_main():
    parts = []
    for fn, tag in main_mods:
        im = Image.open(os.path.join(IMG, fn)).convert('RGB')
        parts.append((im, tag))
    # 计算高度：每张图 + 标签 40
    gap = 16
    label_h = 40
    total_h = sum(p.height + label_h + gap for p, _ in parts) + gap
    W = max(p.width for p, _ in parts)
    canvas = Image.new('RGB', (W, total_h), BG)
    d = ImageDraw.Draw(canvas)
    y = gap
    for im, tag in parts:
        # 居中贴图
        x = (W - im.width) // 2
        canvas.paste(im, (x, y))
        # 标签
        ty = y + im.height + 8
        d.text((x, ty), tag, font=F_TAG, fill=MUT)
        y += im.height + label_h + gap
    return canvas

def scale(im, w):
    r = w / im.width
    return im.resize((w, max(1, int(im.height * r))), Image.LANCZOS)

def main():
    main_img = build_main()
    task = Image.open(os.path.join(IMG, '02-task-sheet.png')).convert('RGB')
    bet  = Image.open(os.path.join(IMG, '03-bet-sheet.png')).convert('RGB')

    main_s = scale(main_img, COL_W)
    task_s = scale(task, COL_W)
    bet_s  = scale(bet, COL_W)

    left_h  = COL_TITLE_H + main_s.height
    right_h = (COL_TITLE_H + task_s.height) + 30 + (COL_TITLE_H + bet_s.height)
    body_h = max(left_h, right_h)

    CW = PAD*2 + COL_W*2 + GAP
    CH = TOP_H + body_h + 40

    canvas = Image.new('RGB', (CW, CH), BG)
    d = ImageDraw.Draw(canvas)

    # 顶部标题
    d.text((PAD, 30), "泰嗨巅峰音乐节 · 活动交互稿（左右布局）", font=F_TOP, fill=WHITE)
    d.text((PAD, 82), "左：一级页全部内容（主页面结构）   右：任务模块 / 充能模块 折叠态单独展开", font=F_SUBS, fill=MUT)

    left_x  = PAD
    right_x = PAD + COL_W + GAP

    # 左列：主页面
    y = TOP_H
    d.rounded_rectangle([left_x, y, left_x+COL_W, y+COL_TITLE_H-14], radius=14, fill=CARD, outline=PINK, width=2)
    d.text((left_x+22, y+18), "① 主页面结构（一级页全部内容）", font=F_COL, fill=GOLD)
    y += COL_TITLE_H
    canvas.paste(main_s, (left_x, y))

    # 右列：任务 + 充能
    ry = TOP_H
    d.rounded_rectangle([right_x, ry, right_x+COL_W, ry+COL_TITLE_H-14], radius=14, fill=CARD, outline=CYAN, width=2)
    d.text((right_x+22, ry+18), "② 任务模块（点击「做任务赚金币」）", font=F_COL, fill=CYAN)
    ry += COL_TITLE_H
    canvas.paste(task_s, (right_x, ry))
    ry += task_s.height + 30
    d.rounded_rectangle([right_x, ry, right_x+COL_W, ry+COL_TITLE_H-14], radius=14, fill=CARD, outline=PINK, width=2)
    d.text((right_x+22, ry+18), "③ 充能模块（点击艺人「充能」）", font=F_COL, fill=PINK)
    ry += COL_TITLE_H
    canvas.paste(bet_s, (right_x, ry))

    # 右栏底部用途说明（填补留白）
    if right_h < body_h:
        sy = ry + bet_s.height + 16
        notes = [
            "【主页面结构】一级页自上而下：KV 主视觉 → 686×200 轮播 → 活动介绍 →",
            "艺人阵容(双日切换) → 购票通道 → 金币面板 → 艺人解锁进度总榜 → 九宫格抽奖。",
            "金币/消耗内置于充能站金币面板，不占用右上角。",
            "【任务模块】底部浮层集中展示 6 个任务 + 超会 ×1.5 加成，完成即入账。",
            "【充能模块】选艺人后底部浮层唤起，投入金币至其能量池，点亮里程节点。",
        ]
        for i, ln in enumerate(notes):
            d.text((right_x, sy + i*30), ln, font=F_SUB, fill=MUT)

    canvas.save(OUT)
    print('saved', OUT, canvas.size)

if __name__ == '__main__':
    main()
