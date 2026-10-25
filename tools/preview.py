# Approximate preview of every clock style, rendered from the generated AdaptiveClock.ini (no Rainmeter needed).
#   python preview.py            -> ../docs/previews/NN-name.png, ../docs/contact-sheet-N.png, prints layout warnings
#   python preview.py 57 58      -> only those styles
# Fonts are stand-ins (DejaVu instead of Segoe UI / Consolas) so widths differ a little; use it to spot overlaps,
# text outside the clock area and shapes that do not draw, not for pixel-exact work.   Needs: matplotlib, pillow.
# Author: Amika Alankara  (MIT License)
import math, os, re, sys, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Wedge, PathPatch, Rectangle
from matplotlib.path import Path
from matplotlib.transforms import Affine2D

HERE = os.path.dirname(os.path.abspath(__file__))
INI = os.path.join(HERE, "..", "AdaptiveClock", "AdaptiveClock.ini")
LUA = os.path.join(HERE, "..", "AdaptiveClock", "AdaptiveClock.lua")
OUT = os.path.join(HERE, "..", "docs")
W, H, CLOCK_BOTTOM = 440, 520, 440

# ------------------------------------------------------------------ ini parsing
def parse(path):
    secs, cur = {}, None
    for line in open(path, encoding="utf-8").read().split("\n"):
        line = line.rstrip("\r")
        m = re.match(r"^\[([^\]]+)\]$", line)
        if m:
            cur = secs.setdefault(m.group(1), {})
        elif cur is not None and "=" in line and not line.startswith(";"):
            k, v = line.split("=", 1)
            cur[k.strip()] = v.strip()
    return secs

SECS = parse(INI)
VARS = dict(SECS["Variables"])
T = dict(h=10, m=8, s=37)
sec_f, min_f, hr_f = T["s"] / 60, (T["m"] * 60 + T["s"]) / 3600, ((T["h"] % 12) * 3600 + T["m"] * 60 + T["s"]) / 43200
day_f = (T["h"] * 3600 + T["m"] * 60 + T["s"]) / 86400

