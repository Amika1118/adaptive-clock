# Changelog

## 4.9
- **The clock remembers where you were.** The style on screen, and whether you picked it yourself (Next, Random, gallery) or the schedule did, are saved in
  `state.txt` (not committed to git). After an accidental close, a Rainmeter restart, or a refresh caused by changing a setting, the clock comes back on the same style.
  A style you chose yourself stays until the next scheduled change; a scheduled style comes back if you return within the same slot, otherwise the schedule
  moves on. A locked style is still kept. Styles that the current profile or theme no longer allows are skipped.
- *Settings > Style > On start* (`ResumeLast`): resume the last clock, or follow the schedule.

## 4.8
- **Quotes are visible again, in every language.** In 4.6 / 4.7 the quote text depended on a Lua file saved with a BOM, which Rainmeter did not run on
  every PC, so the quote card stayed empty. Nothing in the clock needs a BOM any more: `AdaptiveClock.lua` is plain ASCII, quotes use plain punctuation,
  and `AdaptiveClockU.lua` is gone.
- **Languages work without Unicode in Lua.** The translations are variables in `Languages\<Name>.inc` (UTF-16 files, read natively by Rainmeter); the script
  only picks which variable to show. Day and month names, greetings, labels, calendar headers, timer, alarm and battery text all follow the language.
- **Symbols are drawn as shapes**, so no font or encoding can break them: the sun / moon in Greeting and Tiles, the weather icon, and the eight moon phases
  in Moon phase and Sun and moon. The temperature is shown as `23 C`.
- `tools/check_ini.py` now also checks that every language file is UTF-16, defines every variable the skin uses, and that no Lua file has a BOM.

## 4.6
- **Fixed garbled symbols** (moon icon, weather cloud, quote marks, other languages): `AdaptiveClock.lua` and `Languages.lua` are now saved
  as UTF-8 with BOM, which is what Rainmeter needs to read Lua text as Unicode. `tools/check_ini.py` checks this.
- **Fixed scattered shapes** in Daisy Chain, Flutter, Ribbon and Orbit: Rainmeter measures a shape's `Rotate` origin from the shape itself, so the
  clocks now rotate around the shape's centre.
- **Location from Windows, kept on the PC**: sunrise, sunset and the sun position use the Windows location (time-zone estimate as a fallback) read by
  `LocationFinder.ps1`; manual `Latitude` / `Longitude` still override. Weather stays off by default; when on, only a position rounded to 0.1 degree
  is sent to open-meteo.com, and `WeatherLatitude` / `WeatherLongitude` can point it somewhere else.
- 7 new clocks (106 in total): Big quote, Weekend, Year grid, Sun and moon, Birthday, Sparkle Pop (Bloom), Pulse Line (Volt).
- Settings has a **Start** page (profile, theme, Surprise me, gallery, tips), a location status line and *Find my location again* under Extras,
  a privacy note, and *Reset all settings* under Actions.
- Weather message no longer gets cut off.

## 4.5
- Themes renamed: *Girl* is now **Bloom** and *Boy* is now **Volt** (Neutral shows as *Classic* in Settings). Existing `Theme=Girl` / `Theme=Boy`
  settings keep working.
- The 20 themed clocks have new names: Blossom, Heartbeat, Pastel Bars, Stardust, Flutter, Cloud Nine, Daisy Chain, Ribbon, Spectrum, Lunar Glow
  (Bloom) and Radar Sweep, Orbit, Redline, Match Day, Launch, Kickoff, Neon Drive, Level Up, Grid Start, Crest (Volt).
- README: the screenshots section was taken out again.

## 4.4
- **Coding clocks rebuilt as IDE scenes** (19 languages): tabs with language badges, syntax-coloured code with the time inside it,
  a debugger line and breakpoint that step through the code every second, minimap, a console that runs the program and prints the
  time, and a status bar with `Ln` / `Col`.
- 8 new coder clocks: Dot matrix, Matrix rain, CI pipeline, Stack trace, Hexdump, Neofetch, htop, Test runner (99 styles in total).
  Code editor is now Live preview (code on the left, a browser preview on the right); Terminal and Git log are larger and livelier.
