#!/usr/bin/env python3
"""README visuals for dsh-gongwen-flow-check — drawn from this package's own artifacts.

Outputs (docs/assets/, idempotent overwrite):

  dsh-gongwen-flow-check-hero-{zh,en}-{light,dark}.webp   1440x576
  dsh-gongwen-flow-check-flow-v5-{light,dark}.svg         1100x660

Nothing here is copied from a sibling checker; both figures are derived from
what this package actually ships:

  * `src/model.ts` — the reader contract: 8 row columns (seq / stage / handler /
    receivedAt / dueAt / doneAt / status / note) with Chinese and English
    aliases, 7 header fields (docNo / title / docKind / issuer / receivedAt /
    dueAt / urgent), and `REQUIRE_ANY_OF` = stage / status / handler.
  * `src/shared/table.ts` — alias matching lowercases and strips spaces,
    underscores and hyphens; at least one known column name must be recognised.
  * `rules/gongwen-flow-check.yaml` — pack `2026.1`, 6 rules. Four cite a
    principle (`derived-from-principle`, capped at `warn`: GF-001, GF-002,
    GF-005, GF-006), two cite an institutional setting (`institutional-
    configuration`, capped at `info`: GF-003, GF-004). The pack has no `direct`
    basis at all, so the severity `error` can never be emitted (asserted by
    `src/shared/ruleset.ts` MAX_SEVERITY_BY_KIND and by the tests).
  * `samples/quickstart/input/GF-001-unsafe.json` — the ledger drawn in both
    figures is that file, cell for cell: 某发〔2026〕15号 / 关于某某工作的通知 /
    通知 / 某某机关 / 2026-03-02, one row 承办 with a blank 承办人, 期限
    2026-03-12, 办结 2026-03-10, 状态 已办结.
  * a real run of that sample (verified with `node samples/quickstart/run.mjs`
    and a direct `gongwen_flow_check` call): issueCount 1 (GF-001 warn, row 1,
    column handler), skippedCount 1 (GF-004: `values` unset), error 0,
    warn 1, info 0; GF-002 / GF-003 / GF-005 / GF-006 ran clean and therefore
    appear in neither list (the documented "ran clean is not skipped" rule in
    `src/shared/rows.ts`).
  * `src/view.ts` — the view fields drawn in the report band: summary,
    issueCount, skippedCount, rulesetVersion, markdown + reportJson, plus the
    wording guard and the mandatory disclaimer.

Hero — left column is copy (kicker / two-line wordmark / two value lines /
two subtitle lines / meta / footer). The right side is this plugin's own
artifact, not a generic dashboard: the receipt register sheet (header fields +
one handling-stage row) with the blank handler cell marked, and beneath it the
difference list it produces (GF-001 finding + GF-004 skipped), sealed
"只列差异 / 不下结论" — differences only, never a verdict, never an edit.

Flow — grammar = TRI-STATE SORTING BENCH, not a row of nodes. A single ledger
feeds six rule gates; every gate leaves in exactly one of three states —
`issues[]` (found something), `skipped[]` (could not run), or neither (ran
clean). The three trays on the right hold those states, and the severity rail
above the gates shows the real ceiling: the pack has no `direct` basis, so
`error` is unreachable, four rules cap at `warn`, two at `info`. A report band
closes the figure with the real counters (error 0 / warn 1 / info 0;
issueCount 1 / skippedCount 1) and hands the verdict to the reviewer.

Every label is measured with the same fonts the SVG names before it is drawn;
anything that would overflow aborts the run instead of shipping clipped text.
Hero title is 89-92px, value lines 28-31px, subtitle 24-25px, meta 20px,
footer 16px. In the 1100px flow, gate expressions are 13px, gate ids 14.5px,
figure title 29px, and every annotation is >= 11px.

Old single-skin assets (`…-flow.svg`, `…-flow-{light,dark}.svg`, `…-hero.png`,
`…-demo.*`, `quickstart.*`) are deliberately left on disk so external links keep
resolving; the READMEs reference only the new hero set and the flow-v5 pair.

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow + Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf /
           consolab.ttf.
"""
from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")
NAME = "dsh-gongwen-flow-check"

FONT_FILES = {
    "cjk": r"C:\Windows\Fonts\msyh.ttc",
    "cjk_bold": r"C:\Windows\Fonts\msyhbd.ttc",
    "mono": r"C:\Windows\Fonts\consola.ttf",
    "mono_bold": r"C:\Windows\Fonts\consolab.ttf",
}
for _kind, _path in FONT_FILES.items():
    if not os.path.exists(_path):
        raise SystemExit(f"FATAL: font missing: {_path}")

RADIUS = 20
os.makedirs(OUT, exist_ok=True)

FONT_CSS_SANS = ("'Microsoft YaHei','Segoe UI','PingFang SC',"
                 "'Noto Sans CJK SC',sans-serif")
FONT_CSS_MONO = "Consolas,'Microsoft YaHei',ui-monospace,monospace"

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", ok="#15803d", warn="#b45309",
        pill="#ece7f9", band="#f5f2fb", grid="#e7e4f0",
        warn_bg="#fbf1e4", miss_bg="#f1eff8",
        shadow=(43, 35, 80), shadow_alpha=52, glow=34,
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", ok="#3fb950", warn="#d9a441",
        pill="#242d42", band="#202839", grid="#2b3348",
        warn_bg="#292217", miss_bg="#232b3d",
        shadow=(0, 0, 0), shadow_alpha=150, glow=46,
    ),
}

