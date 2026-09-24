"""
PAIMANA AI - Single Text File Codebase Bundler
Consolidates all project source code, documentation, backend modules,
and React frontend components into a single structured .txt bundle in the project root.
"""

import os
import sys
import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TEXT_EXTENSIONS = {
    ".py", ".jsx", ".js", ".json", ".html", ".css", ".md", ".bat", ".ps1", ".txt", ".sql", ".rules"
}

EXCLUDE_DIRS = {
    "node_modules", "__pycache__", ".git", ".venv", "venv", "dist",
    ".pytest_cache", ".idea", ".vscode", ".gemini"
}

EXCLUDE_FILES = {
    "package-lock.json", "PAIMANA_AI_CODE_BUNDLE.txt"
}


def is_text_file(filepath: str) -> bool:
    ext = os.path.splitext(filepath)[1].lower()
    if os.path.basename(filepath).startswith(".") and not ext:
        return True
    return ext in TEXT_EXTENSIONS


def generate_code_bundle():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bundle_filename = "PAIMANA_AI_CODE_BUNDLE.txt"
    bundle_filepath = os.path.join(ROOT_DIR, bundle_filename)

    print("=" * 65)
    print("PAIMANA AI - TEXT CODEBASE BUNDLE GENERATOR")
    print("=" * 65)
    print(f"Target Bundle: {bundle_filepath}\n")

    files_to_bundle = []

    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]

        for file in files:
            if file in EXCLUDE_FILES or file.endswith(".zip") or file.endswith(".db"):
                continue

            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")

            if is_text_file(full_path):
                files_to_bundle.append((rel_path, full_path))

    files_to_bundle.sort(key=lambda x: (
        0 if x[0].endswith(".md") or x[0].startswith(".") else
        1 if x[0].startswith("src/") else
        2 if x[0].startswith("frontend/") else
        3 if x[0].startswith("scripts/") else 4,
        x[0]
    ))

    total_lines = 0
    total_chars = 0

    with open(bundle_filepath, 'w', encoding='utf-8') as out_f:
        out_f.write("=" * 80 + "\n")
        out_f.write("PAIMANA AI — COMPLETE SOURCE CODE & SPECIFICATION BUNDLE\n")
        out_f.write("Theme: Predictive Analytics & Early Warning Infrastructure Monitoring (MoSPI)\n")
        out_f.write(f"Generated On: {timestamp}\n")
        out_f.write(f"Total Bundled Files: {len(files_to_bundle)}\n")
        out_f.write("=" * 80 + "\n\n")

        out_f.write("TABLE OF CONTENTS / BUNDLED MANIFEST:\n")
        out_f.write("-" * 80 + "\n")
        for idx, (rel_path, full_path) in enumerate(files_to_bundle, 1):
            try:
                size_kb = os.path.getsize(full_path) / 1024
                out_f.write(f"{idx:02d}. [{rel_path}] ({size_kb:.1f} KB)\n")
            except Exception:
                out_f.write(f"{idx:02d}. [{rel_path}]\n")
        out_f.write("-" * 80 + "\n\n\n")

        for idx, (rel_path, full_path) in enumerate(files_to_bundle, 1):
            try:
                with open(full_path, 'r', encoding='utf-8', errors='replace') as in_f:
                    content = in_f.read()
                    lines = content.count('\n') + (1 if content else 0)
                    total_lines += lines
                    total_chars += len(content)

                    out_f.write("=" * 80 + "\n")
                    out_f.write(f"FILE {idx:02d}/{len(files_to_bundle):02d}: {rel_path}\n")
                    out_f.write(f"Lines: {lines} | Size: {len(content):,} chars\n")
                    out_f.write("=" * 80 + "\n\n")
                    out_f.write(content)
                    out_f.write("\n\n\n")
                    print(f"  [{idx:02d}/{len(files_to_bundle):02d}] Bundled: {rel_path} ({lines} lines)")
            except Exception as e:
                print(f"  [ERROR] Could not read {rel_path}: {e}")

    bundle_size_mb = os.path.getsize(bundle_filepath) / (1024 * 1024)

    print("\n" + "=" * 65)
    print("CODEBASE BUNDLE GENERATED SUCCESSFULLY!")
    print("=" * 65)
    print(f"• Total Files Bundled: {len(files_to_bundle)}")
    print(f"• Total Lines of Code: {total_lines:,}")
    print(f"• Total Characters:    {total_chars:,}")
    print(f"• Bundle File Size:    {bundle_size_mb:.2f} MB")
    print(f"• Output File:         {bundle_filepath}")
    print("=" * 65)
    return bundle_filepath


if __name__ == "__main__":
    generate_code_bundle()
