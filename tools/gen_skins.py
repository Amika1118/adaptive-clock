# Generates the Settings and Gallery skins.  Run from the tools folder:  python gen_skins.py
# Author: Amika Alankara  (MIT License)
import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
SKIN = os.path.join(HERE, "..", "AdaptiveClock")
lua = open(os.path.join(SKIN, "AdaptiveClock.lua"), encoding="utf-8").read()

# style names and tags come straight from AdaptiveClock.lua (single source of truth)
names_block = lua[lua.index("local NAMES = {"):lua.index("-- Styles that only appear")]
NAMES = re.findall(r"'([^']+)'", names_block)
TAGS = {}
for a, b, tag in re.findall(r"for i = (\d+), (\d+) do TAGS\[i\] = '(\w+)'", lua):
    for k in range(int(a), int(b) + 1):
        TAGS[k] = tag
for a, b in re.findall(r"TAGS\[(\d+)\], TAGS\[(\d+)\] = 'en', 'en'", lua):
    TAGS[int(a)] = TAGS[int(b)] = "en"

OFF, ON = "255,255,255,28", "77,142,255,235"
BASE_FONT = "Segoe UI"

def sec(name, **o):
    return "\n".join([f"[{name}]"] + [f"{k}={v}" for k, v in o.items()])

def panel(w, h, title, sub=None):
    out = [sec("Bg", Meter="Shape", X=0, Y=0, W=w, H=h,
               Shape=f"Rectangle 0,0,{w},{h},12 | Fill Color 22,25,33,238 | StrokeWidth 1 | Stroke Color 255,255,255,30"),
           sec("Title", Meter="String", X=18, Y=16, Text=title, FontFace=BASE_FONT, FontSize=16, StringStyle="Bold",
               FontColor="250,250,250", AntiAlias=1),
           sec("Close", Meter="String", X=w - 18, Y=14, Text="X", StringAlign="Right", FontFace=BASE_FONT, FontSize=14,
               FontColor="200,200,210", AntiAlias=1, LeftMouseUpAction="[!DeactivateConfig]")]
    if sub:
        out.append(sec("Sub", Meter="String", X=18, Y=40, Text=sub, FontFace=BASE_FONT, FontSize=10,
                       FontColor="170,175,190", AntiAlias=1))
    return out

def button(n, x, y, w, h, text, action, color_var=None, fill=None, fs=10):
    fillc = f"#{color_var}#" if color_var else fill
    shape = sec(f"Btn{n}", Meter="Shape", X=x, Y=y, W=w, H=h, Shape=f"Rectangle 0,0,{w},{h},6 | Fill Color {fillc} | StrokeWidth 0",
                LeftMouseUpAction=action, DynamicVariables=1)
    label = sec(f"Btn{n}T", Meter="String", X=x + w / 2, Y=y + h / 2, W=w - 4, H=h, Text=text, StringAlign="CenterCenter",
                FontFace=BASE_FONT, FontSize=fs, FontColor="245,245,250", ClipString=1, AntiAlias=1)
    return [shape, label]

def act(call):                                    # call a function in the main skin
    return f'[!CommandMeasure mMain "{call}" "#Main#"]'

