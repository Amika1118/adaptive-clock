# Regenerates AdaptiveClock/AdaptiveClock.ini  (run from the tools folder: python gen_ini.py)
import math
from math import cos, sin, pi as PI

S = []          # style sections
CX = CY = 220
W, H = 440, 520

def sec(i, name, kind, var="H", **o):
    L = [f"[S{i}_{name}]", f"Meter={kind}"]
    L += [f"{k}={v}" for k, v in o.items()]
    L += [f"Hidden=#{var}{i}#", "DynamicVariables=1"]
    S.append("\n".join(L))

def shp(i, name, shapes):
    o = {"X": 0, "Y": 0, "W": W, "H": H}
    for n, s in enumerate(shapes):
        o["Shape" if n == 0 else f"Shape{n+1}"] = s
    sec(i, name, "Shape", **o)

def txt(i, name, text, x, y, size, color="#Color#", align="CenterCenter",
        face="Segoe UI Light", style=None, **extra):
    o = dict(X=x, Y=y, Text=text, FontFace=face, FontSize=size, FontColor=color,
             StringAlign=align, AntiAlias=1)
    if style: o["StringStyle"] = style
    o.update(extra)
    sec(i, name, "String", **o)

def hand(i, name, x, y, L, meas, width, color, start=-PI/2, rot=2*PI, lstart=0, solid=0):
    o = dict(X=x-L, Y=y-L, W=2*L, H=2*L, MeasureName=meas,
             StartAngle=f"{start:.4f}", RotationAngle=f"{rot:.4f}",
             LineStart=lstart, LineLength=L, LineWidth=width, LineColor=color, AntiAlias=1)
    if solid: o["Solid"] = 1
    sec(i, name, "Roundline", **o)

def ring(i, name, x, y, ro, ri, meas, color, start=-PI/2, rot=2*PI):
    hand(i, name, x, y, ro, meas, 1, color, start, rot, lstart=ri, solid=1)

def tick(x, y, r1, r2, a, w, col):
    return (f"Line {x+r1*cos(a):.1f},{y+r1*sin(a):.1f},{x+r2*cos(a):.1f},{y+r2*sin(a):.1f}"
            f" | StrokeWidth {w} | Stroke Color {col}")

