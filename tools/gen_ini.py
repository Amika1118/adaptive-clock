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
txt(i, "Title", "[mLblWorld]", 220, 128, 30, "245,245,245", face="Segoe UI Semibold")
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
txt(i, "Time", "[mH]:[mM]", 220, 190, 112, "245,245,245")
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
for n, (lab, m, y, c) in enumerate((("[mLblHour]", "mHrF", 235, "#Color#"),
                                    ("[mLblMinute]", "mMinF", 285, "#ColorDim#"),
                                    ("[mLblSecond]", "mSecF", 335, "#ColorMid#"))):
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
txt(i, "H", "[mH]", 220, 155, 132, "245,245,245", face="Segoe UI Semibold")
txt(i, "M", "[mM]", 220, 325, 132, "#Color#")
txt(i, "Date", "[mDowS] [mDnum] [mMonS]", 30, 30, 16, "#ColorDim#", align="Left", face="Segoe UI")

# ------------------------------------------------------------------ 15  Date card
i = 15
txt(i, "Dow", "[mDow]", 220, 80, 24, "#ColorDim#", style="Bold", face="Segoe UI", StringCase="Upper")
txt(i, "Day", "[mDnum]", 220, 208, 148, "#Color#", face="Segoe UI Semibold")
txt(i, "Mon", "[mMon] [mYear]", 220, 322, 28, "245,245,245")
txt(i, "Time", "[mH]:[mM]", 220, 375, 40, "#ColorDim#")

# ------------------------------------------------------------------ 16  Line tracks
i = 16
txt(i, "Time", "[mH]:[mM]", 220, 110, 56, "245,245,245")
sh = []
for n, (lab, m, y) in enumerate((("[mLblHour]", "mHrF", 190), ("[mLblMinute]", "mMinF", 240), ("[mLblSecond]", "mSecF", 290))):
    sh.append(f"Line 40,{y},400,{y} | StrokeWidth 2 | Stroke Color #ColorMid#")
    sh.append(f"Ellipse (40+360*[{m}]),{y},{9-2*n} | Fill Color #Color# | StrokeWidth 0")
shp(i, "Tracks", sh)
for n, lab in enumerate(("[mLblHour]", "[mLblMinute]", "[mLblSecond]")):
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
for n, (x, m, lab, t) in enumerate(((80, "mHrF", "[mLblHours]", "[mH]"), (220, "mMinF", "[mLblMinutes]", "[mM]"),
                                    (360, "mSecF", "[mLblSeconds]", "[mS]"))):
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
txt(i, "Time", "[mH]:[mM]   [mDowS] [mDnum] [mMonS]", 220, 414, 17, "245,245,245")

# ------------------------------------------------------------------ 21  Split
i = 21
shp(i, "Line", ["Line 220,100,220,340 | StrokeWidth 2 | Stroke Color #ColorMid#"])
txt(i, "Dow", "[mDow]", 205, 135, 26, "#ColorDim#", align="RightCenter")
txt(i, "Day", "[mDnum]", 205, 215, 86, "245,245,245", align="RightCenter", face="Segoe UI Semibold")
txt(i, "Mon", "[mMon]", 205, 295, 26, "#ColorDim#", align="RightCenter")
txt(i, "H", "[mH]", 235, 168, 84, "245,245,245", align="LeftCenter")
txt(i, "M", "[mM]", 235, 272, 84, "#Color#", align="LeftCenter")

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
TBG, TBAR = "#CTbg#", "#CTbar#"           # terminal-style windows keep their own dark colours
TXT, GREY, GREEN, BLUE, AMBER = "#CTtext#", "#CTcomment#", "#CTfunc#", "#CTtype#", "#CTkeyword#"

def window(i, x, y, w, h, title, bg=TBG):
    shp(i, "Win", [rrect(x, y, w, h, 10, bg, 1, "#InkSoft#"),
                   rrect(x, y, w, 30, 10, TBAR), rrect(x, y + 15, w, 15, 0, TBAR),
                   circle(x + 22, y + 15, 5, "255,95,86"), circle(x + 40, y + 15, 5, "255,189,46"),
                   circle(x + 58, y + 15, 5, "39,201,63")])
    txt(i, "Title", title, x + w / 2, y + 15, 11, GREY, face="Consolas")

# ---- 25 Terminal (coder)
i = 25
window(i, 14, 92, 412, 322, "bash - clock")
txt(i, "L1", "user@clock:~$ date", 34, 140, 13, GREEN, align="LeftCenter", face="Consolas")
txt(i, "L2", "[mH]:[mM]:[mS]", 220, 192, 50, "#CTfunc#", face="Consolas", style="Bold")
txt(i, "L3", "[mDow] [mMon] [mDnum] [mYear]", 220, 236, 13, GREY, face="Consolas")
txt(i, "L4", "user@clock:~$ uptime", 34, 276, 13, GREEN, align="LeftCenter", face="Consolas")
txt(i, "L5", " up [mUptime],  cpu [mCPU:0]%,  ram [mRAM:%]%", 34, 302, 12, BLUE, align="LeftCenter", face="Consolas")
txt(i, "L6", "user@clock:~$ [mCursor]", 34, 340, 13, GREEN, align="LeftCenter", face="Consolas")

# ---- 26 Live preview (coder)
i = 26
x0, y0, w = 14, 86, 412
shp(i, "Win", [rrect(x0, y0, w, 330, 10, "#CTbg#", 1, "#InkSoft#"), rrect(x0, y0, w, 26, 10, "#CTbar#"), rrect(x0, y0 + 13, w, 13, 0, "#CTbar#"),
               circle(x0 + 16, y0 + 13, 4.5, "255,95,86"), circle(x0 + 32, y0 + 13, 4.5, "255,189,46"), circle(x0 + 48, y0 + 13, 4.5, "39,201,63"),
               rrect(x0, y0 + 26, 206, 26, 0, "#CTbar#,170"), rrect(x0 + 8, y0 + 27, 92, 25, 0, "#CTbg#"),
               f"Line {x0+8},{y0+28},{x0+100},{y0+28} | StrokeWidth 2 | Stroke Color #CTstatus#",
               rrect(x0, y0 + 304, w, 26, 10, "#CTstatus#"), rrect(x0, y0 + 304, w, 13, 0, "#CTstatus#"),
               f"Line {x0+206},{y0+26},{x0+206},{y0+304} | StrokeWidth 1 | Stroke Color #InkSoft#",
               rrect(x0 + 216, y0 + 62, 180, 232, 8, "250,250,252", 1, "200,200,210"),
               rrect(x0 + 216, y0 + 62, 180, 26, 8, "232,234,240"), rrect(x0 + 216, y0 + 76, 180, 12, 0, "232,234,240"),
               rrect(x0 + 226, y0 + 68, 160, 14, 7, "250,250,252"),
               rrect(x0 + 236, y0 + 214, 140, 7, 3, "225,227,238"), rrect(x0 + 236, y0 + 214, "(6+134*[mSecF])", 7, 3, "79,70,229"),
               circle(x0 + 224, y0 + 75, 3, "255,95,86"), circle(x0 + 235, y0 + 75, 3, "255,189,46")])
txt(i, "Title", "Live Server - port 5500", x0 + w / 2, y0 + 13, 9, "#CTcomment#", face="Segoe UI")
txt(i, "Tab", "index.html", x0 + 54, y0 + 39.5, 10, "#CTtext#", face="Segoe UI")
txt(i, "Url", "localhost:5500", x0 + 306, y0 + 75, 8, "110,114,130", face="Segoe UI")
lines = [("<!-- clock -->", "comment"), ("<style>", "keyword"), ("h1 { color: indigo }", "string"), ("</style>", "keyword"),
         ("<h1>[mH]:[mM]</h1>", "func"), ("<p>[mDowS] [mDnum]</p>", "text"), ('<meter value="[mS]">', "number")]
for n, (line, role) in enumerate(lines):
    y = y0 + 70 + n * 30
    txt(i, f"N{n}", str(n + 1), x0 + 28, y, 11, "#CTnum#", align="RightCenter", face="Consolas")
    txt(i, f"C{n}", line, x0 + 38, y, 11, f"#CT{role}#", align="LeftCenter", face="Consolas")
txt(i, "PreTime", "[mH]:[mM]", x0 + 306, y0 + 150, 44, "30,34,48", face="Segoe UI Semibold")
txt(i, "PreDate", "[mDow], [mDnum] [mMon]", x0 + 306, y0 + 190, 11, "100,104,120", face="Segoe UI")
txt(i, "PreSec", "[mS] s", x0 + 306, y0 + 240, 10, "79,70,229", face="Consolas", style="Bold")
txt(i, "Status", "Go Live", x0 + 14, y0 + 317, 10, "250,250,250", align="LeftCenter", face="Segoe UI", style="Bold")
txt(i, "Pos", "HTML    UTF-8", x0 + w - 12, y0 + 317, 10, "250,250,250", align="RightCenter", face="Segoe UI")

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
txt(i, "Epoch", "[mEpoch]", 220, 175, 50, INK, face="Consolas")
txt(i, "L2", "ISO 8601", 220, 250, 12, "#Color#", face="Segoe UI", style="Bold")
txt(i, "Iso", "[mISO]", 220, 288, 25, INK, face="Consolas")
txt(i, "Sha", "commit [mSha]", 220, 345, 16, DIM, face="Consolas")

