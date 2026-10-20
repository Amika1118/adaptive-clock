# Author: Amika Alankara  (MIT License)
# Prints the average brightness (0..1) of the wallpaper area behind the skin.
# Optional args: -X -Y -W -H = skin rectangle in screen pixels. If it does not fall on the wallpaper image
# (for example on a second monitor) the whole wallpaper is averaged instead.
param([int]$X = 0, [int]$Y = 0, [int]$W = 0, [int]$H = 0)

Add-Type -AssemblyName System.Drawing
$p = Join-Path $env:APPDATA 'Microsoft\Windows\Themes\TranscodedWallpaper'
if (-not (Test-Path $p)) { $p = (Get-ItemProperty 'HKCU:\Control Panel\Desktop').WallPaper }
if (-not $p -or -not (Test-Path $p)) { exit }

$img  = [System.Drawing.Image]::FromFile($p)
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
  $c = $bmp.GetPixel($a, $b)
  $sum += 0.299 * $c.R + 0.587 * $c.G + 0.114 * $c.B
} }
$img.Dispose(); $g.Dispose(); $bmp.Dispose()
[math]::Round($sum / ($n * $n) / 255, 3).ToString([System.Globalization.CultureInfo]::InvariantCulture)