def dial_ticks(x, y, r1, r2, col, big=None, n=60, w1=1, w2=3):
    out = []
    for k in range(n):
        a = k / n * 2 * PI - PI / 2
        isbig = (k % (n // 12) == 0)
        out.append(tick(x, y, (big if (isbig and big) else r1), r2, a, w2 if isbig else w1, col))
    return out

def mdot(x, y, r, ang, rad, col):
    return (f"Ellipse ({x}+{r}*Cos({ang})),({y}+{r}*Sin({ang})),{rad}"
            f" | Fill Color {col} | StrokeWidth 0")

def circle(x, y, r, fill="0,0,0,0", sw=0, stroke="0,0,0,0"):
    return f"Ellipse {x},{y},{r} | Fill Color {fill} | StrokeWidth {sw} | Stroke Color {stroke}"

WHITE = "245,245,245"

# ------------------------------------------------------------------ 1  Chronograph
i = 1
sh = [circle(220, 220, 205, "12,12,14", 5, "190,190,195"),
      circle(220, 220, 170, sw=1, stroke="110,110,115")]
sh += dial_ticks(220, 220, 180, 196, "235,235,235", big=172)
shp(i, "Dial", sh)
subs = [(140, 222, "mSecF"), (300, 222, "mMinF"), (220, 300, "mHrF")]
sh = []
for x, y, m in subs:
    sh.append(circle(x, y, 44, "232,232,226", 5, "35,35,38"))
    sh += dial_ticks(x, y, 34, 40, "30,30,30", n=12, w1=1, w2=2)
shp(i, "Subdials", sh)
for n, (x, y, m) in enumerate(subs):
    hand(i, f"SubHand{n}", x, y, 32, m, 2, "20,20,20")
txt(i, "Brand", "CHRONOGRAPH", 220, 125, 13, "235,235,235", face="Segoe UI", style="Bold")
txt(i, "Date", "[mDowS] [mDnum]", 220, 365, 15, "235,235,235", face="Segoe UI")
hand(i, "Hour", 220, 220, 100, "mHrF", 7, WHITE)
hand(i, "Min", 220, 220, 150, "mMinF", 5, WHITE)
hand(i, "Sec", 220, 220, 172, "mSecF", 2, "225,30,30")
shp(i, "Hub", [circle(220, 220, 8, "225,30,30")])

# ------------------------------------------------------------------ 2  Grey bubbles
i = 2
shp(i, "Bubbles", [circle(130, 320, 75, "210,210,215,90"),
                   circle(235, 240, 48, "160,160,168,110"),
                   circle(305, 170, 30, "110,110,118,140")])
txt(i, "H", "[mH]", 130, 320, 80, "255,255,255")
txt(i, "M", "[mM]", 235, 240, 50, "255,255,255")
txt(i, "S", "[mS]", 305, 170, 28, "255,255,255")
txt(i, "Dow", "[mDowS]", 240, 62, 22, "#Color#", align="Left")
txt(i, "Date", "[mDnum]  [mMonS]", 240, 100, 44, "245,245,245", align="Left")

# ------------------------------------------------------------------ 3  World time
i = 3
shp(i, "Ring", [circle(220, 220, 170, sw=2, stroke="#ColorMid#"),
                mdot(220, 220, 170, "#HourRad#", 6, "#Color#")])
txt(i, "Title", "World Time", 220, 140, 36, "245,245,245", face="Segoe UI Semibold")
txt(i, "Names", "[mWName]", 100, 235, 13, "235,235,235", align="LeftCenter", face="Segoe UI")
txt(i, "Days", "[mWDay]", 220, 235, 13, "#ColorDim#", align="CenterCenter", face="Segoe UI")
txt(i, "Times", "[mWTime]", 340, 235, 13, "235,235,235", align="RightCenter", face="Segoe UI")

# ------------------------------------------------------------------ 4  Halo
i = 4
ring(i, "Day", 220, 220, 150, 100, "mDayF", "#ColorMid#")
sh = [circle(220, 220, 150, sw=1, stroke="255,255,255,80"),
      circle(220, 220, 100, sw=1, stroke="255,255,255,80"),
      circle(220, 220, 70, "0,0,0,60", 3, "#ColorDim#")]
sh += dial_ticks(220, 220, 60, 66, "#ColorDim#", n=12, w2=2)
shp(i, "Face", sh)
hand(i, "Hour", 220, 220, 38, "mHrF", 3, "#ColorDim#")
hand(i, "Min", 220, 220, 56, "mMinF", 2, "#ColorDim#")
hand(i, "Sec", 220, 220, 62, "mSecF", 1, "255,255,255")
txt(i, "Time", "[mH]:[mM]", 220, 395, 26, "245,245,245")

# ------------------------------------------------------------------ 5  Roman
i = 5
shp(i, "Dial", [circle(220, 220, 170, "120,120,120,110", 2, "255,255,255,90"),
                circle(220, 220, 112, sw=1, stroke="255,255,255,70"),
                circle(220, 150, 24, "255,255,255,40", 2, "70,70,70")])
rom = ["XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
for k, r in enumerate(rom):
    a = k / 12 * 2 * PI - PI / 2
    txt(i, f"N{k}", r, f"{220+140*cos(a):.1f}", f"{220+140*sin(a):.1f}", 17,
        "240,240,240", face="Georgia")
hand(i, "SubSec", 220, 150, 18, "mSecF", 1, "50,50,50")
hand(i, "Hour", 220, 220, 75, "mHrF", 8, "55,55,55")
hand(i, "Min", 220, 220, 110, "mMinF", 6, "55,55,55")
shp(i, "Hub", [circle(220, 220, 9, "55,55,55")])

# ------------------------------------------------------------------ 6  Bubble rings
i = 6
rings = [(130, 315, 78, "mHrF", "[mH]", 66), (230, 215, 50, "mMinF", "[mM]", 42),
         (300, 135, 32, "mSecF", "[mS]", 26)]
shp(i, "Tracks", [circle(x, y, r, sw=3, stroke="255,255,255,70") for x, y, r, *_ in rings])
for n, (x, y, r, m, t, fs) in enumerate(rings):
    ring(i, f"Arc{n}", x, y, r + 3, r - 3, m, "255,255,255")
    txt(i, f"T{n}", t, x, y, fs, "255,255,255", face="Segoe UI Semibold")

# ------------------------------------------------------------------ 7  Words
i = 7
txt(i, "A", "[mWordA]", 220, 175, 40, "#ColorDim#")
txt(i, "B", "[mWordB]", 220, 265, 100, "245,245,245", face="Segoe UI Semibold")
shp(i, "Line", [tick(0, 0, 0, 0, 0, 0, "0,0,0,0").replace("Line 0.0,0.0,0.0,0.0", "Line 170,330,270,330")
                .replace("StrokeWidth 0", "StrokeWidth 2").replace("0,0,0,0", "#ColorMid#")])

# ------------------------------------------------------------------ 8  Digital
i = 8
txt(i, "Time", "[mH]:[mM]", 220, 190, 130, "245,245,245")
txt(i, "Sec", "[mS]", 220, 285, 36, "#Color#")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 345, 20, "#ColorDim#")

# ------------------------------------------------------------------ 9  Concentric rings
i = 9
cr = [(180, "mSecF", "#Color#"), (150, "mMinF", "#ColorDim#"), (120, "mHrF", "#ColorMid#")]
shp(i, "Tracks", [circle(220, 220, r - 7, sw=14, stroke="#ColorSoft#") for r, *_ in cr])
for n, (r, m, c) in enumerate(cr):
    ring(i, f"Arc{n}", 220, 220, r, r - 14, m, c)
txt(i, "Time", "[mH]:[mM]", 220, 215, 52, "245,245,245")
txt(i, "Date", "[mDowS] [mDnum] [mMonS]", 220, 262, 16, "#ColorDim#")

# ------------------------------------------------------------------ 10  Orbit dots
i = 10
shp(i, "Orbits", [circle(220, 220, 170, sw=1, stroke="#ColorSoft#"),
                  circle(220, 220, 135, sw=1, stroke="#ColorSoft#"),
                  circle(220, 220, 100, sw=1, stroke="#ColorSoft#"),
                  mdot(220, 220, 170, "#SecRad#", 7, "#Color#"),
                  mdot(220, 220, 135, "#MinRad#", 10, "#ColorDim#"),
                  mdot(220, 220, 100, "#HourRad#", 14, "255,255,255")])
txt(i, "Time", "[mH]:[mM]", 220, 215, 44, "245,245,245")
txt(i, "Date", "[mDowS] [mDnum]", 220, 255, 15, "#ColorDim#")

# ------------------------------------------------------------------ 11  Classic analog
i = 11
sh = [circle(220, 220, 195, sw=2, stroke="255,255,255,200")]
sh += dial_ticks(220, 220, 175, 188, "255,255,255", big=165)
shp(i, "Dial", sh)
for t, a in (("12", 0), ("3", 1), ("6", 2), ("9", 3)):
    ang = a * PI / 2 - PI / 2
    txt(i, f"N{t}", t, f"{220+140*cos(ang):.1f}", f"{220+140*sin(ang):.1f}", 30,
        "245,245,245", face="Segoe UI Semilight")
hand(i, "Hour", 220, 220, 90, "mHrF", 6, WHITE)
hand(i, "Min", 220, 220, 130, "mMinF", 4, WHITE)
hand(i, "Sec", 220, 220, 160, "mSecF", 1, "#Color#")
shp(i, "Hub", [circle(220, 220, 7, "#Color#")])

# ------------------------------------------------------------------ 12  Bars
i = 12
txt(i, "Time", "[mH]:[mM]", 220, 140, 80, "245,245,245")
for n, (lab, m, y, c) in enumerate((("HOUR", "mHrF", 235, "#Color#"),
                                    ("MINUTE", "mMinF", 285, "#ColorDim#"),
                                    ("SECOND", "mSecF", 335, "#ColorMid#"))):
    txt(i, f"L{n}", lab, 70, y - 14, 10, "#ColorDim#", align="Left", face="Segoe UI")
    sec(i, f"Bar{n}", "Bar", X=70, Y=y, W=300, H=8, MeasureName=m, BarColor=c,
        SolidColor="#ColorSoft#", BarOrientation="Horizontal")

# ------------------------------------------------------------------ 13  Sun path
i = 13
hand(i, "Track", 220, 310, 165, "mOne", 1, "#ColorSoft#", start=PI, rot=PI, lstart=161, solid=1)
hand(i, "Prog", 220, 310, 165, "mDayF", 1, "#ColorDim#", start=PI, rot=PI, lstart=157, solid=1)
shp(i, "Sun", [tick(0, 0, 0, 0, 0, 0, "0").replace("Line 0.0,0.0,0.0,0.0", "Line 40,310,400,310")
               .replace("StrokeWidth 0", "StrokeWidth 1").replace("Stroke Color 0", "Stroke Color #ColorMid#"),
               mdot(220, 310, 161, "#DayRad#", 20, "#ColorSoft#"),
               mdot(220, 310, 161, "#DayRad#", 10, "255,255,255")])
txt(i, "Dow", "[mDow]", 220, 250, 18, "#ColorDim#")
txt(i, "Time", "[mH]:[mM]", 220, 365, 60, "245,245,245")

# ------------------------------------------------------------------ 14  Stack
i = 14
txt(i, "H", "[mH]", 220, 150, 170, "245,245,245", face="Segoe UI Semibold")
txt(i, "M", "[mM]", 220, 320, 170, "#Color#")
txt(i, "Date", "[mDowS] [mDnum] [mMonS]", 30, 30, 16, "#ColorDim#", align="Left", face="Segoe UI")

# ------------------------------------------------------------------ 15  Date card
i = 15
txt(i, "Dow", "[mDow]", 220, 80, 24, "#ColorDim#", style="Bold", face="Segoe UI", StringCase="Upper")
txt(i, "Day", "[mDnum]", 220, 195, 200, "#Color#", face="Segoe UI Semibold")
txt(i, "Mon", "[mMon] [mYear]", 220, 315, 30, "245,245,245")
txt(i, "Time", "[mH]:[mM]", 220, 375, 40, "#ColorDim#")

# ------------------------------------------------------------------ 16  Line tracks
i = 16
txt(i, "Time", "[mH]:[mM]", 220, 110, 56, "245,245,245")
sh = []
for n, (lab, m, y) in enumerate((("HOUR", "mHrF", 190), ("MINUTE", "mMinF", 240), ("SECOND", "mSecF", 290))):
    sh.append(f"Line 40,{y},400,{y} | StrokeWidth 2 | Stroke Color #ColorMid#")
    sh.append(f"Ellipse (40+360*[{m}]),{y},{9-2*n} | Fill Color #Color# | StrokeWidth 0")
shp(i, "Tracks", sh)
for n, lab in enumerate(("HOUR", "MINUTE", "SECOND")):
    txt(i, f"L{n}", lab, 40, 190 + 50 * n - 20, 10, "#ColorDim#", align="Left", face="Segoe UI")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 350, 18, "#ColorDim#")

# ------------------------------------------------------------------ 17  Dash ring
i = 17
sh = dial_ticks(220, 220, 168, 178, "#ColorSoft#", big=160, w1=1, w2=2)
for ang, r1, r2, w, col in (("#SecRad#", 148, 182, 3, "#Color#"),
                            ("#MinRad#", 128, 168, 5, "#ColorDim#"),
                            ("#HourRad#", 100, 148, 8, "255,255,255")):
    sh.append(f"Line (220+{r1}*Cos({ang})),(220+{r1}*Sin({ang})),(220+{r2}*Cos({ang})),(220+{r2}*Sin({ang}))"
              f" | StrokeWidth {w} | Stroke Color {col}")
shp(i, "Ring", sh)
txt(i, "Time", "[mH]:[mM]", 220, 215, 40, "245,245,245")
txt(i, "Date", "[mDowS] [mDnum]", 220, 252, 15, "#ColorDim#")

# ------------------------------------------------------------------ 18  Gauges
i = 18
g0, gr = 2.3562, 4.7124
for n, (x, m, lab, t) in enumerate(((80, "mHrF", "HOURS", "[mH]"), (220, "mMinF", "MINUTES", "[mM]"),
                                    (360, "mSecF", "SECONDS", "[mS]"))):
    hand(i, f"T{n}", x, 215, 62, "mOne", 1, "#ColorSoft#", start=g0, rot=gr, lstart=54, solid=1)
    hand(i, f"A{n}", x, 215, 62, m, 1, "#Color#", start=g0, rot=gr, lstart=54, solid=1)
    txt(i, f"V{n}", t, x, 215, 34, "245,245,245")
    txt(i, f"L{n}", lab, x, 285, 11, "#ColorDim#", face="Segoe UI")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 370, 18, "#ColorDim#")