def set_palette(ink="255,255,255", color=None, color2=None):
    color = color or ink
    color2 = color2 or color
    VARS.update(Ink=ink, InkDim=ink + ",190", InkMid=ink + ",120", InkSoft=ink + ",60", Color=color, ColorDim=color + ",190",
                ColorMid=color + ",120", ColorSoft=color + ",60", Color2=color2, Color2Soft=color2 + ",70",
                GradA="120,140,255", GradB="255,130,200", SecRad=f"{sec_f*2*math.pi-math.pi/2:.5f}",
                MinRad=f"{min_f*2*math.pi-math.pi/2:.5f}", HourRad=f"{hr_f*2*math.pi-math.pi/2:.5f}",
                DayRad=f"{math.pi+day_f*math.pi:.5f}", DayF=f"{day_f:.5f}", SunRad=f"{math.pi+0.55*math.pi:.5f}",
                PomoFrac="0.62", PomoText="14:20", PomoLabel="FOCUS", PomoBtn=">", AlarmText="Alarm 07:00  ON",
                CalToday="25", WeekIdx="4", WkH1="Mo", WkH2="Tu", WkH3="We", WkH4="Th", WkH5="Fr", WkH6="Sa", WkH7="Su", QHf="0", QHc="1")
    for i, d in enumerate("MoTuWeThFrSaSu", 0):
        pass
    G = {"0": ["1111","1001","1001","1001","1111"], "1": ["0110","0010","0010","0010","0111"], "8": ["1111","1001","1111","1001","1111"]}
    for d, ch in enumerate("1008"):
        for r in range(5):
            for c in range(4):
                VARS[f"PX{d*20+r*4+c+1}"] = "255" if G[ch][r][c] == "1" else "40"
    VARS["PX81"] = VARS["PX82"] = "255"
    for c, name in enumerate(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"], 1):
        VARS[f"CalH{c}"] = name
    off = 3                                             # October 2026 starts on a Thursday (Monday first -> offset 3)
    for i in range(1, 43):
        d = i - off
        VARS[f"CalD{i}"] = str(d) if 1 <= d <= 31 else ""

MEAS = dict(mPomoLabel="FOCUS", mAlarmText="Alarm 07:00  ON", mQPlain="The best time to plant a tree was twenty years ago. The second best time is now.", mQAuthor="\u2014 Proverb", mWkText="2d 05h", mWkF=0.42, mWkDay=4, mWeekNo=43,
            mBdayDays=62, mBdayText="62 days until your birthday", mDayLen="11h 55m", mLblWeekendLeft="until the weekend", mLblDaylight="of daylight", mSecN=37, mLn8=6, mCi0="passed", mCi1="passed", mCi2="running", mCi3="queued", mCore0=23, mCore1=41, mCore2=12, mCore3=68,
            mHx0="0000  31 30 3a 30  38 3a 33 37  |10:08:37|", mHx1="0008  20 54 68 75  20 32 32 20  | Thu 22 |",
            mHx2="0010  4f 63 74 20  32 30 32 36  |Oct 2026|", mH="10", mM="08", mS="37", mDow="Thursday", mDowS="Thu", mDnum="22", mMon="October", mMonS="Oct", mYear="2026",
            mSecF=sec_f, mMinF=min_f, mHrF=hr_f, mDayF=day_f, mOne=1, mDHT=1, mDHU=0, mDMT=0, mDMU=8, mDST=3, mDSU=7,
            mHexH="0x0A", mHexM="0x08", mHexS="0x25", mBinH="01010", mBinM="001000", mBinS="100101",
            mEpoch="1792650517", mISO="2026-10-22T10:08:37", mSha="a3f9c21", mCPU=23, mRAM=61, mUptime="2d 04h 15m",
            mGreet="Good morning", mGreetIcon="\u2600", mYearPct="80%", mYearF=0.80, mDaysLeft=70, mAmPm="", mCursor="_",
            mQMark="\u201c", mQBody="\u201cWell begun is half done.\u201d", mQWho="\u2014 Proverb",
            mLblHour="HOUR", mLblMinute="MINUTE", mLblSecond="SECOND", mLblHours="HOURS", mLblMinutes="MINUTES",
            mLblSeconds="SECONDS", mLblWorld="World Time", mLblDaysLeft="70 days left", mLblDaysLeftYear="70 days left in 2026",
            mLblYearDone="of 2026 is done", mLblOfYear="of 2026", mLblSecondsLow="seconds", mLblSunrise="Sunrise",
            mLblSunset="Sunset", mWName="NEW YORK\nLONDON\nDUBAI\nTOKYO\nSYDNEY", mWDay="THU\nTHU\nTHU\nTHU\nTHU",
            mWTime="01:08\n06:08\n10:08\n15:08\n21:08", mWordA="TEN PAST", mWordB="TEN", mWxIcon="\u2601", mWxTempTxt="23\u00b0C",
            mWxText="Overcast", mSunRise="06:12", mSunSet="18:20", mSunF=0.55, mSunNote="", mBatTxt="Charging", mBatPct=86,
            mPomoF=0.62, mMoonIcon="\u25d1", mMoonName="Waxing gibbous", mMoonPct="73%", mMoonF=0.39)
for k, nm in enumerate(("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"), 1):
    MEAS[f"mCalH{k}"] = nm
    MEAS[f"mWkH{k}"] = nm
for k in range(5):
    MEAS[f"mLogHash{k}"] = ["a3f9c21", "7be41d0", "19c8e5a", "e02b7f3", "5d6a912"][k]
    MEAS[f"mLogTime{k}"] = f"10:{8 - k:02d}"
import random
random.seed(4)
for k in range(10):
    MEAS[f"mRain{k}"] = "\n".join(random.choice("ABCDEF0123456789<>/{}=;") for _ in range(15))
for key, digit in (("mDHT", 1), ("mDHU", 0), ("mDMT", 0), ("mDMU", 8), ("mDST", 3), ("mDSU", 7)):
    pass
for c, key in enumerate(["mDHT", "mDHU", "mDMT", "mDMU", "mDST", "mDSU"]):
    for b in range(4):
        MEAS[f"mBit{c}_{b}"] = (MEAS[key] >> b) & 1

def fn_env():
    import math as m
    return dict(Cos=m.cos, Sin=m.sin, Trunc=lambda x: int(x), BitAnd=lambda a, b: int(a) & int(b),
                BitRShift=lambda a, b: int(a) >> int(b), Abs=abs, Max=max, Min=min, Round=round)

def subst(text):
    for _ in range(3):
        text = re.sub(r"#(\w+)#", lambda m: VARS.get(m.group(1), m.group(0)), text)
    return text

def measure_value(name, fmt):
    v = MEAS.get(name, 0)
    if fmt == "%":
        return str(int(round(float(v) * (1 if name in ("mRAM", "mCPU") else 100) / (1 if name in ("mRAM", "mCPU") else 1))))
    if fmt is not None and fmt.isdigit():
        return f"{float(v):.{int(fmt)}f}"
    return str(v)

def fill_measures(text):
    return re.sub(r"\[(m\w+?)(?::([^\]]*))?\]", lambda m: measure_value(m.group(1), m.group(2)) if m.group(1) in MEAS else m.group(0), text)

def _balanced(t):
    d = 0
    for ch in t:
        d += (ch == "(") - (ch == ")")
        if d < 0: return False
    return d == 0

def evaluate(expr):
    expr = fill_measures(subst(expr))
    expr = expr.replace("%", "%").replace("?", " if ", 1) if False else expr
    inner = expr.strip()
    while inner.startswith('(') and inner.endswith(')') and inner.count('(') == inner.count(')') and _balanced(inner[1:-1]):
        inner = inner[1:-1].strip()
    expr = inner
    m = re.match(r"^(.*)\?(.*):(.*)$", expr)
    try:
        if m:
            cond = eval(m.group(1), {"__builtins__": {}}, fn_env())
            return float(eval(m.group(2 if cond else 3), {"__builtins__": {}}, fn_env()))
        return float(eval(expr, {"__builtins__": {}}, fn_env()))
    except Exception:
        return 0.0

def num(s):
    s = fill_measures(subst(str(s))).strip()
    if s.startswith("("):
        return evaluate(s)
    try:
        return float(s)
    except ValueError:
        return evaluate(s)

def split_args(s):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(": depth += 1
        if ch == ")": depth -= 1
        if ch == "," and depth == 0:
            out.append(cur); cur = ""
        else:
            cur += ch
    out.append(cur)
    return [a.strip() for a in out]

def color(c, default=(0, 0, 0, 0)):
    c = subst(c).strip()
    try:
        p = [float(x) for x in c.split(",")]
    except ValueError:
        return default
    if len(p) == 3: p.append(255)
    return (p[0] / 255, p[1] / 255, p[2] / 255, p[3] / 255)

# ------------------------------------------------------------------ drawing
FONTS = {"consolas": "DejaVu Sans Mono", "georgia": "DejaVu Serif"}
def font_family(face):
    f = subst(face).lower()
    if "consolas" in f or "mono" in f: return "DejaVu Sans Mono"
    if "georgia" in f: return "DejaVu Serif"
    return "DejaVu Sans"

def draw_shape_meter(ax, opts, hit):
    shapes = [(k, v) for k, v in opts.items() if re.match(r"^Shape\d*$", k)]
    shapes.sort(key=lambda kv: int(kv[0][5:] or 1))
    ox, oy = num(opts.get("X", 0)), num(opts.get("Y", 0))
    for _, spec in shapes:
        parts = [p.strip() for p in spec.split("|")]
        kind, _, args = parts[0].partition(" ")
        fill, stroke, sw, rot, grad = None, None, 1.0, None, None
        for mod in parts[1:]:
            mk, _, mv = mod.partition(" ")
            mk = mk.strip()
            if mk == "Fill":
                if mv.startswith("Color"): fill = color(mv[5:])
                elif mv.startswith("LinearGradient"):
                    g = subst(opts.get(mv.split()[1], "")).split("|")
                    cols = [c.split(";")[-1] if ";" in c else c for c in g[1:]]
                    try:
                        fill = color(g[1].split(";")[0]) if len(g) > 1 else None
                    except Exception:
                        fill = None
                    if fill is None: fill = (0.5, 0.5, 0.5, 1)
            elif mk == "Stroke" and mv.startswith("Color"): stroke = color(mv[5:])
            elif mk == "StrokeWidth": sw = num(mv)
            elif mk == "Rotate":
                r = split_args(mv)
                rot = (num(r[0]), num(r[1]) if len(r) > 1 else None, num(r[2]) if len(r) > 2 else None)
        tr = Affine2D().translate(ox, oy)
        patch = None
        a = split_args(args)
        if kind == "Rectangle":
            x, y, w, h = [num(v) for v in a[:4]]
            r = num(a[4]) if len(a) > 4 else 0
            r = min(r, w / 2, h / 2)
            if w <= 0 or h <= 0: continue
            patch = FancyBboxPatch((x + r, y + r), max(w - 2 * r, 0.01), max(h - 2 * r, 0.01),
                                   boxstyle=f"round,pad={r},rounding_size={r}" if r > 0 else "square,pad=0")
            bbox = (x, y, x + w, y + h)
        elif kind == "Ellipse":
            x, y, rx = num(a[0]), num(a[1]), num(a[2])
            ry = num(a[3]) if len(a) > 3 else rx
            if rx <= 0 or ry <= 0: continue
            patch = Ellipse((x, y), 2 * rx, 2 * ry)
            bbox = (x - rx, y - ry, x + rx, y + ry)
        elif kind == "Line":
            x1, y1, x2, y2 = [num(v) for v in a[:4]]
            ln = plt.Line2D([x1, x2], [y1, y2], color=stroke or (1, 1, 1, 1), linewidth=sw * 0.72, solid_capstyle="butt")
            ln.set_transform(tr + ax.transData)
            ax.add_line(ln)
            continue
        elif kind == "Path":
            name = args.strip()
            spec2 = subst(opts.get(name, ""))
            verts, codes = [], []
            for j, seg in enumerate(s.strip() for s in spec2.split("|")):
                if j == 0:
                    px, py = [num(v) for v in split_args(seg)]
                    verts.append((px, py)); codes.append(Path.MOVETO)
                elif seg.startswith("LineTo"):
                    px, py = [num(v) for v in split_args(seg[6:])]
                    verts.append((px, py)); codes.append(Path.LINETO)
                elif seg.startswith("CurveTo"):
                    v = [num(x) for x in split_args(seg[7:])]
                    verts += [(v[2], v[3]), (v[4], v[5]), (v[0], v[1])]
                    codes += [Path.CURVE4] * 3
                elif seg.startswith("ClosePath"):
                    verts.append(verts[0]); codes.append(Path.CLOSEPOLY)
            if len(verts) < 2: continue
            patch = PathPatch(Path(verts, codes))
            bbox = (min(v[0] for v in verts), min(v[1] for v in verts), max(v[0] for v in verts), max(v[1] for v in verts))
        if patch is None: continue
        if rot:
            cx, cy = (rot[1], rot[2]) if rot[1] is not None else ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
            tr = Affine2D().rotate_deg_around(cx, cy, rot[0]) + tr
        patch.set_transform(tr + ax.transData)
        patch.set_facecolor(fill if fill else (0, 0, 0, 0))
        patch.set_edgecolor(stroke if (stroke and sw > 0) else (0, 0, 0, 0))
        patch.set_linewidth(max(sw, 0) * 0.72 if stroke else 0)
        ax.add_patch(patch)

def draw_roundline(ax, o):
    x, y, w, h = [num(o.get(k, 0)) for k in "XYWH"]
    cx, cy = x + w / 2, y + h / 2
    v = float(MEAS.get(o.get("MeasureName", ""), 0))
    if o.get("MeasureName") in ("mBatPct",): v /= 100
    a0, rot = num(o.get("StartAngle", 0)), num(o.get("RotationAngle", 6.2832))
    ls, ll, lw = num(o.get("LineStart", 0)), num(o.get("LineLength", 20)), num(o.get("LineWidth", 1))
    col = color(o.get("LineColor", "255,255,255"))
    ang = a0 + rot * v
    if o.get("Solid") == "1":
        if abs(rot * v) < 1e-6: return
        wd = max(ll - ls, 0.5)
        ax.add_patch(Wedge((cx, cy), ll, math.degrees(a0), math.degrees(ang), width=wd, facecolor=col, edgecolor="none"))
    else:
        ln = plt.Line2D([cx + ls * math.cos(ang), cx + ll * math.cos(ang)], [cy + ls * math.sin(ang), cy + ll * math.sin(ang)],
                        color=col, linewidth=lw * 0.72, solid_capstyle="round")
        ax.add_line(ln)

def draw_bar(ax, o):
    x, y, w, h = [num(o.get(k, 0)) for k in "XYWH"]
    v = float(MEAS.get(o.get("MeasureName", ""), 0))
    if o.get("MeasureName") in ("mCPU", "mRAM") or str(o.get("MeasureName")).startswith("mCore"): v /= 100
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color(o.get("SolidColor", "0,0,0,0")), edgecolor="none"))
    ax.add_patch(Rectangle((x, y), w * max(0, min(1, v)), h, facecolor=color(o.get("BarColor", "255,255,255")), edgecolor="none"))

