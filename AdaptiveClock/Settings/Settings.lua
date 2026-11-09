-- Settings.lua  -  logic of the Settings window and the style gallery
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