# ======================================================================== Settings
LANGS = ["Windows", "English", "Spanish", "French", "German", "Portuguese", "Italian", "Sinhala", "Tamil", "Hindi", "Japanese"]
GROUPS = [
    ("Profile", "Profile", [("All", "All"), ("Coder", "Coder"), ("Everyday", "Everyday")]),
    ("Theme", "Theme", [("Neutral", "Neutral"), ("Girl", "Girl"), ("Boy", "Boy")]),
    ("Text colour", "ColorMode", [("Invert", "Invert"), ("Accent", "Accent"), ("White", "White"), ("Black", "Black")]),
    ("Language", "Language", [(l, l) for l in LANGS]),
    ("Clock", "HourFormat", [("24 hour", "H24"), ("12 hour", "H12")]),
    ("Week starts", "WeekStart", [("Monday", "1"), ("Sunday", "0")]),
    ("Style changes", "ShuffleMinutes", [("60 min", "60"), ("30 min", "30"), ("15 min", "15"), ("5 min", "5"), ("Daily", "1440")]),
    ("Quote", "QuoteHidden", [("Show", "0"), ("Hide", "1")]),
    ("Quote changes", "QuoteMinutes", [("Daily", "1440"), ("Hourly", "60"), ("30 min", "30"), ("10 min", "10")]),
    ("Quote design", "QuoteStyle", [("Auto", "Auto"), ("Friendly", "Friendly"), ("Terminal", "Terminal")]),
    ("Smooth seconds", "Smooth", [("Off", "0"), ("On", "1")]),
    ("Weather", "WeatherOff", [("Off", "1"), ("On", "0")]),
    ("Temperature", "TempUnit", [("Celsius", "celsius"), ("Fahrenheit", "fahrenheit")]),
    ("Focus timer", "PomoWork", [("15 min", "15"), ("25 min", "25"), ("50 min", "50")]),
    ("Break", "PomoBreak", [("5 min", "5"), ("10 min", "10"), ("15 min", "15")]),
    ("Timer beep", "TimerBeep", [("On", "1"), ("Off", "0")]),
]
ACTIONS = [("Next style", "Next()"), ("Random style", "RandomStyle()"), ("Lock / unlock", "ToggleLock()"),
           ("Next quote", "NextQuote()"), ("Skip this style", "SkipThisStyle()"), ("Show all styles", "ShowAllStyles()")]

SW = 480
meters, variables, n, y = [], [], 0, 70
for label, var, opts in GROUPS:
    chunks = [opts[i:i + 6] for i in range(0, len(opts), 6)]
    k = len(chunks[0])
    bw = (332 - (k - 1) * 4) / k
    meters.append(sec(f"Lbl{var}", Meter="String", X=18, Y=y + 12, Text=label, StringAlign="LeftCenter", FontFace=BASE_FONT,
                      FontSize=10, FontColor="170,175,190", AntiAlias=1))
    for chunk in chunks:
        for j, (text, val) in enumerate(chunk):
            n += 1
            variables += [f"B{n}V={var}", f"B{n}X={val}", f"B{n}C={OFF}"]
            meters += button(n, 130 + j * (bw + 4), y, bw, 24, text, act(f"Set('{var}','{val}')"), color_var=f"B{n}C")
        y += 32
y += 6
meters.append(sec("LblActions", Meter="String", X=18, Y=y + 2, Text="Actions", FontFace=BASE_FONT, FontSize=10,
                  FontColor="170,175,190", AntiAlias=1))