TEXTS = []
def draw_string(ax, name, o):
    text = fill_measures(subst(o.get("Text", "")))
    if text.strip() == "":
        return
    size = num(o.get("FontSize", 10))
    fam = font_family(o.get("FontFace", "Segoe UI"))
    if o.get("StringCase", "") == "Upper": text = text.upper()
    if o.get("StringCase", "") == "Lower": text = text.lower()
    x, y = num(o.get("X", 0)), num(o.get("Y", 0))
    al = o.get("StringAlign", "Left")
    m = re.match(r"(Left|Right|Center)(Top|Bottom|Center)?", al)
    hz = {"Left": "left", "Right": "right", "Center": "center"}[m.group(1)] if m else "left"
    vt = {"Center": "center", "Bottom": "bottom"}.get(m.group(2) if m else None, "top")
    wlim = num(o["W"]) if "W" in o else None
    clip = o.get("ClipString", "0")
    scale = 0.93 if fam != "DejaVu Sans Mono" else 0.91
    px = size * 1.333 * scale
    if wlim and clip == "2":
        cw = px * (0.60 if fam == "DejaVu Sans Mono" else 0.55)
        text = "\n".join(textwrap.wrap(text, max(4, int(wlim / cw))))
    weight = "bold" if "Bold" in o.get("StringStyle", "") else "normal"
    style = "italic" if "Italic" in o.get("StringStyle", "") else "normal"
    col = color(o.get("FontColor", "255,255,255"), (1, 1, 1, 1))
    t = ax.text(x, y, text, fontsize=px * 0.72, family=fam, color=col, ha=hz, va=vt, weight=weight, style=style,
                linespacing=1.15)
    TEXTS.append((name, t, wlim, clip))

