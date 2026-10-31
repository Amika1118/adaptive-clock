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
    eng = os.path.join(SKIN, "Languages", "English.inc")
    if rel == "AdaptiveClock.ini" and os.path.exists(eng):
        defined |= set(re.findall(r"^(\w+)=", open(eng, encoding="utf-16").read(), re.M))
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
    for rel in ("AdaptiveClock.lua", "Settings/Settings.lua"):
        raw = open(os.path.join(SKIN, rel), "rb").read()
        if len(raw) < 200:
            print(f"{rel}: file is empty or truncated ({len(raw)} bytes)"); bad += 1
        if raw[:3] == b"\xef\xbb\xbf":
            print(f"{rel}: must have NO byte-order mark (Lua 5.1 cannot load one)"); bad += 1
        if any(b > 127 for b in raw):
            print(f"{rel}: must be plain ASCII (translations live in Languages/*.inc)"); bad += 1
    t = open(os.path.join(SKIN, "AdaptiveClock.ini"), encoding="utf-8").read()
    anchors = re.findall(r"Rotate -?[\d.]+,", t)
    if anchors:
        print(f"AdaptiveClock.ini: {len(anchors)} Rotate shapes have an anchor; rotate around the centre (no anchor)"); bad += len(anchors)
    print("Script files used:", sorted(set(re.findall(r"^ScriptFile=(.+)$", t, re.M))))
    # every language include must be UTF-16 and define every variable the ini uses
    english = open(os.path.join(SKIN, "Languages", "English.inc"), encoding="utf-16").read()
    names = set(re.findall(r"^(\w+)=", english, re.M))
    for inc in sorted(os.listdir(os.path.join(SKIN, "Languages"))):
        raw = open(os.path.join(SKIN, "Languages", inc), "rb").read()
        if raw[:2] != b"\xff\xfe":
            print(f"Languages/{inc}: must be UTF-16 LE with BOM"); bad += 1
        have = set(re.findall(r"^(\w+)=", raw.decode("utf-16"), re.M))
        if have != names:
            print(f"Languages/{inc}: variables differ from English.inc: {sorted(names ^ have)[:5]}"); bad += 1
    used = set(re.findall(r"#((?:T_\w+|Dow\d+|DowS\d+|DowH\d+|Mon\d+|MonS\d+|Greet(?:Night|Morning|Afternoon|Evening)))#", t))
    missing = used - names
    if missing:
        print("ini uses variables that Languages/English.inc does not define:", sorted(missing)[:6]); bad += len(missing)
    try:                                                    # compile the Lua with real Lua 5.1 (what Rainmeter uses)
        from lupa.lua51 import LuaRuntime
        lua = LuaRuntime(encoding=None)
        for rel in ("AdaptiveClock.lua", "Settings/Settings.lua"):
            src = open(os.path.join(SKIN, rel), "rb").read()
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
