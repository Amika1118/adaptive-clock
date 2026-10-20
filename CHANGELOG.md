# Changelog

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