# ---- 31 Git log (coder)
i = 31
window(i, 14, 92, 412, 322, "git log --oneline --graph")
shp(i, "Graph", ["Line 40,138,40,318 | StrokeWidth 2 | Stroke Color #CTcomment#"] + [circle(40, 140 + k * 40, 5, "#CTkeyword#") for k in range(5)])
for k in range(5):
    y = 140 + k * 40
    txt(i, f"H{k}", f"[mLogHash{k}]", 58, y, 13, AMBER, align="LeftCenter", face="Consolas")
    txt(i, f"M{k}", f"tick: [mLogTime{k}]", 148, y, 13, TXT, align="LeftCenter", face="Consolas")
txt(i, "Head", "HEAD -> main", 404, 140, 10, GREEN, align="RightCenter", face="Consolas", style="Bold")
txt(i, "Big", "[mH]:[mM]:[mS]", 220, 366, 26, "#CTfunc#", face="Consolas", style="Bold")

# ---- 32 Greeting (everyday)
i = 32
txt(i, "Icon", "[mGreetIcon]", 220, 120, 64, "#Color#", face="Segoe UI Symbol")
txt(i, "Greet", "[mGreet]", 220, 188, 34, INK)
txt(i, "Time", "[mH]:[mM]", 220, 284, 80, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 364, 18, DIM)
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
txt(i, "Of", "[mLblYearDone]", 220, 242, 20, DIM)
sec(i, "Bar", "Bar", X=70, Y=274, W=300, H=12, MeasureName="mYearF", BarColor="#Color#",
    SolidColor="#InkSoft#", BarOrientation="Horizontal")
txt(i, "Left", "[mLblDaysLeft]", 220, 322, 22, "#Color#")
txt(i, "Date", "[mDow], [mDnum] [mMon]  -  [mH]:[mM]", 220, 372, 16, DIM)

# ---- 35 Sticky note (everyday)
i = 35
shp(i, "Note", [rrect(62, 112, 330, 300, 4, "0,0,0,50"), rrect(55, 105, 330, 300, 4, "255,236,128"),
                circle(220, 112, 9, "214,64,64", 1, "150,30,30")])
txt(i, "Dow", "[mDow]", 220, 150, 28, "100,80,30", face="Segoe UI Semibold")
txt(i, "Day", "[mDnum]", 220, 240, 92, "80,64,20", face="Segoe UI Semibold")
txt(i, "Mon", "[mMon]", 220, 322, 28, "100,80,30")
txt(i, "Time", "[mH]:[mM]", 220, 372, 30, "90,72,24")

# ---- 36 Week strip (everyday)
i = 36
txt(i, "Time", "[mH]:[mM]", 220, 140, 104, INK, face="Segoe UI Semibold")
shp(i, "Today", [f"Ellipse (60+(#WeekIdx#-1)*53),262,25 | Fill Color #ColorSoft# | StrokeWidth 3 | Stroke Color #Color#"])
for c in range(7):
    shp(i, f"Ring{c}", [circle(60 + c * 53, 262, 22, sw=1, stroke="#InkSoft#")])
    txt(i, f"D{c}", f"#CalH{c+1}#", 60 + c * 53, 262, 15, INK)
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 328, 20, DIM)
txt(i, "Left", "[mLblDaysLeftYear]", 220, 366, 15, "#Color#")

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
for n, (lab, m, val, col) in enumerate((("[mLblHours]", "mHrF", "[mH]", "#Color#"), ("[mLblMinutes]", "mMinF", "[mM]", "#Color2#"),
                                        ("[mLblSeconds]", "mSecF", "[mS]", "#Color#"))):
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
txt(i, "Time", "[mH]:[mM]", 220, 372, 44, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 412, 15, DIM)

# ---- 44 Scoreboard (boy)
i = 44
shp(i, "Panel", [rrect(40, 115, 360, 235, 16, "18,22,30,245", 2, "60,66,81")] +
    [circle(x, y, 4, "60,66,81") for x, y in ((58, 133), (382, 133), (58, 332), (382, 332))])
txt(i, "Head", "MATCH CLOCK", 220, 143, 12, "150,160,176", face="Segoe UI", style="Bold")
txt(i, "Sec", "SEC [mS]", 360, 143, 12, "255,184,0", face="Consolas")
txt(i, "H", "[mH]", 130, 232, 90, "255,184,0", face="Consolas", style="Bold")
txt(i, "Colon", ":", 220, 224, 70, "255,184,0", face="Consolas", style="Bold")
txt(i, "M", "[mM]", 310, 232, 90, "255,184,0", face="Consolas", style="Bold")
txt(i, "Date", "[mDow] [mDnum] [mMon]", 220, 318, 16, "150,160,176", face="Consolas")

# ---- 45 Flip clock
i = 45
shp(i, "Cards", [rrect(55, 135, 150, 190, 18, "28,28,32"), rrect(235, 135, 150, 190, 18, "28,28,32"),
                 "Line 55,230,205,230 | StrokeWidth 3 | Stroke Color 8,8,10", "Line 235,230,385,230 | StrokeWidth 3 | Stroke Color 8,8,10"])
txt(i, "H", "[mH]", 130, 230, 84, "250,250,250", face="Segoe UI Semibold")
txt(i, "M", "[mM]", 310, 230, 84, "250,250,250", face="Segoe UI Semibold")
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
txt(i, "T", "[mH]:[mM]", 160, 165, 62, INK, face="Segoe UI Semibold")
txt(i, "TD", "[mDow]", 160, 226, 16, DIM)
txt(i, "D1", "[mDowS]", 355, 128, 16, DIM)
txt(i, "D2", "[mDnum]", 355, 188, 64, INK, face="Segoe UI Semibold")
txt(i, "G1", "[mGreetIcon]", 92, 300, 36, "#Color#", face="Segoe UI Symbol")
txt(i, "G2", "[mGreet]", 92, 352, 13, INK)
txt(i, "Y1", "[mYearPct]", 227, 305, 34, INK, face="Segoe UI Semibold")
txt(i, "Y2", "[mLblOfYear]", 227, 348, 13, DIM)
txt(i, "S1", "[mS]", 355, 305, 46, INK)
txt(i, "S2", "[mLblSecondsLow]", 355, 348, 13, DIM)

# ---- 48 Aurora
i = 48
shpx(i, "Card", [rrect(40, 110, 360, 270, 32, "0,0,0,0")], Shape="Rectangle 40,110,360,270,32 | Fill LinearGradient AuroraGrad | StrokeWidth 0",
     AuroraGrad="135 | #GradA# ; 0.0 | #GradB# ; 1.0")
txt(i, "Time", "[mH]:[mM]", 220, 225, 84, "250,250,250", face="Segoe UI Semibold",
    StringEffect="Shadow", FontEffectColor="0,0,0,60")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 312, 20, "250,250,250")
shp(i, "Bar", [rrect(80, 346, 280, 6, 3, "250,250,250,70"), rrect(80, 346, "(6+274*[mSecF])", 6, 3, "250,250,250,230")])

# ---- 49-53: weather, sun times, now playing, battery, timer and alarm
meas("mWxRaw", "WebParser",
     URL="https://api.open-meteo.com/v1/forecast?latitude=#Latitude#&longitude=#Longitude#&current=temperature_2m,weather_code&temperature_unit=#TempUnit#",
     UpdateRate="(900*#Div#)", Disabled="#WeatherOff#",
     RegExp='(?siU)"current":\\{.*"temperature_2m":(.*),"weather_code":(.*)\\}')
meas("mWxT", "WebParser", URL="[mWxRaw]", StringIndex=1)
meas("mWxC", "WebParser", URL="[mWxRaw]", StringIndex=2)
for _nm, _md in [("mWxIcon", "wxIcon"), ("mWxTempTxt", "wxTemp"), ("mWxText", "wxText"), ("mSunRise", "sunRise"),
                 ("mSunSet", "sunSet"), ("mSunF", "sunF"), ("mSunNote", "sunNote"), ("mBatTxt", "batText")]:
    lmeas(_nm, _md)
meas("mBatPct", "Plugin", Plugin="PowerPlugin", PowerState="Percent", MinValue=0, MaxValue=100)
meas("mBatAC", "Plugin", Plugin="PowerPlugin", PowerState="ACLine")
meas("mPomoF", "Calc", Formula="#PomoFrac#", DynamicVariables=1)

def button(i, name, cx, cy, r, text, action, fs=16):
    sec(i, name + "B", "Shape", X=cx - r, Y=cy - r, W=2 * r, H=2 * r,
        Shape=f"Ellipse {r},{r},{r-1} | Fill Color #ColorSoft# | StrokeWidth 2 | Stroke Color #Color#",
        LeftMouseUpAction=action)
    txt(i, name + "T", text, cx, cy, fs, INK, face="Segoe UI Semibold")

