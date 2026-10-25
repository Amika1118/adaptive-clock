# Generates the Settings and Gallery skins.  Run from the tools folder:  python gen_skins.py
# Author: Amika Alankara  (MIT License)
import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
SKIN = os.path.join(HERE, "..", "AdaptiveClock")
lua = open(os.path.join(SKIN, "AdaptiveClock.lua"), encoding="utf-8-sig").read()

# style names and tags come straight from AdaptiveClock.lua (single source of truth)
names_block = lua[lua.index("local NAMES = {"):lua.index("-- Styles that only appear")]
NAMES = re.findall(r"'([^']+)'", names_block)
TAGS = {}
for a, b, tag in re.findall(r"for i = (\d+), (\d+) do TAGS\[i\] = '(\w+)'", lua):
    for k in range(int(a), int(b) + 1):
        TAGS[k] = tag
for a, b in re.findall(r"TAGS\[(\d+)\], TAGS\[(\d+)\] = 'en', 'en'", lua):
    TAGS[int(a)] = TAGS[int(b)] = "en"

OFF, ON, TAB_OFF = "255,255,255,28", "77,142,255,235", "255,255,255,18"
FONT = "Segoe UI"

def sec(name, **o):
    return "\n".join([f"[{name}]"] + [f"{k}={v}" for k, v in o.items()])

def panel(w, h, title):
    return [sec("Bg", Meter="Shape", X=0, Y=0, W=w, H=h,
                Shape=f"Rectangle 0,0,{w},{h},12 | Fill Color 22,25,33,238 | StrokeWidth 1 | Stroke Color 255,255,255,30"),
            sec("Title", Meter="String", X=18, Y=14, Text=title, FontFace=FONT, FontSize=16, StringStyle="Bold",
                FontColor="250,250,250", AntiAlias=1),
            sec("Close", Meter="String", X=w - 18, Y=14, Text="X", StringAlign="Right", FontFace=FONT, FontSize=14,
                FontColor="200,200,210", AntiAlias=1, LeftMouseUpAction="[!DeactivateConfig]")]

def button(n, x, y, w, h, text, action, color_var=None, fill=None, fs=10, hide=None, dyn=True):
    fillc = f"#{color_var}#" if color_var else fill
    o = dict(Meter="Shape", X=x, Y=y, W=w, H=h, Shape=f"Rectangle 0,0,{w},{h},6 | Fill Color {fillc} | StrokeWidth 0")
    if action:
        o["LeftMouseUpAction"] = action
    if hide:
        o["Hidden"] = f"#{hide}#"
    o["DynamicVariables"] = 1
    t = dict(Meter="String", X=x + w / 2, Y=y + h / 2, W=w - 4, H=h, Text=text, StringAlign="CenterCenter", FontFace=FONT,
             FontSize=fs, FontColor="245,245,250", ClipString=1, AntiAlias=1)
    if hide:
        t["Hidden"] = f"#{hide}#"
        t["DynamicVariables"] = 1
    return [sec(f"Btn{n}", **o), sec(f"Btn{n}T", **t)]

def act(call):                                    # call a function in the clock skin
    return f'[!CommandMeasure mMain "{call}" "#Main#"]'

