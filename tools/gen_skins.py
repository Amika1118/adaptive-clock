# Generates the Settings and Gallery skins.  Run from the tools folder:  python gen_skins.py
# Author: Amika Alankara  (MIT License)
import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
SKIN = os.path.join(HERE, "..", "AdaptiveClock")
lua = open(os.path.join(SKIN, "AdaptiveClock.lua"), encoding="utf-8-sig").read()

# style names and tags come straight from AdaptiveClock.lua (single source of truth)
names_block = lua[lua.index("local NAMES = {"):lua.index("-- Styles that only appear")]
NAMES = re.findall(r"'([^']+)'", names_block)
STYLE_COUNT = len(NAMES)
lua_count = re.search(r"local N\s*=\s*(\d+)", lua)
if not lua_count or int(lua_count.group(1)) != STYLE_COUNT:
    raise ValueError(f"AdaptiveClock.lua lists {STYLE_COUNT} names but declares {lua_count.group(1) if lua_count else 'no'} styles")
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

# ======================================================================== Settings
LANGS = ["Windows", "English", "Spanish", "French", "German", "Portuguese", "Italian", "Sinhala", "Tamil", "Hindi", "Japanese"]
PROFILE = ("Profile", "Profile", [("All", "All"), ("Coder", "Coder"), ("Everyday", "Everyday")])
THEME = ("Theme", "Theme", [("Classic", "Neutral"), ("Bloom", "Bloom"), ("Volt", "Volt")])
STYLE_OPTIONS = {"ColorMode", "QuoteHidden", "QuoteMinutes", "QuoteStyle"}
PAGES = [
    ("Start", "start", [PROFILE, THEME]),
    ("Appearance", "appearance", [
        ("Apply to", "CustomizeScope", [("This style", "Style"), ("All styles", "All")]),
        ("Colour mode", "ColorMode", [("Adaptive", "Invert"), ("Windows accent", "Accent"), ("White", "White"), ("Black", "Black"), ("Custom", "Custom")]),
        ("Code colours", "CodeTheme", [("Dark", "Dark"), ("Dracula", "Dracula"), ("Monokai", "Monokai"), ("Light", "Light")]),
        ("Style changes", "ShuffleMinutes", [("60 min", "60"), ("30 min", "30"), ("15 min", "15"), ("5 min", "5"), ("Daily", "1440")]),
        ("On start", "ResumeLast", [("Resume last clock", "1"), ("Follow schedule", "0")]),
    ]),
    ("Language", "plain", [
        ("Language", "Language", [(l, l) for l in LANGS]),
        ("Clock", "HourFormat", [("24 hour", "H24"), ("12 hour", "H12")]),
        ("Week starts", "WeekStart", [("Monday", "1"), ("Sunday", "0")]),
    ]),
    ("Quotes", "quotes", [
        ("Quote", "QuoteHidden", [("Show", "0"), ("Hide", "1")]),
        ("Changes", "QuoteMinutes", [("Daily", "1440"), ("Hourly", "60"), ("30 min", "30"), ("10 min", "10")]),
        ("Design", "QuoteStyle", [("Auto", "Auto"), ("Friendly", "Friendly"), ("Terminal", "Terminal")]),
    ]),
    ("Extras", "timers", [
        ("Smooth seconds", "Smooth", [("Off", "0"), ("On", "1")]),
        ("Weather", "WeatherOff", [("Off", "1"), ("On", "0")]),
        ("Temperature", "TempUnit", [("Celsius", "celsius"), ("Fahrenheit", "fahrenheit")]),
        ("Focus timer", "PomoWork", [("15 min", "15"), ("25 min", "25"), ("50 min", "50")]),
        ("Break", "PomoBreak", [("5 min", "5"), ("10 min", "10"), ("15 min", "15")]),
        ("Timer beep", "TimerBeep", [("On", "1"), ("Off", "0")]),
        ("Alarm", "AlarmOn", [("Off", "0"), ("On", "1")]),
    ]),
    ("Personal", "personal", []),
    ("Actions", "actions", []),
]
PAGE_HINTS = {
    "start": "Choose a profile and theme, then browse or surprise yourself with a clock.",
    "appearance": "Tune colours, fonts, code palettes, and when the clock changes.",
    "plain": "Set your language, time format, and the first day of the week.",
    "quotes": "Choose how quotes appear and add your own local favourites.",
    "timers": "Configure the focus timer, alarm, weather, and sunrise location.",
    "personal": "Personalize greetings and dates; these details stay on this PC.",
    "actions": "Quick actions for styles, shuffle, quotes, and settings.",
}
ACTIONS = [("Next style", "Next()"), ("Random style", "RandomStyle()"), ("Lock / unlock this style", "ToggleLock()"),
           ("Resume shuffle + re-check wallpaper", "Resume()"), ("Next quote", "NextQuote()"),
           ("Skip this style in future", "SkipThisStyle()"), ("Show all styles again", "ShowAllStyles()"),
           ("Reset all settings", "ResetSettings()")]
