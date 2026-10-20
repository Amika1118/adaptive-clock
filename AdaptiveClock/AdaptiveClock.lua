-- AdaptiveClock.lua  v3.3.1   (Rainmeter 4.x, Lua 5.1)
-- Author: Amika Alankara  (MIT License)
--
-- One file, several small jobs. Each Script measure in the .ini picks its job with  Mode=
--   main                          accent colour, hourly style shuffle, daily quote (its value is the quote text)
--   secF minF hrF dayF            numbers 0..1 that drive the rings, arcs and hands
--   worldName worldDay worldTime  multi-line text for the "World Time" style
--   wordsA wordsB                 text for the "Words" style ("quarter past" / "three")

local mode = 'main'
local N = 24                       -- number of styles (the .ini sets StyleCount)
local current, lastSlot, lastYday, lastAccent
local pool = {}                   -- style numbers that take part in the shuffle (SkipStyles removes some)
local interval = 60               -- minutes per style (ShuffleMinutes)
local NAMES = { 'Chronograph', 'Grey bubbles', 'World time', 'Halo', 'Roman dial', 'Bubble rings', 'Words',
  'Digital', 'Concentric rings', 'Orbit dots', 'Classic analog', 'Progress bars', 'Sun path', 'Stacked digits',
  'Date card', 'Line tracks', 'Dash ring', 'Gauges', 'Neon', '24-hour dial', 'Split', 'Analog + digital',
  'Phrase', 'Pulse' }
local locked = false              -- true = keep the current style (no hourly change)

local D  = '\226\128\148'          -- em dash   (UTF-8 written as escapes so the file encoding never matters)
local LQ = '\226\128\156'          -- left curly quote
local RQ = '\226\128\157'          -- right curly quote

local function Q(text, who) return LQ .. text .. RQ .. ' ' .. D .. ' ' .. who end