# ======================================================================== Settings (6 pages)
LANGS = ["Windows", "English", "Spanish", "French", "German", "Portuguese", "Italian", "Sinhala", "Tamil", "Hindi", "Japanese"]
PROFILE = ("Profile", "Profile", [("All", "All"), ("Coder", "Coder"), ("Everyday", "Everyday")])
THEME = ("Theme", "Theme", [("Classic", "Neutral"), ("Bloom", "Bloom"), ("Volt", "Volt")])
PAGES = [
    ("Start", "start", [PROFILE, THEME]),
    ("Style", "plain", [
        ("Code colours", "CodeTheme", [("Dark", "Dark"), ("Dracula", "Dracula"), ("Monokai", "Monokai"), ("Light", "Light")]),
        ("Text colour", "ColorMode", [("Invert", "Invert"), ("Accent", "Accent"), ("White", "White"), ("Black", "Black")]),
        ("Style changes", "ShuffleMinutes", [("60 min", "60"), ("30 min", "30"), ("15 min", "15"), ("5 min", "5"), ("Daily", "1440")]),
    ]),
    ("Language", "plain", [
        ("Language", "Language", [(l, l) for l in LANGS]),
        ("Clock", "HourFormat", [("24 hour", "H24"), ("12 hour", "H12")]),
        ("Week starts", "WeekStart", [("Monday", "1"), ("Sunday", "0")]),
    ]),
    ("Quote", "plain", [
        ("Quote", "QuoteHidden", [("Show", "0"), ("Hide", "1")]),
        ("Changes", "QuoteMinutes", [("Daily", "1440"), ("Hourly", "60"), ("30 min", "30"), ("10 min", "10")]),
        ("Design", "QuoteStyle", [("Auto", "Auto"), ("Friendly", "Friendly"), ("Terminal", "Terminal")]),
    ]),
    ("Extras", "extras", [
        ("Smooth seconds", "Smooth", [("Off", "0"), ("On", "1")]),
        ("Weather", "WeatherOff", [("Off", "1"), ("On", "0")]),
        ("Temperature", "TempUnit", [("Celsius", "celsius"), ("Fahrenheit", "fahrenheit")]),
        ("Focus timer", "PomoWork", [("15 min", "15"), ("25 min", "25"), ("50 min", "50")]),
        ("Break", "PomoBreak", [("5 min", "5"), ("10 min", "10"), ("15 min", "15")]),
        ("Timer beep", "TimerBeep", [("On", "1"), ("Off", "0")]),
    ]),
    ("Actions", "actions", []),
]
ACTIONS = [("Next style", "Next()"), ("Random style", "RandomStyle()"), ("Lock / unlock this style", "ToggleLock()"),
           ("Resume shuffle + re-check wallpaper", "Resume()"), ("Next quote", "NextQuote()"),
           ("Skip this style in future", "SkipThisStyle()"), ("Show all styles again", "ShowAllStyles()"),
           ("Reset all settings", "ResetSettings()")]
GALLERY = '[!ActivateConfig "#Main#\\\\Gallery" "Gallery.ini"]'

SW, ROW, TOP = 500, 42, 138
meters, variables, n, group_id = [], [], 0, 0
page_h = []

def note(name, text, x, y, w, h, size=9, color="140,146,165", hide=None, bold=False):
    o = dict(Meter="String", X=x, Y=y, W=w, H=h, Text=text, ClipString=2, FontFace=FONT, FontSize=size, FontColor=color, AntiAlias=1)
    if bold: o["StringStyle"] = "Bold"
    if hide: o.update(Hidden=f"#{hide}#", DynamicVariables=1)
    return sec(name, **o)