# 49 Weather
i = 49
txt(i, "Icon", "[mWxIcon]", 220, 106, 54, "#Color#", face="Segoe UI Symbol")
txt(i, "Temp", "[mWxTempTxt]", 220, 215, 88, INK, face="Segoe UI Semibold")
txt(i, "Text", "[mWxText]", 220, 285, 20, DIM, W=380, ClipString=2, H=48)
txt(i, "Time", "[mH]:[mM]", 220, 342, 40, INK)
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 385, 16, DIM)

# 50 Sun times
i = 50
hand(i, "Track", 220, 310, 165, "mOne", 1, "#InkSoft#", start=PI, rot=PI, lstart=161, solid=1)
hand(i, "Prog", 220, 310, 165, "mSunF", 1, "#ColorDim#", start=PI, rot=PI, lstart=157, solid=1)
shp(i, "Sun", ["Line 40,310,400,310 | StrokeWidth 1 | Stroke Color #ColorMid#",
               mdot(220, 310, 161, "#SunRad#", 20, "#ColorSoft#"), mdot(220, 310, 161, "#SunRad#", 10, "#Color#")])
txt(i, "Time", "[mH]:[mM]", 220, 240, 60, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 282, 15, DIM)
txt(i, "L1", "[mLblSunrise]", 95, 338, 13, DIM)
txt(i, "T1", "[mSunRise]", 95, 362, 24, INK, face="Segoe UI Semibold")
txt(i, "L2", "[mLblSunset]", 345, 338, 13, DIM)
txt(i, "T2", "[mSunSet]", 345, 362, 24, INK, face="Segoe UI Semibold")
txt(i, "Note", "[mSunNote]", 220, 405, 12, "#Color#")

# 51 Battery
i = 51
hand(i, "Track", 220, 215, 160, "mOne", 1, "#InkSoft#", lstart=145, solid=1)
hand(i, "Prog", 220, 215, 160, "mBatPct", 1, "#Color#", lstart=145, solid=1)
txt(i, "Pct", "[mBatPct:0]%", 220, 205, 84, INK, face="Segoe UI Semibold")
txt(i, "State", "[mBatTxt]", 220, 270, 18, "#Color#")
txt(i, "Time", "[mH]:[mM]", 220, 330, 44, INK)
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 406, 15, DIM)

# 52 Timer and alarm (click the buttons)
i = 52
hand(i, "Track", 220, 195, 152, "mOne", 1, "#InkSoft#", lstart=138, solid=1)
hand(i, "Prog", 220, 195, 152, "mPomoF", 1, "#Color#", lstart=138, solid=1)
txt(i, "Label", "#PomoLabel#", 220, 118, 16, "#Color#", face="Segoe UI Semibold")
txt(i, "Left", "#PomoText#", 220, 195, 76, INK)
button(i, "Reset", 165, 262, 17, "R", '[!CommandMeasure mMain "PomoReset()"]', 12)
button(i, "Go", 220, 262, 26, "#PomoBtn#", '[!CommandMeasure mMain "PomoToggle()"]', 16)
button(i, "Skip", 275, 262, 17, ">>", '[!CommandMeasure mMain "PomoSkip()"]', 11)
txt(i, "Alarm", "#AlarmText#", 220, 374, 17, INK, face="Segoe UI Semibold",
    LeftMouseUpAction='[!CommandMeasure mMain "AlarmClick()"]')
button(i, "Minus", 150, 414, 17, "-15", '[!CommandMeasure mMain "AlarmAdd(-15)"]', 11)
button(i, "Plus", 290, 414, 17, "+15", '[!CommandMeasure mMain "AlarmAdd(15)"]', 11)
txt(i, "Time", "[mH]:[mM]", 220, 414, 16, DIM)

# ================================================================== v4.3: more clocks (53-91)
for _nm, _md in [("mMoonIcon", "moonIcon"), ("mMoonName", "moonName"), ("mMoonPct", "moonPct"), ("mMoonF", "moonF")]:
    lmeas(_nm, _md)

SEQ = [52]
def nxt():
    SEQ[0] += 1
    return SEQ[0]

# ---- coder styles: one IDE scene per programming language (v4.4)
for _nm, _md in [("mSecN", "secN")]:
    lmeas(_nm, _md)
meas("mLn8", "Calc", Formula="([mSecN]%8)+1")
for _k in range(4):
    lmeas(f"mCi{_k}", "ciStatus", Index=_k)
for _k in range(3):
    lmeas(f"mHx{_k}", "hexRow", Index=_k)
for _k in range(10):
    lmeas(f"mRain{_k}", "rain", Index=_k)
for _k in range(4):
    meas(f"mCore{_k}", "CPU", Processor=_k + 1)

# name: (badge text, badge colour, badge text colour, run command)
BADGE = {"Python": ("Py", "55,118,171", "255,222,87", "python clock.py"), "JavaScript": ("JS", "247,223,30", "30,30,30", "node clock.js"),
         "TypeScript": ("TS", "49,120,198", "250,250,250", "ts-node clock.ts"), "Java": ("Jv", "232,111,0", "250,250,250", "java Clock"),
         "C": ("C", "85,107,153", "250,250,250", "gcc clock.c && ./a.out"), "C++": ("C+", "0,89,156", "250,250,250", "g++ clock.cpp && ./a.out"),
         "C#": ("C#", "104,33,122", "250,250,250", "dotnet run"), "Go": ("Go", "0,173,216", "250,250,250", "go run clock.go"),
         "Rust": ("Rs", "183,65,14", "250,250,250", "cargo run"), "PHP": ("php", "119,123,179", "20,20,40", "php clock.php"),
         "Ruby": ("Rb", "204,52,45", "250,250,250", "ruby clock.rb"), "Swift": ("Sw", "240,81,56", "250,250,250", "swift Clock.swift"),
         "Kotlin": ("Kt", "127,82,255", "250,250,250", "kotlin ClockKt"), "SQL": ("SQL", "0,117,143", "250,250,250", "sqlite3 clock.db < clock.sql"),
         "HTML": ("<>", "227,79,38", "250,250,250", "open index.html"), "Bash": ("$_", "78,170,37", "250,250,250", "bash clock.sh"),
         "PowerShell": ("PS", "1,60,130", "250,250,250", "pwsh clock.ps1"), "Lua": ("Lu", "0,0,128", "250,250,250", "lua clock.lua"),
         "Dart": ("Dt", "1,117,194", "250,250,250", "dart run")}

