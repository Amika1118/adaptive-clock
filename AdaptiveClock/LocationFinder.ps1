# LocationFinder.ps1  -  finds this PC's approximate location WITHOUT using the internet.
# Author: Amika Alankara  (MIT License)
#
# 1. Asks Windows (System.Device.Location, the same location service apps use). It needs Windows location to be on and
#    "Let desktop apps access your location" in Settings > Privacy & security > Location.
# 2. If Windows does not answer, it estimates from the PC's time zone (a built-in table, no network).
# The result is rounded to about 1 km and saved to State\location.txt on this PC only. Nothing is sent anywhere by this script.
param([string]$Out, [switch]$Force)
$ErrorActionPreference = 'SilentlyContinue'
if (-not $Out) { exit }
$dir = Split-Path $Out
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
if (-not $Force -and (Test-Path $Out)) {                       # a recent answer is still good
  $age = (Get-Date) - (Get-Item $Out).LastWriteTime
  if ($age.TotalDays -lt 7 -and ((Get-Content $Out) -match 'source=(windows|timezone)')) { exit }
}

$inv = [System.Globalization.CultureInfo]::InvariantCulture
$lat = $null; $lon = $null; $source = 'none'
try {
  Add-Type -AssemblyName System.Device
  $w = New-Object System.Device.Location.GeoCoordinateWatcher([System.Device.Location.GeoPositionAccuracy]::Default)
  if ($w.TryStart($false, [TimeSpan]::FromSeconds(10))) {
    $p = $w.Position.Location
    if (-not $p.IsUnknown -and -not [double]::IsNaN($p.Latitude)) { $lat = $p.Latitude; $lon = $p.Longitude; $source = 'windows' }
  }
  $w.Stop()
} catch {}

if ($source -eq 'none') {                                      # time-zone estimate (a big city in the zone)
  $zones = @{
    'UTC' = @(51.5, -0.1); 'GMT Standard Time' = @(51.5, -0.1); 'Greenwich Standard Time' = @(64.1, -21.9);
    'W. Europe Standard Time' = @(52.5, 13.4); 'Central Europe Standard Time' = @(50.1, 14.4); 'Central European Standard Time' = @(52.2, 21.0);
    'Romance Standard Time' = @(48.9, 2.4); 'E. Europe Standard Time' = @(47.0, 28.9); 'GTB Standard Time' = @(38.0, 23.7);
    'FLE Standard Time' = @(50.5, 30.5); 'Russian Standard Time' = @(55.8, 37.6); 'Turkey Standard Time' = @(41.0, 29.0);
    'Arab Standard Time' = @(24.7, 46.7); 'Arabian Standard Time' = @(25.2, 55.3); 'Arabic Standard Time' = @(33.3, 44.4);
    'Iran Standard Time' = @(35.7, 51.4); 'Israel Standard Time' = @(31.8, 35.2); 'Egypt Standard Time' = @(30.0, 31.2);
    'South Africa Standard Time' = @(-26.2, 28.0); 'E. Africa Standard Time' = @(-1.3, 36.8); 'W. Central Africa Standard Time' = @(6.5, 3.4);
    'Pakistan Standard Time' = @(24.9, 67.0); 'India Standard Time' = @(19.1, 72.9); 'Sri Lanka Standard Time' = @(6.9, 79.9);
    'Nepal Standard Time' = @(27.7, 85.3); 'Bangladesh Standard Time' = @(23.8, 90.4); 'Myanmar Standard Time' = @(16.8, 96.2);
    'SE Asia Standard Time' = @(13.8, 100.5); 'Singapore Standard Time' = @(1.4, 103.8); 'China Standard Time' = @(39.9, 116.4);
    'Taipei Standard Time' = @(25.0, 121.6); 'Tokyo Standard Time' = @(35.7, 139.7); 'Korea Standard Time' = @(37.6, 127.0);
    'W. Australia Standard Time' = @(-32.0, 115.9); 'Cen. Australia Standard Time' = @(-34.9, 138.6); 'AUS Eastern Standard Time' = @(-33.9, 151.2);
    'E. Australia Standard Time' = @(-27.5, 153.0); 'New Zealand Standard Time' = @(-36.9, 174.8); 'Central Asia Standard Time' = @(43.2, 76.9);
    'West Asia Standard Time' = @(41.3, 69.2); 'Eastern Standard Time' = @(40.7, -74.0); 'Central Standard Time' = @(41.9, -87.6);
    'Mountain Standard Time' = @(39.7, -105.0); 'US Mountain Standard Time' = @(33.4, -112.1); 'Pacific Standard Time' = @(34.1, -118.2);
    'Alaskan Standard Time' = @(61.2, -149.9); 'Hawaiian Standard Time' = @(21.3, -157.9); 'Canada Central Standard Time' = @(49.9, -97.1);
    'Atlantic Standard Time' = @(44.7, -63.6); 'Mexico Standard Time' = @(19.4, -99.1); 'SA Pacific Standard Time' = @(4.7, -74.1);
    'E. South America Standard Time' = @(-23.6, -46.6); 'Argentina Standard Time' = @(-34.6, -58.4); 'Pacific SA Standard Time' = @(-33.5, -70.7);
    'SA Western Standard Time' = @(10.5, -66.9)
  }
  $id = [System.TimeZoneInfo]::Local.Id
  if ($zones.ContainsKey($id)) { $lat = $zones[$id][0]; $lon = $zones[$id][1]; $source = 'timezone' }
}

$unix = [int][DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
if ($source -eq 'none') {
  [System.IO.File]::WriteAllText($Out, "source=none`ntime=$unix", (New-Object System.Text.UTF8Encoding($false)))
} else {
  $la = ([math]::Round([double]$lat, 2)).ToString($inv); $lo = ([math]::Round([double]$lon, 2)).ToString($inv)
  [System.IO.File]::WriteAllText($Out, "lat=$la`nlon=$lo`nsource=$source`ntime=$unix", (New-Object System.Text.UTF8Encoding($false)))
}
