-- AdaptiveClock.lua  v4.7   (Rainmeter 4.x, Lua 5.1)
-- Author: Amika Alankara  (MIT License)
-- This file is plain ASCII and has NO byte-order mark, so it loads everywhere.
-- Measures that return symbols or non-English text use AdaptiveClockU.lua instead (a tiny loader saved WITH a BOM; it runs this file),
-- because Rainmeter only treats Lua strings as Unicode when the script file it loads starts with a BOM.
--
-- One file, many small jobs. Each Script measure in the .ini picks its job with  Mode=
--   main            colours (ink / theme palette), style shuffle, calendar variables, quote flags (value = full quote)
--   secF minF hrF dayF yearF          numbers 0..1 that drive rings, arcs, bars and hands
--   dHT dHU dMT dMU dST dSU           single digits (binary clock)
--   hexH hexM hexS binH binM binS     hex / binary text
--   secN ciStatus hexRow rain         integer second, CI stage text, hexdump row, matrix-rain column
--   epoch sha logHash logTime         unix time, short commit-like hashes
--   greet greetIcon yearPct daysLeft  friendly text
--   ampm cursor qmark                 small helpers
--   quoteBody quoteWho                the quote, split in two lines
--   worldName worldDay worldTime      multi-line text for the "World time" style
--   wordsA wordsB                     text for the "Words" style
--   moonIcon moonName moonPct moonF   moon phase
--   dow dowS mon monS lbl             date names and labels in the chosen Language
--   sunRise sunSet sunF sunNote       sunrise / sunset (needs Latitude + Longitude)
--   wxIcon wxTemp wxText batText     weather and battery text

local mode = 'main'
local N = 106                       -- number of styles (the .ini sets StyleCount)
local current, lastSlot, lastYday, lastKey, lastLuma, wasBright, lastCalDay, lastQKey
local pool = {}                    -- style numbers that take part in the shuffle
local interval = 60               -- minutes per style (ShuffleMinutes)
local locked, lockedStyle = false, 0
local wxLat, lastLocSrc
local lblKey = ''
local logIndex = 0
local qpool

local NAMES = {
  'Chronograph', 'Grey bubbles', 'World time', 'Halo', 'Roman dial', 'Bubble rings', 'Words', 'Digital',
  'Concentric rings', 'Orbit dots', 'Classic analog', 'Progress bars', 'Sun path', 'Stacked digits', 'Date card',
  'Line tracks', 'Dash ring', 'Gauges', 'Neon', '24-hour dial', 'Split', 'Analog + digital', 'Phrase', 'Pulse',
  'Terminal', 'Live preview', 'Hex clock', 'Binary dots', 'System monitor', 'Epoch and ISO', 'Git log',
  'Greeting', 'Month calendar', 'Year progress', 'Sticky note', 'Week strip',
  'Blossom', 'Heartbeat', 'Pastel Bars', 'Stardust',
  'Radar Sweep', 'Orbit', 'Redline', 'Match Day',
  'Flip clock', 'Minimal analog', 'Tiles', 'Aurora',
  'Weather', 'Sun times', 'Battery', 'Timer and alarm',
  'Python', 'JavaScript', 'TypeScript', 'Java', 'C', 'C++', 'C#', 'Go', 'Rust', 'PHP', 'Ruby', 'Swift', 'Kotlin',
  'SQL', 'HTML', 'Bash', 'PowerShell', 'Lua', 'Dart',
  'Flutter', 'Cloud Nine', 'Daisy Chain', 'Ribbon', 'Spectrum', 'Lunar Glow',
  'Launch', 'Kickoff', 'Neon Drive', 'Level Up', 'Grid Start', 'Crest',
  'Nixie', 'Vinyl', 'Compass', 'Waves', 'Zen circle', 'Day bar', 'Moon phase', 'Skyline',
  'Dot matrix', 'Matrix rain', 'CI pipeline', 'Stack trace', 'Hexdump', 'Neofetch', 'htop', 'Test runner',
  'Big quote', 'Weekend', 'Year grid', 'Sun and moon', 'Sparkle Pop', 'Pulse Line', 'Birthday',
}

-- Styles that only appear for a profile / theme (all others always appear)
local TAGS = {}
for i = 25, 31 do TAGS[i] = 'code' end      -- Profile: All or Coder
for i = 53, 71 do TAGS[i] = 'code' end      -- one editor window per programming language
for i = 92, 99 do TAGS[i] = 'code' end
for i = 32, 36 do TAGS[i] = 'easy' end      -- Profile: All or Everyday
for i = 37, 40 do TAGS[i] = 'girl' end      -- Theme: Bloom
for i = 72, 77 do TAGS[i] = 'girl' end
for i = 41, 44 do TAGS[i] = 'boy' end       -- Theme: Volt
for i = 78, 83 do TAGS[i] = 'boy' end
for i = 100, 102 do TAGS[i] = 'easy' end
for i = 106, 106 do TAGS[i] = 'easy' end
for i = 104, 104 do TAGS[i] = 'girl' end
for i = 105, 105 do TAGS[i] = 'boy' end
TAGS[7], TAGS[23] = 'en', 'en'              -- word clocks: English only

local D  = '\226\128\148'          -- em dash   (UTF-8 written as escapes so the file encoding never matters)
local LQ = '\226\128\156'          -- left curly quote
local RQ = '\226\128\157'          -- right curly quote
local SUN, MOON = '\226\152\128', '\226\152\190'

-- kind: 'b' = both profiles, 'c' = coder, 'e' = everyday
local function Q(kind, text, who) return { text, who, kind } end