# ------------------------------------------------------------------ 19  Neon
i = 19
shp(i, "Lines", ["Line 70,120,370,120 | StrokeWidth 2 | Stroke Color #ColorMid#",
                 "Line 70,300,370,300 | StrokeWidth 2 | Stroke Color #ColorMid#"])
txt(i, "Time", "[mH]:[mM]", 220, 210, 120, "255,255,255", StringEffect="Border", FontEffectColor="#ColorDim#")
txt(i, "Date", "[mDow]  [mDnum]  [mMon]", 220, 345, 18, "#Color#", face="Segoe UI", StringCase="Upper")

# ------------------------------------------------------------------ 20  24 hour dial
i = 20
sh = [circle(220, 220, 170, sw=1, stroke="#ColorMid#")]
sh += dial_ticks(220, 220, 160, 170, "#ColorDim#", n=24, w1=1, w2=1)
sh.append(mdot(220, 220, 170, "(#DayF#*6.28318-1.5708)", 8, "#Color#"))
shp(i, "Dial", sh)
for h in range(0, 24, 3):
    a = h / 24 * 2 * PI - PI / 2
    txt(i, f"N{h}", str(h), f"{220+140*cos(a):.1f}", f"{220+140*sin(a):.1f}", 16, "#ColorDim#", face="Segoe UI")
hand(i, "Hand", 220, 220, 125, "mDayF", 3, "#Color#")
txt(i, "Time", "[mH]:[mM]", 220, 290, 30, "245,245,245")
txt(i, "Date", "[mDowS] [mDnum] [mMonS]", 220, 320, 14, "#ColorDim#")

# ------------------------------------------------------------------ 21  Split
i = 21
shp(i, "Line", ["Line 220,100,220,340 | StrokeWidth 2 | Stroke Color #ColorMid#"])
txt(i, "Dow", "[mDow]", 205, 135, 26, "#ColorDim#", align="RightCenter")
txt(i, "Day", "[mDnum]", 205, 215, 100, "245,245,245", align="RightCenter", face="Segoe UI Semibold")
txt(i, "Mon", "[mMon]", 205, 295, 26, "#ColorDim#", align="RightCenter")
txt(i, "H", "[mH]", 235, 175, 100, "245,245,245", align="LeftCenter")
txt(i, "M", "[mM]", 235, 275, 100, "#Color#", align="LeftCenter")

# ------------------------------------------------------------------ 22  Analog + digital
i = 22
sh = [circle(220, 165, 105, sw=2, stroke="255,255,255,180")]
sh += dial_ticks(220, 165, 92, 100, "255,255,255", n=60, w1=1, w2=2)
shp(i, "Dial", sh)
hand(i, "Hour", 220, 165, 52, "mHrF", 5, WHITE)
hand(i, "Min", 220, 165, 80, "mMinF", 3, WHITE)
hand(i, "Sec", 220, 165, 92, "mSecF", 1, "#Color#")
txt(i, "Time", "[mH]:[mM]", 220, 330, 68, "245,245,245")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 385, 17, "#ColorDim#")

# ------------------------------------------------------------------ 23  Phrase
i = 23
ring(i, "Sec", 220, 220, 188, 185, "mSecF", "#Color#")
txt(i, "A", "[mWordA]", 220, 175, 34, "#ColorDim#", StringCase="Lower")
txt(i, "B", "[mWordB]", 220, 255, 84, "245,245,245", face="Segoe UI Semibold", StringCase="Lower")

# ------------------------------------------------------------------ 24  Pulse
i = 24
shp(i, "Pulse", [circle(220, 220, 150, "#ColorSoft#", 2, "#ColorMid#"),
                 circle(220, 220, 180, sw=1, stroke="#ColorSoft#"),
                 mdot(220, 220, 180, "#SecRad#", 7, "#Color#")])
ring(i, "Min", 220, 220, 150, 144, "mMinF", "#Color#")
txt(i, "Time", "[mH]:[mM]", 220, 215, 64, "245,245,245")
txt(i, "Date", "[mDowS] [mDnum] [mMonS]", 220, 270, 16, "#ColorDim#")

# ================================================================== v4: styles 25-48 + shared quote block
EXTRA = []                                   # extra measure sections

def meas(name, kind, **o):
    L = [f"[{name}]", f"Measure={kind}"] + [f"{k}={v}" for k, v in o.items()]
    EXTRA.append("\n".join(L))

def lmeas(name, mode, **o):
    meas(name, "Script", ScriptFile="#CURRENTPATH#AdaptiveClock.lua", Mode=mode, **o)