CODE = [
 ("Python", "clock.py", [("# clock.py", "comment"), ("import time", "keyword"), ("def now() -> str:", "keyword"),
     ('    return "[mH]:[mM]:[mS]"', "string"), ("while True:", "keyword"), ("    print(now())", "func"), ("    time.sleep(1)", "func"),
     ("# [mDowS] [mDnum] [mMonS]", "comment")]),
 ("JavaScript", "clock.js", [("// clock.js", "comment"), ("const now = () =>", "keyword"), ('  "[mH]:[mM]:[mS]";', "string"),
     ("setInterval(() => {", "func"), ("  console.log(now());", "func"), ("}, 1000);", "func"), ("export default now;", "keyword"),
     ("// [mDowS] [mDnum] [mMonS]", "comment")]),
 ("TypeScript", "clock.ts", [("// clock.ts", "comment"), ("type Clock = () => string;", "type"), ("const now: Clock = () =>", "keyword"),
     ('  "[mH]:[mM]:[mS]";', "string"), ("let ticks: number = [mS];", "number"), ("setInterval(() => ticks++, 1000);", "func"),
     ("console.log(now());", "func"), ("export type { Clock };", "keyword")]),
 ("Java", "Clock.java", [("// Clock.java", "comment"), ("public class Clock {", "keyword"), ("  static String now() {", "keyword"),
     ('    return "[mH]:[mM]:[mS]";', "string"), ("  }", "text"), ("  static void main() {", "keyword"),
     ("    System.out.println(now());", "func"), ("}", "keyword")]),
 ("C", "clock.c", [("/* clock.c */", "comment"), ("#include <stdio.h>", "keyword"), ("int main(void) {", "keyword"),
     ('  char *t = "[mH]:[mM]:[mS]";', "string"), ("  int sec = [mS];", "number"), ("  puts(t);", "func"),
     ("  return 0;", "keyword"), ("}", "keyword")]),
 ("C++", "clock.cpp", [("// clock.cpp", "comment"), ("#include <iostream>", "keyword"), ("int main() {", "keyword"),
     ('  auto t = "[mH]:[mM]:[mS]";', "string"), ("  int s = [mS];", "number"), ("  std::cout << t << std::endl;", "func"),
     ("  return 0;", "keyword"), ("}", "keyword")]),
 ("C#", "Clock.cs", [("// Clock.cs", "comment"), ("using System;", "keyword"), ("class Clock {", "keyword"),
     ("  static void Main() {", "keyword"), ('    var t = "[mH]:[mM]:[mS]";', "string"), ("    Console.WriteLine(t);", "func"),
     ("  }", "text"), ("}", "keyword")]),
 ("Go", "clock.go", [("// clock.go", "comment"), ("package main", "keyword"), ('import "fmt"', "keyword"), ("func main() {", "keyword"),
     ('  t := "[mH]:[mM]:[mS]"', "string"), ("  s := [mS]", "number"), ("  fmt.Println(t, s)", "func"), ("}", "keyword")]),
 ("Rust", "clock.rs", [("// clock.rs", "comment"), ("fn main() {", "keyword"), ('    let t = "[mH]:[mM]:[mS]";', "string"),
     ("    let s: u32 = [mS];", "number"), ('    println!("{t}");', "func"), ("    let _ = s + 1;", "text"), ("}", "keyword"),
     ("// cargo run", "comment")]),
 ("PHP", "clock.php", [("<?php", "keyword"), ("// clock.php", "comment"), ('$t = "[mH]:[mM]:[mS]";', "string"), ("$sec = [mS];", "number"),
     ("echo $t . PHP_EOL;", "func"), ('echo date("D j M");', "func"), ("sleep(1);", "func"), ("?>", "keyword")]),
 ("Ruby", "clock.rb", [("# clock.rb", "comment"), ("def now", "keyword"), ('  "[mH]:[mM]:[mS]"', "string"), ("end", "keyword"),
     ("loop do", "keyword"), ("  puts now", "func"), ("  sleep 1", "func"), ("end", "keyword")]),
 ("Swift", "Clock.swift", [("// Clock.swift", "comment"), ("import Foundation", "keyword"), ("func now() -> String {", "keyword"),
     ('  return "[mH]:[mM]:[mS]"', "string"), ("}", "keyword"), ("var sec = [mS]", "number"), ("print(now())", "func"), ("sec += 1", "text")]),
 ("Kotlin", "clock.kt", [("// clock.kt", "comment"), ('fun now() = "[mH]:[mM]:[mS]"', "string"), ("fun main() {", "keyword"),
     ("  var sec = [mS]", "number"), ("  println(now())", "func"), ("  sec++", "text"), ("}", "keyword"), ("// ./gradlew run", "comment")]),
 ("SQL", "clock.sql", [("-- clock.sql", "comment"), ("SELECT", "keyword"), ("  '[mH]:[mM]:[mS]' AS now,", "string"),
     ("  [mS] AS seconds,", "number"), ("  '[mDowS] [mDnum] [mMonS]' AS day", "string"), ("FROM clock", "keyword"),
     ("WHERE tick = 1", "keyword"), ("LIMIT 1;", "keyword")]),
 ("HTML", "index.html", [("<!-- index.html -->", "comment"), ('<main class="clock">', "keyword"), ("  <h1>[mH]:[mM]:[mS]</h1>", "string"),
     ("  <p>[mDowS] [mDnum] [mMonS]</p>", "text"), ('  <meter value="[mS]" max="60">', "number"), ("  </meter>", "keyword"),
     ("</main>", "keyword"), ('<script src="tick.js"></script>', "func")]),
 ("Bash", "clock.sh", [("#!/bin/bash", "comment"), ('now="[mH]:[mM]:[mS]"', "string"), ("sec=[mS]", "number"), ("while true; do", "keyword"),
     ('  echo "$now"', "func"), ("  sleep 1", "func"), ("done", "keyword"), ("# [mDowS] [mDnum] [mMonS]", "comment")]),
 ("PowerShell", "clock.ps1", [("# clock.ps1", "comment"), ('$now = "[mH]:[mM]:[mS]"', "string"), ("$sec = [mS]", "number"),
     ("while ($true) {", "keyword"), ("  Write-Host $now", "func"), ("  Start-Sleep 1", "func"), ("}", "keyword"),
     ("# [mDowS] [mDnum] [mMonS]", "comment")]),
 ("Lua", "clock.lua", [("-- clock.lua", "comment"), ("local function now()", "keyword"), ('  return "[mH]:[mM]:[mS]"', "string"), ("end", "keyword"),
     ("local sec = [mS]", "number"), ("print(now(), sec)", "func"), ('os.execute("sleep 1")', "func"), ("-- [mDowS] [mDnum] [mMonS]", "comment")]),
 ("Dart", "clock.dart", [("// clock.dart", "comment"), ("String now() =>", "keyword"), ('    "[mH]:[mM]:[mS]";', "string"), ("void main() {", "keyword"),
     ("  var sec = [mS];", "number"), ("  print(now());", "func"), ("}", "keyword"), ("// dart run", "comment")]),
]

def ide(i, lang, fname, lines):
    badge, bcol, btxt, run = BADGE[lang]
    x0, y0, w = 14, 78, 412
    rows = 22
    first = y0 + 66
    sh = [rrect(x0, y0, w, 336, 10, "#CTbg#", 1, "#InkSoft#"), rrect(x0, y0, w, 26, 10, "#CTbar#"), rrect(x0, y0 + 13, w, 13, 0, "#CTbar#"),
          circle(x0 + 16, y0 + 13, 4.5, "255,95,86"), circle(x0 + 32, y0 + 13, 4.5, "255,189,46"), circle(x0 + 48, y0 + 13, 4.5, "39,201,63"),
          rrect(x0, y0 + 26, w, 26, 0, "#CTbar#,170"), rrect(x0 + 8, y0 + 27, 112, 25, 0, "#CTbg#"),
          f"Line {x0+8},{y0+28},{x0+120},{y0+28} | StrokeWidth 2 | Stroke Color #CTstatus#",
          rrect(x0 + 14, y0 + 31, 17, 17, 4, bcol),
          f"Rectangle {x0+1},({y0+55}+([mSecN]%8)*{rows}),{w-2},{rows} | Fill Color #CTtext#,24 | StrokeWidth 0",
          f"Ellipse {x0+14},({first}+([mSecN]%8)*{rows}),4.5 | Fill Color 232,72,72 | StrokeWidth 0",
          rrect(x0, y0 + 236, w, 78, 0, "#CTbar#"), f"Line {x0+14},{y0+256},{x0+66},{y0+256} | StrokeWidth 2 | Stroke Color #CTstatus#",
          rrect(x0, y0 + 314, w, 22, 10, "#CTstatus#"), rrect(x0, y0 + 314, w, 11, 0, "#CTstatus#"), circle(x0 + 16, y0 + 325, 5, bcol)]
    mx = x0 + w - 50
    for k, (line, role) in enumerate(lines):
        bw = min(38, 3 + len(line.strip()) * 1.15)
        sh.append(f"Rectangle {mx + (len(line) - len(line.lstrip())) * 1.1:.1f},{y0 + 62 + k * 7},{bw:.1f},4,2 | Fill Color #CT{role}#,200 | StrokeWidth 0")
    sh.append(f"Rectangle {mx-3},({y0+58}+([mSecN]%8)*7),46,11,2 | Fill Color 0,0,0,0 | StrokeWidth 1 | Stroke Color #CTtext#,140")
    shp(i, "Ide", sh)
    txt(i, "Title", f"{fname} - Adaptive IDE", x0 + w / 2, y0 + 13, 9, "#CTcomment#", face="Segoe UI")
    txt(i, "Badge", badge, x0 + 22.5, y0 + 39.5, 7 if len(badge) > 2 else 8, btxt, face="Segoe UI", style="Bold")
    txt(i, "Tab", fname, x0 + 37, y0 + 39.5, 10, "#CTtext#", align="LeftCenter", face="Segoe UI")
    txt(i, "Tab2", "README.md", x0 + 134, y0 + 39.5, 10, "#CTcomment#", align="LeftCenter", face="Segoe UI")
    for n, (line, role) in enumerate(lines):
        y = first + n * rows
        indent = len(line) - len(line.lstrip(" "))
        txt(i, f"N{n}", str(n + 1), x0 + 36, y, 11, "#CTnum#", align="RightCenter", face="Consolas")
        txt(i, f"C{n}", line.strip(), x0 + 48 + indent * 8.2, y, 12, f"#CT{role}#", align="LeftCenter", face="Consolas")
    txt(i, "TabOut", "OUTPUT", x0 + 14, y0 + 247, 9, "#CTtext#", align="LeftCenter", face="Segoe UI", style="Bold")
    txt(i, "TabProb", "PROBLEMS  0", x0 + 82, y0 + 247, 9, "#CTcomment#", align="LeftCenter", face="Segoe UI")
    txt(i, "Run", "$ " + run, x0 + 14, y0 + 268, 11, "#CTcomment#", align="LeftCenter", face="Consolas")
    txt(i, "Exit", "exit 0", x0 + w - 14, y0 + 268, 10, "80,200,110", align="RightCenter", face="Consolas")
    txt(i, "Out", "> [mH]:[mM]:[mS][mCursor]", x0 + 14, y0 + 295, 24, "#CTfunc#", align="LeftCenter", face="Consolas", style="Bold")
    txt(i, "Lang", lang, x0 + 28, y0 + 325, 10, "250,250,250", align="LeftCenter", face="Segoe UI", style="Bold")
    txt(i, "Pos", "Ln [mLn8], Col [mM]    UTF-8", x0 + w - 12, y0 + 325, 10, "250,250,250", align="RightCenter", face="Segoe UI")

for lang_name, fname, lines in CODE:
    ide(nxt(), lang_name, fname, lines)