local QUOTES = {
  Q('b', 'The best way out is always through.', 'Robert Frost'),
  Q('b', 'We suffer more often in imagination than in reality.', 'Seneca'),
  Q('b', 'A journey of a thousand miles begins with a single step.', 'Lao Tzu'),
  Q('b', 'The unexamined life is not worth living.', 'Socrates'),
  Q('b', 'Fortune favors the bold.', 'Virgil'),
  Q('b', 'The only thing we have to fear is fear itself.', 'Franklin D. Roosevelt'),
  Q('b', 'I think, therefore I am.', 'Rene Descartes'),
  Q('b', 'Stay hungry, stay foolish.', 'Steve Jobs'),
  Q('b', 'Genius is one percent inspiration and ninety-nine percent perspiration.', 'Thomas Edison'),
  Q('b', 'Imagination is more important than knowledge.', 'Albert Einstein'),
  Q('b', 'Do what you can, with what you have, where you are.', 'Theodore Roosevelt'),
  Q('b', 'The only way to do great work is to love what you do.', 'Steve Jobs'),
  Q('b', 'It does not matter how slowly you go as long as you do not stop.', 'Confucius'),
  Q('b', 'Waste no more time arguing what a good man should be. Be one.', 'Marcus Aurelius'),
  Q('b', 'Fall seven times, stand up eight.', 'Japanese proverb'),
  Q('b', 'Energy and persistence conquer all things.', 'Benjamin Franklin'),
  Q('b', 'Lost time is never found again.', 'Benjamin Franklin'),
  Q('b', 'Time is what we want most, but what we use worst.', 'William Penn'),
  Q('b', 'Well done is better than well said.', 'Benjamin Franklin'),
  Q('b', 'We are what we repeatedly do. Excellence, then, is not an act, but a habit.', 'Will Durant'),
  Q('b', 'Make each day your masterpiece.', 'John Wooden'),
  Q('b', 'Failure is simply the opportunity to begin again, this time more intelligently.', 'Henry Ford'),
  Q('b', 'Any sufficiently advanced technology is indistinguishable from magic.', 'Arthur C. Clarke'),
  Q('b', 'We can only see a short distance ahead, but we can see plenty there that needs to be done.', 'Alan Turing'),
  Q('b', 'Strive not to be a success, but rather to be of value.', 'Albert Einstein'),
  Q('b', 'Life is like riding a bicycle. To keep your balance, you must keep moving.', 'Albert Einstein'),
  Q('b', 'Nothing in life is to be feared, it is only to be understood.', 'Marie Curie'),
  Q('b', 'Slow and steady wins the race.', 'Aesop'),
  Q('b', 'A year from now you may wish you had started today.', 'Karen Lamb'),
  Q('b', 'Light tomorrow with today.', 'Elizabeth Barrett Browning'),
  Q('b', 'Hope is being able to see that there is light despite all of the darkness.', 'Desmond Tutu'),
  Q('b', 'Small deeds done are better than great deeds planned.', 'Peter Marshall'),
  Q('b', "Don't count the days, make the days count.", 'Muhammad Ali'),
  Q('b', 'The best time to plant a tree was twenty years ago. The second best time is now.', 'Proverb'),
  Q('b', 'A smooth sea never made a skilled sailor.', 'Proverb'),
  Q('b', 'Courage is grace under pressure.', 'Ernest Hemingway'),
  Q('b', 'Dwell on the beauty of life.', 'Marcus Aurelius'),
  Q('b', 'An investment in knowledge pays the best interest.', 'Benjamin Franklin'),
  Q('b', 'Well begun is half done.', 'Proverb'),
  Q('b', 'Know thyself.', 'Delphic maxim'),
  Q('b', 'Not all those who wander are lost.', 'J.R.R. Tolkien'),
  Q('b', 'Learn from yesterday, live for today, hope for tomorrow.', 'Albert Einstein'),
  -- everyday
  Q('e', 'Be kind whenever possible. It is always possible.', 'Dalai Lama'),
  Q('e', 'Every day may not be good, but there is something good in every day.', 'Alice Morse Earle'),
  Q('e', 'Happiness is not by chance, but by choice.', 'Jim Rohn'),
  Q('e', 'Do something today that your future self will thank you for.', 'Sean Patrick Flanery'),
  Q('e', 'The secret of getting ahead is getting started.', 'Attributed to Mark Twain'),
  Q('e', 'What we think, we become.', 'Attributed to Buddha'),
  Q('e', 'Today is a good day to have a good day.', 'Anonymous'),
  Q('e', 'Small steps every day add up to big things.', 'Anonymous'),
  Q('e', 'Kindness is a language everyone understands.', 'Anonymous'),
  Q('e', 'Dream big. Start small. Begin today.', 'Anonymous'),
  Q('e', 'Breathe. You have got this.', 'Anonymous'),
  Q('e', 'Be the reason someone smiles today.', 'Anonymous'),
  Q('e', 'Progress, not perfection.', 'Anonymous'),
  Q('e', 'Rest is part of the work.', 'Anonymous'),
  -- coder
  Q('c', 'Premature optimization is the root of all evil.', 'Donald Knuth'),
  Q('c', 'Talk is cheap. Show me the code.', 'Linus Torvalds'),
  Q('c', 'Programs must be written for people to read, and only incidentally for machines to execute.', 'Harold Abelson'),
  Q('c', 'Simplicity is prerequisite for reliability.', 'Edsger Dijkstra'),
  Q('c', 'The best way to predict the future is to invent it.', 'Alan Kay'),
  Q('c', 'All models are wrong, but some are useful.', 'George Box'),
  Q('c', 'Make it work, make it right, make it fast.', 'Kent Beck'),
  Q('c', 'Machines take me by surprise with great frequency.', 'Alan Turing'),
  Q('c', 'Any fool can write code that a computer can understand. Good programmers write code that humans can understand.', 'Martin Fowler'),
  Q('c', 'Debugging is twice as hard as writing the code in the first place.', 'Brian Kernighan'),
  Q('c', 'The function of good software is to make the complex appear to be simple.', 'Grady Booch'),
  Q('c', 'There are only two hard things in computer science: cache invalidation and naming things.', 'Attributed to Phil Karlton'),
  Q('c', 'Deleted code is debugged code.', 'Jeff Sickel'),
  Q('c', 'Good code is its own best documentation.', 'Steve McConnell'),
  Q('c', 'First, solve the problem. Then, write the code.', 'John Johnson'),
  Q('c', 'Before software can be reusable it first has to be usable.', 'Ralph Johnson'),
  Q('c', 'Code never lies, comments sometimes do.', 'Ron Jeffries'),
  Q('c', 'Simplicity is the soul of efficiency.', 'Austin Freeman'),
}

-- ---------------------------------------------------------------- helpers

local function setv(name, value)
  SKIN:Bang('!SetVariable', name, tostring(value))
end

local function setnum(name, value)
  SKIN:Bang('!SetVariable', name, string.format('%.5f', value))
end

local function refresh()
  SKIN:Bang('!UpdateMeter', '*')
  SKIN:Bang('!Redraw')
end

local function var(name, default) return SKIN:GetVariable(name, default) end

local function safe(f, ...)                         -- an error in an optional part must not stop the clock
  local ok, err = pcall(f, ...)
  if not ok then SKIN:Bang('!Log', 'AdaptiveClock: ' .. tostring(err), 'Error') end
end
local function profile() return var('Profile', 'All') end
local function is12h() return var('HourFormat', '%H') ~= '%H' end

local function theme()                          -- Neutral | Bloom | Volt   (the old names Girl / Boy still work)
  local t = var('Theme', 'Neutral')
  if t == 'Girl' then return 'Bloom' end
  if t == 'Boy' then return 'Volt' end
  return t
end

-- ---------------------------------------------------------------- colours

local PAL = {
  Bloom = { c = '255,105,180', c2 = '187,134,252' },
  Volt  = { c = '56,152,255',  c2 = '0,224,208' },
}

local CODE = {                                  -- role colours of the editor / terminal windows
  Dark    = { bg = '30,30,30,240',   bar = '37,37,38',   num = '110,110,110', comment = '106,153,85',  keyword = '86,156,214',
              string = '206,145,120', func = '220,220,170', type = '78,201,176',   number = '181,206,168', text = '204,204,204', status = '0,122,204' },
  Dracula = { bg = '40,42,54,240',   bar = '33,34,44',   num = '98,114,164',  comment = '98,114,164',  keyword = '255,121,198',
              string = '241,250,140', func = '80,250,123',  type = '139,233,253', number = '189,147,249', text = '248,248,242', status = '189,147,249' },
  Monokai = { bg = '39,40,34,240',   bar = '30,31,26',   num = '144,144,138', comment = '117,113,94',  keyword = '249,38,114',
              string = '230,219,116', func = '166,226,46',  type = '102,217,239', number = '174,129,255', text = '248,248,242', status = '73,72,62' },
  Light   = { bg = '255,255,255,245', bar = '236,236,236', num = '160,160,160', comment = '106,115,125', keyword = '215,58,73',
              string = '3,47,98',     func = '111,66,193',  type = '0,92,197',    number = '0,92,197',    text = '36,41,46',    status = '0,92,197' },
}

local function wallpaperLuma()                  -- 0..1 from the RunCommand measure [mLum]; keeps the last good value
  local m = SKIN:GetMeasure('mLum')
  if m then
    local str = (m:GetStringValue() or ''):gsub(',', '.')
    local n = tonumber(str:match('%d+%.?%d*'))
    if n then lastLuma = n end
  end
  return lastLuma
end