FLOW = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        panel="#ffffff", card="#ffffff", edge="#e6e2ef",
        band="#f5f2fb", pill="#ece7f9", tint="#f7f4ec",
        warn_bg="#fbf1e4", miss_bg="#f2f0f8",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", ok="#15803d", warn="#b45309",
        rule="#e7e4f0", shadow="#2b2440", shadow_op="0.14",
        dot="#cfc8e2", dot_op="0.5",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        panel="#1b2231", card="#1b2231", edge="#2e374b",
        band="#202839", pill="#242d42", tint="#2a2419",
        warn_bg="#292217", miss_bg="#232b3d",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", ok="#3fb950", warn="#d9a441",
        rule="#2b3348", shadow="#000000", shadow_op="0.52",
        dot="#2a3346", dot_op="0.5",
    ),
}

# ---------------------------------------------------------------------------
# fonts + measuring
# ---------------------------------------------------------------------------
_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}
_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def font(size: float, kind: str = "cjk") -> ImageFont.FreeTypeFont:
    key = (kind, int(round(size)))
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_FILES[kind], key[1])
    return _font_cache[key]


def measure(text: str, size: float, kind: str = "cjk") -> float:
    return _MEASURE.textlength(text, font=font(size, kind))


def require_w(text: str, size: float, kind: str, max_w: float,
              what: str) -> None:
    got = measure(text, size, kind)
    if got > max_w + 0.4:
        raise SystemExit(f"FATAL: {what} overflows: {text!r} needs "
                         f"{got:.1f}px > {max_w:.0f}px")


def fit(text: str, kind: str, max_w: float, start: float,
        minimum: float) -> float:
    size = float(start)
    while size > minimum:
        if measure(text, size, kind) <= max_w:
            return size
        size -= 1
    raise SystemExit(f"FATAL: text does not fit {max_w:.0f}px at >= "
                     f"{minimum}px: {text!r}")


def fit_lines(lines: list[str], kind: str, max_w: float, start: float,
              minimum: float) -> float:
    return min(fit(line, kind, max_w, start, minimum) for line in lines)