# ---- girl styles (Theme: Girl)
i = nxt()   # 72 Butterfly
sh = ["Ellipse 150,178,72,50 | Fill Color #ColorSoft# | StrokeWidth 3 | Stroke Color #Color# | Rotate -28,150,178",
      "Ellipse 290,178,72,50 | Fill Color #ColorSoft# | StrokeWidth 3 | Stroke Color #Color# | Rotate 28,290,178",
      "Ellipse 166,258,50,38 | Fill Color #Color2Soft# | StrokeWidth 3 | Stroke Color #Color2# | Rotate 25,166,258",
      "Ellipse 274,258,50,38 | Fill Color #Color2Soft# | StrokeWidth 3 | Stroke Color #Color2# | Rotate -25,274,258",
      circle(142, 172, 10, "#Color2Soft#"), circle(298, 172, 10, "#Color2Soft#"),
      circle(168, 262, 7, "#ColorSoft#"), circle(272, 262, 7, "#ColorSoft#"),
      "Rectangle 213,150,14,130,7 | Fill Color #Color2# | StrokeWidth 0", circle(220, 144, 11, "#Color2#"),
      "Line 216,136,200,104 | StrokeWidth 2 | Stroke Color #Color2#", "Line 224,136,240,104 | StrokeWidth 2 | Stroke Color #Color2#"]
shp(i, "Butterfly", sh)
txt(i, "Time", "[mH]:[mM]", 220, 338, 54, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 384, 15, DIM)

i = nxt()   # 73 Cloud
sh = [circle(x, y, r, "#Color2Soft#", 2, "#Color#") for x, y, r in ((135, 232, 46), (200, 195, 62), (278, 212, 54), (238, 252, 52), (170, 258, 42))]
sh += [circle(x, y, r, "#Color2Soft#") for x, y, r in ((135, 232, 44), (200, 195, 60), (278, 212, 52), (238, 252, 50), (170, 258, 40))]
for k, (x, y) in enumerate(((120, 330), (165, 345), (215, 335), (265, 348), (315, 332))):
    sh.append(f"Line {x},{y},{x-8},{y+22} | StrokeWidth 3 | Stroke Color #Color2#")
for x, y, r in ((90, 130, 9), (340, 120, 12), (380, 200, 7), (70, 215, 7)):
    sh.append("Path S%d%d | Fill Color #Color# | StrokeWidth 0" % (x, y))
stars = {f"S{x}{y}": star_path(x, y, r, r * 0.42) for x, y, r in ((90, 130, 9), (340, 120, 12), (380, 200, 7), (70, 215, 7))}
shpx(i, "Cloud", sh, **stars)
txt(i, "Time", "[mH]:[mM]", 220, 228, 48, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDowS] [mDnum] [mMonS]", 220, 392, 15, DIM)

i = nxt()   # 74 Daisy
sh = [circle(220, 215, 150, sw=1, stroke="#ColorSoft#")]
for k in range(12):
    a = k * PI / 6
    px, py = 220 + 82 * cos(a), 215 + 82 * sin(a)
    sh.append(f"Ellipse {px:.1f},{py:.1f},44,15 | Fill Color #ColorSoft# | StrokeWidth 2 | Stroke Color #Color# | Rotate {k*30},{px:.1f},{py:.1f}")
sh += [circle(220, 215, 50, "#Color2Soft#", 3, "#Color2#"), mdot(220, 215, 150, "#SecRad#", 7, "#Color2#")]
shp(i, "Daisy", sh)
txt(i, "Time", "[mH]:[mM]", 220, 208, 30, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDowS] [mDnum]", 220, 236, 12, DIM)

i = nxt()   # 75 Bow
shpx(i, "Bow", ["Ellipse 158,190,66,46 | Fill Color #ColorSoft# | StrokeWidth 4 | Stroke Color #Color# | Rotate -16,158,190",
                "Ellipse 282,190,66,46 | Fill Color #ColorSoft# | StrokeWidth 4 | Stroke Color #Color# | Rotate 16,282,190",
                "Ellipse 158,190,36,20 | Fill Color 0,0,0,0 | StrokeWidth 2 | Stroke Color #Color2# | Rotate -16,158,190",
                "Ellipse 282,190,36,20 | Fill Color 0,0,0,0 | StrokeWidth 2 | Stroke Color #Color2# | Rotate 16,282,190",
                "Path Tail1 | Fill Color #Color2Soft# | StrokeWidth 3 | Stroke Color #Color2#",
                "Path Tail2 | Fill Color #Color2Soft# | StrokeWidth 3 | Stroke Color #Color2#",
                circle(220, 198, 25, "#Color#", 3, "#Color2#")],
     Tail1="206,218 | LineTo 162,302 | LineTo 194,290 | LineTo 210,316 | ClosePath 1",
     Tail2="234,218 | LineTo 278,302 | LineTo 246,290 | LineTo 230,316 | ClosePath 1")
txt(i, "Time", "[mH]:[mM]", 220, 352, 54, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 396, 15, DIM)

i = nxt()   # 76 Rainbow
for k, (r, col) in enumerate(zip((165, 150, 135, 120, 105, 90), ("255,120,140", "255,180,110", "255,230,120", "140,215,150", "130,185,250", "185,150,240"))):
    hand(i, f"B{k}", 220, 290, r, "mOne", 1, col, start=PI, rot=PI, lstart=r - 14, solid=1)
shp(i, "Sky", [mdot(220, 290, 128, "#DayRad#", 10, "250,250,250"),
               circle(62, 300, 24, "250,250,250,210"), circle(92, 290, 28, "250,250,250,210"), circle(120, 304, 22, "250,250,250,210"),
               circle(320, 304, 22, "250,250,250,210"), circle(348, 290, 28, "250,250,250,210"), circle(378, 300, 24, "250,250,250,210")])
txt(i, "Time", "[mH]:[mM]", 220, 262, 50, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 350, 16, DIM)

i = nxt()   # 77 Moonlight
sh = ["Path Moon | Fill Color #Color2# | StrokeWidth 0"]
stars = {"Moon": "182,100 | CurveTo 182,330,46,125,46,300 | CurveTo 182,100,118,310,112,140 | ClosePath 1"}
for k, (x, y, r) in enumerate(((250, 120, 10), (370, 140, 8), (330, 330, 9), (60, 70, 8), (300, 90, 6), (390, 260, 6))):
    sh.append(f"Path St{k} | Fill Color #Color# | StrokeWidth 0")
    stars[f"St{k}"] = star_path(x, y, r, r * 0.42)
shpx(i, "Night", sh, **stars)
txt(i, "Time", "[mH]:[mM]", 300, 205, 56, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum]", 300, 252, 16, DIM)
txt(i, "Mon", "[mMon]", 300, 276, 16, "#Color#")

# ---- boy styles (Theme: Boy)
i = nxt()   # 78 Rocket
ox = -95
shpx(i, "Rocket", [circle(60, 120, 2, "#InkMid#"), circle(150, 80, 3, "#InkMid#"), circle(40, 260, 2, "#InkMid#"),
                   circle(160, 340, 3, "#InkMid#"), circle(100, 370, 2, "#InkMid#"), circle(30, 170, 3, "#InkMid#"),
                   "Ellipse %d,334,16,32 | Fill Color 255,140,40 | StrokeWidth 0" % (220 + ox),
                   "Ellipse %d,326,9,20 | Fill Color 255,225,100 | StrokeWidth 0" % (220 + ox),
                   "Path FinL | Fill Color 226,60,60 | StrokeWidth 3 | Stroke Color 120,30,30",
                   "Path FinR | Fill Color 226,60,60 | StrokeWidth 3 | Stroke Color 120,30,30",
                   "Ellipse %d,215,42,100 | Fill Color 236,239,246 | StrokeWidth 3 | Stroke Color 90,96,112" % (220 + ox),
                   "Path Nose | Fill Color 226,60,60 | StrokeWidth 3 | Stroke Color 120,30,30",
                   circle(220 + ox, 205, 18, "100,190,255", 4, "70,80,100")],
     FinL=f"{182+ox},262 | LineTo {140+ox},322 | LineTo {184+ox},306 | ClosePath 1",
     FinR=f"{258+ox},262 | LineTo {300+ox},322 | LineTo {256+ox},306 | ClosePath 1",
     Nose=f"{180+ox},150 | CurveTo {260+ox},150,{198+ox},72,{242+ox},72 | ClosePath 1")
txt(i, "Time", "[mH]:[mM]", 310, 200, 56, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 310, 250, 15, DIM)
txt(i, "Sec", "T+ [mS]s", 310, 280, 15, "#Color#", face="Consolas")

i = nxt()   # 79 Pitch
sh = [rrect(40, 120, 360, 240, 8, "28,110,60,210", 3, "250,250,250,190"),
      "Line 220,120,220,360 | StrokeWidth 2 | Stroke Color 250,250,250,190",
      circle(220, 240, 38, sw=2, stroke="250,250,250,190"),
      rrect(40, 185, 62, 110, 0, "0,0,0,0", 2, "250,250,250,190"), rrect(338, 185, 62, 110, 0, "0,0,0,0", 2, "250,250,250,190"),
      rrect(40, 215, 22, 50, 0, "0,0,0,0", 2, "250,250,250,190"), rrect(378, 215, 22, 50, 0, "0,0,0,0", 2, "250,250,250,190"),
      "Ellipse (50+340*[mDayF]),(240+34*Sin([mDayF]*18.85)),9 | Fill Color 250,250,250 | StrokeWidth 2 | Stroke Color 40,40,40"]
