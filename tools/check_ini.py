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

def check_files():
    global bad
    for rel, want_bom in (("AdaptiveClock.lua", False), ("Languages.lua", False), ("AdaptiveClockU.lua", True)):
        raw = open(os.path.join(SKIN, rel), "rb").read()
        if len(raw) < 200:
            print(f"{rel}: file is empty or truncated ({len(raw)} bytes)"); bad += 1
        has = raw[:3] == b"\xef\xbb\xbf"
        if has != want_bom:
            print(f"{rel}: must be saved {'WITH' if want_bom else 'WITHOUT'} a UTF-8 BOM"); bad += 1
    if any(b > 127 for b in open(os.path.join(SKIN, "AdaptiveClock.lua"), "rb").read()):
        print("AdaptiveClock.lua must be plain ASCII (use \\ddd escapes for symbols)"); bad += 1
    t = open(os.path.join(SKIN, "AdaptiveClock.ini"), encoding="utf-8").read()
    anchors = re.findall(r"Rotate -?[\d.]+,", t)
    if anchors:
        print(f"AdaptiveClock.ini: {len(anchors)} Rotate shapes have an anchor; rotate around the centre (no anchor)"); bad += len(anchors)
    files = set(re.findall(r"^ScriptFile=(.+)$", t, re.M))
    print("Script files used:", sorted(files))
    try:                                                    # compile every Lua file with real Lua 5.1 (what Rainmeter uses)
        from lupa.lua51 import LuaRuntime
        lua = LuaRuntime(encoding=None)
        for rel in ("AdaptiveClock.lua", "AdaptiveClockU.lua", "Languages.lua"):
            src = open(os.path.join(SKIN, rel), "rb").read()
            if src[:3] == b"\xef\xbb\xbf": src = src[3:]
            ok, err = lua.eval("function(s) local f, e = loadstring(s); return f ~= nil, e end")(src)
            if not ok:
                print(f"{rel}: Lua 5.1 syntax error: {err}"); bad += 1
    except ImportError:
        print("(install lupa to also compile the Lua files with Lua 5.1)")

check_files()
check("AdaptiveClock.ini")
check(os.path.join("Settings", "Settings.ini"), external_measures={"mMain"})
check(os.path.join("Gallery", "Gallery.ini"), external_measures={"mMain"})
sys.exit(1 if bad else 0)