def render(n, name, out_path, light=False, theme="Neutral"):
    TEXTS.clear()
    if theme == "Girl": set_palette("255,255,255", "255,105,180", "187,134,252")
    elif theme == "Boy": set_palette("255,255,255", "56,152,255", "0,224,208")
    else: set_palette("0,0,0" if light else "255,255,255")
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    bg = (0.93, 0.93, 0.95) if light else (0.22, 0.26, 0.34)
    fig.patch.set_facecolor(bg)
    ax.add_patch(Rectangle((0, 0), W, H, facecolor=bg, edgecolor="none"))
    ax.plot([0, W], [CLOCK_BOTTOM, CLOCK_BOTTOM], color=(1, 0, 0, 0.18), linewidth=0.6)
    prefix = f"S{n}_"
    for sec_name, o in SECS.items():
        if not (sec_name.startswith(prefix) or sec_name.startswith("QF_")): continue
        kind = o.get("Meter")
        try:
            if kind == "Shape": draw_shape_meter(ax, o, None)
            elif kind == "Roundline": draw_roundline(ax, o)
            elif kind == "Bar": draw_bar(ax, o)
            elif kind == "String": draw_string(ax, sec_name, o)
        except Exception as e:                                   # keep going, report
            print(f"  ! {sec_name}: {type(e).__name__}: {e}")
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    warns = []
    boxes = []
    for nm, t, wlim, clip in TEXTS:
        bb = t.get_window_extent(r)
        x0, x1 = bb.x0, bb.x1
        y0, y1 = H - bb.y1, H - bb.y0
        boxes.append((nm, x0, y0, x1, y1))
        in_quote = nm.startswith("QF_")
        if x0 < -1 or x1 > W + 1:
            warns.append(f"text '{t.get_text()[:24]}' ({nm}) leaves the skin horizontally ({x0:.0f}..{x1:.0f})")
        if not in_quote and y1 > CLOCK_BOTTOM + 2:
            warns.append(f"text '{t.get_text()[:24]}' ({nm}) runs into the quote area (bottom {y1:.0f})")
        if y0 < -1:
            warns.append(f"text '{t.get_text()[:24]}' ({nm}) is above the skin")
        if wlim and clip == "1" and (x1 - x0) > wlim + 6:
            warns.append(f"text '{t.get_text()[:24]}' ({nm}) is wider than its box ({x1-x0:.0f} > {wlim:.0f}) and will be clipped")
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            if a[0].startswith("QF_") or b[0].startswith("QF_"): continue
            ox = min(a[3], b[3]) - max(a[1], b[1]); oy = min(a[4], b[4]) - max(a[2], b[2])
            if ox > 4 and oy > 4:
                warns.append(f"texts overlap: '{TEXTS[i][1].get_text()[:16]}' ({a[0]}) and '{TEXTS[j][1].get_text()[:16]}' ({b[0]}) by {ox:.0f}x{oy:.0f}px")
    fig.savefig(out_path, dpi=100, facecolor=bg)
    plt.close(fig)
    return warns

