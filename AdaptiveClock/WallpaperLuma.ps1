# Prints the average brightness (0..1) of the current desktop wallpaper.
Add-Type -AssemblyName System.Drawing
$p = Join-Path $env:APPDATA 'Microsoft\Windows\Themes\TranscodedWallpaper'
if (-not (Test-Path $p)) { $p = (Get-ItemProperty 'HKCU:\Control Panel\Desktop').WallPaper }
if (-not $p -or -not (Test-Path $p)) { exit }
$img = [System.Drawing.Image]::FromFile($p)
$bmp = New-Object System.Drawing.Bitmap 1, 1
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.InterpolationMode = 'HighQualityBicubic'
$g.DrawImage($img, 0, 0, 1, 1)
$c = $bmp.GetPixel(0, 0)
$img.Dispose(); $g.Dispose(); $bmp.Dispose()
$l = (0.299 * $c.R + 0.587 * $c.G + 0.114 * $c.B) / 255
[math]::Round($l, 3).ToString([System.Globalization.CultureInfo]::InvariantCulture)
