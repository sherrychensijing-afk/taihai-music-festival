from PIL import Image, ImageDraw, ImageFont
import os

IMG = '/Users/chensijing/WorkBuddy/2026-07-15-17-02-13/img'
OUT = os.path.join(IMG, 'long.png')

# 字体
try:
    F = '/System/Library/Fonts/STHeiti Light.ttc'
    F_TITLE = ImageFont.truetype(F, 34, index=0)
    F_PURP = ImageFont.truetype(F, 22, index=0)
    F_TOP = ImageFont.truetype(F, 40, index=0)
    F_TOPS = ImageFont.truetype(F, 22, index=0)
    F_NUM = ImageFont.truetype(F, 26, index=0)
except Exception as e:
    F = '/Library/Fonts/Arial Unicode.ttf'
    F_TITLE = ImageFont.truetype(F, 34)
    F_PURP = ImageFont.truetype(F, 22)
    F_TOP = ImageFont.truetype(F, 40)
    F_TOPS = ImageFont.truetype(F, 22)
    F_NUM = ImageFont.truetype(F, 26)

BG = (14, 10, 28)
PINK = (255, 46, 136)
CYAN = (25, 230, 255)
GOLD = (255, 210, 74)
WHITE = (245, 240, 255)
MUT = (155, 143, 199)
LINE = (255, 255, 255, 30)

PAD = 50
CONTENT_W = 780
CANVAS_W = CONTENT_W + PAD * 2  # 880

modules = [
    ("01", "KV 主视觉", "活动第一视觉，承载活动名 / 日期 / 标语，快速建立音乐节氛围", "mod_01_kv.png"),
    ("02", "轮播 Banner（686×200）", "宣发位，轮播玩法福利与跳转入口，置于 KV 之下", "mod_02_banner.png"),
    ("03", "活动介绍", "官宣视频 + 图文，传递音乐节背景与核心亮点", "mod_03_intro.png"),
    ("04", "艺人阵容", "DAY1 / DAY2 双日切换的头像墙，概览 16 组艺人，点击可定位充能站", "mod_04_roster.png"),
    ("05", "购票通道", "单日 / 双日 / VIP 票种，承接流量转化", "mod_05_ticket.png"),
    ("06", "金币面板（充能站头）", "展示「我的金币 / 已消耗」，「做任务赚金币」唤起任务浮层", "mod_06_coin.png"),
    ("07", "艺人解锁进度（终极混战总榜）", "世界杯式卡片：排名 + 累计能量 + 里程节点 + 充能 / 分享；按能量实时排序，Top3 即终极混战", "mod_07_artistlist.png"),
    ("08", "九宫格抽奖", "1000 金币 / 次，抽取签名照 / 门票 / 周边等", "mod_08_lottery.png"),
    ("09", "任务浮层（折叠态）", "点击「做任务」唤起，集中展示全部任务与超会 ×1.5 加成", "mod_09_tasksheet.png"),
    ("10", "充能浮层（折叠态）", "点击艺人「充能」唤起，投入金币至该艺人能量池", "mod_10_betsheet.png"),
    ("11", "艺人卡展开（折叠态）", "点击卡片展开 4 节点奖励明细：语音电话 / 大礼包 / 彩蛋 / 终极混战", "mod_11_expand.png"),
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
                lines.append(cur)
                cur = ch
        lines.append(cur)
    return lines


def main():
    # 先算总高
    draw_tmp = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    blocks = []  # (y, render_fn)
    y = PAD
    # 顶部标题
    y += 70  # 标题
    y += 34  # 副标题
    y += 24  # 间距

    for idx, title, purp, fn in modules:
        lines = wrap(draw_tmp, purp, F_PURP, CANVAS_W - (PAD + 64) - PAD)
        h_header = 44 + len(lines) * 32 + 14
        img = Image.open(os.path.join(IMG, fn)).convert('RGB')
        blocks.append((y, idx, title, lines, img))
        y += h_header
        y += 14  # 图与标题间距
        y += img.height
        y += 30  # 模块间距

    CANVAS_H = y + PAD
    canvas = Image.new('RGB', (CANVAS_W, CANVAS_H), BG)
    d = ImageDraw.Draw(canvas)

    # 顶部标题
    ty = PAD
    d.text((PAD, ty), "泰嗨巅峰音乐节 · 活动交互稿（图片版）", font=F_TOP, fill=WHITE)
    ty += 70
    d.text((PAD, ty), "按页面顺序拆解各模块用途 · 折叠态（任务 / 充能 / 卡片展开）单独展开说明", font=F_TOPS, fill=MUT)
    ty += 34 + 24

    for (yy, idx, title, lines, img) in blocks:
        # 编号圆点
        cx, cy = PAD + 24, yy + 22
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=PINK)
        d.text((cx, cy), idx, font=F_NUM, fill=(255, 255, 255), anchor='mm')
        # 标题
        d.text((PAD + 64, yy), title, font=F_TITLE, fill=GOLD)
        # 用途
        ly = yy + 44
        for ln in lines:
            d.text((PAD + 64, ly), ln, font=F_PURP, fill=MUT)
            ly += 32
        # 图片居中
        ix = (CANVAS_W - img.width) // 2
        canvas.paste(img, (ix, ly + 14))
        # 分隔线
        sep_y = ly + 14 + img.height + 15
        d.line([PAD, sep_y, CANVAS_W - PAD, sep_y], fill=LINE, width=1)

    canvas.save(OUT)
    print('saved', OUT, canvas.size)


if __name__ == '__main__':
    main()