local function accent()
  local m = SKIN:GetMeasure('mAccent')
  local v = m and (tonumber(m:GetValue()) or 0) or 0
  if v < 0 then v = v + 4294967296 end

  local luma   = wallpaperLuma()
  local cm     = var('ColorMode', 'Invert')            -- Invert | Accent | White | Black   (text / ink colour)
  local th     = theme()                               -- Neutral | Bloom | Volt             (accent palette)
  local pal    = PAL[th]
  local bright = wasBright or false                    -- small hysteresis so a mid-grey wallpaper does not flicker
  if luma then
    if bright then bright = luma > 0.48 else bright = luma > 0.55 end
  end
  wasBright = bright
  if cm == 'White' then bright = false elseif cm == 'Black' then bright = true end

  local ct  = var('CodeTheme', 'Dark')
  local key = v .. '|' .. tostring(bright) .. '|' .. cm .. '|' .. th .. '|' .. ct
  if key == lastKey then return end
  lastKey = key

  local ink = bright and '0,0,0' or '255,255,255'
  setv('Ink',     ink)
  setv('InkDim',  ink .. ',190')
  setv('InkMid',  ink .. ',120')
  setv('InkSoft', ink .. ',60')

  local rgb = ink                               -- Invert / White / Black: accent colour = ink
  if pal then
    rgb = pal.c
  elseif cm == 'Accent' then                    -- Windows accent colour (ABGR DWORD)
    local r, g, b = 255, 255, 255
    if v > 0 then
      r = v % 256
      g = math.floor(v / 256) % 256
      b = math.floor(v / 65536) % 256
    end
    rgb = string.format('%d,%d,%d', r, g, b)
  end
  local rgb2 = pal and pal.c2 or rgb
  setv('Color',      rgb)
  setv('ColorDim',   rgb .. ',190')
  setv('ColorMid',   rgb .. ',120')
  setv('ColorSoft',  rgb .. ',60')
  setv('Color2',     rgb2)
  setv('Color2Soft', rgb2 .. ',70')
  for role, col in pairs(CODE[ct] or CODE.Dark) do setv('CT' .. role, col) end
  setv('GradA', pal and pal.c  or '120,140,255')
  setv('GradB', pal and pal.c2 or '255,130,200')
end

-- ---------------------------------------------------------------- angles for the dash / marker meters

local sLast, sTicks = -1, 0
local function subSecond(sec)                   -- fraction of the current second (only with Smooth=1, Update=100)
  if var('Smooth', '0') ~= '1' then return 0 end
  if sec ~= sLast then sLast, sTicks = sec, 0 else sTicks = sTicks + 1 end
  return math.min(sTicks * 0.1, 0.99)
end

local function angles(t)
  local sec = t.sec + subSecond(t.sec)
  local min = t.min + sec / 60
  local hr  = (t.hour % 12) + min / 60
  local day = t.hour + min / 60
  local q   = math.pi / 2
  setnum('SecRad',  sec / 60 * 2 * math.pi - q)
  setnum('MinRad',  min / 60 * 2 * math.pi - q)
  setnum('HourRad', hr / 12 * 2 * math.pi - q)
  setnum('DayRad',  math.pi + day / 24 * math.pi)     -- left -> top -> right (a half circle)
  setnum('DayF',    day / 24)
end

-- ---------------------------------------------------------------- style shuffle
-- Every day the styles in the pool are shuffled once; slot 0 uses the 1st, slot 1 the 2nd ... in an order that is the
-- same all day long (a skin refresh will not change it). The last style of yesterday never repeats as the first of today.

local function allowed(i)
  local tag = TAGS[i]
  if not tag then return true end
  local p, th = profile(), theme()
  if tag == 'code' then return p ~= 'Everyday' end
  if tag == 'easy' then return p ~= 'Coder' end
  if tag == 'girl' then return th == 'Bloom' end
  if tag == 'boy'  then return th == 'Volt' end
  if tag == 'en'   then local l = var('Language', 'Windows'); return l == 'English' or l == 'Windows' end
  return true
end

local function lcg(seed)
  local s = seed % 4294967296
  local function nxt()
    s = (1664525 * s + 1013904223) % 4294967296
    return s / 4294967296
  end
  for _ = 1, 12 do nxt() end                -- warm-up, so neighbouring days do not look alike
  return nxt
end

local function shuffled(year, yday)
  local rnd = lcg(year * 400 + yday)
  local p = {}
  for i = 1, #pool do p[i] = pool[i] end
  for i = #p, 2, -1 do
    local j = math.floor(rnd() * i) + 1
    p[i], p[j] = p[j], p[i]
  end
  return p
end

local function slot(t) return math.floor((t.hour * 60 + t.min) / interval) end

local function styleFor(t)
  local M = #pool
  local p = shuffled(t.year, t.yday)
  local y = os.date('*t', os.time({ year = t.year, month = t.month, day = t.day - 1, hour = 12 }))
  local q = shuffled(y.year, y.yday)
  local last = ((math.ceil(1440 / interval) - 1) % M) + 1
  if M > 1 and p[1] == q[last] then p[1], p[2] = p[2], p[1] end
  return p[(slot(t) % M) + 1]
end

local coords                                      -- defined below (location helpers)

local function writeState()                       -- read by the Settings window and the gallery
  local f = io.open(var('CURRENTPATH', '') .. 'state.txt', 'w')
  if not f then return end
  f:write('StyleNo=', tostring(current or 0), '\nStyleName=', NAMES[current or 0] or '', '\nStyleTotal=', tostring(N),
          '\nLocked=', locked and '1' or '0', '\nLocation=', select(3, coords()) or 'none', '\n')
  f:close()
end

local function showStyle(n)
  if n == current then return end
  if current then setv('H' .. current, 1) end
  setv('H' .. n, 0)
  setv('StyleNo', n)
  setv('StyleName', NAMES[n] or ('Style ' .. n))
  current = n
  writeState()
end

-- ---------------------------------------------------------------- menu actions

local function saveVar(name, value)
  local path = var('CURRENTPATH', '') .. var('CURRENTFILE', '')
  SKIN:Bang('!WriteKeyValue', 'Variables', name, tostring(value), path)
end