shp(i, "Pitch", sh)
txt(i, "Time", "[mH]:[mM]", 220, 70, 58, INK, face="Segoe UI Semibold")
txt(i, "Mid", "[mS]", 220, 240, 24, "250,250,250", face="Consolas", style="Bold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 392, 15, DIM)

i = nxt()   # 80 Synthwave
sh = [rrect(30, 100, 380, 280, 14, "18,6,40"), "Ellipse 220,290,78 | Fill LinearGradient SunGrad | StrokeWidth 0",
      rrect(30, 290, 380, 90, 0, "18,6,40")]
for k in range(1, 6):
    y = 290 + k * k * 3.4
    sh.append(f"Line 30,{y:.1f},410,{y:.1f} | StrokeWidth 2 | Stroke Color 255,60,200,{230 - k * 25}")
for k in range(-7, 8):
    sh.append(f"Line 220,290,{220 + k * 26},380 | StrokeWidth 1 | Stroke Color 255,60,200,200")
shpx(i, "Grid", sh, SunGrad="90 | 255,210,70 ; 0.0 | 255,60,150 ; 1.0")
txt(i, "Date", "[mDow]  [mDnum]  [mMon]", 220, 126, 13, "100,230,255", face="Consolas", StringCase="Upper")
txt(i, "Time", "[mH]:[mM]", 220, 190, 70, "250,250,250", face="Consolas", style="Bold",
    StringEffect="Border", FontEffectColor="255,60,200,230")

i = nxt()   # 81 Game HUD
txt(i, "Name", "PLAYER 1", 40, 100, 12, "#Color#", align="LeftCenter", face="Consolas", style="Bold")
txt(i, "Lvl", "LVL [mDnum]", 400, 100, 12, "#Color2#", align="RightCenter", face="Consolas", style="Bold")
txt(i, "Time", "[mH]:[mM]", 220, 160, 74, INK, face="Consolas", style="Bold")
for n, (lab, m, val, col) in enumerate((("HP", "mHrF", "[mH]", "#Color#"), ("MP", "mMinF", "[mM]", "#Color2#"), ("XP", "mSecF", "[mS]", "#Color#"))):
    y = 250 + n * 42
    sh = [rrect(90, y - 11, 270, 22, 4, "0,0,0,130", 2, "#ColorMid#"), rrect(90, y - 11, f"(8+262*[{m}])", 22, 4, col)]
    sh += [f"Line {90 + k * 27},{y-11},{90 + k * 27},{y+11} | StrokeWidth 2 | Stroke Color 0,0,0,170" for k in range(1, 10)]
    shp(i, f"Bar{n}", sh)
    txt(i, f"L{n}", lab, 50, y, 15, INK, align="LeftCenter", face="Consolas", style="Bold")
    txt(i, f"V{n}", val, 392, y, 15, INK, align="RightCenter", face="Consolas")

i = nxt()   # 82 Race lights
sh = [rrect(40, 105, 360, 90, 14, "20,20,24,235", 2, "#ColorMid#")]
for k in range(5):
    x = 90 + k * 65
    sh.append(circle(x, 150, 24, "50,10,10", 3, "90,90,96"))
    sh.append(f"Ellipse {x},150,((([mSecF]*60)>={(k + 1) * 12 - 11})*20) | Fill Color 255,40,40 | StrokeWidth 0")
shp(i, "Lights", sh)
txt(i, "Lap", "LAP TIME", 220, 232, 12, "#Color#", face="Consolas", style="Bold")
txt(i, "Time", "[mH]:[mM]:[mS]", 220, 285, 64, INK, face="Consolas", style="Bold")
sec(i, "Bar", "Bar", X=70, Y=335, W=300, H=10, MeasureName="mMinF", BarColor="#Color#", SolidColor="#InkSoft#", BarOrientation="Horizontal")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 375, 15, DIM)

i = nxt()   # 83 Shield
shpx(i, "Shield", ["Path Shield | Fill Color #ColorSoft# | StrokeWidth 6 | Stroke Color #Color#",
                   "Path Inner | Fill Color 0,0,0,0 | StrokeWidth 2 | Stroke Color #Color2#",
                   "Path Star | Fill Color #Color2# | StrokeWidth 0"],
     Shield="95,100 | LineTo 345,100 | LineTo 345,225 | CurveTo 220,376,345,312,288,348 | CurveTo 95,225,152,348,95,312 | ClosePath 1",
     Inner="115,120 | LineTo 325,120 | LineTo 325,222 | CurveTo 220,350,325,300,278,326 | CurveTo 115,222,162,326,115,300 | ClosePath 1",
     Star=star_path(220, 158, 20, 8))
txt(i, "Time", "[mH]:[mM]", 220, 222, 58, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum]", 220, 272, 16, DIM)
txt(i, "Mon", "[mMon]", 220, 296, 16, "#Color#")

# ---- everyone: more neutral clocks
i = nxt()   # 84 Nixie
shp(i, "Tubes", [rrect(x, 130, 72, 140, 34, "26,14,8,240", 3, "255,150,50,170") for x in (40, 122, 246, 328)] +
    [circle(220, 175, 6, "255,150,50"), circle(220, 225, 6, "255,150,50")])
for x, m in ((76, "mDHT"), (158, "mDHU"), (282, "mDMT"), (364, "mDMU")):
    txt(i, f"D{x}", f"[{m}]", x, 200, 96, "255,166,60", face="Consolas", style="Bold", StringEffect="Border", FontEffectColor="255,90,20,120")
txt(i, "Sec", "[mS]", 220, 310, 28, "#Color#", face="Consolas")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 352, 16, DIM)

i = nxt()   # 85 Vinyl
sh = [circle(220, 215, 170, "18,18,20")] + [circle(220, 215, r, sw=1, stroke="55,55,60") for r in (150, 132, 114, 96, 78)]
sh += [circle(220, 215, 62, "230,90,70"), circle(220, 215, 6, "18,18,20"), mdot(220, 215, 48, "#SecRad#", 4, "250,250,250"),
       "Line 392,70,(220+(165-110*[mDayF])*0.82),(215-(165-110*[mDayF])*0.57) | StrokeWidth 6 | Stroke Color 205,205,210",
       circle(392, 70, 14, "60,60,66", 3, "205,205,210")]
shp(i, "Record", sh)
txt(i, "Time", "[mH]:[mM]", 220, 215, 24, "250,250,250", face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 412, 15, DIM)

i = nxt()   # 86 Compass
sh = [circle(220, 215, 170, sw=3, stroke="#InkMid#"), circle(220, 215, 120, sw=1, stroke="#InkSoft#")]
sh += dial_ticks(220, 215, 158, 168, "#InkMid#", n=72, w1=1, w2=2)
shp(i, "Dial", sh)
for t, a in (("N", 0), ("E", 1), ("S", 2), ("W", 3)):
    ang = a * PI / 2 - PI / 2
    txt(i, f"N{t}", t, f"{220+138*cos(ang):.1f}", f"{215+138*sin(ang):.1f}", 22, "#Color#" if t == "N" else INK, face="Segoe UI Semibold")
hand(i, "Min", 220, 215, 118, "mMinF", 2, "#Ink#")
hand(i, "Needle", 220, 215, 104, "mHrF", 7, "220,60,60")
hand(i, "Tail", 220, 215, 74, "mHrF", 7, "#Ink#", start=PI / 2)
shp(i, "Hub", [circle(220, 215, 9, "#Ink#")])
txt(i, "Time", "[mH]:[mM]", 220, 410, 22, DIM)

i = nxt()   # 87 Waves
sh = []
for k, (y, a) in enumerate(((268, 255), (292, 190), (316, 130))):
    sh.append(f"Path W{k} | Fill Color 0,0,0,0 | StrokeWidth {4 - k} | Stroke Color #Color#,{a}")
paths = {}
for k, y in enumerate((268, 292, 316)):
    seg = f"30,{y}"
    for j in range(4):
        x = 30 + j * 95
        seg += f" | CurveTo {x+95},{y},{x+32},{y-26},{x+63},{y-26}"
        seg = seg.replace(f"CurveTo {x+95},{y},{x+32},{y-26},{x+63},{y-26}", f"CurveTo {x+95},{y},{x+30},{y-24},{x+65},{y+24}")
    paths[f"W{k}"] = seg
shpx(i, "Waves", sh, **paths)
txt(i, "Time", "[mH]:[mM]", 220, 150, 92, INK)
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 222, 17, DIM)
txt(i, "Sec", "[mS]", 220, 360, 20, "#Color#")

i = nxt()   # 88 Zen circle
hand(i, "Ensou", 220, 215, 152, "mOne", 1, "#InkDim#", start=-1.15, rot=5.2, lstart=134, solid=1)
shp(i, "Dot", [mdot(220, 215, 143, "#MinRad#", 8, "#Color#")])
txt(i, "Time", "[mH]:[mM]", 220, 215, 62, INK)
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 268, 15, DIM)

