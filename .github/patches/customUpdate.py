import io

UPDATE_JSON_URL = "https://raw.githubusercontent.com/cptn73m0/rdgen/master/update/version.json"


def patch(path, repls):
    with io.open(path, "r", encoding="utf-8") as f:
        c = f.read()
    for old, new in repls:
        n = c.count(old)
        if n == 0:
            print(f"WARN: pattern not found in {path}: {old[:80]!r}")
            continue
        c = c.replace(old, new)
        print(f"OK {path}: replaced {n} occurrence(s) of {old[:60]!r}")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(c)


patch("flutter/lib/common.dart", [
    (
        "  if (!isWeb) {\n    if (!bind.isCustomClient()) {\n",
        "  if (!isWeb) {\n",
    ),
    (
        "      Timer(const Duration(seconds: 1), () async {\n"
        "        bind.mainGetSoftwareUpdateUrl();\n"
        "      });\n"
        "    }\n"
        "  }\n"
        "}",
        "      Timer(const Duration(seconds: 1), () async {\n"
        "        bind.mainGetSoftwareUpdateUrl();\n"
        "      });\n"
        "  }\n"
        "}",
    ),
])

patch("src/common.rs", [
    (
        "pub fn check_software_update() {\n"
        "    if is_custom_client() {\n"
        "        return;\n"
        "    }\n",
        "pub fn check_software_update() {\n",
    ),
    (
        "    let (request, url) =\n"
        "        hbb_common::version_check_request(hbb_common::VER_TYPE_RUSTDESK_CLIENT.to_string());\n",
        f'    let url = "{UPDATE_JSON_URL}".to_string();\n',
    ),
    ("client.post(&url).json(&request).send().await", "client.get(&url).send().await"),
])

print("customUpdate patch applied")
