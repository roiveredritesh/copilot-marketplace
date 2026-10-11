"""Every .md frontmatter in the repo must parse as YAML (skills, agents, templates, eval cases).
No model calls, free to run.  usage: python evals/frontmatter_test.py"""
import glob, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GITHUB_ENTRY = '  - github:\n      type: http\n      url: "https://example.com/mcp"\n'


def frontmatter(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
    return m.group(1) if m else None


def main():
    failed, checked = 0, 0
    for path in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        if f"{os.sep}results{os.sep}" in path or f"{os.sep}node_modules{os.sep}" in path:
            continue
        text = open(path, encoding="utf-8").read()
        variants = [text]
        if path.endswith(os.path.join("templates", "publisher.md")):  # as /core:setup fills it
            variants.append(text.replace("  # {{GITHUB_SERVER}}\n", GITHUB_ENTRY))
        for t in variants:
            fm = frontmatter(t)
            if fm is None:
                continue
            checked += 1
            try:
                yaml.safe_load(fm)
            except yaml.YAMLError as e:
                failed += 1
                print(f"FAIL {os.path.relpath(path, ROOT)}: {str(e).splitlines()[0]}")
    print(f"\n{checked - failed}/{checked} frontmatter blocks parse")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