i = nxt()   # 89 Day bar
segs = [(40, "#InkSoft#"), (130, "#ColorSoft#"), (220, "#Color2Soft#"), (310, "#ColorSoft#")]
shp(i, "Day", [rrect(x, 250, 90, 26, 0, c) for x, c in segs] +
    [rrect(40, 250, 360, 26, 6, "0,0,0,0", 2, "#ColorMid#"),
     "Line (40+360*[mDayF]),238,(40+360*[mDayF]),288 | StrokeWidth 3 | Stroke Color #Color#",
     "Ellipse (40+360*[mDayF]),238,8 | Fill Color #Color# | StrokeWidth 0"])
for k, hh in enumerate(("00", "06", "12", "18", "24")):
    txt(i, f"H{k}", hh, 40 + k * 90, 300, 11, DIM, face="Segoe UI")
txt(i, "Time", "[mH]:[mM]", 220, 140, 90, INK)
txt(i, "Pct", "[mDayF:%]% of today", 220, 205, 16, "#Color#")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 352, 16, DIM)

i = nxt()   # 90 Moon phase
hand(i, "Track", 220, 175, 112, "mOne", 1, "#InkSoft#", lstart=106, solid=1)
hand(i, "Prog", 220, 175, 112, "mMoonF", 1, "#Color#", lstart=106, solid=1)
txt(i, "Icon", "[mMoonIcon]", 220, 175, 110, INK, face="Segoe UI Emoji")
txt(i, "Name", "[mMoonName]", 220, 270, 22, INK, face="Segoe UI Semibold")
txt(i, "Pct", "[mMoonPct] lit", 220, 300, 15, "#Color#")
txt(i, "Time", "[mH]:[mM]", 220, 352, 44, INK)
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 396, 15, DIM)

i = nxt()   # 91 Skyline
hand(i, "Arc", 220, 360, 152, "mOne", 1, "#InkSoft#", start=PI, rot=PI, lstart=149, solid=1)
sh = [mdot(220, 360, 150, "#DayRad#", 20, "#ColorSoft#"),
      mdot(220, 360, 150, "#DayRad#", 11, "#Color#")]
for x, w, hh in ((30, 40, 70), (72, 34, 105), (108, 46, 60), (156, 30, 125), (188, 50, 85), (240, 36, 140), (278, 44, 75), (324, 32, 110), (358, 52, 62)):
    sh.append(f"Rectangle {x},{360-hh},{w},{hh} | Fill Color #InkDim# | StrokeWidth 0")
sh.append("Line 20,360,420,360 | StrokeWidth 2 | Stroke Color #InkDim#")
shp(i, "Sky", sh)
txt(i, "Time", "[mH]:[mM]", 220, 120, 74, INK, face="Segoe UI Semibold")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 178, 17, DIM)
assert SEQ[0] == 91, SEQ[0]
# ---- 92-99: more coder clocks
i = nxt()   # 92 Dot matrix
sh, cell, gap = [], 14, 3.5
for d, x in enumerate((52, 130, 238, 316)):
    for r in range(5):
        for c in range(4):
            sh.append(f"Rectangle {x + c * (cell + gap):.1f},{128 + r * (cell + gap):.1f},{cell},{cell},3 | Fill Color #Color#,#PX{d * 20 + r * 4 + c + 1}# | StrokeWidth 0")
for k, r in enumerate((1, 3)):
    sh.append(f"Rectangle 210,{128 + r * (cell + gap):.1f},{cell},{cell},3 | Fill Color #Color#,#PX{81 + k}# | StrokeWidth 0")
shp(i, "Matrix", sh)
shp(i, "Secs", [circle(40 + k * 6.2, 272, 1.2, "#InkSoft#") for k in range(60)] +
    [f"Ellipse {40 + k * 6.2:.1f},272,(([mSecN]>{k})*3.2) | Fill Color #Color# | StrokeWidth 0" for k in range(60)])
txt(i, "Cmt", "// dot matrix display", 220, 100, 12, "#Color#", face="Consolas")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 322, 16, DIM)

i = nxt()   # 93 Matrix rain
shp(i, "Panel", [rrect(14, 70, 412, 362, 12, "2,12,6,235", 1, "0,255,100,70")])
for k in range(10):
    txt(i, f"R{k}", f"[mRain{k}]", 38 + k * 40.5, 78, 13, "0,255,110,140", align="CenterTop", face="Consolas")
shp(i, "Box", [rrect(66, 180, 308, 124, 14, "0,14,6,225", 2, "0,255,110,210")])
txt(i, "Time", "[mH]:[mM]:[mS]", 220, 226, 46, "190,255,215", face="Consolas", style="Bold", StringEffect="Border", FontEffectColor="0,255,110,130")
txt(i, "Date", "[mDow], [mDnum] [mMon]", 220, 278, 13, "0,255,110", face="Consolas")

i = nxt()   # 94 CI pipeline
shp(i, "Card", [rrect(14, 84, 412, 340, 12, "#CTbg#", 1, "#InkSoft#")])
txt(i, "Head", "Pipeline #[mSha]", 34, 112, 15, "#CTtext#", align="LeftCenter", face="Segoe UI", style="Bold")
txt(i, "Branch", "main  -  tick: [mH]:[mM]", 34, 136, 11, "#CTcomment#", align="LeftCenter", face="Consolas")
for k, name in enumerate(("lint", "test", "build", "deploy")):
    y = 188 + k * 52
    run = f"(([mSecN]>={15 * k})*([mSecN]<{15 * (k + 1)}))"
    done = f"([mSecN]>={15 * (k + 1)})"
    shp(i, f"St{k}", [circle(46, y, 10, "0,0,0,0", 2, "#CTcomment#"),
                      f"Ellipse 46,{y},({done}*10) | Fill Color 63,185,80 | StrokeWidth 0",
                      f"Ellipse 46,{y},({run}*10) | Fill Color 56,152,255 | StrokeWidth 0",
                      rrect(72, y + 14, 250, 5, 2, "#CTbar#"),
                      rrect(72, y + 14, f"(0.01+{done}*250)", 5, 2, "63,185,80"),
                      rrect(72, y + 14, f"(0.01+{run}*250*(([mSecN]%15)/15))", 5, 2, "56,152,255")])
    txt(i, f"N{k}", name, 72, y - 4, 14, "#CTtext#", align="LeftCenter", face="Consolas", style="Bold")
    txt(i, f"S{k}", f"[mCi{k}]", 410, y - 4, 11, "#CTcomment#", align="RightCenter", face="Consolas")
txt(i, "Time", "[mH]:[mM]:[mS]", 220, 404, 20, "#CTfunc#", face="Consolas", style="Bold")

i = nxt()   # 95 Stack trace
window(i, 14, 92, 412, 322, "python3 clock.py")
txt(i, "L1", "Traceback (most recent call last):", 34, 142, 12, "244,100,100", align="LeftCenter", face="Consolas")
txt(i, "L2", '  File "clock.py", line [mS], in tick', 34, 170, 12, GREY, align="LeftCenter", face="Consolas")
txt(i, "L3", "    now = time.now()", 34, 194, 12, TXT, align="LeftCenter", face="Consolas")
txt(i, "L4", "AttributeError: no attribute 'now'", 34, 224, 12, "244,100,100", align="LeftCenter", face="Consolas")
txt(i, "Err", "ClockError: it is [mH]:[mM]:[mS]", 220, 282, 16, "255,176,64", face="Consolas", style="Bold")
txt(i, "Fix", "# fix: wait [mS] more seconds", 34, 330, 12, GREY, align="LeftCenter", face="Consolas")
txt(i, "Prompt", ">>> [mCursor]", 34, 360, 12, GREEN, align="LeftCenter", face="Consolas")

i = nxt()   # 96 Hexdump
window(i, 14, 92, 412, 322, "xxd clock.bin")
txt(i, "Head", "OFFS  00 01 02 03  04 05 06 07  ASCII", 34, 138, 10, GREY, align="LeftCenter", face="Consolas")
for k in range(3):
    txt(i, f"Row{k}", f"[mHx{k}]", 34, 174 + k * 34, 11, TXT if k else BLUE, align="LeftCenter", face="Consolas")
txt(i, "Time", "[mH]:[mM]:[mS]", 220, 300, 34, "#CTfunc#", face="Consolas", style="Bold")
txt(i, "Epoch", "epoch  [mEpoch]", 220, 346, 12, GREY, face="Consolas")

