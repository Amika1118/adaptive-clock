-- AdaptiveClockU.lua  -  loader for the measures that return symbols or non-English text
-- Author: Amika Alankara  (MIT License)
--
-- SAVE THIS FILE AS "UTF-8 WITH BOM". Rainmeter then reads every string this script returns as Unicode (UTF-8).
-- All the real code is in AdaptiveClock.lua (plain ASCII, no BOM); this file only runs it inside its own Rainmeter script.
-- If a BOM file ever failed to load on a machine, only the symbols / translated text would be missing, never the clock itself.
function Initialize()
  local path = SKIN:GetVariable('CURRENTPATH', '') .. 'AdaptiveClock.lua'
  local chunk, err = loadfile(path)
  if not chunk then
    SKIN:Bang('!Log', 'AdaptiveClockU: cannot load ' .. path .. ' : ' .. tostring(err), 'Error')
    return
  end
  setfenv(chunk, getfenv(1))        -- run it in this script's own environment: Initialize, Update and the menu functions land here
  chunk()
  Initialize()                      -- now the real Initialize
end

function Update() return 0 end      -- replaced by the real Update once the chunk has run
