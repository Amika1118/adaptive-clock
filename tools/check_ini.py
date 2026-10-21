# Sanity checks for the generated skins: python check_ini.py   (exit code 1 on problems)
# Author: Amika Alankara  (MIT License)
import re, os, sys, collections

SKIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "AdaptiveClock")
BUILTIN = {"CURRENTPATH", "CURRENTFILE", "CURRENTCONFIG", "CURRENTCONFIGX", "CURRENTCONFIGY",
           "CURRENTCONFIGWIDTH", "CURRENTCONFIGHEIGHT"}
bad = 0

def check(rel, external_measures=()):
    global bad
    t = open(os.path.join(SKIN, rel), encoding="utf-8").read()
    problems = []
    if any(ord(c) > 127 for c in t):
        problems.append("non-ASCII characters")
    secs = re.findall(r"^\[([^\]]+)\]", t, re.M)
    problems += [f"duplicate section {k}" for k, v in collections.Counter(secs).items() if v > 1]
    vsec = t.split("[Variables]")[1].split("\n[")[0] if "[Variables]" in t else ""
    defined = set(re.findall(r"^(\w+)=", vsec, re.M))
    problems += [f"undefined variable #{v}#" for v in sorted(set(re.findall(r"#(\w+)#", t)) - defined - BUILTIN)]
    meas = {s for s in secs if s.startswith("m")} | set(external_measures)
    refs = set(re.findall(r"\[(m\w+?)(?::[^\]]*)?\]", t)) | set(re.findall(r"MeasureName=(\w+)", t))
    problems += [f"undefined measure {r}" for r in sorted(refs - meas)]
    problems += [f"hidden variable {v} undefined" for v in sorted(set(re.findall(r"Hidden=#(\w+)#", t)) - defined)]
    print(f"{rel}: {len(secs)} sections, {len(problems)} problems")
    for p in problems:
        print("  -", p)
    bad += len(problems)

check("AdaptiveClock.ini")
check(os.path.join("Settings", "Settings.ini"), external_measures={"mMain"})
check(os.path.join("Gallery", "Gallery.ini"), external_measures={"mMain"})
sys.exit(1 if bad else 0)
