-- Settings.lua  -  highlights the active choices in the Settings window and finds the main skin
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