local QUOTES = {
  Q('The best way out is always through.', 'Robert Frost'),
  Q('We suffer more often in imagination than in reality.', 'Seneca'),
  Q('A journey of a thousand miles begins with a single step.', 'Lao Tzu'),
  Q('The unexamined life is not worth living.', 'Socrates'),
  Q('Fortune favors the bold.', 'Virgil'),
  Q('The only thing we have to fear is fear itself.', 'Franklin D. Roosevelt'),
  Q('I think, therefore I am.', 'Rene Descartes'),
  Q('Stay hungry, stay foolish.', 'Steve Jobs'),
  Q('Genius is one percent inspiration and ninety-nine percent perspiration.', 'Thomas Edison'),
  Q('Imagination is more important than knowledge.', 'Albert Einstein'),
  Q('Do what you can, with what you have, where you are.', 'Theodore Roosevelt'),
  Q('The only way to do great work is to love what you do.', 'Steve Jobs'),
  Q('It does not matter how slowly you go as long as you do not stop.', 'Confucius'),
  Q('Waste no more time arguing what a good man should be. Be one.', 'Marcus Aurelius'),
  Q('Fall seven times, stand up eight.', 'Japanese proverb'),
  Q('Energy and persistence conquer all things.', 'Benjamin Franklin'),
  Q('Lost time is never found again.', 'Benjamin Franklin'),
  Q('Time is what we want most, but what we use worst.', 'William Penn'),
  Q('Well done is better than well said.', 'Benjamin Franklin'),
  Q('We are what we repeatedly do. Excellence, then, is not an act, but a habit.', 'Will Durant'),
  Q('Make each day your masterpiece.', 'John Wooden'),
  Q('Failure is simply the opportunity to begin again, this time more intelligently.', 'Henry Ford'),
  Q('Premature optimization is the root of all evil.', 'Donald Knuth'),
  Q('Talk is cheap. Show me the code.', 'Linus Torvalds'),
  Q('Programs must be written for people to read, and only incidentally for machines to execute.', 'Harold Abelson'),
  Q('Simplicity is prerequisite for reliability.', 'Edsger Dijkstra'),
  Q('The best way to predict the future is to invent it.', 'Alan Kay'),
  Q('Any sufficiently advanced technology is indistinguishable from magic.', 'Arthur C. Clarke'),
  Q('We can only see a short distance ahead, but we can see plenty there that needs to be done.', 'Alan Turing'),
  Q('All models are wrong, but some are useful.', 'George Box'),
  Q('Make it work, make it right, make it fast.', 'Kent Beck'),
  Q('Strive not to be a success, but rather to be of value.', 'Albert Einstein'),
  Q('Life is like riding a bicycle. To keep your balance, you must keep moving.', 'Albert Einstein'),
  Q('Nothing in life is to be feared, it is only to be understood.', 'Marie Curie'),
  Q('Slow and steady wins the race.', 'Aesop'),
  Q('A year from now you may wish you had started today.', 'Karen Lamb'),
  Q('Light tomorrow with today.', 'Elizabeth Barrett Browning'),
  Q('Hope is being able to see that there is light despite all of the darkness.', 'Desmond Tutu'),
  Q('Small deeds done are better than great deeds planned.', 'Peter Marshall'),
  Q("Don't count the days, make the days count.", 'Muhammad Ali'),
  Q('The best time to plant a tree was twenty years ago. The second best time is now.', 'Proverb'),
  Q('A smooth sea never made a skilled sailor.', 'Proverb'),
  Q('Courage is grace under pressure.', 'Ernest Hemingway'),
  Q('Machines take me by surprise with great frequency.', 'Alan Turing'),
  Q('Dwell on the beauty of life.', 'Marcus Aurelius'),
  Q('An investment in knowledge pays the best interest.', 'Benjamin Franklin'),
  Q('Well begun is half done.', 'Proverb'),
  Q('Know thyself.', 'Delphic maxim'),
  Q('Not all those who wander are lost.', 'J.R.R. Tolkien'),
  Q('Learn from yesterday, live for today, hope for tomorrow.', 'Albert Einstein'),
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

-- ---------------------------------------------------------------- colours (black/white ink from the wallpaper, or Windows accent)

local lastKey

local lastLuma, wasBright

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

  -- "ink": black on a bright wallpaper, white on a dark one (like the mouse cursor that inverts)
  local luma   = wallpaperLuma()
  local cm     = SKIN:GetVariable('ColorMode', 'Invert')       -- Invert | Accent | White | Black
  local bright = wasBright or false             -- small hysteresis so a mid-grey wallpaper does not flicker
  if luma then
    if bright then bright = luma > 0.48 else bright = luma > 0.55 end
  end
  wasBright = bright
  if cm == 'White' then bright = false elseif cm == 'Black' then bright = true end

  local key = v .. '|' .. tostring(bright) .. '|' .. cm
  if key == lastKey then return end
  lastKey = key

  local ink = bright and '0,0,0' or '255,255,255'
  setv('Ink',     ink)
  setv('InkDim',  ink .. ',190')
  setv('InkMid',  ink .. ',120')
  setv('InkSoft', ink .. ',60')

  local rgb = ink                               -- Invert / White / Black: accent colour = ink
  if cm == 'Accent' then                        -- Windows accent colour (ABGR DWORD)
    local r, g, b = 255, 255, 255
    if v > 0 then
      r = v % 256
      g = math.floor(v / 256) % 256
      b = math.floor(v / 65536) % 256
    end
    rgb = string.format('%d,%d,%d', r, g, b)
  end
  setv('Color',     rgb)
  setv('ColorDim',  rgb .. ',190')
  setv('ColorMid',  rgb .. ',120')
  setv('ColorSoft', rgb .. ',60')
end

-- ---------------------------------------------------------------- angles for the dash / marker meters

local function angles(t)
  local sec = t.sec
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

-- ---------------------------------------------------------------- hourly style shuffle
-- Every day the N styles are shuffled once; hour 0 uses the 1st, hour 1 the 2nd ... so all 24 styles
-- appear exactly once per day, in a random order that is the same all day long (a skin refresh will not
-- change the current style), and the last style of yesterday never repeats as the first of today.

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

local function showStyle(n)
  if n == current then return end
  local qh = tonumber(SKIN:GetVariable('QuoteHidden', '0')) or 0
  if current then
    setv('H' .. current, 1)
    setv('Q' .. current, 1)
  end
  setv('H' .. n, 0)
  setv('StyleNo', n)
  setv('StyleName', NAMES[n] or ('Style ' .. n))
  setv('Q' .. n, qh)
  current = n
end

-- Called from the right-click menu of the skin
local function saveVar(name, value)
  local path = SKIN:GetVariable('CURRENTPATH', '') .. SKIN:GetVariable('CURRENTFILE', '')
  SKIN:Bang('!WriteKeyValue', 'Variables', name, tostring(value), path)
end

local function cycleVar(name, list, default)
  local cur, idx = SKIN:GetVariable(name, default), 0
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

function ToggleHourFormat() cycleVar('HourFormat', { '%H', '%I' }, '%H') end
function ToggleQuote()      cycleVar('QuoteHidden', { 0, 1 }, '0') end
function ToggleQuoteRate()  cycleVar('QuoteEveryHour', { 0, 1 }, '0') end
function CycleColors()      cycleVar('ColorMode', { 'Invert', 'Accent', 'White', 'Black' }, 'Invert') end
function CycleShuffle()     cycleVar('ShuffleMinutes', { 60, 30, 15, 5, 1440 }, '60') end

function SkipThisStyle()
  if #pool <= 1 or not current then return end
  local list = (SKIN:GetVariable('SkipStyles', '') ~= '' and (SKIN:GetVariable('SkipStyles', '') .. ',') or '') .. current
  saveVar('SkipStyles', list)
  SKIN:Bang('!Refresh')
end

function ShowAllStyles()
  saveVar('SkipStyles', '')
  SKIN:Bang('!Refresh')
end

function ToggleLock()
  if locked then Unlock() else Lock() end
end

function Lock()
  locked = true
  setv('LockMark', ' [locked]')
  refresh()
end

function Unlock()
  locked = false
  setv('LockMark', '')
  showStyle(styleFor(os.date('*t')))
  refresh()
end

function Resume()
  locked = false
  setv('LockMark', '')
  showStyle(styleFor(os.date('*t')))
  refresh()
end

-- Optional quotes.txt next to the skin: one quote per line, "text | author". Lines starting with # are ignored.
local function loadQuotes()
  local f = io.open(SKIN:GetVariable('CURRENTPATH', '') .. 'quotes.txt', 'r')
  if not f then return end
  local list = {}
  for raw in f:lines() do
    local line = raw:gsub('^\239\187\191', ''):gsub('\r', ''):match('^%s*(.-)%s*$')
    if line ~= '' and line:sub(1, 1) ~= '#' then
      local text, who = line:match('^(.-)%s*|%s*(.+)$')
      if text and text ~= '' then list[#list + 1] = Q(text, who)
      else list[#list + 1] = LQ .. line .. RQ end
    end
  end
  f:close()
  if #list > 0 then QUOTES = list end
end

-- ---------------------------------------------------------------- quote of the day

local function quoteText(t)
  local idx = t.year * 366 + t.yday
  if SKIN:GetVariable('QuoteEveryHour', '0') == '1' then idx = idx * 24 + t.hour end
  return QUOTES[idx % #QUOTES + 1]
end

-- ---------------------------------------------------------------- world time (with daylight saving rules)

local DIM = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 }

local function daysInMonth(y, m)
  if m == 2 and ((y % 4 == 0 and y % 100 ~= 0) or y % 400 == 0) then return 29 end
  return DIM[m]
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
-- Edit this list to change the cities (keep it to 5 rows so it fits the style).
local CITIES = {
  { 'NEW YORK', -5, 'US' },
  { 'LONDON',    0, 'EU' },
  { 'DUBAI',     4, nil  },
  { 'TOKYO',     9, nil  },
  { 'SYDNEY',   10, 'AU' },
}

-- Optional  Cities=  variable in the .ini:  NAME:offset:RULE|NAME:offset:RULE ...   (RULE = US, EU, AU or -)
local function loadCities()
  local v = SKIN:GetVariable('Cities', '')
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
  local h12 = (SKIN:GetVariable('HourFormat', '%H') == '%I')
  local out = {}
  for i, c in ipairs(CITIES) do
    local lt = cityTime(c, utc)
    if kind == 'name' then
      out[i] = c[1]
    elseif kind == 'day' then
      out[i] = string.upper(os.date('!%a', lt))
    else
      out[i] = os.date(h12 and '!%I:%M %p' or '!%H:%M', lt)
    end
  end
  return table.concat(out, '\n')
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

-- ---------------------------------------------------------------- measure entry points

local MODES = {
  secF  = function() local t = os.date('*t'); return t.sec / 60 end,
  minF  = function() local t = os.date('*t'); return (t.min * 60 + t.sec) / 3600 end,
  hrF   = function() local t = os.date('*t'); return ((t.hour % 12) * 3600 + t.min * 60 + t.sec) / 43200 end,
  dayF  = function() local t = os.date('*t'); return (t.hour * 3600 + t.min * 60 + t.sec) / 86400 end,
  worldName = function() return world('name') end,
  worldDay  = function() return world('day') end,
  worldTime = function() return world('time') end,
  wordsA = function() local a = words(); return a end,
  wordsB = function() local _, b = words(); return b end,
}

function Initialize()
  mode = SELF:GetOption('Mode', 'main')
  N = tonumber(SKIN:GetVariable('StyleCount', '24')) or 24
  interval = math.max(1, math.min(1440, tonumber(SKIN:GetVariable('ShuffleMinutes', '60')) or 60))
  local skip = {}
  for n in (SKIN:GetVariable('SkipStyles', '')):gmatch('%d+') do skip[tonumber(n)] = true end
  pool = {}
  for i = 1, N do if not skip[i] then pool[#pool + 1] = i end end
  if #pool == 0 then for i = 1, N do pool[i] = i end end
  loadQuotes()
  loadCities()
end

function Update()
  if mode ~= 'main' then
    local f = MODES[mode]
    if f then return f() end
    return 0
  end

  local t = os.date('*t')
  accent()
  angles(t)
  if current == nil or (not locked and (slot(t) ~= lastSlot or t.yday ~= lastYday)) then
    lastSlot, lastYday = slot(t), t.yday
    showStyle(styleFor(t))
  end
  return quoteText(t)
end