for _nm, _md in [("mDHT", "dHT"), ("mDHU", "dHU"), ("mDMT", "dMT"), ("mDMU", "dMU"), ("mDST", "dST"), ("mDSU", "dSU"),
                 ("mHexH", "hexH"), ("mHexM", "hexM"), ("mHexS", "hexS"), ("mBinH", "binH"), ("mBinM", "binM"),
                 ("mBinS", "binS"), ("mEpoch", "epoch"), ("mSha", "sha"), ("mGreet", "greet"),
                 ("mGreetIcon", "greetIcon"), ("mYearPct", "yearPct"), ("mYearF", "yearF"), ("mDaysLeft", "daysLeft"),
                 ("mAmPm", "ampm"), ("mCursor", "cursor"), ("mQBody", "quoteBody"), ("mQWho", "quoteWho"),
                 ("mQMark", "qmark")]:
    lmeas(_nm, _md)
for _k in range(5):
    lmeas(f"mLogHash{_k}", "logHash", Index=_k)
    lmeas(f"mLogTime{_k}", "logTime", Index=_k)
meas("mCPU", "CPU")
meas("mRAM", "PhysicalMemory")
meas("mUptime", "Uptime", Format="%4!i!d %3!02i!h %2!02i!m")
meas("mISO", "Time", Format="%Y-%m-%dT%H:%M:%S")

def shpx(i, name, shapes, **extra):
    o = {"X": 0, "Y": 0, "W": W, "H": H}
    for n, s in enumerate(shapes):
        o["Shape" if n == 0 else f"Shape{n+1}"] = s
    o.update(extra)
    sec(i, name, "Shape", **o)

def rrect(x, y, w, h, r, fill, sw=0, stroke="0,0,0,0"):
    return f"Rectangle {x},{y},{w},{h},{r} | Fill Color {fill} | StrokeWidth {sw} | Stroke Color {stroke}"

def star_path(x, y, ro, ri):
    pts = []
    for k in range(10):
        a = -PI / 2 + k * PI / 5
        r = ro if k % 2 == 0 else ri
        pts.append((x + r * cos(a), y + r * sin(a)))
    s = f"{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for px, py in pts[1:]:
        s += f" | LineTo {px:.1f},{py:.1f}"
    return s + " | ClosePath 1"

INK, DIM, SOFT, MID = "#Ink#", "#InkDim#", "#InkSoft#", "#InkMid#"
TBG, TBAR = "13,17,23,235", "33,38,45"           # terminal-style windows keep their own dark colours
TXT, GREY, GREEN, BLUE, AMBER = "201,209,218", "139,148,158", "63,185,80", "88,166,255", "210,153,34"

def window(i, x, y, w, h, title, bg=TBG):
    shp(i, "Win", [rrect(x, y, w, h, 10, bg, 1, "#InkSoft#"),
                   rrect(x, y, w, 30, 10, TBAR), rrect(x, y + 15, w, 15, 0, TBAR),
                   circle(x + 22, y + 15, 5, "255,95,86"), circle(x + 40, y + 15, 5, "255,189,46"),
                   circle(x + 58, y + 15, 5, "39,201,63")])
    txt(i, "Title", title, x + w / 2, y + 15, 11, GREY, face="Consolas")

# ---- 25 Terminal (coder)
i = 25
window(i, 30, 95, 380, 250, "bash - clock")
txt(i, "L1", "user@clock:~$ date", 48, 148, 13, GREEN, align="LeftCenter", face="Consolas")
txt(i, "L2", "[mH]:[mM]:[mS]", 220, 192, 42, "230,237,243", face="Consolas")
txt(i, "L3", "[mDowS] [mMonS] [mDnum] [mYear]", 48, 238, 13, GREY, align="LeftCenter", face="Consolas")
txt(i, "L4", "user@clock:~$ uptime", 48, 272, 13, GREEN, align="LeftCenter", face="Consolas")
txt(i, "L5", "up [mUptime]", 48, 296, 13, BLUE, align="LeftCenter", face="Consolas")
txt(i, "L6", "user@clock:~$ [mCursor]", 48, 322, 13, GREEN, align="LeftCenter", face="Consolas")

# ---- 26 Code editor (coder)
i = 26
shp(i, "Win", [rrect(30, 95, 380, 255, 10, "30,30,30,240", 1, "#InkSoft#"), rrect(30, 95, 380, 30, 10, "37,37,38"),
               rrect(30, 110, 380, 15, 0, "37,37,38"), rrect(40, 95, 92, 30, 0, "30,30,30"),
               "Line 40,96,132,96 | StrokeWidth 2 | Stroke Color 0,122,204"])
txt(i, "Tab", "clock.js", 86, 111, 11, "204,204,204", face="Segoe UI")
code = [("// clock.js", "106,153,85"), ('const time = "[mH]:[mM]";', "156,220,254"),
        ('const date = "[mDowS] [mDnum] [mMonS]";', "206,145,120"), ("let focus = true;", "86,156,214"),
        ("tick(); // [mS]s", "220,220,170"), ("export default time;", "197,134,192")]
for n, (line, col) in enumerate(code):
    y = 150 + n * 30
    txt(i, f"N{n}", str(n + 1), 62, y, 13, "110,110,110", align="RightCenter", face="Consolas")
    txt(i, f"C{n}", line, 76, y, 14, col, align="LeftCenter", face="Consolas")

# ---- 27 Hex clock (coder)
i = 27
txt(i, "Head", "HEX CLOCK", 220, 100, 13, "#Color#", face="Segoe UI", style="Bold")
rows = (("HOUR", "mHexH", "mBinH", 160), ("MIN", "mHexM", "mBinM", 245), ("SEC", "mHexS", "mBinS", 330))
for n, (lab, hx, bn, y) in enumerate(rows):
    txt(i, f"L{n}", lab, 40, y, 12, DIM, align="LeftCenter", face="Segoe UI")
    txt(i, f"X{n}", f"[{hx}]", 112, y, 50, INK, align="LeftCenter", face="Consolas")
    txt(i, f"B{n}", f"[{bn}]", 400, y, 18, "#Color#", align="RightCenter", face="Consolas")
    if n < 2:
        shp(i, f"Sep{n}", [f"Line 40,{y+42},400,{y+42} | StrokeWidth 1 | Stroke Color #InkSoft#"])
txt(i, "Dec", "[mH]:[mM]:[mS]", 220, 388, 20, DIM, face="Consolas")

# ---- 28 Binary dots (coder)
i = 28
cols = [("mDHT", 2), ("mDHU", 4), ("mDMT", 3), ("mDMU", 4), ("mDST", 3), ("mDSU", 4)]
for c, (m, nb) in enumerate(cols):
    for k in range(nb):
        meas(f"mBit{c}_{k}", "Calc", Formula=f"BitAnd(BitRShift([{m}],{k}),1)")
sh = []
for c, (m, nb) in enumerate(cols):
    for k in range(nb):
        x, y = 80 + c * 56, 150 + (3 - k) * 55
        sh.append(f"Ellipse {x},{y},19 | Fill Color 0,0,0,0 | StrokeWidth 2 | Stroke Color #ColorMid#")
        sh.append(f"Ellipse {x},{y},(15*[mBit{c}_{k}]) | Fill Color #Color# | StrokeWidth 0")