local function cycleVar(name, list, default)
  local cur, idx = var(name, default), 0
  for i, v in ipairs(list) do if tostring(v) == cur then idx = i end end
  saveVar(name, list[(idx % #list) + 1])
  SKIN:Bang('!Refresh')
end

function Next()
  local idx = 0
  for i, n in ipairs(pool) do if n == current then idx = i end end
  showStyle(pool[(idx % #pool) + 1])
  refresh()
end

function RandomStyle()
  math.randomseed(os.time())
  math.random()
  local n = pool[math.random(#pool)]
  if n == current and #pool > 1 then
    local idx = 1
    for i, v in ipairs(pool) do if v == n then idx = i end end
    n = pool[(idx % #pool) + 1]
  end
  showStyle(n)
  refresh()
end

function ToggleHourFormat() cycleVar('HourFormat', { '%H', '%#I' }, '%H') end
function ToggleQuote()      cycleVar('QuoteHidden', { 0, 1 }, '0') end
function CycleQuoteRate()   cycleVar('QuoteMinutes', { 1440, 60, 30, 10 }, '1440') end
function CycleColors()      cycleVar('ColorMode', { 'Invert', 'Accent', 'White', 'Black' }, 'Invert') end
function CycleShuffle()     cycleVar('ShuffleMinutes', { 60, 30, 15, 5, 1440 }, '60') end
function CycleProfile()     cycleVar('Profile', { 'All', 'Coder', 'Everyday' }, 'All') end
function CycleTheme()       cycleVar('Theme', { 'Neutral', 'Bloom', 'Volt' }, 'Neutral') end
local LANGUAGES = { 'Windows', 'English', 'Spanish', 'French', 'German', 'Portuguese', 'Italian', 'Sinhala', 'Tamil', 'Hindi', 'Japanese' }
local function langFile(name) return (name == 'Windows' or name == 'English') and 'AdaptiveClock.lua' or 'AdaptiveClockU.lua' end
function CycleLanguage()
  local cur, idx = var('Language', 'Windows'), 0
  for i, v in ipairs(LANGUAGES) do if v == cur then idx = i end end
  local nxtLang = LANGUAGES[(idx % #LANGUAGES) + 1]
  saveVar('Language', nxtLang)
  saveVar('LangFile', langFile(nxtLang))
  SKIN:Bang('!Refresh')
end

-- Used by the Settings skin:  [!CommandMeasure mMain "Set('Theme','Bloom')" "AdaptiveClock"]
local SETTABLE = { Profile = 1, Theme = 1, ColorMode = 1, ShuffleMinutes = 1, QuoteMinutes = 1, QuoteHidden = 1,
  QuoteStyle = 1, HourFormat = 1, Language = 1, WeekStart = 1, Smooth = 1, TempUnit = 1, WeatherOff = 1,
  PomoWork = 1, PomoBreak = 1, TimerBeep = 1, CodeTheme = 1 }

function Set(name, value)
  if not SETTABLE[name] then return end
  value = tostring(value)
  if name == 'HourFormat' then value = (value == 'H12') and '%#I' or '%H' end
  saveVar(name, value)
  if name == 'Language' then saveVar('LangFile', langFile(value)) end
  if name == 'Smooth' then
    saveVar('UpdateMs', value == '1' and 100 or 1000)
    saveVar('Div', value == '1' and 10 or 1)
  end
  SKIN:Bang('!Refresh')
end

function NextQuote()                              -- every quote measure reads this variable
  setv('QuoteBump', (tonumber(var('QuoteBump', '0')) or 0) + 1)
  refresh()
end

function SkipThisStyle()
  if #pool <= 1 or not current then return end
  local cur = var('SkipStyles', '')
  saveVar('SkipStyles', (cur ~= '' and (cur .. ',') or '') .. current)
  SKIN:Bang('!Refresh')
end

function ShowAllStyles()
  saveVar('SkipStyles', '')
  SKIN:Bang('!Refresh')
end

function Lock()
  if not current then return end
  locked, lockedStyle = true, current
  saveVar('LockedStyle', current)                 -- survives a refresh
  setv('LockMark', ' [locked]')
  writeState()
  refresh()
end

function Unlock()
  locked, lockedStyle = false, 0
  saveVar('LockedStyle', 0)
  setv('LockMark', '')
  showStyle(styleFor(os.date('*t')))
  writeState()
  refresh()
end

function ToggleLock()
  if locked then Unlock() else Lock() end
end

function Resume()
  Unlock()
end

function GoTo(n)                                  -- used by the style gallery: show a style and keep it
  n = tonumber(n)
  if not n or n < 1 or n > N then return end
  showStyle(n)
  Lock()
end

-- ---------------------------------------------------------------- quotes

-- Optional quotes.txt next to the skin: one quote per line, "text | author". Lines starting with # are ignored.
local function loadQuotes()
  local f = io.open(var('CURRENTPATH', '') .. 'quotes.txt', 'r')
  if not f then return end
  local list = {}
  for raw in f:lines() do
    local line = raw:gsub('^\239\187\191', ''):gsub('\r', ''):match('^%s*(.-)%s*$')
    if line ~= '' and line:sub(1, 1) ~= '#' then
      local text, who = line:match('^(.-)%s*|%s*(.+)$')
      if text and text ~= '' then list[#list + 1] = Q('b', text, who)
      else list[#list + 1] = Q('b', line, '') end
    end
  end
  f:close()
  if #list > 0 then QUOTES = list end
end

local function buildQuotePool()
  local p = profile()
  qpool = {}
  for _, q in ipairs(QUOTES) do
    if q[3] == 'b' or p == 'All' or (p == 'Coder' and q[3] == 'c') or (p == 'Everyday' and q[3] == 'e') then
      qpool[#qpool + 1] = q
    end
  end
  if #qpool == 0 then qpool = QUOTES end
end

local function quoteEntry(t)
  local qm = math.max(1, math.min(1440, tonumber(var('QuoteMinutes', '1440')) or 1440))
  local per = math.ceil(1440 / qm)
  local sl = (qm >= 1440) and 0 or math.floor((t.hour * 60 + t.min) / qm)
  local bump = tonumber(var('QuoteBump', '0')) or 0
  return qpool[((t.year * 366 + t.yday) * per + sl + bump) % #qpool + 1]
end

local function quoteMode()
  local qs = var('QuoteStyle', 'Auto')
  if qs == 'Terminal' then return 'terminal' end
  if qs == 'Friendly' then return 'friendly' end
  return (profile() == 'Coder') and 'terminal' or 'friendly'
end

local function quoteFlags()                       -- which of the two quote designs is visible
  local hidden = (var('QuoteHidden', '0') == '1')
  local m = quoteMode()
  if current == 100 then hidden = true end       -- the Big quote clock shows the quote itself
  local key = tostring(hidden) .. m
  if key == lastQKey then return end
  lastQKey = key
  setv('QHf', (hidden or m ~= 'friendly') and 1 or 0)
  setv('QHc', (hidden or m ~= 'terminal') and 1 or 0)
end

local function quoteBody()
  local q = quoteEntry(os.date('*t'))
  if quoteMode() == 'terminal' then return '// ' .. q[1] end
  return LQ .. q[1] .. RQ
end

local function quoteWho()
  local q = quoteEntry(os.date('*t'))
  if quoteMode() == 'terminal' then
    return '-- ' .. q[2] .. (os.date('*t').sec % 2 == 0 and '_' or ' ')
  end
  return (q[2] ~= '') and (D .. ' ' .. q[2]) or ''
end

-- ---------------------------------------------------------------- calendar maths + world time (with daylight saving rules)

local DIM = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 }

local function isLeap(y) return (y % 4 == 0 and y % 100 ~= 0) or y % 400 == 0 end

local function daysInMonth(y, m)
  if m == 2 and isLeap(y) then return 29 end
  return DIM[m]
end

-- ---------------------------------------------------------------- language (Languages.lua holds the other languages)

local EN = {
  dow  = { 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' },
  dowS = { 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat' },
  dowH = { 'Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa' },
  mon  = { 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' },
  monS = { 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' },
  greet = { night = 'Good night', morning = 'Good morning', afternoon = 'Good afternoon', evening = 'Good evening' },
  t = { hour = 'HOUR', minute = 'MINUTE', second = 'SECOND', hours = 'HOURS', minutes = 'MINUTES', seconds = 'SECONDS',
        world = 'World Time', daysLeft = '{n} days left', daysLeftYear = '{n} days left in {year}',
        yearDone = 'of {year} is done', ofYear = 'of {year}', secondsLow = 'seconds', focus = 'FOCUS', rest = 'BREAK',
        alarm = 'Alarm', ringing = 'ALARM!', sunrise = 'Sunrise', sunset = 'Sunset',
        nothing = 'Nothing playing', battery = 'Battery', charging = 'Charging',
        setLocation = 'Location not found - see Settings > Extras', weatherOff = 'Weather is off - enable it in Settings',
        loading = 'Loading...', itsWeekend = "It's the weekend!", weekendLeft = 'until the weekend',
        daylight = 'of daylight', bdayUnset = 'Set Birthday=MM-DD in AdaptiveClock.ini', bdayToday = 'Happy birthday!', bdayLeft = 'days until your birthday' },
}
local LANGS

local function lang()                           -- returns the active language table and its name
  local name = var('Language', 'Windows')
  if name == 'English' or name == 'Windows' then return EN, name end
  if not LANGS then
    local ok, t = pcall(dofile, var('CURRENTPATH', '') .. 'Languages.lua')
    LANGS = (ok and type(t) == 'table') and t or {}
  end
  return LANGS[name] or EN, name
end

local function tr(key)
  local l = lang()
  return (l.t and l.t[key]) or EN.t[key] or key
end

local function label(key)                         -- translated label with {n} and {year} filled in
  local t = os.date('*t')
  local s = tr(key)
  s = s:gsub('{n}', function() return tostring((((t.year % 4 == 0 and t.year % 100 ~= 0) or t.year % 400 == 0) and 366 or 365) - t.yday) end)
  s = s:gsub('{year}', tostring(t.year))
  return s
end

local function windowsText(measure)               -- text of a Windows-language Time measure in the .ini
  local m = SKIN:GetMeasure(measure)
  return m and (m:GetStringValue() or '') or ''
end

local function dateName(kind, windowsMeasure)     -- kind = dow | dowS | mon | monS
  local l, name = lang()
  if name == 'Windows' then return windowsText(windowsMeasure) end
  local t = os.date('*t')
  local idx = (kind == 'dow' or kind == 'dowS') and t.wday or t.month
  return (l[kind] and l[kind][idx]) or EN[kind][idx]
end

local function daysFromCivil(y, m, d)           -- days since 1970-01-01 (proleptic Gregorian)
  if m <= 2 then y = y - 1 end
  local era = math.floor(y / 400)
  local yoe = y - era * 400
  local mp  = (m + 9) % 12
  local doy = math.floor((153 * mp + 2) / 5) + d - 1
  local doe = yoe * 365 + math.floor(yoe / 4) - math.floor(yoe / 100) + doy
  return era * 146097 + doe - 719468
end

local function weekday(days) return (days + 4) % 7 end     -- 0 = Sunday

local function nthSunday(y, m, n)
  local first = 1 + (7 - weekday(daysFromCivil(y, m, 1))) % 7
  return first + 7 * (n - 1)
end

local function lastSunday(y, m)
  local dim = daysInMonth(y, m)
  return dim - weekday(daysFromCivil(y, m, dim))
end

local function dayEpoch(y, m, d) return daysFromCivil(y, m, d) * 86400 end

local function isDST(rule, std, utc)
  if not rule then return false end
  local y = tonumber(os.date('!%Y', utc))
  if rule == 'US' then
    local s = dayEpoch(y, 3, nthSunday(y, 3, 2)) + (2 - std) * 3600
    local e = dayEpoch(y, 11, nthSunday(y, 11, 1)) + (1 - std) * 3600
    return utc >= s and utc < e
  elseif rule == 'EU' then
    local s = dayEpoch(y, 3, lastSunday(y, 3)) + 3600
    local e = dayEpoch(y, 10, lastSunday(y, 10)) + 3600
    return utc >= s and utc < e
  elseif rule == 'AU' then                                  -- southern hemisphere
    local s = dayEpoch(y, 10, nthSunday(y, 10, 1)) + (2 - std) * 3600
    local e = dayEpoch(y, 4, nthSunday(y, 4, 1)) + (3 - (std + 1)) * 3600
    return utc >= s or utc < e
  end
  return false
end

-- { name, standard UTC offset in hours, daylight-saving rule: 'US' | 'EU' | 'AU' | nil }
local CITIES = {
  { 'NEW YORK', -5, 'US' },
  { 'LONDON',    0, 'EU' },
  { 'DUBAI',     4, nil  },
  { 'TOKYO',     9, nil  },
  { 'SYDNEY',   10, 'AU' },
}

-- Optional  Cities=  variable in the .ini:  NAME:offset:RULE|NAME:offset:RULE ...   (RULE = US, EU, AU or -)
local function loadCities()
  local v = var('Cities', '')
  if v == '' then return end
  local list = {}
  for item in v:gmatch('[^|]+') do
    local name, off, rule = item:match('^%s*(.-)%s*:%s*(%-?[%d%.]+)%s*:%s*(%a*%-?)%s*$')
    if name and name ~= '' then
      list[#list + 1] = { string.upper(name), tonumber(off), (rule == 'US' or rule == 'EU' or rule == 'AU') and rule or nil }
    end
    if #list == 5 then break end
  end
  if #list > 0 then CITIES = list end
end

local function cityTime(c, utc)
  local off = c[2] + (isDST(c[3], c[2], utc) and 1 or 0)
  return utc + off * 3600
end

local function world(kind)
  local utc = os.time()
  local h12 = is12h()
  local out = {}
  for i, c in ipairs(CITIES) do
    local lt = cityTime(c, utc)
    if kind == 'name' then
      out[i] = c[1]
    elseif kind == 'day' then
      local u0 = os.date('!*t', lt)
      local l = lang()
      out[i] = string.upper((l.dowS or EN.dowS)[u0.wday] or EN.dowS[u0.wday])
    else
      local u = os.date('!*t', lt)
      if h12 then
        out[i] = string.format('%d:%02d %s', (u.hour % 12 == 0) and 12 or (u.hour % 12), u.min, u.hour < 12 and 'AM' or 'PM')
      else
        out[i] = string.format('%02d:%02d', u.hour, u.min)
      end
    end
  end
  return table.concat(out, '\n')
end

-- month grid for the calendar styles (variables CalH1..7, CalD1..42, CalToday, WeekIdx)
local function calendar(t)
  local ws = tonumber(var('WeekStart', '1')) or 1             -- 0 = Sunday first, 1 = Monday first
  local names = lang().dowH or EN.dowH
  local first = os.date('*t', os.time({ year = t.year, month = t.month, day = 1, hour = 12 }))
  local off = (first.wday - 1 - ws) % 7
  local dim = daysInMonth(t.year, t.month)
  for i = 1, 42 do
    local d = i - off
    setv('CalD' .. i, (d >= 1 and d <= dim) and tostring(d) or '')
  end
  setv('CalToday', off + t.day)
  setv('WeekIdx', ((t.wday - 1 - ws) % 7) + 1)
end

-- ---------------------------------------------------------------- word clock

local HOURS = { 'TWELVE', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'ELEVEN' }
local PHRASE = {
  [0] = "IT'S", [5] = 'FIVE PAST', [10] = 'TEN PAST', [15] = 'QUARTER PAST', [20] = 'TWENTY PAST',
  [25] = 'TWENTY-FIVE PAST', [30] = 'HALF PAST', [35] = 'TWENTY-FIVE TO', [40] = 'TWENTY TO',
  [45] = 'QUARTER TO', [50] = 'TEN TO', [55] = 'FIVE TO',
}

local function words()
  local t = os.date('*t')
  local m5 = math.floor((t.min + 2) / 5) * 5
  local h = t.hour
  if m5 == 60 then m5 = 0; h = h + 1 end
  if m5 > 30 then h = h + 1 end
  return PHRASE[m5], HOURS[(h % 12) + 1]
end

-- ---------------------------------------------------------------- small helpers for the new styles

local function bits(n, w)
  local s = ''
  for i = w - 1, 0, -1 do s = s .. ((math.floor(n / 2 ^ i) % 2 == 1) and '1' or '0') end
  return s
end

local function greeting(h)
  local g = lang().greet or EN.greet
  if h < 5 then return g.night end
  if h < 12 then return g.morning end
  if h < 17 then return g.afternoon end
  if h < 21 then return g.evening end
  return g.night
end

local function yearFraction(t)
  local len = isLeap(t.year) and 366 or 365
  return ((t.yday - 1) * 86400 + t.hour * 3600 + t.min * 60 + t.sec) / (len * 86400)
end


-- ---------------------------------------------------------------- sunrise / sunset (needs Latitude and Longitude)

local locCache, locRead = nil, 0

local function readLocation()                      -- State\location.txt is written by LocationFinder.ps1 (no internet involved)
  local t = os.time()
  if locCache ~= nil and t - locRead < 30 then return locCache end
  locRead, locCache = t, false
  local f = io.open(var('CURRENTPATH', '') .. 'State\\location.txt', 'r')
  if f then
    local d = {}
    for raw in f:lines() do
      local k, v = raw:gsub('\r', ''):match('^(%w+)=(.*)$')
      if k then d[k] = v end
    end
    f:close()
    local la, lo = tonumber(d.lat), tonumber(d.lon)
    if la and lo and (d.source == 'windows' or d.source == 'timezone') then locCache = { lat = la, lon = lo, source = d.source } end
  end
  return locCache
end

coords = function()                            -- typed in the .ini, or found on this PC. Never looked up online.
  local la, lo = tonumber(var('Latitude', '')), tonumber(var('Longitude', ''))
  if la and lo then return la, lo, 'manual' end
  local c = readLocation()
  if c then return c.lat, c.lon, c.source end
  return nil
end

local sunCache = {}

local function sunTimes(t)                        -- unix times of sunrise and sunset, or nil without coordinates
  local lat, lon = coords()
  if not lat then return nil end
  local c = sunCache
  if c.yday == t.yday and c.year == t.year and c.lat == lat and c.lon == lon then return c.rise, c.set end
  local rad = math.pi / 180
  local noon = os.time({ year = t.year, month = t.month, day = t.day, hour = 12 })
  local n  = math.ceil(noon / 86400 + 2440587.5 - 2451545.0 + 0.0008)
  local js = n - lon / 360
  local M  = (357.5291 + 0.98560028 * js) % 360
  local C  = 1.9148 * math.sin(M * rad) + 0.0200 * math.sin(2 * M * rad) + 0.0003 * math.sin(3 * M * rad)
  local lam = (M + C + 180 + 102.9372) % 360
  local jt = 2451545.0 + js + 0.0053 * math.sin(M * rad) - 0.0069 * math.sin(2 * lam * rad)
  local sd = math.sin(lam * rad) * math.sin(23.4397 * rad)
  local cd = math.cos(math.asin(sd))
  local cw = (math.sin(-0.833 * rad) - math.sin(lat * rad) * sd) / (math.cos(lat * rad) * cd)
  local rise, set
  if cw >= -1 and cw <= 1 then
    local w = math.acos(cw) / rad
    rise = (jt - w / 360 - 2440587.5) * 86400
    set  = (jt + w / 360 - 2440587.5) * 86400
  end
  sunCache = { yday = t.yday, year = t.year, lat = lat, lon = lon, rise = rise, set = set }
  return rise, set
end

local function sunPair(t)                         -- falls back to 06:00 / 18:00 so the style still looks alive
  local r, s = sunTimes(t)
  if r and s then return r, s, true end
  return os.time({ year = t.year, month = t.month, day = t.day, hour = 6 }),
         os.time({ year = t.year, month = t.month, day = t.day, hour = 18 }), false
end

local function sunFraction(t)
  local r, s = sunPair(t)
  return math.max(0, math.min(1, (os.time() - r) / (s - r)))
end

local function fmtClock(unix)
  local u = os.date('*t', math.floor(unix + 0.5))
  if is12h() then
    return string.format('%d:%02d %s', (u.hour % 12 == 0) and 12 or (u.hour % 12), u.min, u.hour < 12 and 'AM' or 'PM')
  end
  return string.format('%02d:%02d', u.hour, u.min)
end

-- ---------------------------------------------------------------- weather text (data comes from the WebParser measures)

local WX = { [0] = 'Clear sky', [1] = 'Mainly clear', [2] = 'Partly cloudy', [3] = 'Overcast', [45] = 'Fog', [48] = 'Rime fog',
  [51] = 'Light drizzle', [53] = 'Drizzle', [55] = 'Heavy drizzle', [56] = 'Freezing drizzle', [57] = 'Freezing drizzle',
  [61] = 'Light rain', [63] = 'Rain', [65] = 'Heavy rain', [66] = 'Freezing rain', [67] = 'Freezing rain',
  [71] = 'Light snow', [73] = 'Snow', [75] = 'Heavy snow', [77] = 'Snow grains', [80] = 'Rain showers', [81] = 'Rain showers',
  [82] = 'Violent showers', [85] = 'Snow showers', [86] = 'Snow showers', [95] = 'Thunderstorm', [96] = 'Thunderstorm, hail',
  [99] = 'Thunderstorm, hail' }

local function wxCode()
  local m = SKIN:GetMeasure('mWxC')
  return m and tonumber((m:GetStringValue() or ''):match('%d+')) or nil
end

local function wxIcon()
  local c = wxCode()
  if c == nil then return '\226\152\129' end
  if c <= 1 then return SUN end
  if c == 2 then return '\226\155\133' end
  if c == 3 or c == 45 or c == 48 then return '\226\152\129' end
  if (c >= 51 and c <= 67) or (c >= 80 and c <= 82) then return '\226\152\130' end
  if (c >= 71 and c <= 77) or c == 85 or c == 86 then return '\226\157\132' end
  if c >= 95 then return '\226\154\161' end
  return '\226\152\129'
end

local function wxTemp()
  local m = SKIN:GetMeasure('mWxT')
  local n = m and tonumber((m:GetStringValue() or ''):match('%-?%d+%.?%d*')) or nil
  if not n then return '--' end
  return string.format('%d', math.floor(n + 0.5)) .. '\194\176' .. (var('TempUnit', 'celsius') == 'fahrenheit' and 'F' or 'C')
end

local function wxText()
  if var('WeatherOff', '1') == '1' then return tr('weatherOff') end
  if not coords() then return tr('setLocation') end
  local c = wxCode()
  if c == nil then return tr('loading') end
  return WX[c] or ''
end

-- ---------------------------------------------------------------- timer (pomodoro) and alarm - run by the main script

local pomo = { mode = 'focus', running = false, remaining = nil, last = nil }
local alarmFired, ringing, ringCount, lastRingT, pubKey = nil, false, 0, 0, nil

local function pomoLen(m)
  if m == 'focus' then return (tonumber(var('PomoWork', '25')) or 25) * 60 end
  return (tonumber(var('PomoBreak', '5')) or 5) * 60
end

local function beep()
  if var('TimerBeep', '1') == '1' then
    SKIN:Bang('!Run', 'PowerShell -NoProfile -WindowStyle Hidden -Command [console]::beep(880,350)')
  end
end

function PomoToggle()
  if not pomo.remaining then pomo.remaining = pomoLen(pomo.mode) end
  pomo.running = not pomo.running
  pomo.last = os.time()
  pubKey = nil
end

function PomoReset()
  pomo.mode, pomo.running, pomo.remaining = 'focus', false, pomoLen('focus')
  pubKey = nil
end

function PomoSkip()
  pomo.mode = (pomo.mode == 'focus') and 'break' or 'focus'
  pomo.remaining = pomoLen(pomo.mode)
  pubKey = nil
end

function AlarmToggle()
  local v = (var('AlarmOn', '0') == '1') and '0' or '1'
  setv('AlarmOn', v)
  saveVar('AlarmOn', v)
  pubKey = nil
end

function AlarmStop() ringing = false; pubKey = nil end

function AlarmClick() if ringing then AlarmStop() else AlarmToggle() end end

function AlarmAdd(minutes)
  local h, m = (var('AlarmTime', '07:00')):match('^(%d+):(%d+)$')
  local total = ((tonumber(h) or 7) * 60 + (tonumber(m) or 0) + (tonumber(minutes) or 0)) % 1440
  local v = string.format('%02d:%02d', math.floor(total / 60), total % 60)
  setv('AlarmTime', v)
  saveVar('AlarmTime', v)
  pubKey = nil
end

local function tickTimers(t)
  if pomo.remaining == nil then pomo.remaining = pomoLen('focus') end
  local nowT = os.time()
  if pomo.running then
    pomo.remaining = pomo.remaining - (nowT - (pomo.last or nowT))
    pomo.last = nowT
    if pomo.remaining <= 0 then
      pomo.mode = (pomo.mode == 'focus') and 'break' or 'focus'
      pomo.remaining = pomoLen(pomo.mode)
      beep()
    end
  end
  local stamp = t.yday * 100000 + t.hour * 60 + t.min
  if var('AlarmOn', '0') == '1' and string.format('%02d:%02d', t.hour, t.min) == var('AlarmTime', '07:00') and alarmFired ~= stamp then
    alarmFired, ringing, ringCount = stamp, true, 0
  end
  if ringing and nowT ~= lastRingT then
    lastRingT = nowT
    ringCount = ringCount + 1
    if ringCount % 2 == 1 then beep() end
    if ringCount > 30 then ringing = false end
  end

  local rem = math.max(0, pomo.remaining)
  local text = string.format('%02d:%02d', math.floor(rem / 60), rem % 60)
  local label2 = pomo.mode
  local alarmText = ringing and 'R' or 'N'
  local key = text .. label2 .. alarmText .. tostring(pomo.running) .. var('AlarmTime', '07:00') .. var('AlarmOn', '0')
  if key == pubKey then return end
  pubKey = key
  setv('PomoText', text)
  setnum('PomoFrac', rem / math.max(1, pomoLen(pomo.mode)))
  setv('PomoMode', label2)
  setv('PomoBtn', pomo.running and '||' or '>')
  setv('AlarmRing', ringing and 1 or 0)
end

-- ---------------------------------------------------------------- moon phase

local MOON_NAMES = { 'New moon', 'Waxing crescent', 'First quarter', 'Waxing gibbous', 'Full moon', 'Waning gibbous',
                     'Last quarter', 'Waning crescent' }
local MOON_ICONS = { '\240\159\140\145', '\240\159\140\146', '\240\159\140\147', '\240\159\140\148',
                     '\240\159\140\149', '\240\159\140\150', '\240\159\140\151', '\240\159\140\152' }
local SYNODIC = 29.530588853

local function moonAge() return ((os.time() - 947182440) / 86400) % SYNODIC end   -- new moon: 2000-01-06 18:14 UTC
local function moonIndex() return math.floor(moonAge() / SYNODIC * 8 + 0.5) % 8 + 1 end

-- ---------------------------------------------------------------- helpers for the coder clocks

local GLYPH = {
  ['0'] = { '1111', '1001', '1001', '1001', '1111' }, ['1'] = { '0110', '0010', '0010', '0010', '0111' },
  ['2'] = { '1111', '0001', '1111', '1000', '1111' }, ['3'] = { '1111', '0001', '0111', '0001', '1111' },
  ['4'] = { '1001', '1001', '1111', '0001', '0001' }, ['5'] = { '1111', '1000', '1111', '0001', '1111' },
  ['6'] = { '1111', '1000', '1111', '1001', '1111' }, ['7'] = { '1111', '0001', '0010', '0100', '0100' },
  ['8'] = { '1111', '1001', '1111', '1001', '1111' }, ['9'] = { '1111', '1001', '1111', '0001', '1111' },
}
local lastPix

local function setPixels(t)                       -- dot-matrix clock: PXn = 255 (lit) or 40 (off)
  local key = t.hour * 100 + t.min
  if key == lastPix then return end
  lastPix = key
  local digits = string.format('%02d%02d', t.hour, t.min)
  for d = 1, 4 do
    local g = GLYPH[digits:sub(d, d)]
    for r = 1, 5 do
      for c = 1, 4 do
        setv('PX' .. ((d - 1) * 20 + (r - 1) * 4 + c), g[r]:sub(c, c) == '1' and 255 or 40)
      end
    end
  end
  setv('PX81', 255); setv('PX82', 255)
end

local RAIN = 'ABCDEF0123456789<>/{}=;'
local function rainColumn(col)                    -- 15 characters that "fall" one row per second
  local t, out = os.time(), {}
  for r = 0, 14 do
    local h = ((t - r) * 7919 + col * 104729 + 13) % 65521
    h = (h * h + 12345) % 65521
    local k = h % #RAIN + 1
    out[#out + 1] = RAIN:sub(k, k)
  end
  return table.concat(out, '\n')
end

local function hexRow(k)                          -- row k of a hexdump of "HH:MM:SS Day DD Mon YYYY"
  local s = os.date('%H:%M:%S %a %d %b %Y')
  local chunk = (s:sub(k * 8 + 1, k * 8 + 8) .. '        '):sub(1, 8)
  local hex, asc = {}, {}
  for i = 1, 8 do
    local b = chunk:byte(i)
    hex[i] = string.format('%02x', b)
    asc[i] = (b >= 32 and b < 127) and string.char(b) or '.'
  end
  return string.format('%04x  %s  %s  |%s|', k * 8, table.concat(hex, ' ', 1, 4), table.concat(hex, ' ', 5, 8), table.concat(asc))
end

-- ---------------------------------------------------------------- friendly helpers (weekend, birthday, week of the year)

local function weekdayMon()                         -- Monday = 1 ... Sunday = 7
  return (os.date('*t').wday + 5) % 7 + 1
end

local function untilWeekend()                       -- seconds until Saturday 00:00, or nil during the weekend
  local t, wd = os.date('*t'), weekdayMon()
  if wd >= 6 then return nil end
  return (5 - wd) * 86400 + (86400 - (t.hour * 3600 + t.min * 60 + t.sec))
end

local function birthdayDays()
  local m, d = (var('Birthday', '')):match('^(%d+)%-(%d+)$')
  if not m then return nil end
  local t = os.date('*t')
  local today = os.time({ year = t.year, month = t.month, day = t.day, hour = 12 })
  local target = os.time({ year = t.year, month = tonumber(m), day = tonumber(d), hour = 12 })
  if target < today then target = os.time({ year = t.year + 1, month = tonumber(m), day = tonumber(d), hour = 12 }) end
  return math.floor((target - today) / 86400 + 0.5)
end

local function weatherCoords()                      -- the ONLY place coordinates are prepared for the internet, and only if Weather is on
  if var('WeatherOff', '1') == '1' then
    setv('WxLat', ''); setv('WxLon', '')
    return
  end
  local la, lo = tonumber(var('WeatherLatitude', '')), tonumber(var('WeatherLongitude', ''))
  if not (la and lo) then la, lo = coords() end
  if not la then return end
  local a, b = string.format('%.1f', la), string.format('%.1f', lo)   -- rounded to about 11 km before it can leave the PC
  if a ~= wxLat then
    local first = (wxLat == nil)
    wxLat = a
    setv('WxLat', a); setv('WxLon', b)
    if first then SKIN:Bang('!CommandMeasure', 'mWxRaw', 'Update') end
  end
end

function RefreshLocation()                          -- Settings > Extras > Find my location again
  local here = var('CURRENTPATH', '')
  SKIN:Bang('!SetOption', 'mLoc', 'Parameter', '-NoProfile -ExecutionPolicy Bypass -File "' .. here ..
            'LocationFinder.ps1" -Out "' .. here .. 'State\\location.txt" -Force')
  SKIN:Bang('!CommandMeasure', 'mLoc', 'Run')
  locRead, locCache = 0, nil
end

local DEFAULTS = { Profile = 'All', Theme = 'Neutral', CodeTheme = 'Dark', ColorMode = 'Invert', ShuffleMinutes = '60',
  QuoteMinutes = '1440', QuoteHidden = '0', QuoteStyle = 'Auto', HourFormat = '%H', Language = 'Windows', WeekStart = '1',
  Smooth = '0', UpdateMs = '1000', Div = '1', TempUnit = 'celsius', WeatherOff = '1', PomoWork = '25', PomoBreak = '5',
  TimerBeep = '1', SkipStyles = '', LockedStyle = '0', LangFile = 'AdaptiveClock.lua' }

function ResetSettings()                            -- Settings > Actions > Reset all settings
  for k, v in pairs(DEFAULTS) do saveVar(k, v) end
  SKIN:Bang('!Refresh')
end

-- ---------------------------------------------------------------- measure entry points

local function now() return os.date('*t') end

local MODES = {
  secF  = function() local t = now(); return (t.sec + subSecond(t.sec)) / 60 end,
  minF  = function() local t = now(); return (t.min * 60 + t.sec) / 3600 end,
  hrF   = function() local t = now(); return ((t.hour % 12) * 3600 + t.min * 60 + t.sec) / 43200 end,
  dayF  = function() local t = now(); return (t.hour * 3600 + t.min * 60 + t.sec) / 86400 end,
  yearF = function() return yearFraction(now()) end,
  dHT = function() return math.floor(now().hour / 10) end,
  dHU = function() return now().hour % 10 end,
  dMT = function() return math.floor(now().min / 10) end,
  dMU = function() return now().min % 10 end,
  dST = function() return math.floor(now().sec / 10) end,
  dSU = function() return now().sec % 10 end,
  hexH = function() return string.format('0x%02X', now().hour) end,
  hexM = function() return string.format('0x%02X', now().min) end,
  hexS = function() return string.format('0x%02X', now().sec) end,
  binH = function() return bits(now().hour, 5) end,
  binM = function() return bits(now().min, 6) end,
  binS = function() return bits(now().sec, 6) end,
  epoch = function() return string.format('%d', os.time()) end,
  sha   = function() return string.format('%07x', (math.floor(os.time() / 60) * 40503 + 2654435) % 268435456) end,
  logHash = function() return string.format('%07x', ((math.floor(os.time() / 60) - logIndex) * 40503 + 2654435) % 268435456) end,
  logTime = function() local u = os.date('*t', os.time() - logIndex * 60); return string.format('%02d:%02d', u.hour, u.min) end,
  greet     = function() return greeting(now().hour) end,
  greetIcon = function() local h = now().hour; return (h >= 6 and h < 18) and SUN or MOON end,
  yearPct   = function() return string.format('%d%%', math.floor(yearFraction(now()) * 100)) end,
  daysLeft  = function() local t = now(); return (isLeap(t.year) and 366 or 365) - t.yday end,
  ampm   = function() if not is12h() then return '' end; return now().hour < 12 and 'AM' or 'PM' end,
  cursor = function() return (now().sec % 2 == 0) and '_' or ' ' end,
  qmark  = function() return LQ end,
  quoteBody = quoteBody,
  quoteWho  = quoteWho,
  secN = function() return now().sec end,
  calH = function()                                -- calendar header: Index 1..7 (week starts on WeekStart)
    local ws = tonumber(var('WeekStart', '1')) or 1
    return (lang().dowH or EN.dowH)[((logIndex - 1 + ws) % 7) + 1]
  end,
  wkH = function() return (lang().dowH or EN.dowH)[(logIndex % 7) + 1] end,   -- Monday-first weekday name: Index 1..7
  pomoLabel = function() return (var('PomoMode', 'focus') == 'focus') and tr('focus') or tr('rest') end,
  alarmText = function()
    if var('AlarmRing', '0') == '1' then return tr('ringing') end
    return tr('alarm') .. ' ' .. var('AlarmTime', '07:00') .. ((var('AlarmOn', '0') == '1') and '  ON' or '  OFF')
  end,
  quotePlain  = function() return quoteEntry(os.date('*t'))[1] end,
  quoteAuthor = function() local a = quoteEntry(os.date('*t'))[2]; return (a ~= '') and (D .. ' ' .. a) or '' end,
  wkText = function()
    local s = untilWeekend()
    if not s then return tr('itsWeekend') end
    return string.format('%dd %02dh', math.floor(s / 86400), math.floor((s % 86400) / 3600))
  end,
  wkF = function()
    local t, wd = os.date('*t'), weekdayMon()
    if wd >= 6 then return 1 end
    return math.min(1, ((wd - 1) * 86400 + t.hour * 3600 + t.min * 60 + t.sec) / (5 * 86400))
  end,
  wkDay = function() return weekdayMon() end,
  weekNo = function() return math.floor((os.date('*t').yday - 1) / 7) + 1 end,
  bdayDays = function() return birthdayDays() or 0 end,
  bdayText = function()
    local d = birthdayDays()
    if not d then return tr('bdayUnset') end
    if d == 0 then return tr('bdayToday') end
    return d .. ' ' .. tr('bdayLeft')
  end,
  dayLen = function()
    local r, s = sunPair(now())
    local m = math.floor((s - r) / 60 + 0.5)
    return string.format('%dh %02dm', math.floor(m / 60), m % 60)
  end,
  ciStatus = function()
    local st = math.floor(now().sec / 15)
    if st > logIndex then return 'passed' end
    if st == logIndex then return 'running' end
    return 'queued'
  end,
  hexRow = function() return hexRow(logIndex) end,
  rain   = function() return rainColumn(logIndex) end,
  moonIcon = function() return MOON_ICONS[moonIndex()] end,
  moonName = function() return MOON_NAMES[moonIndex()] end,
  moonPct  = function() return string.format('%d%%', math.floor((1 - math.cos(2 * math.pi * moonAge() / SYNODIC)) / 2 * 100 + 0.5)) end,
  moonF    = function() return moonAge() / SYNODIC end,
  dow  = function() return dateName('dow',  'mDowW') end,
  dowS = function() return dateName('dowS', 'mDowSW') end,
  mon  = function() return dateName('mon',  'mMonW') end,
  monS = function() return dateName('monS', 'mMonSW') end,
  lbl  = function() return label(lblKey) end,
  sunRise = function() local r = sunPair(now()); return fmtClock(r) end,
  sunSet  = function() local _, s = sunPair(now()); return fmtClock(s) end,
  sunF    = function() return sunFraction(now()) end,
  sunNote = function() local _, _, real = sunPair(now()); return real and '' or tr('setLocation') end,
  wxIcon = wxIcon, wxTemp = wxTemp, wxText = wxText,
  batText = function()
    local m = SKIN:GetMeasure('mBatAC')
    return (m and m:GetValue() == 1) and tr('charging') or tr('battery')
  end,
  worldName = function() return world('name') end,
  worldDay  = function() return world('day') end,
  worldTime = function() return world('time') end,
  wordsA = function() local a = words(); return a end,
  wordsB = function() local _, b = words(); return b end,
}

function Initialize()
  mode = SELF:GetOption('Mode', 'main')
  N = tonumber(var('StyleCount', '106')) or 106
  lblKey = SELF:GetOption('Key', '')
  logIndex = tonumber(SELF:GetOption('Index', '0')) or 0

  if mode == 'main' or mode == 'quoteBody' or mode == 'quoteWho' or mode == 'quotePlain' or mode == 'quoteAuthor' then
    loadQuotes()
    buildQuotePool()
  end
  if mode:match('^world') then loadCities() end

  if mode == 'main' then
    interval = math.max(1, math.min(1440, tonumber(var('ShuffleMinutes', '60')) or 60))
    local skip = {}
    for n in (var('SkipStyles', '')):gmatch('%d+') do skip[tonumber(n)] = true end
    pool = {}
    for i = 1, N do if not skip[i] and allowed(i) then pool[#pool + 1] = i end end
    if #pool == 0 then for i = 1, N do pool[i] = i end end
    lockedStyle = tonumber(var('LockedStyle', '0')) or 0
    locked = (lockedStyle >= 1 and lockedStyle <= N)
    if locked then setv('LockMark', ' [locked]') end
  end
end

function Update()
  if mode ~= 'main' then
    local f = MODES[mode]
    if f then return f() end
    return 0
  end

  local t = os.date('*t')
  safe(accent)
  safe(angles, t)
  safe(quoteFlags)
  safe(setPixels, t)
  safe(weatherCoords)
  safe(function()
    local _, _, src = coords()
    if src ~= lastLocSrc then lastLocSrc = src; writeState() end
  end)
  safe(tickTimers, t)
  safe(function()
    local f = sunFraction(t)
    setnum('SunRad', math.pi + f * math.pi)
  end)
  if t.yday ~= lastCalDay then
    lastCalDay = t.yday
    calendar(t)
  end
  if current == nil then
    showStyle(locked and lockedStyle or styleFor(t))
    lastSlot, lastYday = slot(t), t.yday
  elseif not locked and (slot(t) ~= lastSlot or t.yday ~= lastYday) then
    lastSlot, lastYday = slot(t), t.yday
    showStyle(styleFor(t))
  end

  return 0
end