i = nxt()   # 97 Neofetch
window(i, 14, 92, 412, 322, "user@clock: ~")
shp(i, "Logo", [rrect(40 + (k % 2) * 44, 150 + (k // 2) * 44, 40, 40, 4, c) for k, c in enumerate(("#Color#", "#Color2#", "#Color2#", "#Color#"))])
txt(i, "Who", "user@clock", 150, 138, 14, "#Color#", align="LeftCenter", face="Consolas", style="Bold")
rows = (("OS", "Windows"), ("Shell", "Rainmeter"), ("Uptime", "[mUptime]"), ("CPU", "[mCPU:0]%"), ("RAM", "[mRAM:%]%"),
        ("Time", "[mH]:[mM]:[mS]"), ("Date", "[mDowS] [mDnum] [mMonS]"))
for k, (lab, val) in enumerate(rows):
    y = 168 + k * 24
    txt(i, f"K{k}", lab + ":", 150, y, 12, "#Color#", align="LeftCenter", face="Consolas", style="Bold")
    txt(i, f"V{k}", val, 222, y, 12, TXT, align="LeftCenter", face="Consolas")
shp(i, "Pal", [rrect(40 + k * 22, 350, 18, 18, 3, c) for k, c in enumerate(("40,40,44", "244,71,71", "63,185,80", "255,200,60", "56,152,255", "200,100,230", "0,200,200", "230,230,235"))])

i = nxt()   # 98 htop
window(i, 14, 92, 412, 322, "htop")
for k in range(4):
    y = 140 + k * 24
    txt(i, f"C{k}", str(k + 1), 34, y, 11, BLUE, align="LeftCenter", face="Consolas", style="Bold")
    sec(i, f"B{k}", "Bar", X=62, Y=y - 5, W=240, H=10, MeasureName=f"mCore{k}", BarColor="63,185,80", SolidColor="#InkSoft#", BarOrientation="Horizontal")
    txt(i, f"P{k}", f"[mCore{k}:0]%", 316, y, 11, TXT, align="LeftCenter", face="Consolas")
sec(i, "BM", "Bar", X=62, Y=231, W=240, H=10, MeasureName="mRAM", BarColor="56,152,255", SolidColor="#InkSoft#", BarOrientation="Horizontal")
txt(i, "CM", "Mem", 34, 236, 11, BLUE, align="LeftCenter", face="Consolas", style="Bold")
txt(i, "PM", "[mRAM:%]%", 316, 236, 11, TXT, align="LeftCenter", face="Consolas")
txt(i, "Tm", "[mH]:[mM]:[mS]   up [mUptime]", 34, 266, 11, "#CTfunc#", align="LeftCenter", face="Consolas")
shp(i, "Hdr", [rrect(24, 282, 392, 18, 3, "63,185,80")])
txt(i, "HT", "PID   USER   CPU%  MEM%  COMMAND", 34, 291, 10, "10,10,10", align="LeftCenter", face="Consolas", style="Bold")
for k, row in enumerate(("4021  root   12.4   3.1  rainmeter.exe", "1337  user    8.0   4.2  code.exe", "2210  user    5.3   6.8  chrome.exe",
                         "9001  user    1.2   0.9  clock.lua", "  88  root    0.3   0.1  system")):
    txt(i, f"R{k}", row, 34, 314 + k * 18, 10, TXT, align="LeftCenter", face="Consolas")

i = nxt()   # 99 Test runner
window(i, 14, 92, 412, 322, "npm test")
shp(i, "Chip", [rrect(30, 130, 44, 20, 3, "63,185,80")])
txt(i, "Pass", "PASS", 52, 140, 10, "10,10,10", face="Consolas", style="Bold")
txt(i, "File", "clock.test.js", 84, 140, 12, TXT, align="LeftCenter", face="Consolas")
for k, row in enumerate(("ok  shows [mH]:[mM]:[mS]", "ok  date is [mDowS] [mDnum] [mMonS]", "ok  tick() runs every second")):
    txt(i, f"T{k}", row, 44, 176 + k * 26, 12, GREEN if False else "#CTfunc#", align="LeftCenter", face="Consolas")
txt(i, "Sum1", "Tests:  3 passed, 3 total", 34, 270, 12, TXT, align="LeftCenter", face="Consolas", style="Bold")
txt(i, "Sum2", "Time:   0.[mS] s", 34, 294, 12, GREY, align="LeftCenter", face="Consolas")
txt(i, "Big", "[mH]:[mM]:[mS]", 220, 352, 28, "#CTfunc#", face="Consolas", style="Bold")
assert SEQ[0] == 99, SEQ[0]


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
SCRIPT = "ScriptFile=#CURRENTPATH#AdaptiveClock.lua"

def script(name, mode):
    return f"[{name}]\nMeasure=Script\n{SCRIPT}\nMode={mode}"

def lbl(name, key):
    return f"[{name}]\nMeasure=Script\n{SCRIPT}\nMode=lbl\nKey={key}"

_LBL = [("mLblHour", "hour"), ("mLblMinute", "minute"), ("mLblSecond", "second"), ("mLblHours", "hours"),
        ("mLblMinutes", "minutes"), ("mLblSeconds", "seconds"), ("mLblWorld", "world"), ("mLblDaysLeft", "daysLeft"),
        ("mLblDaysLeftYear", "daysLeftYear"), ("mLblYearDone", "yearDone"), ("mLblOfYear", "ofYear"),
        ("mLblSecondsLow", "secondsLow"), ("mLblSunrise", "sunrise"), ("mLblSunset", "sunset")]
DATE_M = "\n\n".join([script("mDow", "dow"), script("mDowS", "dowS"), script("mMon", "mon"), script("mMonS", "monS")]
                      + [lbl(n, k) for n, k in _LBL])
HV = "\n".join(f"H{n}=1" for n in range(1, 100)) + "\nQHf=1\nQHc=1\n" + "\n".join(f"CalH{n}=" for n in range(1, 8)) + "\n" + "\n".join(f"CalD{n}=" for n in range(1, 43)) + "\n" + "\n".join(f"PX{n}=40" for n in range(1, 83))
def tm(name, fmt):
    return f"[{name}]\nMeasure=Time\nFormat={fmt}"

head = f"""; AdaptiveClock.ini  by Amika Alankara  -  99 clock styles driven by AdaptiveClock.lua (same folder)
; Right-click the skin: Next / Random style, resume hourly shuffle, 12/24h, quote options.

[Rainmeter]
Update=#UpdateMs#
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
ContextTitle7=Language: next
ContextAction7=[!CommandMeasure mMain "CycleLanguage()"]
ContextTitle8=Colours: next mode (invert / accent / white / black)
ContextAction8=[!CommandMeasure mMain "CycleColors()"]
ContextTitle9=Next quote
ContextAction9=[!CommandMeasure mMain "NextQuote()"]
ContextTitle10=Show / hide quote
ContextAction10=[!CommandMeasure mMain "ToggleQuote()"]
ContextTitle11=Switch 12 / 24-hour
ContextAction11=[!CommandMeasure mMain "ToggleHourFormat()"]
ContextTitle12=Skip this style in future
ContextAction12=[!CommandMeasure mMain "SkipThisStyle()"]
ContextTitle13=Show all styles again
ContextAction13=[!CommandMeasure mMain "ShowAllStyles()"]
ContextTitle14=Open settings
ContextAction14=[!ActivateConfig "#CURRENTCONFIG#\\Settings" "Settings.ini"]
ContextTitle15=Open style gallery
ContextAction15=[!ActivateConfig "#CURRENTCONFIG#\\Gallery" "Gallery.ini"]

[Metadata]
Name=Adaptive Clock
Author=Amika Alankara
Version=4.4
Description=91 clock styles, coder (19 languages) / everyday profiles, girl / boy themes, 10 languages, weather, timer and more.

[Variables]
StyleCount=99
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
CodeTheme=Dark
CTbg=30,30,30,240
CTbar=37,37,38
CTnum=110,110,110
CTcomment=106,153,85
CTkeyword=86,156,214
CTstring=206,145,120
CTfunc=220,220,170
CTtype=78,201,176
CTnumber=181,206,168
CTtext=204,204,204
CTstatus=0,122,204
Language=Windows
Smooth=0
UpdateMs=1000
Div=1
Latitude=
Longitude=
TempUnit=celsius
WeatherOff=1
PomoWork=25
PomoBreak=5
TimerBeep=1
AlarmTime=07:00
AlarmOn=0
PomoText=25:00
PomoFrac=1.00000
PomoLabel=FOCUS
PomoBtn=>
AlarmText=Alarm 07:00  OFF
SunRad=3.14159
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
UpdateDivider=(30*#Div#)

[mWall]
Measure=Registry
RegHKey=HKEY_CURRENT_USER
RegSubKey=Control Panel\\Desktop
RegValue=WallPaper
UpdateDivider=(2*#Div#)
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

{tm('mDowW', '%A')}

{tm('mDowSW', '%a')}

{tm('mDnum', '%#d')}

{tm('mMonW', '%B')}

{tm('mMonSW', '%b')}

{tm('mYear', '%Y')}

{DATE_M}

; ---------------------------------------------------------------- meters
[Bg]
Meter=Shape
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
FAST = {"mAccent", "mMain", "mSecF", "mMinF", "mHrF", "mDayF", "mOne", "mWxRaw"}
SLOW = ("mGreet", "mGreetIcon", "mYearPct", "mYearF", "mDaysLeft", "mLbl", "mDow", "mDowS", "mMon", "mMonS", "mDowW",
        "mDowSW", "mMonW", "mMonSW", "mSunRise", "mSunSet", "mSunNote")
def with_dividers(text):
    out = []
    for block in text.split("\n\n"):
        m = re.match(r"\[(m\w+)\]", block)
        if m and "UpdateDivider" not in block and m.group(1) not in FAST:
            name = m.group(1)
            div = "(30*#Div#)" if name.startswith(SLOW) else "#Div#"
            block = block.rstrip("\n") + f"\nUpdateDivider={div}"
        out.append(block)
    return "\n\n".join(out)
open("../AdaptiveClock/AdaptiveClock.ini", "w", encoding="utf-8").write(with_dividers(head + "\n\n".join(S) + "\n"))
print(len(S), "meters")
