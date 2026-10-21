# Builds dist/AdaptiveClock-<version>.rmskin  (double-click to install in Rainmeter).
# Run from the repo root or the tools folder:  python build_rmskin.py
# Author: Amika Alankara  (MIT License)
import os, re, struct, zipfile

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
skin = os.path.join(root, "AdaptiveClock")
ini = open(os.path.join(skin, "AdaptiveClock.ini"), encoding="utf-8").read()
version = re.search(r"^Version=(.+)$", ini, re.M).group(1).strip()
author = re.search(r"^Author=(.+)$", ini, re.M).group(1).strip()
out_dir = os.path.join(root, "dist")
os.makedirs(out_dir, exist_ok=True)
path = os.path.join(out_dir, f"AdaptiveClock-{version}.rmskin")

rmskin_ini = f"""[rmskin]
Name=Adaptive Clock
Author={author}
Version={version}
LoadType=Skin
Load=AdaptiveClock\\AdaptiveClock.ini
MinimumRainmeter=4003000
MinimumWindows=6.1
"""
tmp = path + ".zip"
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("RMSKIN.ini", rmskin_ini)
    for folder, _, files in os.walk(skin):
        for f in files:
            full = os.path.join(folder, f)
            rel = os.path.relpath(full, skin).replace(os.sep, "/")
            z.write(full, "Skins/AdaptiveClock/" + rel)
data = open(tmp, "rb").read()
os.remove(tmp)
# Rainmeter package footer: zip size (int64), flags (byte), "RMSKIN" + NUL
open(path, "wb").write(data + struct.pack("<qB", len(data), 0) + b"RMSKIN\x00")
print("built", path, len(data) + 16, "bytes")