shp(i, "Dots", sh)
for r, v in enumerate("8421"):
    txt(i, f"W{r}", v, 30, 150 + r * 55, 12, DIM, face="Consolas")
for c, ch in enumerate("HHMMSS"):
    txt(i, f"C{c}", ch, 80 + c * 56, 100, 12, DIM, face="Consolas")
txt(i, "Time", "[mH]:[mM]:[mS]", 220, 385, 24, INK, face="Consolas")

# ---- 29 System monitor (coder)
i = 29
txt(i, "Time", "[mH]:[mM]", 220, 130, 72, INK)
for n, (lab, m, val, col) in enumerate((("CPU", "mCPU", "[mCPU:0]%", "#Color#"),
                                        ("RAM", "mRAM", "[mRAM:%]%", "#Color2#"),
                                        ("DAY", "mDayF", "[mDayF:%]%", "#Color#"))):
    y = 220 + n * 42
    txt(i, f"L{n}", lab, 50, y, 13, DIM, align="LeftCenter", face="Consolas")
    sec(i, f"Bar{n}", "Bar", X=100, Y=y - 5, W=240, H=10, MeasureName=m, BarColor=col,
        SolidColor="#InkSoft#", BarOrientation="Horizontal")
    txt(i, f"V{n}", val, 392, y, 13, INK, align="RightCenter", face="Consolas")
txt(i, "Up", "uptime  [mUptime]", 220, 355, 14, DIM, face="Consolas")
txt(i, "Date", "[mDow], [mDnum] [mMon] [mYear]", 220, 385, 14, DIM, face="Consolas")

# ---- 30 Epoch and ISO (coder)
i = 30
txt(i, "L1", "UNIX TIME", 220, 120, 12, "#Color#", face="Segoe UI", style="Bold")
txt(i, "Epoch", "[mEpoch]", 220, 175, 62, INK, face="Consolas")
txt(i, "L2", "ISO 8601", 220, 250, 12, "#Color#", face="Segoe UI", style="Bold")
txt(i, "Iso", "[mISO]", 220, 288, 25, INK, face="Consolas")
txt(i, "Sha", "commit [mSha]", 220, 345, 16, DIM, face="Consolas")

# ---- 31 Git log (coder)
i = 31
window(i, 30, 95, 380, 250, "git log --oneline")
for k in range(5):
    y = 148 + k * 38
    txt(i, f"H{k}", f"[mLogHash{k}]", 48, y, 15, AMBER, align="LeftCenter", face="Consolas")
    txt(i, f"M{k}", f"tick: [mLogTime{k}]", 138, y, 15, TXT, align="LeftCenter", face="Consolas")
txt(i, "Head", "HEAD", 395, 148, 12, GREEN, align="RightCenter", face="Consolas", style="Bold")

# ---- 32 Greeting (everyday)
i = 32
txt(i, "Icon", "[mGreetIcon]", 220, 120, 64, "#Color#", face="Segoe UI Symbol")
txt(i, "Greet", "[mGreet]", 220, 195, 38, INK)
txt(i, "Time", "[mH]:[mM]", 220, 275, 84, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 350, 18, DIM)
txt(i, "AP", "[mAmPm]", 395, 252, 16, DIM)

# ---- 33 Month calendar (everyday)
i = 33
txt(i, "Title", "[mMon] [mYear]", 220, 95, 26, INK, face="Segoe UI Semibold")
for c in range(7):
    txt(i, f"H{c}", f"#CalH{c+1}#", 60 + c * 53, 140, 12, DIM, face="Segoe UI")