def names():
    lua = open(LUA, encoding="utf-8-sig").read()
    block = lua[lua.index("local NAMES = {"):lua.index("-- Styles that only appear")]
    return re.findall(r"'([^']+)'", block)

def contact_sheets(nlist, out_dir):
    from PIL import Image, ImageDraw
    per, cols = 12, 4
    tw, th = 330, 390
    sheets = []
    for s in range(0, len(nlist), per):
        chunk = nlist[s:s + per]
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw, rows * (th + 22)), (20, 22, 28))
        d = ImageDraw.Draw(sheet)
        for k, (n, nm) in enumerate(chunk):
            im = Image.open(os.path.join(out_dir, "previews", f"{n:02d}-{re.sub(r'[^A-Za-z0-9]+', '-', nm).strip('-')}.png")).resize((tw, int(tw * H / W)))
            r, c = divmod(k, cols)
            sheet.paste(im, (c * tw, r * (th + 22) + 20))
            d.text((c * tw + 6, r * (th + 22) + 4), f"{n}  {nm}", fill=(235, 235, 240))
        p = os.path.join(out_dir, f"contact-sheet-{s // per + 1}.png")
        sheet.save(p)
        sheets.append(p)
    return sheets

if __name__ == "__main__":
    nm = names()
    pick = [int(a) for a in sys.argv[1:]] or list(range(1, len(nm) + 1))
    os.makedirs(os.path.join(OUT, "previews"), exist_ok=True)
    total = 0
    done = []
    for n in pick:
        name = nm[n - 1]
        theme = "Girl" if 37 <= n <= 40 or 72 <= n <= 77 else "Boy" if 41 <= n <= 44 or 78 <= n <= 83 else "Neutral"
        path = os.path.join(OUT, "previews", f"{n:02d}-{re.sub(r'[^A-Za-z0-9]+', '-', name).strip('-')}.png")
        warns = render(n, name, path, theme=theme)
        done.append((n, name))
        if warns:
            total += len(warns)
            print(f"[{n}] {name}")
            for w in warns:
                print("   -", w)
    print("styles rendered:", len(done), "| warnings:", total)
    if len(sys.argv) == 1:
        print("\n".join(contact_sheets(done, OUT)))
