# Author: Amika Alankara  (MIT License)
# Prints the average brightness (0..1) of the wallpaper area behind the skin.
# Args: -X -Y -W -H = skin rectangle in screen pixels (if it is not on the wallpaper image, the whole image is used).
# Results are cached in %TEMP% and only recomputed when the wallpaper, its file or the skin position changes,
# so it is cheap to call often (Rainmeter calls it every 30 s and whenever the wallpaper setting changes).
param([int]$X = 0, [int]$Y = 0, [int]$W = 0, [int]$H = 0)

$inv   = [System.Globalization.CultureInfo]::InvariantCulture
$cache = Join-Path $env:TEMP 'AdaptiveClock_luma.txt'
$reg   = ''
try { $reg = [string](Get-ItemProperty 'HKCU:\Control Panel\Desktop').WallPaper } catch {}
$old = @()
if (Test-Path $cache) { $old = @(Get-Content $cache -ErrorAction SilentlyContinue) }

# The wallpaper setting just changed: give Windows a moment to write its transcoded copy.
if ($old.Count -ge 3 -and $old[0] -ne $reg) { Start-Sleep -Seconds 2 }

$tw  = Join-Path $env:APPDATA 'Microsoft\Windows\Themes\TranscodedWallpaper'
$src = $null
if (Test-Path $tw) { $src = $tw } elseif ($reg -and (Test-Path $reg)) { $src = $reg }

if (-not $src) {                                   # no picture: solid colour background
  try {
    $c = ([string](Get-ItemProperty 'HKCU:\Control Panel\Colors').Background).Trim() -split '\s+'
    if ($c.Count -eq 3) {
      ([math]::Round((0.299 * [int]$c[0] + 0.587 * [int]$c[1] + 0.114 * [int]$c[2]) / 255, 3)).ToString($inv)
    }
  } catch {}
  exit
}

$fi  = Get-Item $src
$key = "$reg|$($fi.FullName)|$($fi.LastWriteTimeUtc.Ticks)|$($fi.Length)|$X,$Y,$W,$H"
if ($old.Count -ge 3 -and $old[1] -eq $key) { $old[2]; exit }

Add-Type -AssemblyName System.Drawing
$img  = [System.Drawing.Image]::FromFile($src)
$rect = New-Object System.Drawing.Rectangle 0, 0, $img.Width, $img.Height
if ($W -gt 0 -and $H -gt 0) {
  $want = New-Object System.Drawing.Rectangle $X, $Y, $W, $H
  $hit  = [System.Drawing.Rectangle]::Intersect($want, $rect)
  if (($hit.Width * $hit.Height) -ge (0.5 * $W * $H)) { $rect = $hit }
}

$n   = 8
$bmp = New-Object System.Drawing.Bitmap $n, $n
$g   = [System.Drawing.Graphics]::FromImage($bmp)
$g.InterpolationMode = 'HighQualityBicubic'
$dest = New-Object System.Drawing.Rectangle 0, 0, $n, $n
$g.DrawImage($img, $dest, $rect.X, $rect.Y, $rect.Width, $rect.Height, [System.Drawing.GraphicsUnit]::Pixel)

$sum = 0.0
for ($a = 0; $a -lt $n; $a++) { for ($b = 0; $b -lt $n; $b++) {
  $p = $bmp.GetPixel($a, $b)
  $sum += 0.299 * $p.R + 0.587 * $p.G + 0.114 * $p.B
} }
$img.Dispose(); $g.Dispose(); $bmp.Dispose()

$val = ([math]::Round($sum / ($n * $n) / 255, 3)).ToString($inv)
try { Set-Content -Path $cache -Value @($reg, $key, $val) } catch {}
$val