GALLERY = '[!ActivateConfig "#Main#\\\\Gallery" "Gallery.ini"]'

SW, ROW, TOP = 680, 42, 144
meters, variables, input_sections, n, group_id = [], [], [], 0, 0
page_h = []
next_button_id = 1000

def unique_button_id():
    global next_button_id
    next_button_id += 1
    return next_button_id

def note(name, text, x, y, w, h, size=9, color="140,146,165", hide=None, bold=False):
    o = dict(Meter="String", X=x, Y=y, W=w, H=h, Text=text, ClipString=2, FontFace=FONT, FontSize=size, FontColor=color, AntiAlias=1)
    if bold: o["StringStyle"] = "Bold"
    if hide: o.update(Hidden=f"#{hide}#", DynamicVariables=1)
    return sec(name, **o)

def input_field(key, label, y, hide, default=""):
    var_name = "Input" + key
    label_name = var_name + "Label"
    variables.extend([f"{var_name}={default}", f"{label_name}="])
    meters.append(note(var_name + "Title", label, 18, y, 150, 24, 10, "200,205,220", hide))
    meters.extend(button(1100 + len(input_sections), 174, y - 2, SW - 192, 28, f"#{label_name}#",
                         f'[!CommandMeasure {var_name} "ExecuteBatch 1"]',
                         fill="255,255,255,36", hide=hide, fs=9))
    input_sections.append(sec(var_name, Measure="Plugin", Plugin="InputText", DefaultValue=f"#{var_name}#",
                              Command1=f"""[!SetVariable InputDraft "$UserInput$"][!CommandMeasure mSettings "SaveInput('{key}')"]""",
                              FocusDismiss=1, SolidColor="22,25,33,255", FontColor="245,245,250",
                              FontFace=FONT, FontSize=10, W=SW - 192, H=28, DynamicVariables=1))
    return y + 34

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
        meters.append(sec(f"GroupBg{group_id}", Meter="Shape", X=12, Y=y, W=SW - 24, H=34,
                          Shape=f"Rectangle 0,0,{SW - 24},34,7 | Fill Color 255,255,255,9 | StrokeWidth 1 | Stroke Color 255,255,255,18",
                          Hidden=f"#{hide}#", DynamicVariables=1))
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
                call = f"SetStyleOption('{var}','{val}')" if var in STYLE_OPTIONS else f"Set('{var}','{val}')"
                meters += button(n, 130 + j * (bw + 4), y + 4, bw, 26, text, act(call), color_var=f"B{n}C", hide=hide)
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
    if kind == "quotes":
        y += 4
        meters += button(unique_button_id(), 18, y, 170, 28, "Show next quote", act("NextQuote()"), fill="255,255,255,36", hide=hide)
        y += 38
        meters.append(note("QuoteHint", "Add a quote as: quote text | author. Custom quotes stay on this PC.", 18, y, SW - 36, 28, 9, hide=hide))
        y += 32
        y = input_field("QuoteDraft", "New quote", y, hide)
        meters.append(note("QuoteStatus", "#QuoteStatus#", 18, y, SW - 36, 28, 9, "110,170,255", hide=hide))
        y += 32
    if kind == "appearance":
        y += 4
        meters.append(note("AppearanceHint", "Choose whether appearance changes apply to this clock style or every style. For Custom, enter RGB values such as 120,140,255.", 18, y, SW - 36, 36, 9, hide=hide))
        y += 40
        y = input_field("CustomColor", "Custom RGB colour", y, hide, "120,140,255")
        y = input_field("FontText", "Clock font", y, hide)
        y = input_field("FontMono", "Monospace font", y, hide)
        meters.append(note("InputStatusFonts", "#InputStatusFonts#", 18, y, SW - 36, 28, 9, "110,170,255", hide=hide))
        y += 32
    if kind == "timers":
        y += 4
        meters.append(note("LocStatus", "#LocStatus#", 18, y, SW - 36, 18, 10, "110,170,255", hide, True))
        meters += button(unique_button_id(), 18, y + 22, 200, 28, "Find my location again", act("RefreshLocation()"), fill="255,255,255,36", hide=hide)
        y += 58
        y = input_field("AlarmTime", "Alarm time (HH:MM)", y, hide, "07:00")
        meters.append(note("Privacy", "Privacy: your location is found on this PC (Windows location, or your time zone) and used only for sunrise and sunset. "
                                      "Weather is the one feature that uses the internet: when you turn it on, it sends your position rounded to about 11 km "
                                      "to open-meteo.com. Weather is off by default; you can type a different place in AdaptiveClock.ini "
                                      "(WeatherLatitude / WeatherLongitude) if you prefer.", 18, y, SW - 36, 84, 9, hide=hide))
        y += 84
    if kind == "personal":
        y += 4
        meters.append(note("PersonalHint", "These details stay on this PC. Birthday uses month and day only. City personalizes the greeting; it does not enable weather.", 18, y, SW - 36, 44, 9, hide=hide))
        y += 48
        y = input_field("GreetingName", "Name for greeting", y, hide)
        y = input_field("Birthday", "Birthday (MM-DD)", y, hide)
        y = input_field("City", "City", y, hide)
        y = input_field("Latitude", "Latitude (optional)", y, hide)
        y = input_field("Longitude", "Longitude (optional)", y, hide)
        meters.append(note("InputStatusPersonal", "#InputStatusPersonal#", 18, y, SW - 36, 28, 9, "110,170,255", hide=hide))
        y += 32
    if kind == "appearance":
        meters += button(unique_button_id(), 18, y, SW - 36, 30, "Open Adaptive Clock User Guide",
                         '[!OpenURL "https://adaptive-clock-help-page.vercel.app/"]',
                         fill="77,142,255,160", hide=hide)
        y += 36
    if kind == "actions":
        aw = (SW - 36 - 8) / 2
        for j, (text, call) in enumerate(ACTIONS):
            meters += button(900 + j, 18 + (j % 2) * (aw + 8), y + (j // 2) * 38, aw, 30, text, act(call), fill="255,255,255,36", hide=hide)
        y += ((len(ACTIONS) + 1) // 2) * 38 + 4
        meters += button(unique_button_id(), 18, y, aw, 30, "Open style gallery", GALLERY, fill="77,142,255,160", hide=hide)
        y += 44
        meters.append(note("ActHint", "Settings are stored locally. The city is used in the greeting; Windows location (or configured coordinates) drives sunrise and sunset. "
                                      "Weather remains off until enabled.", 18, y, SW - 36, 60, 9, hide=hide))
        y += 60
    page_h.append(y)

H = max(page_h) + 24
TAB_Y, TAB_H = 100, 30
tw = (SW - 36 - 4 * (len(PAGES) - 1)) / len(PAGES)
header = [
    sec("Crumb", Meter="String", X=18, Y=39, Text="SETTINGS  /  #CrumbPage#", FontFace=FONT, FontSize=11, StringStyle="Bold",
        FontColor="110,170,255", AntiAlias=1, DynamicVariables=1),
    sec("Now", Meter="String", X=18, Y=59, W=SW - 36, H=16, Text="#NowShowing#", FontFace=FONT, FontSize=9,
        FontColor="195,200,215", ClipString=1, AntiAlias=1, DynamicVariables=1),
    sec("PageHint", Meter="String", X=18, Y=78, W=SW - 36, H=14, Text="#PageHint#", FontFace=FONT, FontSize=9,
        FontColor="145,153,172", ClipString=1, AntiAlias=1, DynamicVariables=1),
]
for p, (pname, _, _) in enumerate(PAGES, start=1):
    header += button(800 + p, 18 + (p - 1) * (tw + 4), TAB_Y, tw, TAB_H, pname, f'[!CommandMeasure mSettings "Page({p})"]',
                     color_var=f"Tab{p}", fs=11)
    variables.append(f"Tab{p}={TAB_OFF}")
    variables.append(f"Pg{p}={0 if p == 1 else 1}")
    variables.append(f"PageName{p}={pname}")
    variables.append(f"PageHint{p}={PAGE_HINTS[PAGES[p - 1][1]]}")
variables.append("CrumbPage=Start")
variables.append(f"PageHint={PAGE_HINTS['start']}")
variables.append("NowShowing=")
variables.append("LocStatus=")
variables += ["InputStatusPersonal=", "InputStatusFonts=", "QuoteStatus="]
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
    shead + "\n\n".join(panel(SW, H, "Adaptive Clock settings") + header + meters + input_sections) + "\n")

open(os.path.join(SKIN, "Settings", "Settings.lua"), "w", encoding="utf-8").write(r"""-- Settings.lua  -  logic of the Settings window and the style gallery
-- Author: Amika Alankara  (MIT License)
--  * shows which page you are on (breadcrumb + highlighted tab)
--  * highlights the active choice of every setting and prints its current value next to the label
--  * shows which clock style is on screen and where the location comes from (the clock writes ..\state.txt)
local count, pages, paths = 0, 0, {}
local lastKey, lastNow, lastLoc, galleryKey
local gallery = false
local readVars, updateGallery
local statusText, inputCache = '', {}
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
  paths = { clock = here .. '..\\AdaptiveClock.ini', state = here .. '..\\state.txt', quotes = here .. '..\\quotes.txt' }
  gallery = pages == 0
  if pages > 0 then
    local clockVars = readVars(paths.clock, true)
    for _, name in ipairs({ 'GreetingName', 'Birthday', 'City', 'Latitude', 'Longitude', 'AlarmTime', 'FontText', 'FontMono', 'CustomColor' }) do
      setv('Input' .. name, clockVars[name] or '')
    end
    Page(1)
  end
end

function Page(p)                                   -- show one page of the Settings window
  p = tonumber(p) or 1
  if p < 1 or p > pages then return end
  for k = 1, pages do
    setv('Pg' .. k, k == p and 0 or 1)
    setv('Tab' .. k, k == p and ON or TAB_OFF)
  end
  setv('CrumbPage', SKIN:GetVariable('PageName' .. p, ''))
  setv('PageHint', SKIN:GetVariable('PageHint' .. p, ''))
  SKIN:Bang('!UpdateMeter', '*')
  SKIN:Bang('!Redraw')
end

readVars = function(path, onlyVariables)
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

local function status(text)
  statusText = text
  setv('InputStatusPersonal', text)
  setv('InputStatusFonts', text)
  setv('QuoteStatus', text)
end

local function trim(s) return (s:gsub('^%s+', ''):gsub('%s+$', '')) end

local function syncStoredInput(name, value)
  local key = 'Input' .. name
  setv(key, value or '')
end

local function setStyleValue(name, value)
  local styleOptions = { ColorMode = true, CustomColor = true, FontText = true, FontMono = true,
                         QuoteHidden = true, QuoteMinutes = true, QuoteStyle = true }
  if not styleOptions[name] then return false end
  local vars = readVars(paths.clock, true)
  local style = tonumber(readVars(paths.state, false).StyleNo)
  if not style then return false end
  if vars.CustomizeScope == 'All' then
    SKIN:Bang('!WriteKeyValue', 'Variables', name, value, paths.clock)
    for n = 1, tonumber(vars.StyleCount or '130') do
      SKIN:Bang('!WriteKeyValue', 'Variables', 'Style' .. n .. name, '', paths.clock)
    end
  else
    SKIN:Bang('!WriteKeyValue', 'Variables', 'Style' .. style .. name, value, paths.clock)
  end
  return true
end

function SaveInput(name)
  local value = trim((SKIN:GetVariable('InputDraft', '') or ''):gsub('[\r\n]', ' '))
  if name == 'GallerySearch' then
    setv('GallerySearch', value:sub(1, 60))
    setv('GalleryPage', 1)
    galleryKey = nil
    return
  end
  if name == 'QuoteDraft' then
    local text, author = value:match('^(.-)%s*|%s*(.-)$')
    if not text then text, author = value, '' end
    text, author = trim(text), trim(author)
    if text == '' or #text > 500 or #author > 100 then status('Enter a quote (up to 500 characters), optionally followed by | author.'); return end
    local f, err = io.open(paths.quotes, 'a')
    if not f then status('Could not save quote: ' .. tostring(err)); SKIN:Bang('!Log', 'Adaptive Clock: ' .. tostring(err), 'Error'); return end
    f:write(text:gsub('|', '/'), author ~= '' and (' | ' .. author:gsub('|', '/')) or '', '\n')
    f:close()
    status('Quote added.')
    SKIN:Bang('!Refresh', '#Main#')
    return
  end

  local allowEmpty = { GreetingName = true, Birthday = true, City = true, Latitude = true, Longitude = true }
  local limits = { GreetingName = 60, City = 60, FontText = 48, FontMono = 48 }
  if value == '' and allowEmpty[name] then
    -- cleared value is allowed: delete the saved entry on this PC
  elseif limits[name] then
    if #value > limits[name] or value:find('[%[%]=]') then status('Value is too long or contains unsupported INI characters.'); return end
  elseif name == 'Birthday' then
    local month, day = value:match('^(%d%d?)%-(%d%d?)$')
    if value ~= '' and (not month or tonumber(month) < 1 or tonumber(month) > 12 or tonumber(day) < 1 or tonumber(day) > ({31,29,31,30,31,30,31,31,30,31,30,31})[tonumber(month)]) then
      status('Use MM-DD, or leave birthday blank.'); return
    end
    if month then value = string.format('%02d-%02d', tonumber(month), tonumber(day)) end
  elseif name == 'CustomColor' then
    local r, g, b = value:match('^(%d+),(%d+),(%d+)$')
    if not r or tonumber(r) > 255 or tonumber(g) > 255 or tonumber(b) > 255 then status('Use RGB values from 0 to 255, for example 120,140,255.'); return end
    value = table.concat({ tonumber(r), tonumber(g), tonumber(b) }, ',')
  elseif name == 'Latitude' or name == 'Longitude' then
    local number = tonumber(value)
    if value ~= '' and (not number or (name == 'Latitude' and math.abs(number) > 90) or (name == 'Longitude' and math.abs(number) > 180)) then
      status(name .. ' must be a valid coordinate, or blank.'); return
    end
    if value ~= '' then value = string.format('%.6f', number) end
  elseif name == 'AlarmTime' then
    local hour, minute = value:match('^(%d%d):(%d%d)$')
    if not hour or tonumber(hour) > 23 or tonumber(minute) > 59 then status('Use a 24-hour time such as 07:30.'); return end
  else
    status('This setting cannot be edited here.')
    return
  end

  if name == 'CustomColor' or name == 'FontText' or name == 'FontMono' then
    if not setStyleValue(name, value) then status('Load a clock before saving this style option.'); return end
  else
    SKIN:Bang('!WriteKeyValue', 'Variables', name, value, paths.clock)
  end
  if name == 'GreetingName' or name == 'Birthday' or name == 'City' or name == 'Latitude' or name == 'Longitude' then
    syncStoredInput(name, value)
  end
  status('Saved on this PC.')
  SKIN:Bang('!Refresh', '#Main#')
end

function FilterGallery(tag)
  setv('GalleryTag', tag)
  setv('GalleryPage', 1)
  galleryKey = nil
  if gallery then updateGallery(readVars(paths.state, false)) end
end

function SortGallery(sort)
  setv('GallerySort', sort)
  setv('GalleryPage', 1)
  galleryKey = nil
  if gallery then updateGallery(readVars(paths.state, false)) end
end

function ClearGallerySearch()
  setv('GallerySearch', '')
  setv('GalleryPage', 1)
  galleryKey = nil
  if gallery then updateGallery(readVars(paths.state, false)) end
end

updateGallery = function(st)
  local query = (SKIN:GetVariable('GallerySearch', '') or ''):lower()
  local filter = SKIN:GetVariable('GalleryTag', 'all')
  local sort = SKIN:GetVariable('GallerySort', 'recent')
  local recent = st.RecentStyles or ''
  local selected = tonumber(st.StyleNo)
  local page = tonumber(SKIN:GetVariable('GalleryPage', '1')) or 1
  local key = query .. '|' .. filter .. '|' .. sort .. '|' .. recent .. '|' .. (st.StyleNo or '') .. '|' .. page
  if key == galleryKey then return end
  galleryKey = key

  local order, seen = {}, {}
  if sort == 'recent' then
    for value in recent:gmatch('%d+') do
      local n = tonumber(value)
      if n and n >= 1 and n <= count and not seen[n] then order[#order + 1] = n; seen[n] = true end
    end
  end
  local rest = {}
  for n = 1, count do if not seen[n] then rest[#rest + 1] = n end end
  if sort == 'name' then
    table.sort(rest, function(a, b)
      return SKIN:GetVariable('B' .. a .. 'L', ''):lower() < SKIN:GetVariable('B' .. b .. 'L', ''):lower()
    end)
  end
  for _, n in ipairs(rest) do order[#order + 1] = n end

  local matching = {}
  for _, n in ipairs(order) do
    local name = SKIN:GetVariable('B' .. n .. 'L', ''):lower()
    local tag = SKIN:GetVariable('B' .. n .. 'T', '')
    if (filter == 'all' or tag == filter)
      and (query == '' or (name .. ' ' .. tostring(n)):find(query, 1, true) ~= nil)
    then
      matching[#matching + 1] = n
    end
  end
  local perPage = tonumber(SKIN:GetVariable('GalleryPerPage', '25')) or 25
  local pages = math.max(1, math.ceil(#matching / perPage))
  page = math.max(1, math.min(page, pages))
  setv('GalleryPage', page)
  setv('GalleryPageCount', pages)
  local cols = tonumber(SKIN:GetVariable('GalleryCols', '5')) or 5
  local width = tonumber(SKIN:GetVariable('GalleryButtonWidth', '128')) or 128
  local height = tonumber(SKIN:GetVariable('GalleryButtonHeight', '34')) or 34
  local gap = tonumber(SKIN:GetVariable('GalleryGap', '6')) or 6
  local top = tonumber(SKIN:GetVariable('GalleryTop', '222')) or 222
  local first = (page - 1) * perPage + 1
  local last = math.min(#matching, first + perPage - 1)
  for n = 1, count do setv('GH' .. n, 1) end
  for index = first, last do
    local n = matching[index]
    local slot = index - first
    local row, col = math.floor(slot / cols), slot % cols
    local x, y = 18 + col * (width + gap), top + row * (height + gap)
    setv('GH' .. n, 0)
    setv('B' .. n .. 'C', selected == n and '0,180,160,230' or SKIN:GetVariable('B' .. n .. 'O', '255,255,255,28'))
    SKIN:Bang('!SetOption', 'Btn' .. n, 'X', x)
    SKIN:Bang('!SetOption', 'Btn' .. n, 'Y', y)
    SKIN:Bang('!SetOption', 'Btn' .. n, 'W', width)
    SKIN:Bang('!SetOption', 'Btn' .. n, 'H', height)
    SKIN:Bang('!SetOption', 'Btn' .. n .. 'T', 'X', x + width / 2)
    SKIN:Bang('!SetOption', 'Btn' .. n .. 'T', 'Y', y + height / 2)
    SKIN:Bang('!SetOption', 'Btn' .. n .. 'T', 'W', width - 8)
  end
  setv('GalleryResults', #matching == 0 and 'No styles found. Try a different search or category.'
    or ('Showing ' .. first .. '-' .. last .. ' of ' .. #matching .. ' matching styles'))
  setv('GalleryPageLabel', 'PAGE ' .. page .. ' / ' .. pages)
  setv('GalleryPrevC', page > 1 and ON or '255,255,255,14')
  setv('GalleryNextC', page < pages and ON or '255,255,255,14')
  for _, tag in ipairs({ 'all', 'code', 'easy', 'girl', 'boy', 'en' }) do
    setv('Filter' .. tag .. 'C', filter == tag and ON or '255,255,255,28')
  end
  setv('SortRecentC', sort == 'recent' and ON or '255,255,255,28')
  setv('SortNameC', sort == 'name' and ON or '255,255,255,28')
  SKIN:Bang('!UpdateMeter', '*')
  SKIN:Bang('!Redraw')
end

function GalleryPage(delta)
  local page = tonumber(SKIN:GetVariable('GalleryPage', '1')) or 1
  local pages = tonumber(SKIN:GetVariable('GalleryPageCount', '1')) or 1
  page = math.max(1, math.min(page + (tonumber(delta) or 0), pages))
  setv('GalleryPage', page)
  galleryKey = nil
  if gallery then updateGallery(readVars(paths.state, false)) end
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
  for _, name in ipairs({ 'GreetingName', 'Birthday', 'City', 'Latitude', 'Longitude', 'FontText', 'FontMono', 'CustomColor', 'AlarmTime' }) do
    local value = files.clock[name] or ''
    local style = tonumber(st.StyleNo)
    if style and ({ FontText = true, FontMono = true, CustomColor = true })[name] then
      value = files.clock['Style' .. style .. name] or value
    end
    local fieldValue, displayValue = value, value ~= '' and value or '(click to enter)'
    if inputCache[name] ~= fieldValue then setv('Input' .. name, fieldValue); inputCache[name] = fieldValue end
    if inputCache[name .. 'Label'] ~= displayValue then setv('Input' .. name .. 'Label', displayValue); inputCache[name .. 'Label'] = displayValue end
  end
  if inputCache.QuoteLabel ~= true then setv('InputQuoteDraftLabel', '(click to add quote text | author)'); inputCache.QuoteLabel = true end
  local searchLabel = SKIN:GetVariable('GallerySearch', '') ~= '' and SKIN:GetVariable('GallerySearch', '') or 'Search styles...'
  if inputCache.GallerySearchLabel ~= searchLabel then setv('GallerySearchLabel', searchLabel); inputCache.GallerySearchLabel = searchLabel end
  if statusText ~= '' then status(statusText) end
  if gallery then updateGallery(st) end
  if count == 0 then return 0 end

  local parts, values = {}, {}
  for n = 1, count do
    local file = files[SKIN:GetVariable('B' .. n .. 'F', 'clock')] or files.clock
    local name = SKIN:GetVariable('B' .. n .. 'V', '')
    local val  = SKIN:GetVariable('B' .. n .. 'X', '')
    local cur = file[name]
    local style = tonumber(st.StyleNo)
    if style and name ~= '' then cur = files.clock['Style' .. style .. name] or cur end
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
PAGE_SIZE = 25
GW, cols, bw, bh = 720, 5, 128, 34
gm, variables, gy = [], [], 222
gallery_top = gy
for i, name in enumerate(NAMES, start=1):
    r, c = divmod(i - 1, cols)
    label = f"{i}  {name}" + ("  (EN)" if TAGS.get(i) == "en" else "")
    tag = TAGS.get(i) or "all"
    variables += [f"B{i}V=StyleNo", f"B{i}X={i}", f"B{i}F=state", f"B{i}G=0", f"B{i}L={name}", f"B{i}T={tag}",
                  f"B{i}O={COL[TAGS.get(i)]}", f"B{i}C={COL[TAGS.get(i)]}", f"GH{i}=0"]
    gm += button(i, 18 + c * (bw + 6), gy + r * (bh + 6), bw, bh, label, act(f"GoTo({i})"), color_var=f"B{i}C", fs=9, hide=f"GH{i}")
filter_options = [("All", "all"), ("Coder", "code"), ("Everyday", "easy"), ("Bloom", "girl"), ("Volt", "boy"), ("English", "en")]
filter_w = (GW - 36 - 5 * 4) / 6
for j, (text, tag) in enumerate(filter_options):
    variables.append(f"Filter{tag}C={ON if tag == 'all' else OFF}")
    gm += button(800 + j, 18 + j * (filter_w + 4), 130, filter_w, 26, text,
                 f'[!CommandMeasure mSettings "FilterGallery(\'{tag}\')"]',
                 color_var=f"Filter{tag}C", fs=9)
variables += ["SortRecentC=" + ON, "SortNameC=" + OFF, "GallerySearch=", "GalleryTag=all", "GallerySort=recent",
              f"GalleryCols={cols}", f"GalleryButtonWidth={bw}", f"GalleryButtonHeight={bh}", "GalleryGap=6",
              f"GalleryTop={gallery_top}", f"GalleryPerPage={PAGE_SIZE}", "GalleryPage=1", "GalleryPageCount=1",
              "GalleryPageLabel=PAGE 1 / 1", "GalleryPrevC=255,255,255,28", "GalleryNextC=255,255,255,28", "GalleryResults="]
gm += button(820, 18, 164, 112, 26, "Recently used",
             '[!CommandMeasure mSettings "SortGallery(\'recent\')"]', color_var="SortRecentC", fs=9)
gm += button(821, 136, 164, 132, 26, "A - Z",
             '[!CommandMeasure mSettings "SortGallery(\'name\')"]', color_var="SortNameC", fs=9)
search_section = sec("GallerySearchInput", Measure="Plugin", Plugin="InputText", DefaultValue="#GallerySearch#",
                     Command1="""[!SetVariable InputDraft "$UserInput$"][!CommandMeasure mSettings "SaveInput('GallerySearch')"]""",
                     FocusDismiss=1, SolidColor="22,25,33,255", FontColor="245,245,250",
                     FontFace=FONT, FontSize=10, W=GW - 364, H=26, DynamicVariables=1)
variables.append("GallerySearchLabel=Search styles...")
gm += button(822, 276, 164, GW - 364, 26, "#GallerySearchLabel#",
             '[!CommandMeasure GallerySearchInput "ExecuteBatch 1"]', fill="255,255,255,36", fs=9)
gm += button(823, GW - 82, 164, 64, 26, "Clear",
             '[!CommandMeasure mSettings "ClearGallerySearch()"]', fill="255,255,255,36", fs=9)
nav_y = gallery_top + (PAGE_SIZE // cols) * (bh + 6) + 8
gm += button(830, 18, nav_y, 120, 28, "Previous",
             '[!CommandMeasure mSettings "GalleryPage(-1)"]', color_var="GalleryPrevC", fs=9)
gm.append(sec("GalleryPageText", Meter="String", X=146, Y=nav_y, W=GW - 292, H=28,
              Text="#GalleryPageLabel#", StringAlign="CenterCenter", FontFace=FONT, FontSize=10,
              StringStyle="Bold", FontColor="210,215,230", AntiAlias=1, DynamicVariables=1))
gm += button(831, GW - 138, nav_y, 120, 28, "Next",
             '[!CommandMeasure mSettings "GalleryPage(1)"]', color_var="GalleryNextC", fs=9)
footer_y = nav_y + 40
footer_w = (GW - 44) / 2
gm += button(850, 18, footer_y, footer_w, 30, "Unlock + resume shuffle", act("Unlock()"), fill="255,255,255,46", fs=10)
gm += button(851, 26 + footer_w, footer_y, footer_w, 30, "Open settings",
             '[!ActivateConfig "#Main#\\\\Settings" "Settings.ini"]', fill="77,142,255,150", fs=10)
gy = footer_y + 46
gheader = [sec("Now", Meter="String", X=18, Y=42, W=GW - 36, H=16, Text="#NowShowing#", FontFace=FONT, FontSize=10,
               StringStyle="Bold", FontColor="110,170,255", ClipString=1, AntiAlias=1, DynamicVariables=1),
           sec("Hint", Meter="String", X=18, Y=64, W=GW - 36, H=30, ClipString=2, FontFace=FONT, FontSize=9,
               FontColor="140,146,165", AntiAlias=1,
               Text="Click a style to show and lock it. The selected style is highlighted. "
                    "Styles marked EN need the Windows or English language."),
           sec("Results", Meter="String", X=18, Y=194, W=GW - 36, H=18, Text="#GalleryResults#", FontFace=FONT,
               FontSize=9, FontColor="170,175,190", AntiAlias=1, DynamicVariables=1)]
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
    ghead + "\n\n".join(panel(GW, gy, "Style gallery") + gheader + gm + [search_section]) + "\n")
print("settings buttons:", n, "| gallery styles:", len(NAMES), "| settings height:", H)
