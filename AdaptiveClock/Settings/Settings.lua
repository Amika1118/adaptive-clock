-- Settings.lua  -  logic of the Settings window and the style gallery
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
