import io
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "src/platform/windows.rs"

with io.open(path, "r", encoding="utf-8") as f:
    c = f.read()

repls = [
    (r"sc create {app_name} binpath=", r"sc create \"{app_name}\" binpath="),
    (r"sc start {app_name}", r"sc start \"{app_name}\""),
    (r"sc stop {app_name}", r"sc stop \"{app_name}\""),
    (r"sc delete {app_name}", r"sc delete \"{app_name}\""),
    (r'format!("sc start {}", &app_name)', r'format!("sc start \"{}\"", &app_name)'),
    (r"taskkill /F /IM {app_name}.exe", r"taskkill /F /IM \"{app_name}.exe\""),
    (r"reg add {subkey}", r"reg add \"{subkey}\""),
    (r"reg delete {subkey}", r"reg delete \"{subkey}\""),
    (r"reg add {} /f", r"reg add \"{}\" /f"),
    (r"reg add HKEY_CLASSES_ROOT\\.{ext}", r"reg add \"HKEY_CLASSES_ROOT\\.{ext}\""),
    (r"reg add HKEY_CLASSES_ROOT\\{ext}", r"reg add \"HKEY_CLASSES_ROOT\\{ext}\""),
    (r"reg delete HKEY_CLASSES_ROOT\\.{ext}", r"reg delete \"HKEY_CLASSES_ROOT\\.{ext}\""),
    (r"reg delete HKEY_CLASSES_ROOT\\{ext}", r"reg delete \"HKEY_CLASSES_ROOT\\{ext}\""),
]

ok_total = 0
for old, new in repls:
    n = c.count(old)
    if n == 0:
        print("WARN: not found:", old[:60])
        continue
    c = c.replace(old, new)
    ok_total += n
    print(f"OK {n:3d}x  {old[:60]}")

with io.open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(c)

print(f"windowsQuotes patch applied ({ok_total} replacements)")