- **Layout fixes** found with the new preview tool: text that collided or ran past its card or panel in Date card, Stacked digits,
  Digital, Epoch, Greeting, Sticky note, Split, World time, 24-hour dial, Speedometer, Scoreboard, Flip clock, Tiles, Aurora,
  Weather, Battery, Timer, Rainbow, Synthwave (lines left the panel), Skyline (half ring leaked into the quote) and Race lights.
- `tools/preview.py`: renders every style from the generated `.ini` and warns about overlaps; contact sheets are in `docs/`.

## 4.3
- The Now Playing widget and its settings were removed.
- The pop-up tooltip over the clock is gone (double-click for the next style still works).
- **39 new clocks (91 in total)**: 19 code-editor clocks, one per programming language; 6 girl clocks (Butterfly, Cloud, Daisy,
  Bow, Rainbow, Moonlight); 6 boy clocks (Rocket, Pitch, Synthwave, Game HUD, Race lights, Shield); 8 for everyone (Nixie, Vinyl,
  Compass, Waves, Zen circle, Day bar, Moon phase, Skyline).
- **Code colours** setting (Dark, Dracula, Monokai, Light) for all editor, terminal and git-log clocks.
- **Settings window redesigned**: five pages with a tab bar and a `Settings > page` breadcrumb, the current value written next to every
  setting, the active choice highlighted, and the clock style currently on screen shown at the top.
- The style gallery highlights the style that is on screen.

## 4.1
- **Language** setting (Windows, English, Spanish, French, German, Portuguese, Italian, Sinhala, Tamil, Hindi, Japanese):
  date names, greeting, calendar headers and labels. The word-clock styles only appear for English / Windows.
- **Settings window** and **style gallery** (new skins) so the right-click menu is short; "Language: next" in the menu.
- New styles: Weather (optional, off by default), Sun times, Now playing, Battery, Timer and alarm. 53 styles in total.
- Smooth seconds option, longer update dividers for slow-changing text (lower CPU use).
- One-click `.rmskin` builder, CI that checks the generated files, release workflow.

## 4.0
- 24 new styles (48 total): Terminal, Code editor, Hex clock, Binary dots, System monitor, Epoch and ISO, Git log (coder);
  Greeting, Month calendar, Year progress, Sticky note, Week strip (everyday); Petals, Heart, Pastel pills, Starlight (girl);
  Radar, Planet orbit, Speedometer, Scoreboard (boy); Flip clock, Minimal analog, Tiles, Aurora (everyone).
- Profiles (All / Coder / Everyday) and themes (Neutral / Girl / Boy), both in the right-click menu.
- New quote card: serif quote mark, italic text and accent author, or a terminal comment with a blinking cursor.
  More quotes (coder and everyday sets), "Next quote", and quote speed (daily / hourly / 30 / 10 min).
- Fixes: 12-hour clock no longer shows a leading zero and shows AM/PM; a locked style survives a refresh;
  one shared quote block instead of one per style; quote text wraps and clips cleanly.

## 3.3.1
- Ink now follows wallpaper changes from Windows Personalization quickly: the wallpaper setting is watched, the
  brightness is re-checked every 30 s (cached, so it is cheap) and a changed wallpaper file or slideshow image is noticed.
- Solid-colour desktops are supported.
- Small hysteresis and "keep last reading" so the ink does not flicker.

## 3.3
- Black/white ink now samples only the wallpaper area behind the skin (falls back to the whole wallpaper).
- Fonts are variables (`FontText`, `FontLight`, `FontBold`) and the quote size is `QuoteSize`.
- GitHub bug-report template.

## 3.2
- Right-click menu reorganised into toggles and "next mode" cycles (12/24 h, quote, colours, shuffle speed, lock).
- New colour modes: always white, always black (plus invert and accent).
- Shuffle speed: 60 / 30 / 15 / 5 minutes or daily (`ShuffleMinutes`).
- Skip styles you don't like (`SkipStyles`, or "Skip this style in future"); "Show all styles again" resets it.
- Tooltip shows the style name and a `[locked]` marker.

## 3.1
- Double-click the skin for the next style; hover shows "Style N of 24".
- Right-click: Lock this style / Unlock style (stops the hourly change until unlocked or refreshed).
- Cities are set with the `Cities=` variable in the `.ini`, so no Lua editing is needed.
- Optional `quotes.txt` replaces the built-in quotes (see `quotes.example.txt`).

## 3.0
- 24 styles with hourly shuffle, wallpaper-based black/white ink or Windows accent, daily quote.