for p, (pname, kind, groups) in enumerate(PAGES, start=1):
    y = TOP
    hide = f"Pg{p}"
    if kind == "start":
        meters.append(note("Welcome", "Welcome! Pick a look below, then press Surprise me. Everything stays on this PC.", 18, y - 8, SW - 36, 34, 11, "200,205,220", hide))
        y += 34
    for label, var, opts in groups:
        group_id += 1
        chunks = [opts[i:i + 6] for i in range(0, len(opts), 6)]
        k = len(chunks[0])
        bw = (SW - 36 - 112 - (k - 1) * 4) / k
        variables.append(f"GV{group_id}=")
        meters.append(sec(f"GLbl{group_id}", Meter="String", X=18, Y=y + 4, Text=label, FontFace=FONT, FontSize=10,
                          FontColor="200,205,220", AntiAlias=1, Hidden=f"#{hide}#", DynamicVariables=1))
        meters.append(sec(f"GVal{group_id}", Meter="String", X=18, Y=y + 20, W=104, H=14, Text=f"#GV{group_id}#", FontFace=FONT,
                          FontSize=9, StringStyle="Bold", FontColor="110,170,255", ClipString=1, AntiAlias=1,
                          Hidden=f"#{hide}#", DynamicVariables=1))
        for chunk in chunks:
            for j, (text, val) in enumerate(chunk):
                n += 1
                variables += [f"B{n}V={var}", f"B{n}X={val}", f"B{n}F=clock", f"B{n}G={group_id}", f"B{n}L={text}",
                              f"B{n}O={OFF}", f"B{n}C={OFF}"]
                meters += button(n, 130 + j * (bw + 4), y + 4, bw, 26, text, act(f"Set('{var}','{val}')"), color_var=f"B{n}C", hide=hide)
            y += ROW
    if kind == "start":
        y += 6
        bw3 = (SW - 36 - 8) / 3
        for j, (text, action, fill) in enumerate((("Surprise me", act("RandomStyle()"), "77,142,255,200"), ("Next style", act("Next()"), "255,255,255,36"),
                                                  ("Open style gallery", GALLERY, "255,255,255,36"))):
            meters += button(950 + j, 18 + j * (bw3 + 4), y, bw3, 34, text, action, fill=fill, hide=hide, fs=11)
        y += 50
        meters.append(note("Tips", "Tips:  double-click the clock for the next style  -  right-click it for the menu  -  "
                                   "Settings > Extras shows where your location comes from (it never leaves this PC).", 18, y, SW - 36, 44, 9, hide=hide))
        y += 44
    if kind == "extras":
        y += 4
        meters.append(note("LocStatus", "#LocStatus#", 18, y, SW - 36, 18, 10, "110,170,255", hide, True))
        meters += button(970, 18, y + 22, 200, 28, "Find my location again", act("RefreshLocation()"), fill="255,255,255,36", hide=hide)
        y += 60
        meters.append(note("Privacy", "Privacy: your location is found on this PC (Windows location, or your time zone) and used only for sunrise and sunset. "
                                      "Weather is the one feature that uses the internet: when you turn it on, it sends your position rounded to about 11 km "
                                      "to open-meteo.com. Weather is off by default; you can type a different place in AdaptiveClock.ini "
                                      "(WeatherLatitude / WeatherLongitude) if you prefer.", 18, y, SW - 36, 84, 9, hide=hide))
        y += 84
    if kind == "actions":
        aw = (SW - 36 - 8) / 2
        for j, (text, call) in enumerate(ACTIONS):
            meters += button(900 + j, 18 + (j % 2) * (aw + 8), y + (j // 2) * 38, aw, 30, text, act(call), fill="255,255,255,36", hide=hide)
        y += ((len(ACTIONS) + 1) // 2) * 38 + 4
        meters += button(990, 18, y, aw, 30, "Open style gallery", GALLERY, fill="77,142,255,160", hide=hide)
        y += 44
        meters.append(note("ActHint", "Weather and sunrise find your location automatically. You can also type Latitude and Longitude in AdaptiveClock.ini "
                                      "([Variables]). Changing a setting refreshes the clock.", 18, y, SW - 36, 60, 9, hide=hide))
        y += 60
    page_h.append(y)

H = max(page_h) + 24
TAB_Y, TAB_H = 92, 30
tw = (SW - 36 - 4 * (len(PAGES) - 1)) / len(PAGES)
header = [
    sec("Crumb", Meter="String", X=18, Y=40, Text="Settings  >  #CrumbPage#", FontFace=FONT, FontSize=11, StringStyle="Bold",
        FontColor="110,170,255", AntiAlias=1, DynamicVariables=1),
    sec("Now", Meter="String", X=18, Y=60, W=SW - 36, H=16, Text="#NowShowing#", FontFace=FONT, FontSize=9,
        FontColor="170,175,190", ClipString=1, AntiAlias=1, DynamicVariables=1),
]
for p, (pname, _, _) in enumerate(PAGES, start=1):
    header += button(800 + p, 18 + (p - 1) * (tw + 4), TAB_Y, tw, TAB_H, pname, f'[!CommandMeasure mSettings "Page({p})"]',
                     color_var=f"Tab{p}", fs=11)
    variables.append(f"Tab{p}={TAB_OFF}")
    variables.append(f"Pg{p}={0 if p == 1 else 1}")
    variables.append(f"PageName{p}={pname}")
variables.append("CrumbPage=Start")
variables.append("NowShowing=")
variables.append("LocStatus=")
shead = f"""; Settings.ini  -  settings window for Adaptive Clock   (generated by tools/gen_skins.py)
; Author: Amika Alankara  (MIT License)

[Rainmeter]
Update=1000
AccurateText=1
OnRefreshAction=[!Move 120 120]

[Variables]
Main=AdaptiveClock
BtnCount={n}
PageCount={len(PAGES)}
{chr(10).join(variables)}

[mSettings]
Measure=Script
ScriptFile=#CURRENTPATH#Settings.lua
UpdateDivider=2

"""
open(os.path.join(SKIN, "Settings", "Settings.ini"), "w", encoding="utf-8").write(
    shead + "\n\n".join(panel(SW, H, "Adaptive Clock settings") + header + meters) + "\n")

open(os.path.join(SKIN, "Settings", "Settings.lua"), "w", encoding="utf-8").write(r"""-- Settings.lua  -  logic of the Settings window and the style gallery
-- Author: Amika Alankara  (MIT License)
--  * shows which page you are on (breadcrumb + highlighted tab)
--  * highlights the active choice of every setting and prints its current value next to the label
--  * shows which clock style is on screen and where the location comes from (the clock writes ..\state.txt)
local count, pages, paths = 0, 5, {}
local lastKey, lastNow, lastLoc
local MAP = { H24 = '%H', H12 = '%#I' }
local ON, TAB_OFF = '77,142,255,235', '255,255,255,18'
local LOC = {
  windows  = 'Location: from Windows - kept on this PC',
  timezone = 'Location: estimated from your time zone - kept on this PC',
  manual   = 'Location: typed in AdaptiveClock.ini - kept on this PC',
  none     = 'Location: not found - turn on Windows location or type it in AdaptiveClock.ini',
}

local function setv(n, v) SKIN:Bang('!SetVariable', n, tostring(v)) end

function Initialize()
  local cfg = SKIN:GetVariable('CURRENTCONFIG', '')
  setv('Main', cfg:match('^(.*)\\[^\\]+$') or 'AdaptiveClock')
  count = tonumber(SKIN:GetVariable('BtnCount', '0')) or 0
  pages = tonumber(SKIN:GetVariable('PageCount', '0')) or 0
  local here = SKIN:GetVariable('CURRENTPATH', '')
  paths = { clock = here .. '..\\AdaptiveClock.ini', state = here .. '..\\state.txt' }
  if pages > 0 then Page(1) end
end

function Page(p)                                   -- show one page of the Settings window
  p = tonumber(p) or 1
  for k = 1, pages do
    setv('Pg' .. k, k == p and 0 or 1)
    setv('Tab' .. k, k == p and ON or TAB_OFF)
  end
  setv('CrumbPage', SKIN:GetVariable('PageName' .. p, ''))
  SKIN:Bang('!UpdateMeter', '*')
  SKIN:Bang('!Redraw')
end

local function readVars(path, onlyVariables)
  local f = io.open(path, 'r')
  if not f then return {} end
  local vars, inVars = {}, not onlyVariables
  for line in f:lines() do
    if onlyVariables and line:match('^%[Variables%]') then inVars = true
    elseif onlyVariables and inVars and line:match('^%[') then break
    elseif inVars then
      local k, v = line:match('^([%w_]+)=(.*)$')
      if k then vars[k] = (v:gsub('\r', '')) end
    end
  end
  f:close()
  return vars
end

function Update()
  local files = { clock = readVars(paths.clock, true), state = readVars(paths.state, false) }
  local st = files.state
  local now = (st.StyleName and st.StyleName ~= '')
      and ('Now showing:  ' .. st.StyleName .. '  (style ' .. (st.StyleNo or '?') .. ' of ' .. (st.StyleTotal or '?') .. ')'
           .. ((st.Locked == '1') and '  -  locked' or ''))
      or 'Now showing: (load the clock to see its style)'
  if now ~= lastNow then lastNow = now; setv('NowShowing', now) end
  local loc = LOC[st.Location or 'none'] or LOC.none
  if loc ~= lastLoc then lastLoc = loc; setv('LocStatus', loc) end
  if count == 0 then return 0 end

  local parts, values = {}, {}
  for n = 1, count do
    local file = files[SKIN:GetVariable('B' .. n .. 'F', 'clock')] or files.clock
    local name = SKIN:GetVariable('B' .. n .. 'V', '')
    local val  = SKIN:GetVariable('B' .. n .. 'X', '')
    local cur = file[name]
    if name == 'Theme' and cur == 'Girl' then cur = 'Bloom' elseif name == 'Theme' and cur == 'Boy' then cur = 'Volt' end
    local on = (cur == (MAP[val] or val))
    parts[n] = on and '1' or '0'
    if on then
      local g = SKIN:GetVariable('B' .. n .. 'G', '0')
      if g ~= '0' then values[g] = SKIN:GetVariable('B' .. n .. 'L', '') end
    end
  end
  local key = table.concat(parts) .. '|' .. loc
  if key ~= lastKey then
    lastKey = key
    for n = 1, count do
      setv('B' .. n .. 'C', parts[n] == '1' and ON or SKIN:GetVariable('B' .. n .. 'O', '255,255,255,28'))
    end
    for g, text in pairs(values) do setv('GV' .. g, text) end
    SKIN:Bang('!UpdateMeter', '*')
    SKIN:Bang('!Redraw')
  end
  return 0
end
""")

# ======================================================================== Gallery
COL = {None: "255,255,255,34", "en": "255,255,255,34", "code": "88,166,255,80", "easy": "63,185,80,80",
       "girl": "255,105,180,90", "boy": "56,152,255,100"}
GW, cols, bw, bh = 568, 5, 104, 28
gm, variables, gy = [], [], 112
for i, name in enumerate(NAMES, start=1):
    r, c = divmod(i - 1, cols)
    label = f"{i}  {name}" + ("  (EN)" if TAGS.get(i) == "en" else "")
    variables += [f"B{i}V=StyleNo", f"B{i}X={i}", f"B{i}F=state", f"B{i}G=0", f"B{i}L={name}", f"B{i}O={COL[TAGS.get(i)]}", f"B{i}C={COL[TAGS.get(i)]}"]
    gm += button(i, 18 + c * (bw + 6), gy + r * (bh + 6), bw, bh, label, act(f"GoTo({i})"), color_var=f"B{i}C", fs=9)
gy += ((len(NAMES) + cols - 1) // cols) * (bh + 6) + 8
legend = [("Everyone", None), ("Coder", "code"), ("Everyday", "easy"), ("Bloom theme", "girl"), ("Volt theme", "boy")]
for j, (text, tag) in enumerate(legend):
    gm += button(800 + j, 18 + j * (bw + 6), gy, bw, 22, text, "", fill=COL[tag], fs=9)
gy += 34
gm += button(850, 18, gy, 170, 26, "Unlock + resume shuffle", act("Unlock()"), fill="255,255,255,46")
gy += 44
gheader = [sec("Now", Meter="String", X=18, Y=42, W=GW - 36, H=16, Text="#NowShowing#", FontFace=FONT, FontSize=10,
               StringStyle="Bold", FontColor="110,170,255", ClipString=1, AntiAlias=1, DynamicVariables=1),
           sec("Hint", Meter="String", X=18, Y=64, W=GW - 36, H=30, ClipString=2, FontFace=FONT, FontSize=9,
               FontColor="140,146,165", AntiAlias=1,
               Text="Click a style to show it and lock it. The highlighted style is the one on screen. "
                    "Styles marked EN need the Windows or English language.")]
ghead = f"""; Gallery.ini  -  click a style to show it and keep it   (generated by tools/gen_skins.py)
; Author: Amika Alankara  (MIT License)

[Rainmeter]
Update=1000
OnRefreshAction=[!Move 160 160]

[Variables]
Main=AdaptiveClock
BtnCount={len(NAMES)}
PageCount=0
NowShowing=
{chr(10).join(variables)}

[mSettings]
Measure=Script
ScriptFile=#CURRENTPATH#..\\Settings\\Settings.lua
UpdateDivider=2

"""
open(os.path.join(SKIN, "Gallery", "Gallery.ini"), "w", encoding="utf-8").write(
    ghead + "\n\n".join(panel(GW, gy, "Style gallery") + gheader + gm) + "\n")
print("settings buttons:", n, "| gallery styles:", len(NAMES), "| settings height:", H)