shp(i, "Today", [f"Ellipse (60+((#CalToday#-1)%7)*53),(180+Trunc((#CalToday#-1)/7)*37),17 | Fill Color #ColorSoft# | StrokeWidth 2 | Stroke Color #Color#"])
for n in range(42):
    txt(i, f"D{n}", f"#CalD{n+1}#", 60 + (n % 7) * 53, 180 + (n // 7) * 37, 17, INK)
txt(i, "Time", "[mH]:[mM]", 220, 418, 16, DIM)

# ---- 34 Year progress (everyday)
i = 34
txt(i, "Pct", "[mYearPct]", 220, 160, 112, INK, face="Segoe UI Semibold")
txt(i, "Of", "of [mYear] is done", 220, 242, 20, DIM)
sec(i, "Bar", "Bar", X=70, Y=274, W=300, H=12, MeasureName="mYearF", BarColor="#Color#",
    SolidColor="#InkSoft#", BarOrientation="Horizontal")
txt(i, "Left", "[mDaysLeft] days left", 220, 322, 22, "#Color#")
txt(i, "Date", "[mDow], [mDnum] [mMon]  -  [mH]:[mM]", 220, 372, 16, DIM)

# ---- 35 Sticky note (everyday)
i = 35
shp(i, "Note", [rrect(62, 112, 330, 300, 4, "0,0,0,50"), rrect(55, 105, 330, 300, 4, "255,236,128"),
                circle(220, 112, 9, "214,64,64", 1, "150,30,30")])
txt(i, "Dow", "[mDow]", 220, 160, 28, "100,80,30", face="Segoe UI Semibold")
txt(i, "Day", "[mDnum]", 220, 248, 112, "80,64,20", face="Segoe UI Semibold")
txt(i, "Mon", "[mMon]", 220, 328, 28, "100,80,30")
txt(i, "Time", "[mH]:[mM]", 220, 372, 30, "90,72,24")

# ---- 36 Week strip (everyday)
i = 36
txt(i, "Time", "[mH]:[mM]", 220, 140, 104, INK, face="Segoe UI Semibold")
shp(i, "Today", [f"Ellipse (60+(#WeekIdx#-1)*53),262,25 | Fill Color #ColorSoft# | StrokeWidth 3 | Stroke Color #Color#"])
for c in range(7):
    shp(i, f"Ring{c}", [circle(60 + c * 53, 262, 22, sw=1, stroke="#InkSoft#")])
    txt(i, f"D{c}", f"#CalH{c+1}#", 60 + c * 53, 262, 15, INK)
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 328, 20, DIM)
txt(i, "Left", "[mDaysLeft] days left in [mYear]", 220, 366, 15, "#Color#")

# ---- 37 Petals (girl)
i = 37
sh = [circle(220, 215, 128, sw=1, stroke="#ColorSoft#"), circle(220, 215, 144, sw=1, stroke="#Color2Soft#")]
for k in range(8):
    a = k * PI / 4
    sh.append(circle(f"{220+62*cos(a):.1f}", f"{215+62*sin(a):.1f}", 50, "#ColorSoft#", 1, "#Color#"))
sh += [circle(220, 215, 54, "#Color2Soft#", 2, "#Color2#"),
       mdot(220, 215, 128, "#SecRad#", 6, "#Color2#"), mdot(220, 215, 144, "#MinRad#", 8, "#Color#")]
shp(i, "Flower", sh)
txt(i, "Time", "[mH]:[mM]", 220, 208, 34, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDowS] [mDnum]", 220, 238, 13, DIM)

# ---- 38 Heart (girl)
i = 38
shpx(i, "Heart", ["Path HeartPath | Fill Color #ColorSoft# | StrokeWidth 4 | Stroke Color #Color#",
                  circle(120, 120, 5, "#Color2Soft#"), circle(335, 135, 4, "#Color2Soft#"),
                  circle(95, 330, 4, "#Color2Soft#"), circle(345, 320, 6, "#Color2Soft#")],
     HeartPath="220,372 | CurveTo 80,215,150,330,80,285 | CurveTo 220,172,80,95,195,85 | "
               "CurveTo 360,215,245,85,360,95 | CurveTo 220,372,360,285,290,330 | ClosePath 1")
txt(i, "Time", "[mH]:[mM]", 220, 205, 66, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 262, 16, DIM)

# ---- 39 Pastel pills (girl)
i = 39
txt(i, "Time", "[mH]:[mM]", 220, 120, 68, INK)
for n, (lab, m, val, col) in enumerate((("HOURS", "mHrF", "[mH]", "#Color#"), ("MINUTES", "mMinF", "[mM]", "#Color2#"),
                                        ("SECONDS", "mSecF", "[mS]", "#Color#"))):
    y = 200 + n * 62
    shp(i, f"Track{n}", [rrect(60, y, 320, 26, 13, "#InkSoft#"),
                         rrect(60, y, f"(26+294*[{m}])", 26, 13, col)])
    txt(i, f"L{n}", lab, 62, y - 14, 11, DIM, align="LeftCenter", face="Segoe UI")
    txt(i, f"V{n}", val, 378, y - 14, 11, DIM, align="RightCenter", face="Segoe UI")

# ---- 40 Starlight (girl)
i = 40
sh = []
for k in range(12):
    a = k / 12 * 2 * PI - PI / 2
    big = (k % 3 == 0)
    sh.append("Path Star%d | Fill Color %s | StrokeWidth 0" % (k, "#Color#" if big else "#Color2Soft#"))
stars = {f"Star{k}": star_path(220 + 150 * cos(k / 12 * 2 * PI - PI / 2), 215 + 150 * sin(k / 12 * 2 * PI - PI / 2),
                               17 if k % 3 == 0 else 11, 7 if k % 3 == 0 else 4.5) for k in range(12)}
shpx(i, "Stars", sh, **stars)
shp(i, "Orbit", [mdot(220, 215, 182, "#SecRad#", 5, "#Color2#")])
hand(i, "Hour", 220, 215, 80, "mHrF", 5, "#Color2#")
hand(i, "Min", 220, 215, 118, "mMinF", 3, "#Color#")
shp(i, "Hub", [circle(220, 215, 7, "#Color#")])
txt(i, "Time", "[mH]:[mM]", 220, 414, 20, DIM)

# ---- 41 Radar (boy)
i = 41
sh = [circle(220, 215, r, sw=1, stroke="#InkSoft#") for r in (170, 128, 86, 44)]
sh += dial_ticks(220, 215, 160, 170, "#InkMid#", n=60, w1=1, w2=2)
sh += ["Line 50,215,390,215 | StrokeWidth 1 | Stroke Color #InkSoft#", "Line 220,45,220,385 | StrokeWidth 1 | Stroke Color #InkSoft#"]
for k in range(9):
    d = round(0.07 * k, 2)
    sh.append(f"Line 220,215,(220+170*Cos(#SecRad#-{d})),(215+170*Sin(#SecRad#-{d})) | StrokeWidth {3 if k == 0 else 2} | Stroke Color #Color2#,{255 - k * 28}")
sh += [circle(290, 150, 5, "#Color2#"), circle(160, 262, 4, "#Color2#"), circle(250, 300, 6, "#Color2#"),
       circle(220, 215, 50, "0,0,0,170", 1, "#Color2#")]
shp(i, "Radar", sh)
txt(i, "Time", "[mH]:[mM]", 220, 208, 26, "250,250,250", face="Consolas")
txt(i, "Sec", "[mS]", 220, 232, 14, "#Color2#", face="Consolas")
txt(i, "Date", "[mDow] [mDnum] [mMon]", 220, 412, 14, DIM, face="Consolas")

# ---- 42 Planet orbit (boy)
i = 42
sh = ["Ellipse 220,200,128,30 | Fill Color 0,0,0,0 | StrokeWidth 5 | Stroke Color #Color2# | Rotate -18,220,200",
      "Ellipse 220,200,70 | Fill LinearGradient PlanetGrad | StrokeWidth 0",
      f"Ellipse (220+165*Cos(#SecRad#)),(200+60*Sin(#SecRad#)),9 | Fill Color #Color2# | StrokeWidth 0"]
for x, y, r in ((60, 110, 2), (110, 70, 3), (350, 90, 2), (390, 160, 3), (70, 260, 2), (380, 300, 2), (140, 320, 3)):
    sh.append(circle(x, y, r, "#InkMid#"))
shpx(i, "Space", sh, PlanetGrad="135 | #Color# ; 0.0 | #Color2# ; 1.0")
txt(i, "Time", "[mH]:[mM]", 220, 325, 58, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 382, 16, DIM)

# ---- 43 Speedometer (boy)
i = 43
g0, gr = 2.3562, 4.7124
hand(i, "Track", 220, 230, 165, "mOne", 1, "#InkSoft#", start=g0, rot=gr, lstart=150, solid=1)
hand(i, "Prog", 220, 230, 165, "mMinF", 1, "#Color#", start=g0, rot=gr, lstart=150, solid=1)
sh = []
for k in range(13):
    a = g0 + k / 12 * gr
    sh.append(tick(220, 230, 134, 146 if k % 2 == 0 else 141, a, 2 if k % 2 == 0 else 1, "#InkMid#"))
shp(i, "Ticks", sh)
for k in range(0, 13, 2):
    a = g0 + k / 12 * gr
    txt(i, f"N{k}", str(k * 5), f"{220+114*cos(a):.1f}", f"{230+114*sin(a):.1f}", 13, DIM, face="Segoe UI")
hand(i, "Needle", 220, 230, 128, "mMinF", 4, "#Color2#", start=g0, rot=gr)
shp(i, "Hub", [circle(220, 230, 10, "#Color2#")])
txt(i, "Time", "[mH]:[mM]", 220, 335, 50, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 378, 15, DIM)

# ---- 44 Scoreboard (boy)
i = 44
shp(i, "Panel", [rrect(40, 115, 360, 235, 16, "18,22,30,245", 2, "60,66,81")] +
    [circle(x, y, 4, "60,66,81") for x, y in ((58, 133), (382, 133), (58, 332), (382, 332))])
txt(i, "Head", "MATCH CLOCK", 220, 143, 12, "150,160,176", face="Segoe UI", style="Bold")
txt(i, "Sec", "SEC [mS]", 360, 143, 12, "255,184,0", face="Consolas")
txt(i, "H", "[mH]", 130, 232, 104, "255,184,0", face="Consolas", style="Bold")
txt(i, "Colon", ":", 220, 224, 80, "255,184,0", face="Consolas", style="Bold")
txt(i, "M", "[mM]", 310, 232, 104, "255,184,0", face="Consolas", style="Bold")
txt(i, "Date", "[mDow] [mDnum] [mMon]", 220, 318, 16, "150,160,176", face="Consolas")

# ---- 45 Flip clock
i = 45
shp(i, "Cards", [rrect(55, 135, 150, 190, 18, "28,28,32"), rrect(235, 135, 150, 190, 18, "28,28,32"),
                 "Line 55,230,205,230 | StrokeWidth 3 | Stroke Color 8,8,10", "Line 235,230,385,230 | StrokeWidth 3 | Stroke Color 8,8,10"])
txt(i, "H", "[mH]", 130, 230, 120, "250,250,250", face="Segoe UI Semibold")
txt(i, "M", "[mM]", 310, 230, 120, "250,250,250", face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 100, 18, DIM)
txt(i, "Sec", "[mS]", 220, 360, 22, INK)
txt(i, "AP", "[mAmPm]", 130, 352, 14, DIM)

# ---- 46 Minimal analog
i = 46
sh = [circle(f"{220+172*cos(k/12*2*PI):.1f}", f"{220+172*sin(k/12*2*PI):.1f}", 5 if k % 3 == 0 else 3, "#Ink#") for k in range(12)]
sh += [rrect(284, 208, 40, 24, 5, "0,0,0,0", 1, "#InkMid#")]
shp(i, "Dial", sh)
txt(i, "Day", "[mDnum]", 304, 220, 13, INK)
hand(i, "Hour", 220, 220, 100, "mHrF", 5, "#Ink#")
hand(i, "Min", 220, 220, 150, "mMinF", 3, "#Ink#")
hand(i, "Sec", 220, 220, 160, "mSecF", 1, "#Color#")
shp(i, "Hub", [circle(220, 220, 7, "0,0,0,0", 2, "#Ink#")])

# ---- 47 Tiles
i = 47
shp(i, "Tiles", [rrect(30, 100, 260, 150, 10, "#ColorSoft#"), rrect(300, 100, 110, 150, 10, "#Color2Soft#"),
                 rrect(30, 260, 125, 120, 10, "#Color2Soft#"), rrect(165, 260, 125, 120, 10, "#ColorSoft#"),
                 rrect(300, 260, 110, 120, 10, "#ColorSoft#")])
txt(i, "T", "[mH]:[mM]", 160, 165, 78, INK, face="Segoe UI Semibold")
txt(i, "TD", "[mDow]", 160, 226, 16, DIM)
txt(i, "D1", "[mDowS]", 355, 128, 16, DIM)
txt(i, "D2", "[mDnum]", 355, 188, 64, INK, face="Segoe UI Semibold")
txt(i, "G1", "[mGreetIcon]", 92, 300, 36, "#Color#", face="Segoe UI Symbol")
txt(i, "G2", "[mGreet]", 92, 352, 13, INK)
txt(i, "Y1", "[mYearPct]", 227, 305, 34, INK, face="Segoe UI Semibold")
txt(i, "Y2", "of [mYear]", 227, 348, 13, DIM)
txt(i, "S1", "[mS]", 355, 305, 46, INK)
txt(i, "S2", "seconds", 355, 348, 13, DIM)

# ---- 48 Aurora
i = 48
shpx(i, "Card", [rrect(40, 110, 360, 270, 32, "0,0,0,0")], Shape="Rectangle 40,110,360,270,32 | Fill LinearGradient AuroraGrad | StrokeWidth 0",
     AuroraGrad="135 | #GradA# ; 0.0 | #GradB# ; 1.0")
txt(i, "Time", "[mH]:[mM]", 220, 225, 112, "250,250,250", face="Segoe UI Semibold",
    StringEffect="Shadow", FontEffectColor="0,0,0,60")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 312, 20, "250,250,250")