def hx(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------------------
# raster primitives
# ---------------------------------------------------------------------------
def gradient(w: int, h: int, top: str, bottom: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    a, b = hx(top), hx(bottom)
    for y in range(h):
        t = 0.12 * (y / h) + 0.88 * (y / h) ** 1.3
        draw.line([(0, y), (w, y)],
                  fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: str,
         alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rgb = hx(color)
    for i in range(10, 0, -1):
        rr = r * i / 10
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=rgb + (int(alpha * (1 - i / 11)),))
    return Image.alpha_composite(img.convert("RGBA"),
                                 layer.filter(ImageFilter.GaussianBlur(26))
                                 ).convert("RGB")


def card(img: Image.Image, box: tuple[int, int, int, int], s: dict,
         radius: int = RADIUS, shadow: int = 22,
         fill: str | None = None, edge: str | None = None) -> Image.Image:
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x0 + 2, y0 + max(4, shadow // 2), x1 + 2,
                         y1 + max(5, shadow // 2)],
                        radius=radius, fill=s["shadow"] + (s["shadow_alpha"],))
    base = Image.alpha_composite(img.convert("RGBA"),
                                 layer.filter(ImageFilter.GaussianBlur(shadow / 2)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=hx(fill or s["card"]),
                        outline=hx(edge or s["edge"]), width=2)
    return base.convert("RGB")


def pill(img: Image.Image, xy: tuple[float, float], text: str, s: dict,
         size: float = 16, fg: str | None = None, bg: str | None = None,
         kind: str = "cjk_bold") -> float:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    h = size + 22
    d.rounded_rectangle([x, y, x + w + 36, y + h], radius=h / 2,
                        fill=hx(bg or s["pill"]))
    d.text((x + 18, y + h / 2), text, font=f, fill=hx(fg or s["accent"]),
           anchor="lm")
    return x + w + 36


def chip_right(img: Image.Image, right: float, y: float, text: str, fg: str,
               bg: str, size: float = 12, height: float = 25,
               kind: str = "mono_bold", pad: float = 10) -> float:
    d = ImageDraw.Draw(img)
    w = d.textlength(text, font=font(size, kind)) + pad * 2
    x = right - w
    d.rounded_rectangle([x, y, right, y + height], radius=height / 2,
                        fill=hx(bg))
    d.text((x + pad, y + height / 2 + 0.5), text, font=font(size, kind),
           fill=hx(fg), anchor="lm")
    return x


def rich_line(img: Image.Image, x: float, y: float,
              runs: list[tuple[str, str, str]], size: float) -> float:
    """Draw runs of (text, colour, kind) left to right; return the end x."""
    d = ImageDraw.Draw(img)
    cursor = float(x)
    for text, color, kind in runs:
        d.text((cursor, y), text, font=font(size, kind), fill=hx(color),
               anchor="ls")
        cursor += measure(text, size, kind)
    return cursor


def seal(img: Image.Image, cx: int, cy: int, radius: int, top: str, bottom: str,
         s: dict, lang: str) -> Image.Image:
    """A slightly rotated official-looking stamp; never red, never a verdict."""
    size = radius * 2 + 24
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = size // 2
    rgb = hx(s["accent"])
    d.ellipse([c - radius, c - radius, c + radius, c + radius],
              outline=rgb + (190,), width=3)
    d.ellipse([c - radius + 7, c - radius + 7, c + radius - 7, c + radius - 7],
              outline=rgb + (120,), width=1)
    top_size = 18 if lang == "zh" else 13
    bot_size = 12 if lang == "zh" else 10.5
    top_font = font(top_size, "cjk_bold" if lang == "zh" else "mono_bold")
    bot_font = font(bot_size, "cjk" if lang == "zh" else "mono")
    d.text((c, c - 4), top, font=top_font, fill=rgb + (215,), anchor="ms")
    d.text((c, c + 20), bottom, font=bot_font, fill=rgb + (170,), anchor="ms")
    # two small ticks, like a registration stamp
    for dx in (-radius + 12, radius - 12):
        d.line([(c + dx, c - 11), (c + dx, c + 11)], fill=rgb + (110,), width=1)
    layer = layer.rotate(-9, resample=Image.BICUBIC, expand=False)
    base = img.convert("RGBA")
    base.alpha_composite(layer, (cx - c, cy - c))
    return base.convert("RGB")


# ---------------------------------------------------------------------------
# hero copy + the one ledger the hero shows
# ---------------------------------------------------------------------------
HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · 收文台账核对",
        title=("dsh-gongwen-", "flow-check"),
        value=("逐个办理环节核对：承办人填没填、",
               "日期先后、办理期限、状态在不在册。"),
        sub=("只列「哪一行、哪一栏、差什么」，",
             "不下合规结论；原件永不修改。"),
        meta=[("gongwen_flow_check", "mono_bold"),
              ("  ·  6 条规则  ·  ", "cjk"),
              ("GF-001..GF-006", "mono_bold")],
        foot="Apache-2.0 · 只读 · 不联网 · 不调用模型 · 不写文件",
        sheet_title="收文登记台账",
        sheet_chip="只读 · JSON / YAML",
        labels=("文号", "标题", "收文日期", "文种 · 机关"),
        values_header=("某发〔2026〕15号", "关于某某工作的通知",
                       "2026-03-02", "通知 · 某某机关"),
        table_head=("环节", "承办人", "收文日期", "办理期限", "办结日期", "办理状态"),
        table_row=("承办", "（空）", "2026-03-02", "2026-03-12", "2026-03-10", "已办结"),
        sheet_foot="8 个环节栏 · 表头 7 栏 · 栏名中英皆可",
        sheet_note="栏名大小写不敏感，忽略空格、下划线与连字符",
        slip_title="差异清单 · 报告",
        chips=(("skipped 1", "accent", "pill"), ("warn 1", "warn", "warn_bg"),
               ("error 0", "faint", "band")),
        find_id="GF-001",
        find_runs=[("第 1 行 · ", "cjk"), ("handler", "mono"), (" 为空", "cjk")],
        sub_runs=[("预期：「", "cjk"), ("handler", "mono"),
                  ("」应填写；建议：补填承办人", "cjk")],
        skip_id="GF-004",
        skip_runs=[("skipped：", "cjk"), ("values", "mono"), (" 未配置", "cjk")],
        slip_foot="结论留给复核人 · 原件永不修改",
        slip_meta="ruleset 2026.1",
        seal=("只列差异", "不下结论"),
    ),
    "en": dict(
        kicker="DeepSeek Harness plugin · receipt register check",
        title=("dsh-gongwen-", "flow-check"),
        value=("Check each handling stage: handler,",
               "dates in order, deadline, status."),
        sub=("Which row, which column, what differs —",
             "no verdict; the original is never modified."),
        meta=[("gongwen_flow_check", "mono_bold"),
              ("  ·  6 rules  ·  ", "cjk"),
              ("GF-001..GF-006", "mono_bold")],
        foot="Apache-2.0 · read-only · no network · no model call",
        sheet_title="Receipt register",
        sheet_chip="read-only · JSON / YAML",
        labels=("docNo", "title", "receivedAt", "docKind · issuer"),
        values_header=("某发〔2026〕15号", "关于某某工作的通知",
                       "2026-03-02", "通知 · 某某机关"),
        table_head=("stage", "handler", "received", "due", "done", "status"),
        table_row=("承办", "(empty)", "2026-03-02", "2026-03-12", "2026-03-10", "已办结"),
        sheet_foot="8 stage columns · 7 header fields · CN or EN column names",
        sheet_note="column names ignore case, spaces, underscores and hyphens",
        slip_title="Differences · report",
        chips=(("skipped 1", "accent", "pill"), ("warn 1", "warn", "warn_bg"),
               ("error 0", "faint", "band")),
        find_id="GF-001",
        find_runs=[("row 1 · ", "cjk"), ("handler", "mono"), (" is empty", "cjk")],
        sub_runs=[("expected: ", "cjk"), ("handler", "mono"),
                  (" must be filled; fix: fill it in", "cjk")],
        skip_id="GF-004",
        skip_runs=[("skipped: ", "cjk"), ("values", "mono"),
                   (" not configured", "cjk")],
        slip_foot="the verdict stays with the reviewer · the original is never modified",
        slip_meta="ruleset 2026.1",
        seal=("DIFFERENCES", "NO VERDICT"),
    ),
}


def hero(lang: str, skin: str) -> None:
    s = SKIN[skin]
    h = HERO[lang]
    W, H = 1440, 576
    img = gradient(W, H, s["bg_from"], s["bg_to"])
    img = glow(img, 1210, 70, 430, s["accent"], s["glow"])
    img = glow(img, 140, 560, 320, s["accent"], max(8, s["glow"] // 3))

    m, col_w = 56, 590
    d = ImageDraw.Draw(img)

    # ---- left copy column ---------------------------------------------------
    kicker_size = fit(h["kicker"], "cjk_bold", 545, 19, 16)
    kicker_w = measure(h["kicker"], kicker_size, "cjk_bold") + 36
    if kicker_w > 600:
        raise SystemExit(f"FATAL: kicker pill {kicker_w:.0f}px wide")
    pill(img, (m, 40), h["kicker"], s, size=kicker_size)
    d = ImageDraw.Draw(img)

    title_size = fit_lines(list(h["title"]), "mono_bold", col_w, 92, 80)
    for line in h["title"]:
        require_w(line, title_size, "mono_bold", col_w, "hero title")
    d.text((m - 1, 178), h["title"][0], font=font(title_size, "mono_bold"),
           fill=hx(s["text"]), anchor="ls")
    d.text((m - 1, 262), h["title"][1], font=font(title_size, "mono_bold"),
           fill=hx(s["accent"]), anchor="ls")

    value_size = fit_lines(list(h["value"]), "cjk_bold", col_w,
                           31 if lang == "zh" else 30, 26)
    for index, line in enumerate(h["value"]):
        require_w(line, value_size, "cjk_bold", col_w, "hero value line")
        d.text((m, 322 + index * 40), line, font=font(value_size, "cjk_bold"),
               fill=hx(s["text"]), anchor="ls")

    sub_size = fit_lines(list(h["sub"]), "cjk", col_w, 25, 22)
    for index, line in enumerate(h["sub"]):
        require_w(line, sub_size, "cjk", col_w, "hero subtitle")
        d.text((m, 412 + index * 30), line, font=font(sub_size, "cjk"),
               fill=hx(s["sub"]), anchor="ls")

    meta_runs = [(text, s["faint"], kind) for text, kind in h["meta"]]
    meta_end = m + sum(measure(text, 20, kind) for text, kind in h["meta"])
    if meta_end > m + col_w:
        raise SystemExit("FATAL: hero meta overflows")
    rich_line(img, m + 1, 480, meta_runs, 20)

    d = ImageDraw.Draw(img)
    d.line([m + 1, 502, m + col_w - 4, 502], fill=hx(s["grid"]), width=2)
    foot_size = fit(h["foot"], "cjk", col_w, 16, 13)
    d.text((m + 1, 528), h["foot"], font=font(foot_size, "cjk"),
           fill=hx(s["faint"]), anchor="ls")

    # ---- right: the register sheet -----------------------------------------
    img = card(img, (680, 48, 1384, 352), s, radius=20, shadow=26)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([680, 48, 1384, 104], radius=20, fill=hx(s["band"]))
    d.rectangle([680, 84, 1384, 104], fill=hx(s["band"]))
    d.line([680, 104, 1384, 104], fill=hx(s["edge"]), width=1)

    d.text((708, 82), h["sheet_title"], font=font(19, "cjk_bold"),
           fill=hx(s["text"]), anchor="ls")
    chip_right(img, 1362, 62, h["sheet_chip"], s["accent"], s["pill"],
               size=11.5, height=26, kind="cjk")

    # header fields: two columns, two rows, label and value on the same line
    d = ImageDraw.Draw(img)
    header_cells = [
        (708, 770, h["labels"][0], h["values_header"][0], "cjk", 240, 136),
        (1020, 1140, h["labels"][2], h["values_header"][2], "mono", 210, 136),
        (708, 770, h["labels"][1], h["values_header"][1], "cjk", 240, 166),
        (1020, 1140, h["labels"][3], h["values_header"][3], "cjk", 210, 166),
    ]
    for label_x, value_x, label, value, kind, limit, y in header_cells:
        d.text((label_x, y), label, font=font(11, "cjk"),
               fill=hx(s["faint"]), anchor="ls")
        require_w(value, 15, kind, limit, "hero header value")
        d.text((value_x, y), value, font=font(15, kind),
               fill=hx(s["text"]), anchor="ls")

    # table
    table_y = 206
    head_y = 208
    row_y = 236
    d.line([708, 192, 1356, 192], fill=hx(s["grid"]), width=1)
    d.line([708, 254, 1356, 254], fill=hx(s["grid"]), width=1)
    col_x = (708, 790, 920, 1050, 1170, 1290)
    col_limits = (70, 118, 118, 108, 108, 66)
    for index, head in enumerate(h["table_head"]):
        require_w(head, 11, "cjk", col_limits[index], "hero table head")
        d.text((col_x[index], head_y), head, font=font(11, "cjk"),
               fill=hx(s["faint"]), anchor="ls")
    # the blank handler cell is the finding: mark it before drawing the text
    d.rounded_rectangle([col_x[1] - 6, table_y + 4, col_x[2] - 8, table_y + 44],
                        radius=10, fill=hx(s["warn_bg"]),
                        outline=hx(s["warn"]), width=1)
    cell_kinds = ("cjk", "cjk", "mono", "mono", "mono", "cjk")
    for index, cell in enumerate(h["table_row"]):
        kind = cell_kinds[index]
        color = s["warn"] if index == 1 else s["text"]
        size = 14
        require_w(cell, size, kind, col_limits[index], "hero table cell")
        d.text((col_x[index], row_y), cell, font=font(size, kind),
               fill=hx(color), anchor="ls")
    d.text((708, 296), h["sheet_foot"], font=font(11, "cjk"),
           fill=hx(s["faint"]), anchor="ls")
    d.text((1356, 296), "JSON / YAML", font=font(11, "mono"),
           fill=hx(s["faint"]), anchor="rs")
    d.text((708, 322), h["sheet_note"], font=font(11, "cjk"),
           fill=hx(s["faint"]), anchor="ls")

    # ---- right: the difference list ----------------------------------------
    img = card(img, (700, 364, 1384, 548), s, radius=20, shadow=28)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([700, 364, 1384, 406], radius=20, fill=hx(s["band"]))
    d.rectangle([700, 390, 1384, 406], fill=hx(s["band"]))
    d.line([700, 406, 1384, 406], fill=hx(s["edge"]), width=1)
    d.text((728, 394), h["slip_title"], font=font(16, "cjk_bold"),
           fill=hx(s["text"]), anchor="ls")

    chip_x = 1362
    for label, fg_key, bg_key in reversed(h["chips"]):
        chip_x = chip_right(img, chip_x, 376, label, s[fg_key], s[bg_key],
                            size=11, height=24, kind="mono_bold") - 8

    d = ImageDraw.Draw(img)
    # GF-001 finding
    d.ellipse([734, 428, 742, 436], fill=hx(s["warn"]))
    d.text((752, 438), h["find_id"], font=font(13, "mono_bold"),
           fill=hx(s["warn"]), anchor="ls")
    find_runs = [(text, s["text"], kind) for text, kind in h["find_runs"]]
    if sum(measure(text, 13, kind) for text, _, kind in find_runs) > 430:
        raise SystemExit("FATAL: hero finding overflows")
    rich_line(img, 812, 438, find_runs, 13)
    sub_runs = [(text, s["sub"], kind) for text, kind in h["sub_runs"]]
    if sum(measure(text, 11.5, kind) for text, _, kind in sub_runs) > 470:
        raise SystemExit("FATAL: hero expected line overflows")
    rich_line(img, 752, 462, sub_runs, 11.5)
    # GF-004 skipped
    d.ellipse([734, 484, 742, 492], fill=hx(s["accent"]))
    d.text((752, 494), h["skip_id"], font=font(12.5, "mono_bold"),
           fill=hx(s["accent"]), anchor="ls")
    skip_runs = [(text, s["sub"], kind) for text, kind in h["skip_runs"]]
    rich_line(img, 812, 494, skip_runs, 11.5)
    # footer
    d.text((728, 528), h["slip_foot"], font=font(11.5, "cjk"),
           fill=hx(s["faint"]), anchor="ls")
    d.text((1206, 528), h["slip_meta"], font=font(11, "mono"),
           fill=hx(s["faint"]), anchor="rs")
    d.rounded_rectangle([700, 364, 1384, 548], radius=20,
                        outline=hx(s["edge"]), width=2)

    img = seal(img, 1306, 492, 52, h["seal"][0], h["seal"][1], s, lang)

    name = f"{NAME}-hero-{lang}-{skin}.webp"
    img.save(os.path.join(OUT, name), "WEBP", quality=92, method=6)
    print(f"wrote {name} ({W}x{H})")


# ---------------------------------------------------------------------------
# flow: one ledger -> six gates -> three states -> one report
# ---------------------------------------------------------------------------
RULES = [
    ("GF-001", "warn", [("承办人 ", "cjk"), ("handler", "mono_bold"),
                        (" 必填", "cjk")],
     "presence", "命中"),
    ("GF-002", "warn", [("receivedAt", "mono_bold"), (" ≤ ", "cjk"),
                        ("doneAt", "mono_bold")],
     "date", "未命中"),
    ("GF-003", "info", [("doneAt", "mono_bold"), (" ≤ ", "cjk"),
                        ("dueAt", "mono_bold")],
     "date", "未命中"),
    ("GF-004", "info", [("status", "mono_bold"), (" ∈ ", "cjk"),
                        ("values", "mono_bold")],
     "enum", "未执行"),
    ("GF-005", "warn", [("docNo", "mono_bold"), (" 唯一登记", "cjk")],
     "unique", "未命中"),
    ("GF-006", "warn", [("表头声明 ", "cjk"), ("title", "mono_bold"),
                        (" · ", "cjk"), ("receivedAt", "mono_bold")],
     "headerPresence", "未命中"),
]

STATE_COLOR = {"命中": "warn", "未执行": "accent", "未命中": "sub"}


class Svg:
    """Tiny SVG writer that measures every label before it is emitted."""

    def __init__(self, s: dict) -> None:
        self.s = s
        self.parts: list[str] = []
        self.bad: list[str] = []

    def add(self, markup: str) -> None:
        self.parts.append(markup)

    def _w(self, content: str, size: float, kind: str,
           tracking: float | None = None) -> float:
        got = measure(content, size, kind)
        if tracking:
            got += tracking * max(len(content) - 1, 0)
        return got

    def text(self, x: float, y: float, content: str, size: float, fill: str, *,
             anchor: str = "start", weight: int | None = None,
             mono: bool = False, max_w: float | None = None,
             opacity: float | None = None, tracking: float | None = None) -> None:
        kind = "mono" if mono else "cjk"
        if weight:
            kind += "_bold"
        if max_w is not None and self._w(content, size, kind, tracking) > max_w + 0.4:
            self.bad.append(f"{content!r} needs "
                            f"{self._w(content, size, kind):.1f}px > {max_w:.0f}px")
        attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"',
                 f'font-family="{FONT_CSS_MONO if mono else FONT_CSS_SANS}"',
                 f'font-size="{size}"', 'xml:space="preserve"']
        if anchor != "start":
            attrs.append(f'text-anchor="{anchor}"')
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if tracking:
            attrs.append(f'letter-spacing="{tracking}"')
        self.add(f'<text {" ".join(attrs)}>{escape(content)}</text>')

    def rich(self, x: float, y: float, runs: list[tuple[str, str, str]],
             size: float, *, max_w: float | None = None) -> float:
        """Draw runs of (text, fill, kind[mono|cjk + optional bold])."""
        widths = [self._w(text, size, kind) for text, _, kind in runs]
        total = sum(widths)
        if max_w is not None and total > max_w + 0.4:
            self.bad.append(f"{''.join(r[0] for r in runs)!r} needs "
                            f"{total:.1f}px > {max_w:.0f}px")
        cursor = x
        for (content, fill, kind), width in zip(runs, widths):
            mono = kind.startswith("mono")
            attrs = [f'x="{cursor}"', f'y="{y}"', f'fill="{fill}"',
                     f'font-family="{FONT_CSS_MONO if mono else FONT_CSS_SANS}"',
                     f'font-size="{size}"', 'xml:space="preserve"']
            if kind.endswith("_bold"):
                attrs.append('font-weight="700"')
            self.add(f'<text {" ".join(attrs)}>{escape(content)}</text>')
            cursor += width
        return cursor

    def rect(self, x: float, y: float, w: float, h: float, *, fill: str,
             rx: float = 0, stroke: str | None = None, sw: float = 1.5,
             shadow: bool = False, dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"']
        if rx:
            attrs.append(f'rx="{rx}"')
        attrs.append(f'fill="{fill}"')
        if stroke:
            attrs += [f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if shadow:
            attrs.append('filter="url(#soft)"')
        self.add(f'<rect {" ".join(attrs)}/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, *, stroke: str,
             sw: float = 1.5, dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"',
                 f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<line {" ".join(attrs)}/>')

    def path(self, d: str, *, stroke: str, sw: float = 1.5,
             fill: str = "none", dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'd="{d}"', f'fill="{fill}"', f'stroke="{stroke}"',
                 f'stroke-width="{sw}"', 'stroke-linejoin="round"',
                 'stroke-linecap="round"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<path {" ".join(attrs)}/>')

    def circle(self, cx: float, cy: float, r: float, *, fill: str,
               stroke: str | None = None, sw: float = 1.5) -> None:
        attrs = [f'cx="{cx}"', f'cy="{cy}"', f'r="{r}"', f'fill="{fill}"']
        if stroke:
            attrs += [f'stroke="{stroke}"', f'stroke-width="{sw}"']
        self.add(f'<circle {" ".join(attrs)}/>')

    def chip_right(self, right: float, y: float, label: str, fg: str, bg: str,
                   *, size: float = 11, pad: float = 9, height: float = 22,
                   mono: bool = False, weight: int | None = None,
                   stroke: str | None = None) -> float:
        kind = "mono" if mono else "cjk"
        if weight:
            kind += "_bold"
        w = self._w(label, size, kind) + pad * 2
        x = right - w
        self.rect(x, y, w, height, fill=bg, rx=height / 2,
                  stroke=stroke, sw=1)
        self.text(x + pad, y + height / 2 + size * 0.35, label, size, fg,
                  mono=mono, weight=weight)
        return x

    def chip(self, x: float, y: float, label: str, fg: str, bg: str,
             *, size: float = 11, pad: float = 9, height: float = 22,
             mono: bool = False, weight: int | None = None,
             stroke: str | None = None) -> float:
        kind = "mono" if mono else "cjk"
        if weight:
            kind += "_bold"
        w = self._w(label, size, kind) + pad * 2
        self.rect(x, y, w, height, fill=bg, rx=height / 2, stroke=stroke, sw=1)
        self.text(x + pad, y + height / 2 + size * 0.35, label, size, fg,
                  mono=mono, weight=weight)
        return x + w

    def arrow_right(self, x1: float, x2: float, y: float, color: str,
                    sw: float = 1.6, dash: str | None = None) -> None:
        self.path(f"M{x1} {y}H{x2 - 9}", stroke=color, sw=sw, dash=dash)
        self.add(f'<path d="M{x2} {y}l-10 -5v10z" fill="{color}"/>')

    def arrow_down(self, x: float, y1: float, y2: float, color: str,
                   sw: float = 1.6, dash: str | None = None) -> None:
        self.path(f"M{x} {y1}V{y2 - 9}", stroke=color, sw=sw, dash=dash)
        self.add(f'<path d="M{x} {y2}l-5 -10h10z" fill="{color}"/>')

    def svg(self, w: int, h: int, title: str, desc: str) -> str:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" '
                f'height="{h}" viewBox="0 0 {w} {h}" role="img" '
                f'aria-labelledby="title desc">')
        return "\n".join([head, f'<title id="title">{escape(title)}</title>',
                          f'<desc id="desc">{escape(desc)}</desc>',
                          *self.parts, "</svg>"]) + "\n"


def flow_svg(skin: str) -> str:
    f = FLOW[skin]
    W, H = 1100, 660
    v = Svg(f)

    v.add("<defs>")
    v.add(f'<linearGradient id="bg" x1="0" y1="0" x2="0.2" y2="1">'
          f'<stop offset="0" stop-color="{f["bg_from"]}"/>'
          f'<stop offset="1" stop-color="{f["bg_to"]}"/></linearGradient>')
    v.add(f'<filter id="soft" x="-30%" y="-30%" width="160%" height="180%">'
          f'<feDropShadow dx="0" dy="7" stdDeviation="9" '
          f'flood-color="{f["shadow"]}" flood-opacity="{f["shadow_op"]}"/>'
          f'</filter>')
    v.add(f'<pattern id="dots" width="24" height="24" '
          f'patternUnits="userSpaceOnUse">'
          f'<circle cx="1.2" cy="1.2" r="1.2" fill="{f["dot"]}"/></pattern>')
    v.add(f'<pattern id="hatch" width="7" height="7" '
          f'patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
          f'<line x1="0" y1="0" x2="0" y2="7" stroke="{f["faint"]}" '
          f'stroke-width="1" opacity="0.45"/></pattern>')
    v.add("</defs>")

    v.rect(0, 0, W, H, fill="url(#bg)")
    v.rect(0, 0, W, H, fill="url(#dots)", opacity=f["dot_op"])

    # ---- header -------------------------------------------------------------
    v.text(44, 54, NAME, 29, f["text"], weight=700, mono=True, max_w=640)
    v.text(44, 84, "六条规则同读一份台账：命中的进 issues[]，跑不了的进 skipped[]，"
                   "跑过没命中的两栏都不进。", 14.5, f["sub"], max_w=820)
    v.chip_right(1056, 28, "rules/gongwen-flow-check.yaml · v2026.1 · 6 条",
                 f["accent"], f["pill"], size=11.5, pad=12, height=28,
                 mono=True)
    v.text(44, 108, "IN  ·  file | material  ·  JSON / YAML  ·  "
                    "表头 7 栏 + rows[] 8 栏  ·  只读",
           11, f["faint"], max_w=620)
    v.text(1056, 108, "OUT  ·  issues[] · skipped[] · summary · "
                      "markdown + reportJson",
           11, f["faint"], mono=True, anchor="end", max_w=560)
    v.line(44, 120, 1056, 120, stroke=f["rule"], sw=1, opacity=0.75)

    # ---- IN: the register ---------------------------------------------------
    v.rect(44, 132, 256, 394, fill=f["panel"], rx=18, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.text(66, 160, "IN · 收文登记台账", 13, f["text"], weight=700, max_w=170)
    v.chip_right(286, 146, "只读", f["accent"], f["pill"], size=11,
                 height=22)

    v.text(66, 186, "表头 7 栏", 11, f["faint"], max_w=120)
    header_rows = [
        ("docNo", "某发〔2026〕15号", "cjk", 11.5),
        ("title", "关于某某工作的通知", "cjk", 11.5),
        ("receivedAt", "2026-03-02", "mono", 11),
        ("docKind", "通知", "cjk", 11.5),
        ("issuer", "某某机关", "cjk", 11.5),
        ("dueAt", "（未填）", "cjk", 11.5),
        ("urgent", "（未填）", "cjk", 11.5),
    ]
    for index, (token, value, kind, size) in enumerate(header_rows):
        y = 204 + index * 18
        v.text(66, y, token, 11, f["faint"], mono=True, max_w=80)
        color = f["faint"] if value == "（未填）" else f["text"]
        v.text(136, y, value, size, color, mono=(kind == "mono"), max_w=156)

    v.line(66, 324, 286, 324, stroke=f["rule"], sw=1)
    v.text(66, 348, "rows[] · 8 栏", 11, f["faint"], max_w=150)
    col_chips = [("序号", 66), ("环节", 112), ("承办人", 158), ("收文", 214)]
    for label, x in col_chips:
        v.chip(x, 356, label, f["sub"], f["band"], size=11, pad=7, height=20)
    col_chips2 = [("期限", 66), ("办结", 112), ("状态", 158), ("备注", 214)]
    for label, x in col_chips2:
        v.chip(x, 382, label, f["sub"], f["band"], size=11, pad=7, height=20)

    v.line(66, 414, 286, 414, stroke=f["rule"], sw=1)
    v.text(66, 436, "别名归一：大小写 / 空格 / _ / - 不计", 11, f["sub"],
           max_w=210)
    v.text(66, 458, "requireAnyOf：环节 / 状态 / 承办人", 11, f["sub"],
           max_w=210)
    v.text(66, 480, "数字可按字符串读，导出无需清洗", 11, f["faint"],
           max_w=210)
    v.text(66, 500, "至少认得一个已知栏名，否则拒读", 11, f["faint"],
           max_w=210)

    # ---- bench: severity rail + six gates ----------------------------------
    v.rect(336, 132, 464, 394, fill=f["panel"], rx=18, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.text(352, 152, "严重级跟着依据走：本库无 direct 依据，因此不产生 error",
           12, f["text"], weight=700, max_w=432)

    # rail: direct is hatched and empty; the two real ceilings follow
    v.rect(346, 162, 130, 30, fill="url(#hatch)", rx=8,
           stroke=f["rule"], sw=1)
    v.text(352, 176, "direct", 11.5, f["faint"], mono=True, weight=700,
           max_w=60)
    v.text(352, 190, "本库 0 条", 11, f["faint"], max_w=80)
    # tiny lock
    v.rect(452, 172, 10, 9, fill="none", rx=2, stroke=f["faint"], sw=1.3)
    v.path("M454.5 172v-3.2a3 3 0 0 1 6 0V172", stroke=f["faint"], sw=1.3)

    v.line(486, 160, 486, 192, stroke=f["rule"], sw=1)
    v.text(498, 176, "原则性条款", 11.5, f["warn"], weight=700, max_w=120)
    v.text(498, 190, "≤ warn · 4 条", 11, f["sub"], max_w=120)
    v.line(632, 160, 632, 192, stroke=f["rule"], sw=1)
    v.text(644, 176, "本机构配置", 11.5, f["accent"], weight=700, max_w=120)
    v.text(644, 190, "≤ info · 2 条", 11, f["sub"], max_w=130)

    gate_x = (350, 574)
    gate_y = (210, 318, 426)
    gate_w, gate_h = 212, 96
    for index, (rid, severity, runs, kind, state) in enumerate(RULES):
        gx = gate_x[index % 2]
        gy = gate_y[index // 2]
        stroke = f["edge"]
        dash = None
        spine = f["faint"]
        if state == "命中":
            stroke = f["warn"]
            spine = f["warn"]
        elif state == "未执行":
            stroke = f["accent"]
            dash = "5 4"
            spine = f["accent"]
        v.rect(gx, gy, gate_w, gate_h, fill=f["card"], rx=18,
               stroke=stroke, sw=1.5, dash=dash, shadow=True)
        v.rect(gx + 1, gy + 12, 4, gate_h - 24, fill=spine, rx=2,
               opacity=0.85)
        v.text(gx + 16, gy + 26, rid, 14.5, f["text"], mono=True, weight=700,
               max_w=80)
        sev_bg = f["warn_bg"] if severity == "warn" else f["pill"]
        sev_fg = f["warn"] if severity == "warn" else f["accent"]
        v.chip_right(gx + gate_w - 14, gy + 10, severity, sev_fg, sev_bg,
                     size=11, height=21, mono=True, weight=700)
        v.rich(gx + 16, gy + 54, [(t, f["text"], k) for t, k in runs], 13,
               max_w=gate_w - 32)
        v.text(gx + 16, gy + 80, kind, 11.5, f["sub"], mono=True,
               max_w=gate_w - 90)
        state_fg = f[STATE_COLOR[state]]
        v.text(gx + gate_w - 16, gy + 80, state, 11, state_fg, anchor="end",
               max_w=60)
        dot_color = f[STATE_COLOR[state]]
        v.circle(gx + gate_w - 20 - measure(state, 11, "cjk"), gy + 76.5,
                 3, fill=dot_color)

    # bench -> trays
    # one ledger feeds all six gates: a short bus with three stubs, one per row
    v.path("M300 222H320V474", stroke=f["accent"], sw=1.5)
    for y in (258, 366, 474):
        v.arrow_right(320, 336, y, f["accent"], sw=1.4)
    for y in (200, 338, 465):
        v.arrow_right(800, 816, y, f["accent"], sw=1.4)

    # ---- OUT: three states --------------------------------------------------
    # issues[]
    v.rect(816, 132, 240, 136, fill=f["card"], rx=18, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.text(834, 158, "issues[]", 13, f["text"], mono=True, weight=700,
           max_w=110)
    v.chip_right(1042, 144, "1 条 · warn", f["warn"], f["warn_bg"], size=11,
                 height=21)
    v.line(834, 166, 1038, 166, stroke=f["rule"], sw=1)
    v.rect(828, 174, 216, 86, fill=f["warn_bg"], rx=12)
    v.text(838, 192, "GF-001 · warn · 第 1 行", 11, f["warn"], max_w=196)
    v.text(838, 212, "handler 为空", 12.5, f["text"], max_w=196)
    v.text(838, 232, "预期：「handler」应填写", 11, f["sub"], max_w=196)
    v.text(838, 252, "建议：补填承办人", 11, f["faint"], max_w=196)

    # skipped[]
    v.rect(816, 280, 240, 120, fill=f["card"], rx=18, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.text(834, 306, "skipped[]", 13, f["text"], mono=True, weight=700,
           max_w=110)
    v.chip_right(1042, 292, "1 条", f["accent"], f["pill"], size=11, height=21)
    v.line(834, 314, 1038, 314, stroke=f["rule"], sw=1)
    v.text(834, 338, "GF-004 · enum · 未执行", 11, f["accent"], max_w=206)
    v.text(834, 360, "未配置 values：「status」的取值", 11, f["sub"],
           max_w=206)
    v.text(834, 378, "口径由本机构规定 → skipped", 11, f["sub"], max_w=206)
    v.text(834, 394, "本条不执行，也不静默通过", 11, f["faint"], max_w=206)

    # neither list
    v.rect(816, 412, 240, 114, fill=f["card"], rx=18, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.text(834, 438, "未命中", 13, f["text"], weight=700, max_w=90)
    v.chip_right(1042, 424, "4 条", f["faint"], f["band"], size=11, height=21)
    v.line(834, 446, 1038, 446, stroke=f["rule"], sw=1)
    v.chip(834, 458, "GF-002", f["sub"], f["band"], size=11, pad=7,
           height=21, mono=True)
    v.chip(896, 458, "GF-003", f["sub"], f["band"], size=11, pad=7,
           height=21, mono=True)
    v.chip(958, 458, "GF-005", f["sub"], f["band"], size=11, pad=7,
           height=21, mono=True)
    v.chip(1020, 458, "GF-006", f["sub"], f["band"], size=11, pad=7,
           height=21, mono=True)
    v.text(834, 500, "跑过而未命中：两栏都不进", 11.5, f["sub"], max_w=206)
    v.text(834, 518, "不等于未执行", 11, f["faint"], max_w=140)

    # ---- report band --------------------------------------------------------
    v.rect(44, 540, 1012, 90, fill=f["panel"], rx=20, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.line(636, 554, 636, 616, stroke=f["rule"], sw=1)
    v.text(68, 562, "样例 samples/quickstart/input/GF-001-unsafe.json · "
                    "report · makeReport + buildView", 11, f["faint"],
           max_w=548)
    v.text(68, 588, "error 0 · warn 1 · info 0 · issueCount 1 · "
                    "skippedCount 1", 15, f["text"], mono=True, weight=700,
           max_w=548)
    v.text(68, 610, "markdown + reportJson · 措辞守卫 + 免责声明 · "
                    "ruleset 2026.1", 11, f["sub"], max_w=548)

    v.text(660, 566, "复核人", 13.5, f["text"], weight=700, max_w=60)
    v.text(716, 566, "结论不在报告里", 11, f["faint"], max_w=140)
    v.text(660, 590, "不判超期 · 不判督办 · 不判责任 · 不判合规", 11,
           f["sub"], max_w=372)
    v.text(660, 610, "报告只列差异，不定性", 11, f["faint"], max_w=220)

    # ---- footer -------------------------------------------------------------
    v.text(44, 648, "原件永不修改：只读 file | material，"
                    "不写文件、不联网、不调用模型。", 11.5, f["sub"],
           max_w=620)
    v.text(1056, 648, "6 条规则 · 5 种检查 · 4 warn + 2 info", 11,
           f["faint"], anchor="end", max_w=300)

    if v.bad:
        raise SystemExit("FATAL: SVG label overflow:\n  " + "\n  ".join(v.bad))
    return v.svg(
        W, H,
        "dsh-gongwen-flow-check: one register, six rules, three states",
        "A receipt-and-handling register (7 header fields plus 8 row columns) "
        "feeds six rules read from rules/gongwen-flow-check.yaml. GF-001 "
        "checks that the handler column is filled; GF-002 that receivedAt is "
        "not after doneAt; GF-003 that doneAt is not after dueAt; GF-004 that "
        "status comes from the configured values list; GF-005 that docNo "
        "appears once; GF-006 that the header declares title and "
        "receivedAt. Every gate leaves in one of three states: what it found "
        "goes to issues[] (GF-001, one warn on row 1 because handler is "
        "empty), what it could not run goes to skipped[] with its own reason "
        "(GF-004, values unset), and a rule that ran clean enters neither "
        "list (GF-002, GF-003, GF-005, GF-006). The severity rail records the "
        "real ceiling: this pack has no direct basis, so error is never "
        "emitted; principle-based rules cap at warn (four rules) and "
        "institution-configured rules cap at info (two rules). The report "
        "band carries error 0, warn 1, info 0, issueCount 1, skippedCount 1, "
        "ruleset 2026.1, markdown plus reportJson under the wording guard and "
        "disclaimer. The tool only reads file or material, never writes it, "
        "and the verdict stays with the reviewer.",
    )


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for skin in ("light", "dark"):
        for lang in ("zh", "en"):
            hero(lang, skin)
        name = f"{NAME}-flow-v5-{skin}.svg"
        text = flow_svg(skin)
        ET.fromstring(text)  # never ship malformed XML
        with open(os.path.join(OUT, name), "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(text)
        print(f"wrote {name} (1100x660)")


if __name__ == "__main__":
    main()
