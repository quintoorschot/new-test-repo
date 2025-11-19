import os
import re
import pathlib


def main() -> None:
    action_dir = pathlib.Path(os.environ.get(
        "ACTION_DIR", "/__w/_actions/quintoorschot/CICD-FlakyDoctor/main"
    ))
    src_path = pathlib.Path(os.environ.get("SRC_PATH", "src/test/java"))
    gw = pathlib.Path(os.environ.get("GITHUB_WORKSPACE", "."))

    tests = []

    def parse_java(p: pathlib.Path) -> None:
        txt = p.read_text(encoding="utf-8", errors="ignore")
        pkg_m = re.search(r'^\s*package\s+([\w.]+)\s*;', txt, re.M)
        pkg = pkg_m.group(1) if pkg_m else ""
        cls_m = re.search(r'\bclass\s+([A-Za-z0-9_]+)\b', txt)
        if not cls_m:
            return
        cls = cls_m.group(1)
        for m in re.finditer(
            r'@Test[\s\S]*?\b(?:public|protected|private)?\s+void\s+([A-Za-z0-9_]+)\s*\(',
            txt,
        ):
            method = m.group(1)
            tests.append(f"{pkg}.{cls}.{method}" if pkg else f"{cls}.{method}")

    if src_path.is_file():
        parse_java(src_path)
    else:
        for p in src_path.rglob("*.java"):
            parse_java(p)

    out = action_dir / "tests.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    project = gw.name

    with out.open("w", encoding="utf-8") as f:
        for t in tests:
            f.write(f"{project},,.,{t},ID,ID,,,\n")

    print(f"Wrote {len(tests)} rows to {out}")


if __name__ == "__main__":
    main()