shp(i, "Bar", [rrect(80, 346, 280, 6, 3, "250,250,250,70"), rrect(80, 346, "(6+274*[mSecF])", 6, 3, "250,250,250,230")])

# ---- extras for older styles: AM/PM markers for the 12-hour clock
txt(8, "AP", "[mAmPm]", 392, 130, 18, "#ColorDim#")
txt(22, "AP", "[mAmPm]", 350, 300, 14, "#ColorDim#")
txt(24, "AP", "[mAmPm]", 220, 302, 14, "#ColorDim#")

# ================================================================== shared quote block (two designs)
def qsec(name, kind, hid, **o):
    L = [f"[{name}]", f"Meter={kind}"] + [f"{k}={v}" for k, v in o.items()] + [f"Hidden=#{hid}#", "DynamicVariables=1"]
    S.append("\n".join(L))

# friendly: short accent line, big quote mark, italic serif quote, accent author
qsec("QF_Line", "Shape", "QHf", X=0, Y=0, W=W, H=H,
     Shape="Line 160,447,280,447 | StrokeWidth 1 | Stroke Color #ColorMid#")
qsec("QF_Mark", "String", "QHf", X=14, Y=474, Text="[mQMark]", FontFace="Georgia", FontSize=54,
     FontColor="#ColorMid#", StringAlign="LeftCenter", AntiAlias=1)
qsec("QF_Body", "String", "QHf", X=220, Y=454, W=330, H=48, Text="[mQBody]", FontFace="Georgia",
     FontSize="(#QuoteSize#+1)", StringStyle="Italic", FontColor="#InkDim#", StringAlign="CenterTop",
     ClipString=2, AntiAlias=1)
qsec("QF_Who", "String", "QHf", X=220, Y=506, Text="[mQWho]", FontFace="Segoe UI", FontSize="(#QuoteSize#-1)",
     StringStyle="Bold", FontColor="#Color#", StringAlign="CenterCenter", AntiAlias=1)

# terminal: dark panel, green comment, blue author with a blinking cursor
qsec("QC_Panel", "Shape", "QHc", X=0, Y=0, W=W, H=H,
     Shape="Rectangle 24,442,392,74,8 | Fill Color 13,17,23,225 | StrokeWidth 1 | Stroke Color #ColorMid#",
     Shape2="Ellipse 40,454,3 | Fill Color 255,95,86 | StrokeWidth 0",
     Shape3="Ellipse 52,454,3 | Fill Color 255,189,46 | StrokeWidth 0",
     Shape4="Ellipse 64,454,3 | Fill Color 39,201,63 | StrokeWidth 0")
qsec("QC_Body", "String", "QHc", X=36, Y=463, W=370, H=32, Text="[mQBody]", FontFace="Consolas",
     FontSize="(#QuoteSize#-1)", FontColor="106,153,85", StringAlign="LeftTop", ClipString=2, AntiAlias=1)
qsec("QC_Who", "String", "QHc", X=36, Y=504, Text="[mQWho]", FontFace="Consolas", FontSize="(#QuoteSize#-1)",
     FontColor="86,156,214", StringAlign="LeftCenter", AntiAlias=1)
EXTRA_M = "\n\n".join(EXTRA)

# ------------------------------------------------------------------ header
HV = "\n".join(f"H{n}=1" for n in range(1, 49)) + "\nQHf=1\nQHc=1\n" + "\n".join(f"CalH{n}=" for n in range(1, 8)) + "\n" + "\n".join(f"CalD{n}=" for n in range(1, 43))
SCRIPT = "ScriptFile=#CURRENTPATH#AdaptiveClock.lua"

def script(name, mode):
    return f"[{name}]\nMeasure=Script\n{SCRIPT}\nMode={mode}"

def tm(name, fmt):
    return f"[{name}]\nMeasure=Time\nFormat={fmt}"

