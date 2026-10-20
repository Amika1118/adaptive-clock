# Regenerates AdaptiveClock/AdaptiveClock.ini  (run from the tools folder: python gen_ini.py)
import math
from math import cos, sin, pi as PI

S = []          # style sections
CX = CY = 220
W, H = 440, 490

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

# ------------------------------------------------------------------ quotes (one per style)
for n in range(1, 25):
    sec(n, "Quote", "String", var="Q", X=220, Y=458, W=400, H=44, Text="[mMain]",
        FontFace="Segoe UI", FontSize=11, FontColor="#ColorDim#", StringAlign="CenterCenter",
        ClipString=2, AntiAlias=1)

# ------------------------------------------------------------------ header
HV = "\n".join(f"H{n}=1\nQ{n}=1" for n in range(1, 25))
SCRIPT = "ScriptFile=#CURRENTPATH#AdaptiveClock.lua"

def script(name, mode):
    return f"[{name}]\nMeasure=Script\n{SCRIPT}\nMode={mode}"

def tm(name, fmt):
    return f"[{name}]\nMeasure=Time\nFormat={fmt}"

head = f"""; AdaptiveClock.ini  by Amika Alankara  -  24 clock styles driven by AdaptiveClock.lua (same folder)
; Right-click the skin: Next / Random style, resume hourly shuffle, 12/24h, quote options.

[Rainmeter]
Update=1000
AccurateText=1
DynamicWindowSize=0
ContextTitle=Next style
ContextAction=[!CommandMeasure mMain "Next()"]
ContextTitle2=Random style
ContextAction2=[!CommandMeasure mMain "RandomStyle()"]
ContextTitle3=Resume hourly shuffle
ContextAction3=[!CommandMeasure mMain "Resume()"]
ContextTitle4=12-hour clock
ContextAction4=[!WriteKeyValue Variables HourFormat "%I" "#CURRENTPATH##CURRENTFILE#"][!Refresh]
ContextTitle5=24-hour clock
ContextAction5=[!WriteKeyValue Variables HourFormat "%H" "#CURRENTPATH##CURRENTFILE#"][!Refresh]
ContextTitle6=Show quote
ContextAction6=[!WriteKeyValue Variables QuoteHidden "0" "#CURRENTPATH##CURRENTFILE#"][!Refresh]
ContextTitle7=Hide quote
ContextAction7=[!WriteKeyValue Variables QuoteHidden "1" "#CURRENTPATH##CURRENTFILE#"][!Refresh]
ContextTitle8=New quote every hour
ContextAction8=[!WriteKeyValue Variables QuoteEveryHour "1" "#CURRENTPATH##CURRENTFILE#"][!Refresh]
ContextTitle9=New quote every day
ContextAction9=[!WriteKeyValue Variables QuoteEveryHour "0" "#CURRENTPATH##CURRENTFILE#"][!Refresh]
ContextTitle10=Colours: invert to wallpaper
ContextAction10=[!WriteKeyValue Variables ColorMode "Invert" "#CURRENTPATH##CURRENTFILE#"][!Refresh]
ContextTitle11=Colours: Windows accent
ContextAction11=[!WriteKeyValue Variables ColorMode "Accent" "#CURRENTPATH##CURRENTFILE#"][!Refresh]
ContextTitle13=Lock this style
ContextAction13=[!CommandMeasure mMain "Lock()"]
ContextTitle14=Unlock style
ContextAction14=[!CommandMeasure mMain "Unlock()"]
ContextTitle12=Re-check wallpaper brightness
ContextAction12=[!CommandMeasure mLum "Run"]

[Metadata]
Name=Adaptive Clock
Author=Amika Alankara
Version=3.1
Description=24 clock styles that shuffle hourly, follow the Windows accent colour and show a daily quote.

[Variables]
StyleCount=24
HourFormat=%H
QuoteHidden=0
QuoteEveryHour=0
StyleNo=1
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
Parameter=-NoProfile -ExecutionPolicy Bypass -File "#CURRENTPATH#WallpaperLuma.ps1"
OutputType=ANSI
State=Hide
Timeout=20000
UpdateDivider=600

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
ToolTipText=Style #StyleNo# of #StyleCount#  (double-click: next style)
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
S[:] = [inkify(x) for x in S]
open("../AdaptiveClock/AdaptiveClock.ini", "w", encoding="utf-8").write(head + "\n\n".join(S) + "\n")
print(len(S), "meters")
