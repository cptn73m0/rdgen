import io
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "flutter/lib/desktop/pages/desktop_home_page.dart"

with io.open(path, "r", encoding="utf-8") as f:
    c = f.read()

repls = [
    (
        re.compile(r"(\n\s*)if \(!bind\.isDisableSettings\(\)\)\s*\n\s*InkWell\("),
        r"\1InkWell(",
        "always show the Change Password button",
    ),
    (
        re.compile(
            r"onTap: \(\) => DesktopSettingPage\.switch2page\(\s*\n\s*SettingsTabKey\.safety\),"
        ),
        "onTap: () => setPasswordDialog(),",
        "open the permanent password dialog directly",
    ),
]

for pattern, new, desc in repls:
    matches = pattern.findall(c)
    if len(matches) != 1:
        print("ERROR: expected 1 occurrence of %r, found %d" % (pattern.pattern[:60], len(matches)))
        sys.exit(1)
    c = pattern.sub(new, c)
    print("OK:", desc)

with io.open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(c)

print("clientPassword patch applied")