y += 24
aw = (SW - 36 - 8) / 3
for j, (text, call) in enumerate(ACTIONS):
    meters += button(900 + j, 18 + (j % 3) * (aw + 4), y + (j // 3) * 32, aw, 26, text, act(call), fill="255,255,255,36")
y += 72
meters.append(sec("Hint", Meter="String", X=18, Y=y, W=SW - 36, H=60, ClipString=2, FontFace=BASE_FONT, FontSize=9,
                  FontColor="140,146,165", AntiAlias=1,
                  Text="Weather and sunrise need Latitude and Longitude in AdaptiveClock.ini ([Variables]). "
                       "Changing a setting refreshes the clock."))
H = y + 52
head = f"""; Settings.ini  -  settings window for Adaptive Clock   (generated by tools/gen_skins.py)
; Author: Amika Alankara  (MIT License)

[Rainmeter]
Update=1000
AccurateText=1
OnRefreshAction=[!Move 120 120]

[Variables]
Main=AdaptiveClock
BtnCount={n}
{chr(10).join(variables)}

[mSettings]
Measure=Script
ScriptFile=#CURRENTPATH#Settings.lua
UpdateDivider=2

"""
open(os.path.join(SKIN, "Settings", "Settings.ini"), "w", encoding="utf-8").write(
    head + "\n\n".join(panel(SW, H, "Adaptive Clock settings", "Click a button. The active choice is highlighted.") + meters) + "\n")

open(os.path.join(SKIN, "Settings", "Settings.lua"), "w", encoding="utf-8").write(r'''-- Settings.lua  -  highlights the active choices in the Settings window and finds the main skin
-- Author: Amika Alankara  (MIT License)
local count, mainIni, lastKey = 0, '', nil
local MAP = { H24 = '%H', H12 = '%#I' }
local ON, OFF = '77,142,255,235', '255,255,255,28'

function Initialize()
  local cfg = SKIN:GetVariable('CURRENTCONFIG', '')
  SKIN:Bang('!SetVariable', 'Main', cfg:match('^(.*)\\[^\\]+$') or 'AdaptiveClock')
  count = tonumber(SKIN:GetVariable('BtnCount', '0')) or 0
  mainIni = SKIN:GetVariable('CURRENTPATH', '') .. '..\\AdaptiveClock.ini'
end

local function readVars()                          -- only the [Variables] block of the main skin
  local f = io.open(mainIni, 'r')
  if not f then return {} end
  local vars, inVars = {}, false
  for line in f:lines() do
    if line:match('^%[Variables%]') then inVars = true
    elseif inVars and line:match('^%[') then break
    elseif inVars then
      local k, v = line:match('^([%w_]+)=(.*)$')
      if k then vars[k] = (v:gsub('\r', '')) end
    end
  end
  f:close()
  return vars
end

function Update()
  if count == 0 then return 0 end
  local v, parts = readVars(), {}
  for n = 1, count do
    local name = SKIN:GetVariable('B' .. n .. 'V', '')
    local val  = SKIN:GetVariable('B' .. n .. 'X', '')
    parts[n] = (v[name] == (MAP[val] or val)) and '1' or '0'
  end
  local key = table.concat(parts)
  if key ~= lastKey then
    lastKey = key
    for n = 1, count do SKIN:Bang('!SetVariable', 'B' .. n .. 'C', parts[n] == '1' and ON or OFF) end
    SKIN:Bang('!UpdateMeter', '*')
    SKIN:Bang('!Redraw')
  end
  return 0
end
''')

# ======================================================================== Gallery
COL = {None: "255,255,255,34", "en": "255,255,255,34", "code": "88,166,255,80", "easy": "63,185,80,80",
       "girl": "255,105,180,90", "boy": "56,152,255,100"}
GW, cols, bw, bh = 568, 5, 104, 28
gm, gy = [], 92
for i, name in enumerate(NAMES, start=1):
    r, c = divmod(i - 1, cols)
    label = f"{i}  {name}" + ("  (EN)" if TAGS.get(i) == "en" else "")
    gm += button(i, 18 + c * (bw + 6), gy + r * (bh + 6), bw, bh, label, act(f"GoTo({i})"), fill=COL[TAGS.get(i)], fs=9)
gy += ((len(NAMES) + cols - 1) // cols) * (bh + 6) + 8
legend = [("Everyone", None), ("Coder", "code"), ("Everyday", "easy"), ("Girl theme", "girl"), ("Boy theme", "boy")]
for j, (text, tag) in enumerate(legend):
    gm += button(800 + j, 18 + j * (bw + 6), gy, bw, 22, text, "", fill=COL[tag], fs=9)
gy += 34
gm += button(850, 18, gy, 170, 26, "Unlock + resume shuffle", act("Unlock()"), fill="255,255,255,46")
gy += 44
ghead = f"""; Gallery.ini  -  click a style to show it and keep it   (generated by tools/gen_skins.py)
; Author: Amika Alankara  (MIT License)

[Rainmeter]
Update=1000
OnRefreshAction=[!Move 160 160]

[Variables]
Main=AdaptiveClock
BtnCount=0

[mSettings]
Measure=Script
ScriptFile=#CURRENTPATH#..\\Settings\\Settings.lua

"""
open(os.path.join(SKIN, "Gallery", "Gallery.ini"), "w", encoding="utf-8").write(
    ghead + "\n\n".join(panel(GW, gy, "Style gallery",
                              "Click a style to show it and lock it. Styles tagged EN need an English or Windows language.") + gm) + "\n")
print("settings buttons:", n, "| gallery styles:", len(NAMES), "| settings height:", H)
