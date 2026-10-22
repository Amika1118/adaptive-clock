# Changelog

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
