# Adaptive Clock - Complete Help & User Guide

Welcome to **Adaptive Clock for Rainmeter!**

This guide explains how to install Rainmeter, install Adaptive Clock, explore its 130 clock styles, customise its appearance, configure additional features and troubleshoot common problems.

No previous Rainmeter experience is required.

---

# Table of Contents

1. [What is Adaptive Clock?](#1-what-is-adaptive-clock)
2. [What is Rainmeter?](#2-what-is-rainmeter)
3. [Installing Rainmeter](#3-installing-rainmeter)
4. [Downloading Adaptive Clock](#4-downloading-adaptive-clock)
5. [Installing Adaptive Clock](#5-installing-adaptive-clock)
6. [Loading Your First Clock](#6-loading-your-first-clock)
7. [Understanding the Clock Controls](#7-understanding-the-clock-controls)
8. [Exploring the 130 Styles](#8-exploring-the-130-styles)
9. [Profiles and Themes](#9-profiles-and-themes)
10. [Using the Settings Window](#10-using-the-settings-window)
11. [Changing Languages](#11-changing-languages)
12. [Customising Colours and Fonts](#12-customising-colours-and-fonts)
13. [Using Quotes](#13-using-quotes)
14. [Weather Configuration](#14-weather-configuration)
15. [Sunrise, Sunset and Location](#15-sunrise-sunset-and-location)
16. [Focus Timer and Alarm](#16-focus-timer-and-alarm)
17. [Battery and Other Extras](#17-battery-and-other-extras)
18. [World-Time Cities](#18-world-time-cities)
19. [Customising Configuration Variables](#19-customising-configuration-variables)
20. [Updating Adaptive Clock](#20-updating-adaptive-clock)
21. [Uninstalling Adaptive Clock](#21-uninstalling-adaptive-clock)
22. [Troubleshooting](#22-troubleshooting)
23. [Privacy and Location](#23-privacy-and-location)
24. [Frequently Asked Questions](#24-frequently-asked-questions)
25. [Support and Feedback](#25-support-and-feedback)

---

# 1. What is Adaptive Clock?

Adaptive Clock is a custom desktop clock developed for Rainmeter on Windows.

Instead of displaying just one traditional clock, it offers **130 different clock styles** that can be changed manually or automatically.

It includes:

- Programming-inspired IDE clocks.
- Minimal everyday clocks.
- Colourful Bloom and Volt themes.
- Animated and decorative clocks.
- Calendar and countdown displays.
- Weather and astronomical information.
- Customisable quotes.
- A focus timer and alarm.
- Multiple languages.

The clock can adapt its text colour to your desktop wallpaper and can use your Windows accent colour.

**You can use it as a simple desktop clock or customise it into a complete desktop experience.**

---

# 2. What is Rainmeter?

[Rainmeter](https://www.rainmeter.net/) is a free desktop customisation application for Windows.

It allows users to add widgets called **skins** to their desktop.

Examples include:

- Clocks.
- Weather displays.
- System monitors.
- Music players.
- Calendars.
- Desktop information panels.

Adaptive Clock is one such Rainmeter skin.

You need Rainmeter installed before you can use Adaptive Clock.

---

# 3. Installing Rainmeter

<details>
<summary>Step 1 - Visit the official Rainmeter website</summary>

Open your browser and visit:

https://www.rainmeter.net/

Make sure you are downloading Rainmeter from the official website.

</details>

<details>
<summary>Step 2 - Download Rainmeter</summary>

1. Find the Downloads section.
2. Download the latest stable Windows installer.
3. Wait for the download to finish.

**Recommended:** Use the standard installer rather than the portable installation.

</details>

<details>
<summary>Step 3 - Run the installer</summary>

1. Open your Downloads folder.
2. Double-click the downloaded Rainmeter installer.
3. If Windows asks for permission, review the publisher information and confirm that you downloaded it from the official source.
4. Select your preferred installation language.

</details>

<details>
<summary>Step 4 - Choose the installation type</summary>

Rainmeter offers two installation types:

**Standard Installation (Recommended)**

- Installs Rainmeter normally on Windows.
- Creates Start menu shortcuts.
- Registers `.rmskin` files.
- Allows Rainmeter to start automatically with Windows if enabled.

**Portable Installation**

- Keeps Rainmeter and its files together in one folder.
- Useful for advanced users or removable drives.
- Does not use the normal Windows installation integration.

For most users, choose **Standard Installation**.

</details>

<details>
<summary>Step 5 - Complete installation</summary>

1. Follow the installer instructions.
2. Choose whether Rainmeter should start with Windows.
3. Finish the installation.
4. Allow Rainmeter to launch.

Rainmeter may display its default sample skins on your desktop.

Congratulations! Rainmeter is now installed.

</details>

**Official installation resources:**

- [Download Rainmeter](https://www.rainmeter.net/)
- [Official Rainmeter Installation Guide](https://docs.rainmeter.net/manual/installing-rainmeter/)
- [Rainmeter Getting Started](https://docs.rainmeter.net/manual/getting-started/setting-up/)

---

# 4. Downloading Adaptive Clock

You can obtain Adaptive Clock in two ways.

### Option A - Download the ready-to-install package

This is the recommended method.

1. Visit the project's GitHub Releases page.
2. Open the latest release.
3. Locate the file named:

   `AdaptiveClock-<version>.rmskin`

4. Download the file.

The `.rmskin` package contains the files required to install the clock.

### Option B - Download the source code

If you prefer installing manually:

1. Open the GitHub repository.
2. Select **Code**.
3. Select **Download ZIP**.
4. Extract the downloaded ZIP file.
5. Locate the `AdaptiveClock` folder.

You should now have the project files on your computer.

---

# 5. Installing Adaptive Clock

There are two installation methods.

## Method A - Using the RMSKIN installer (Recommended)

This is the easiest method.

1. Locate the downloaded `AdaptiveClock-<version>.rmskin` file.
2. Double-click it.
3. Rainmeter's Skin Installer will appear.
4. Review the installation options.
5. Click **Install**.
6. Wait for the installation to complete.

Rainmeter will install the skin into its Skins directory.

The usual installation location is:

`Documents\Rainmeter\Skins\AdaptiveClock`

You can now load the clock.

## Method B - Installing manually

Use this method if you downloaded the source ZIP.

1. Extract the ZIP file.
2. Open the extracted project folder.
3. Find the folder named `AdaptiveClock`.
4. Copy the entire folder.
5. Navigate to:

   `Documents\Rainmeter\Skins\`

6. Paste the `AdaptiveClock` folder inside `Skins`.

Your directory should look similar to this:

```text
Documents
└── Rainmeter
    └── Skins
        └── AdaptiveClock
            ├── AdaptiveClock.ini
            ├── AdaptiveClock.lua
            ├── Settings
            │   └── Settings.ini
            ├── Gallery
            │   └── Gallery.ini
            ├── Languages
            ├── State
            ├── LocationFinder.ps1
            └── WallpaperLuma.ps1
```

Some supporting files and directories may differ between releases. Keep the complete distributed folder intact.

### Important

Do not copy only `AdaptiveClock.ini`.

The Lua script, language files and supporting scripts are required for the skin to work correctly.

---

# 6. Loading Your First Clock

Once Adaptive Clock is installed:

1. Find the Rainmeter icon in the Windows system tray.
2. Right-click the Rainmeter icon.
3. Select **Manage**.
4. Navigate to the Skins tab.
5. Find `AdaptiveClock`.
6. Expand the folder.
7. Select `AdaptiveClock.ini`.
8. Click **Load**.

Your Adaptive Clock should now appear on the desktop.

You can close the Rainmeter Manage window without closing the clock.

### Loading Settings

To open the settings interface:

1. Right-click the clock.
2. Find the Settings option.
3. Open the settings window.

Alternatively, from Rainmeter Manage, navigate to:

`AdaptiveClock > Settings > Settings.ini`

Select the file and click **Load**.

### Opening the Style Gallery

The gallery can be opened through the clock's right-click menu.

Alternatively, load:

`AdaptiveClock > Gallery > Gallery.ini`

The gallery lets you search by style name or number, filter by collection, sort by recent use or name, and select a style. Selecting a style displays it immediately and locks it until you resume shuffle.

---

# 7. Understanding the Clock Controls

Adaptive Clock includes mouse controls and a right-click menu.

## Mouse Controls

| Action | Result |
|---|---|
| Double-click | Switch to the next clock style |
| Hover | Display style name and number |
| Right-click | Open the context menu |

The hover information also indicates whether the current style is locked.

The clock remembers its selected style after a Rainmeter restart or skin refresh. A manually selected style stays until the next scheduled change; an automatically selected style resumes only if you return during the same shuffle interval. The saved interval includes the year, so a date from a previous year cannot be mistaken for today's interval.

## Right-Click Menu

The right-click menu provides access to the following features.

| Option | Description |
|---|---|
| Next Style | Move to the next clock |
| Random Style | Select a random clock |
| Lock / Unlock | Keep the current style on screen |
| Resume Shuffle | Resume automatic style rotation |
| Re-check Wallpaper | Recalculate wallpaper brightness |
| Profile | Select the style collection |
| Theme | Change the visual theme |
| Language | Change the display language |
| Colour Mode | Change text colour behaviour |
| Next Quote | Display another quote |
| Show / Hide Quote | Toggle the quote display |
| 12 / 24 Hour | Change time format |
| Skip This Style | Exclude the current style |
| Show All Styles | Restore previously skipped styles |
| Settings | Open the configuration interface |
| Style Gallery | Open the style gallery |

### Locking a Clock

If you find a clock you like:

1. Right-click it.
2. Select **Lock**.
3. The current style will remain selected.

To resume automatic rotation, select **Resume Shuffle**.

### Skipping a Clock

If you do not like a particular style:

1. Right-click the clock.
2. Select **Skip This Style**.

To restore all excluded styles, select **Show All Styles Again**.

---

# 8. Exploring the 130 Styles

Adaptive Clock contains a collection of 130 styles.

The styles include several categories.

## Coder Collection

The Coder collection includes 19 programming-language scenes.

| Language | Clock Scene |
|---|---|
| Python | Python IDE |
| JavaScript | JavaScript IDE |
| TypeScript | TypeScript IDE |
| Java | Java IDE |
| C | C IDE |
| C++ | C++ IDE |
| C# | C# IDE |
| Go | Go IDE |
| Rust | Rust IDE |
| PHP | PHP IDE |
| Ruby | Ruby IDE |
| Swift | Swift IDE |
| Kotlin | Kotlin IDE |
| SQL | SQL IDE |
| HTML | HTML IDE |
| Bash | Bash IDE |
| PowerShell | PowerShell IDE |
| Lua | Lua IDE |
| Dart | Dart IDE |

Each IDE scene includes editor-inspired elements, syntax colours, a live debugger indicator, status information and a simulated console.

### Additional Coder Styles

- Terminal
- Live Preview
- Hex Clock
- Binary Dots
- System Monitor
- Epoch and ISO
- Git Log
- Dot Matrix
- Matrix Rain
- CI Pipeline
- Stack Trace
- Hexdump
- Neofetch
- htop
- Test Runner

## Everyday Collection

Designed for simple daily desktop use.

- Greeting
- Month Calendar
- Year Progress
- Sticky Note
- Week Strip

## General Collection

Other visual styles include:

- Chronograph
- Flip Clock
- Nixie
- Vinyl
- Compass
- Moon Phase
- Skyline
- Aurora

## Friendly Collection

- Big Quote
- Weekend Countdown
- Year Grid
- Sun and Moon
- Birthday Countdown
- Sparkle Pop
- Pulse Line

Additional styles are available through the Classic, Bloom and Volt themes.

### Browsing Styles

Open the Style Gallery from the right-click menu.

The gallery shows 25 styles per page, with Previous and Next controls. Search by style name or number, filter by collection,
sort by recently used or name, and use Clear to reset the search. The selected style is highlighted; clicking a style displays
it and locks it until you resume shuffle.

---

# 9. Profiles and Themes

Adaptive Clock has three profiles and three visual themes.

## Profiles

| Profile | Description |
|---|---|
| All | Includes the complete collection |
| Coder | Focuses on programming and developer-inspired styles |
| Everyday | Focuses on everyday clocks and displays |

To change the profile:

1. Right-click the clock.
2. Open **Profile**.
3. Select your preferred profile.

## Themes

### Classic

A neutral and versatile appearance.

It uses the default accent palette and includes the original collection of styles.

### Bloom

A pink and lilac-inspired theme.

Some of its styles include:

- Blossom
- Heartbeat
- Flutter
- Ribbon
- Spectrum
- Lunar Glow

### Volt

An electric blue and cyan-inspired theme.

Some of its styles include:

- Radar Sweep
- Launch
- Kickoff
- Neon Drive
- Level Up
- Grid Start
- Crest

### Changing Themes

1. Right-click the clock.
2. Open **Theme**.
3. Select Classic, Bloom or Volt.

Bloom and Volt introduce their own styles and accent colours.

**Note:** The older theme values `Girl` and `Boy` are still supported for compatibility.

---

# 10. Using the Settings Window

Adaptive Clock includes a seven-page Settings interface.

Open it from the clock's right-click menu.

## Page 1 - Start

Choose a profile and theme, then use Surprise me, Next style or open the gallery.

## Page 2 - Appearance

Choose whether appearance changes apply to the current clock style or all styles.
Choose adaptive, Windows accent, white, black or custom colour. Custom colour uses
three RGB values from 0 to 255 (for example `120,140,255`). Font and code-editor
colours are available on the same page.

The page also controls automatic style rotation and whether the last clock is restored on startup.

### Shuffle Duration

The shuffle duration determines how long a style remains active before another style is selected.
The supported range is 1–1440 minutes.

If you prefer a permanent clock, lock the current style instead.

## Page 3 - Language

Configure:

- Display language.
- 12-hour or 24-hour format.
- First day of the week.

## Page 4 - Quotes

Configure the quote display.

Available options include:

- Show or hide quotes.
- Quote presentation style.
- Quote text size.
- Quote rotation behaviour.

## Page 5 - Extras

Configure additional features.

These include:

- Smooth seconds.
- Weather.
- Focus timer.

## Page 6 - Personal

Set or update your greeting name, birthday, city and optional location coordinates.
Click a field to edit it; clear the value and save to remove it. These values stay on this PC.

## Page 7 - Actions

Quick access to:

- Next style.
- Random style.
- Lock or unlock.
- Skip style.
- Open the style gallery.

### Understanding the Settings Interface

The Settings window displays:

- The current page.
- The clock style currently displayed.
- The active choice for each setting.

Selected options are highlighted, and their names are displayed next to the relevant settings.

---

# 11. Changing Languages

Adaptive Clock supports 11 language options.

1. Open Settings.
2. Navigate to Language.
3. Select your preferred language.

Available options:

| Language | Option |
|---|---|
| System language | Windows |
| English | English |
| Spanish | Spanish |
| French | French |
| German | German |
| Portuguese | Portuguese |
| Italian | Italian |
| Sinhala | Sinhala |
| Tamil | Tamil |
| Hindi | Hindi |
| Japanese | Japanese |

The selected language affects date names, greetings and labels.

### Important Notes

- Quotes remain in English.
- Weather descriptions remain in English.
- The two word-clock styles require English or Windows language mode.

If a translation does not appear, check that the appropriate `.inc` file exists inside the `Languages` directory.

---

# 12. Customising Colours and Fonts

Adaptive Clock supports adaptive text colours and multiple font settings.

## Colour Modes

| Mode | Behaviour |
|---|---|
| Invert | Chooses black or white text based on wallpaper brightness |
| Accent | Uses the Windows accent colour |
| White | Uses white text |
| Black | Uses black text |

### Adaptive Wallpaper Colours

The Invert mode checks the desktop wallpaper locally.

It determines whether black or white text is more suitable for the background.

To re-check the wallpaper:

1. Change your Windows wallpaper.
2. Right-click Adaptive Clock.
3. Select **Re-check Wallpaper**.

### Coder Editor Themes

The Coder collection supports four editor themes:

- Dark
- Dracula
- Monokai
- Light

Change the editor theme through Settings → Appearance → Code colours.

### Custom Fonts

The font variables are:

| Variable | Purpose |
|---|---|
| `FontText` | Main text |
| `FontLight` | Light-weight text |
| `FontBold` | Bold text |
| `FontMono` | Monospaced text |

Font names must correspond to fonts installed on Windows.

---

# 13. Using Quotes

Adaptive Clock includes a quote display.

You can choose between two presentation styles:

**Friendly Card**

Displays quotes in a dedicated visual card.

**Code Comment**

Displays quotes using a programming-inspired comment format, designed for the Coder profile.

### Changing Quotes

Right-click the clock and select **Next Quote**.

### Hiding Quotes

Use the **Show / Hide Quote** option in the context menu.

### Adding Your Own Quotes

Adaptive Clock supports custom quote files.

1. Locate `quotes.example.txt` in the project.
2. Rename it to `quotes.txt`.
3. Open it with Notepad.
4. Add quotes using the following format:

```text
Your first quote | Author
Your second quote | Author
Your third quote | Author
```

5. Save the file.

Your custom quote file replaces the built-in quotes across profiles.

Use plain ASCII punctuation to maintain compatibility.

---

# 14. Weather Configuration

Weather is an optional feature.

It is disabled by default.

When enabled, Adaptive Clock retrieves weather information from Open-Meteo.

### Enabling Weather

1. Open the Settings window.
2. Navigate to Extras.
3. Enable Weather.

You can also configure the weather variables directly in `AdaptiveClock.ini`.

```ini
WeatherOff=0
TempUnit=celsius
```

### Disabling Weather

Set:

```ini
WeatherOff=1
```

### Temperature Units

Supported values:

```ini
TempUnit=celsius
```

or

```ini
TempUnit=fahrenheit
```

### Using a Different Weather Location

You can configure a separate location for weather without changing the location used for sunrise and sunset.

For example:

```ini
WeatherLatitude=48.9
WeatherLongitude=2.3
```

Replace these example coordinates with your preferred location.

### Weather Update Frequency

When enabled, weather information is requested every 15 minutes.

An internet connection is required.

---

# 15. Sunrise, Sunset and Location

Adaptive Clock can calculate:

- Sunrise.
- Sunset.
- Daylight duration.
- Sun position.

These calculations are performed locally.

### Automatic Location Detection

Adaptive Clock uses `LocationFinder.ps1` to request location information from Windows.

For automatic location detection:

1. Open Windows Settings.
2. Navigate to Privacy & security.
3. Select Location.
4. Enable Location services.
5. Allow desktop apps to access your location.

Then open:

**Adaptive Clock → Settings → Extras**

Use **Find my location again** to request a fresh location.

### Manual Location Configuration

If automatic detection is unavailable, you can enter coordinates manually.

Open `AdaptiveClock.ini` and configure:

```ini
Latitude=51.5
Longitude=-0.12
```

These are example coordinates. Replace them with your intended location.

### Location Fallback

If Windows cannot provide a location, the clock estimates coordinates using the time zone and an internal lookup table.

The estimated location may not be as accurate as Windows location services.

---

# 16. Focus Timer and Alarm

Adaptive Clock includes a focus timer with an optional alarm.

It supports configurable work and break durations.

### Timer Configuration

The following variables control the timer:

```ini
PomoWork=25
PomoBreak=5
TimerBeep=1
```

| Variable | Description |
|---|---|
| `PomoWork` | Work duration in minutes |
| `PomoBreak` | Break duration in minutes |
| `TimerBeep` | Enable or disable the timer sound |

### Alarm Configuration

The alarm variables are:

```ini
AlarmTime=07:00
AlarmOn=0
```

| Variable | Description |
|---|---|
| `AlarmTime` | Alarm time in 24-hour format |
| `AlarmOn` | Enable or disable the alarm |

The timer style includes the relevant controls for operating the timer and alarm.

---

# 17. Battery and Other Extras

Adaptive Clock includes additional desktop information displays.

Depending on the selected style, these include:

- Battery information.
- System monitor.
- Weather information.
- Sunrise and sunset.
- Daylight duration.
- Moon-related information.
- Focus timer.

Not every feature appears in every clock style.

Select the relevant style through the gallery or style controls.

---

# 18. World-Time Cities

Adaptive Clock supports a maximum of five additional world-time cities.

You can configure them using the `Cities` variable in `AdaptiveClock.ini`.

### Configuration Format

```ini
Cities=NAME:offset:RULE|NAME:offset:RULE
```

Each entry contains:

- `NAME`: City label.
- `offset`: UTC offset in hours.
- `RULE`: Daylight-saving rule.

Supported rules:

| Rule | Meaning |
|---|---|
| `US` | US daylight-saving rules |
| `EU` | European daylight-saving rules |
| `AU` | Australian daylight-saving rules |
| `-` | No daylight-saving adjustment |

Maximum: 5 cities.

Follow the format carefully when editing the configuration.

---

# 19. Customising Configuration Variables

Advanced users can customise Adaptive Clock directly through its INI configuration.

Open:

`Documents\Rainmeter\Skins\AdaptiveClock\AdaptiveClock.ini`

Locate the `[Variables]` section.

You can configure:

- Profile.
- Theme.
- Language.
- Colour mode.
- Shuffle duration.
- Quote behaviour.
- Timer.
- Alarm.
- Location.
- Weather.
- Fonts.
- World-time cities.

### Important

Always keep the original variable names and expected value formats.

Incorrect configuration values may cause individual features to behave unexpectedly.

After editing the file:

1. Save your changes.
2. Open Rainmeter.
3. Right-click the skin.
4. Select Refresh skin.

If a change affects other supporting files or generated configuration, follow the relevant development instructions instead.

---

# 20. Updating Adaptive Clock

To install a newer release:

1. Visit the project's GitHub Releases page.
2. Download the latest `.rmskin` package.
3. Double-click the package.
4. Install the updated skin.
5. Refresh Rainmeter.
6. Load `AdaptiveClock.ini` if necessary.

### Updating from Source

If you installed manually:

1. Back up any custom configuration and quote files.
2. Download the latest source.
3. Replace the existing project files with the updated version.
4. Preserve any personal customisations you want to keep.
5. Refresh Rainmeter.

**Important:** Avoid keeping an old and new copy of Adaptive Clock under different folder names unless you intentionally want separate installations.

---

# 21. Uninstalling Adaptive Clock

If you want to remove Adaptive Clock without uninstalling Rainmeter:

1. Open Rainmeter Manage.
2. Locate `AdaptiveClock`.
3. Unload the active clock.
4. Unload the Settings and Gallery skins if they are running.
5. Navigate to:

   `Documents\Rainmeter\Skins\`

6. Delete the `AdaptiveClock` folder.

This removes the skin files.

If you also want to remove Rainmeter itself:

1. Open Windows Settings.
2. Navigate to Apps → Installed apps.
3. Find Rainmeter.
4. Select Uninstall.
5. Follow the Windows instructions.

Uninstalling Rainmeter is not necessary to remove Adaptive Clock.

---

# 22. Troubleshooting

This section covers common issues.

## Clock does not appear

Try the following:

1. Open Rainmeter Manage.
2. Navigate to Skins.
3. Find AdaptiveClock.
4. Select `AdaptiveClock.ini`.
5. Click Load.

If it still does not appear, select **Refresh all** from Rainmeter's tray menu.

## Clock appears blank

Check the Rainmeter log:

1. Right-click the Rainmeter tray icon.
2. Select About.
3. Open the Log tab.
4. Look for red `ERR` messages.

These messages generally identify the affected file and line number.

Check that the complete Adaptive Clock folder has been installed.

## Settings window does not open

Check that:

`AdaptiveClock\Settings\Settings.ini`

exists.

You can also load it manually through Rainmeter Manage.

## Style Gallery does not open

Check that:

`AdaptiveClock\Gallery\Gallery.ini`

exists.

Try loading it manually through Rainmeter Manage.

## Language does not change

Check the following:

- The selected language is supported.
- The relevant `.inc` file exists.
- The language files are in the correct directory.
- The skin has been refreshed.

The language files are located inside:

`AdaptiveClock\Languages\`

## Sunrise or location says "not found"

1. Open Windows Settings.
2. Navigate to Privacy & security → Location.
3. Enable Location services.
4. Enable desktop app location access.
5. Open Adaptive Clock Settings → Extras.
6. Select Find my location again.

Alternatively, configure Latitude and Longitude manually.

## Weather does not appear

Check:

- Weather is enabled.
- `WeatherOff=0`.
- Your internet connection is working.
- Your weather coordinates are valid.

Weather requires an internet connection.

## Wallpaper colour detection is incorrect

1. Change your Windows wallpaper if necessary.
2. Right-click Adaptive Clock.
3. Select Re-check Wallpaper.

The brightness detection reads the wallpaper locally.

## Custom quotes do not appear

Check that:

- The file is named `quotes.txt`.
- It is in the expected project directory.
- Each quote uses the `text | author` format.
- The file uses plain ASCII punctuation.

## Smooth seconds uses more resources

Smooth seconds updates ten times per second.

If you prefer lower resource usage, disable it:

```ini
Smooth=0
```

## Clock stops changing automatically

Check:

- Shuffle is active.
- The style is not locked.
- The selected profile contains multiple available styles.
- The shuffle interval is configured correctly.

You can resume automatic rotation through the right-click menu.

## Alarm does not sound

Check that the skin is loaded, `AlarmOn=1`, and `AlarmTime` is set to the intended local time in 24-hour `HH:MM` format. The alarm is checked while the skin is running; an alarm time that has already passed is not replayed after the fact. The alarm's fired marker includes the year, so the same date and time can trigger again in a later year.

## Still having problems?

Visit the project's GitHub Issues page and create a report.

When reporting an issue, include:

- Windows version.
- Rainmeter version.
- Adaptive Clock version.
- The clock style affected.
- A description of the problem.
- Relevant Rainmeter log messages.

Do not include private location coordinates or other personal information in public issue reports.

---

# 23. Privacy and Location

Adaptive Clock is designed to process personal desktop information locally wherever possible.

Understanding what happens to your information is important.

## Location Detection

`LocationFinder.ps1` requests location information from Windows.

If Windows does not provide a location, an approximate position is estimated using a time-zone lookup table.

The resulting coordinates are rounded to approximately 1 km and saved locally in:

`AdaptiveClock\State\location.txt`

This state file is listed in `.gitignore` and is not intended to be committed to the Git repository.

The Settings → Extras page allows you to view the location source.

## Sunrise and Sunset

Sunrise, sunset, daylight duration and sun position are calculated locally.

These calculations do not require an external network connection.

## Weather

Weather is the only feature that makes an external network request.

It is disabled by default.

When enabled:

- Weather information is requested from Open-Meteo.
- Requests occur every 15 minutes.
- Coordinates are rounded to one decimal place.
- The weather service receives those coordinates to provide local weather information.

If you do not want to share your approximate location:

- Keep weather disabled; or
- Configure a separate WeatherLatitude and WeatherLongitude using a nearby city.

## Wallpaper Detection

Wallpaper brightness is checked locally using the wallpaper file.

The wallpaper image is not uploaded.

## Privacy Summary

| Feature | Uses Internet? | Sends Location? |
|---|---|---|
| Clock display | No | No |
| Coder clocks | No | No |
| Quotes | No | No |
| Calendar | No | No |
| Wallpaper detection | No | No |
| Sunrise and sunset | No | No |
| Automatic location detection | No external service required | No |
| Weather | Yes, when enabled | Yes, rounded coordinates |

---

# 24. Frequently Asked Questions

### Do I need Rainmeter to use Adaptive Clock?

Yes. Adaptive Clock is a Rainmeter skin and requires Rainmeter on Windows.

### Is Adaptive Clock free?

Yes. The project is distributed under the MIT License.

### Does it work on Windows 10 and Windows 11?

Yes. Both are supported.

### Does it work on macOS or Linux?

No. Adaptive Clock is designed for Rainmeter on Windows.

### How many clock styles are available?

The project includes 130 styles.

### Can I use only programming-themed clocks?

Yes. Select the Coder profile.

### Can I use only simple clocks?

Yes. Select the Everyday profile.

### Can I stop the clock from changing automatically?

Yes. Lock the current style or disable automatic rotation.

### Can I use my own quotes?

Yes. Create a `quotes.txt` file using the documented format.

### Can I change the clock language?

Yes. Eleven language options are available, including Sinhala and Tamil.

### Does the clock need internet access?

No, not for normal clock functionality. Weather is optional and disabled by default.

### Does it automatically detect my location?

It can request location information from Windows. If unavailable, it uses an approximate time-zone-based fallback.

### Can I use a different location for weather?

Yes. Configure WeatherLatitude and WeatherLongitude.

### Will the clock start when Windows starts?

Rainmeter can be configured to start automatically with Windows. This is an application-level setting.

### Can I use more than one clock?

Rainmeter supports loading multiple skins. However, Adaptive Clock's different styles are designed as alternatives within the same clock skin.

### Can I customise the styles?

Yes. Advanced users can edit the generator scripts and Rainmeter configuration files.

### Will my settings disappear when I update?

Back up custom files and configuration before updating. The installation method and changes between releases can affect customised files.

---

# 25. Support and Feedback

Thank you for using Adaptive Clock!

If you encounter a problem, have a suggestion or want to contribute, use the project links below.

- **Project Repository:** [GitHub Repository](../../)
- **Downloads:** [GitHub Releases](../../releases)
- **Bug Reports:** [Report an Issue](../../issues)
- **Feature Requests:** [Suggest a Feature](../../issues)

For general Rainmeter questions, you can also visit:

- [Official Rainmeter Website](https://www.rainmeter.net/)
- [Rainmeter Documentation](https://docs.rainmeter.net/)
- [Rainmeter Community Forum](https://forum.rainmeter.net/)

---

<p align="center">

**Adaptive Clock for Rainmeter**

130 styles. One desktop. Your way.

Created by **Amika Alankara**

</p>