head = f"""; AdaptiveClock.ini  by Amika Alankara  -  48 clock styles driven by AdaptiveClock.lua (same folder)
; Right-click the skin: Next / Random style, resume hourly shuffle, 12/24h, quote options.

[Rainmeter]
Update=1000
AccurateText=1
DynamicWindowSize=0
ContextTitle=Next style
ContextAction=[!CommandMeasure mMain "Next()"]
ContextTitle2=Random style
ContextAction2=[!CommandMeasure mMain "RandomStyle()"]
ContextTitle3=Lock / unlock this style
ContextAction3=[!CommandMeasure mMain "ToggleLock()"]
ContextTitle4=Resume shuffle + re-check wallpaper
ContextAction4=[!CommandMeasure mMain "Resume()"][!CommandMeasure mLum "Run"]
ContextTitle5=Profile: next (all / coder / everyday)
ContextAction5=[!CommandMeasure mMain "CycleProfile()"]
ContextTitle6=Theme: next (neutral / girl / boy)
ContextAction6=[!CommandMeasure mMain "CycleTheme()"]
ContextTitle7=Colours: next mode (invert / accent / white / black)
ContextAction7=[!CommandMeasure mMain "CycleColors()"]
ContextTitle8=Next quote
ContextAction8=[!CommandMeasure mMain "NextQuote()"]
ContextTitle9=Quote speed: next (daily / hourly / 30 / 10 min)
ContextAction9=[!CommandMeasure mMain "CycleQuoteRate()"]
ContextTitle10=Show / hide quote
ContextAction10=[!CommandMeasure mMain "ToggleQuote()"]
ContextTitle11=Switch 12 / 24-hour
ContextAction11=[!CommandMeasure mMain "ToggleHourFormat()"]
ContextTitle12=Shuffle speed: next (60 / 30 / 15 / 5 min / daily)
ContextAction12=[!CommandMeasure mMain "CycleShuffle()"]
ContextTitle13=Skip this style in future
ContextAction13=[!CommandMeasure mMain "SkipThisStyle()"]
ContextTitle14=Show all styles again
ContextAction14=[!CommandMeasure mMain "ShowAllStyles()"]

[Metadata]
Name=Adaptive Clock
Author=Amika Alankara
Version=4.0
Description=48 clock styles with coder / everyday profiles, girl / boy themes, wallpaper-aware colours and a daily quote.

[Variables]
StyleCount=48
HourFormat=%H
QuoteHidden=0
QuoteMinutes=1440
QuoteStyle=Auto
QuoteBump=0
Profile=All
Theme=Neutral
LockedStyle=0
WeekStart=1
CalToday=1
WeekIdx=1
Color2=255,255,255
Color2Soft=255,255,255,70
GradA=120,140,255
GradB=255,130,200
FontMono=Consolas
StyleNo=1
FontText=Segoe UI
FontLight=Segoe UI Light
FontBold=Segoe UI Semibold
QuoteSize=11
StyleName=
LockMark=
ShuffleMinutes=60
SkipStyles=
Cities=NEW YORK:-5:US|LONDON:0:EU|DUBAI:4:-|TOKYO:9:-|SYDNEY:10:AU
Color=255,255,255
ColorDim=255,255,255,190
ColorMid=255,255,255,120
ColorSoft=255,255,255,60
ColorMode=Invert
Ink=255,255,255
InkDim=255,255,255,190
InkMid=255,255,255,120
InkSoft=255,255,255,60
SecRad=0
MinRad=0
HourRad=0
DayRad=3.14159
DayF=0
{HV}

; ---------------------------------------------------------------- measures
[mAccent]
Measure=Registry
RegHKey=HKEY_CURRENT_USER
RegSubKey=Software\\Microsoft\\Windows\\DWM
RegValue=AccentColor

[mLum]
Measure=Plugin
Plugin=RunCommand
Program=PowerShell
Parameter=-NoProfile -ExecutionPolicy Bypass -File "#CURRENTPATH#WallpaperLuma.ps1" -X #CURRENTCONFIGX# -Y #CURRENTCONFIGY# -W #CURRENTCONFIGWIDTH# -H #CURRENTCONFIGHEIGHT#
DynamicVariables=1
OutputType=ANSI
State=Hide
Timeout=20000
UpdateDivider=30

[mWall]
Measure=Registry
RegHKey=HKEY_CURRENT_USER
RegSubKey=Control Panel\\Desktop
RegValue=WallPaper
UpdateDivider=2
OnChangeAction=[!CommandMeasure mLum "Run"]

{script('mMain', 'main')}

{script('mSecF', 'secF')}

{script('mMinF', 'minF')}

{script('mHrF', 'hrF')}

{script('mDayF', 'dayF')}

{script('mWName', 'worldName')}

{script('mWDay', 'worldDay')}

{script('mWTime', 'worldTime')}

{script('mWordA', 'wordsA')}

{script('mWordB', 'wordsB')}

[mOne]
Measure=Calc
Formula=1

{EXTRA_M}

{tm('mH', '#HourFormat#')}

{tm('mM', '%M')}

{tm('mS', '%S')}

{tm('mDow', '%A')}

{tm('mDowS', '%a')}

{tm('mDnum', '%#d')}

{tm('mMon', '%B')}

{tm('mMonS', '%b')}

{tm('mYear', '%Y')}

; ---------------------------------------------------------------- meters
[Bg]
Meter=Shape
ToolTipText=#StyleName#  -  style #StyleNo# of #StyleCount##LockMark#  (double-click: next style)
LeftMouseDoubleClickAction=[!CommandMeasure mMain "Next()"]
DynamicVariables=1
X=0
Y=0
W={W}
H={H}
Shape=Rectangle 0,0,{W},{H} | Fill Color 0,0,0,1 | StrokeWidth 0

"""
import re
def inkify(t):
    if t.startswith("[S1_"): return t
    for a in ("210,210,215,90","160,160,168,110","110,110,118,140"):
        t = t.replace(a, "#InkSoft#")
    t = re.sub(r"255,255,255,(40|60|70|80|90)\b", "#InkSoft#", t)
    t = re.sub(r"255,255,255,(200|180)", "#InkDim#", t)
    for a in ("245,245,245","235,235,235","240,240,240","255,255,255","55,55,55","50,50,50"):
        t = re.sub(r"(?<![\d,])" + a + r"(?![\d,])", "#Ink#", t)
    t = t.replace("70,70,70", "#InkMid#").replace("120,120,120,110", "#InkSoft#")
    return t
def fontify(t):
    t = t.replace("FontFace=Segoe UI Semibold", "FontFace=#FontBold#")
    t = t.replace("FontFace=Segoe UI Semilight", "FontFace=#FontLight#")
    t = t.replace("FontFace=Segoe UI Light", "FontFace=#FontLight#")
    t = re.sub(r"FontFace=Consolas(?=\n)", "FontFace=#FontMono#", t)
    return re.sub(r"FontFace=Segoe UI(?=\n)", "FontFace=#FontText#", t)
S[:] = [fontify(inkify(x)) for x in S]
open("../AdaptiveClock/AdaptiveClock.ini", "w", encoding="utf-8").write(head + "\n\n".join(S) + "\n")
print(len(S), "meters")
