import subprocess
import xml.etree.ElementTree as ET
import json
from pycparser import parse_file, c_ast
import os
import re

# -------------------------------
# Configurations
# -------------------------------
ORIGINAL_C_FILE = r"C:\Users\User\Downloads\12c.c"
STRIPPED_C_FILE = "temp_cleaned.c"
CPPCHECK_PATH = r"D:\Univercity\Spring 2025\Capstone Project II\cpp check\cppcheck.exe"

UNSAFE_FUNCTIONS = {'gets', 'strcpy', 'strcat', 'sprintf', 'scanf', 'memcpy'}
MEMORY_KEYWORDS = ['overflow', 'use after free', 'leak', 'null', 'uninitialized']

# -------------------------------
# Step 1: Clean the input C code
# -------------------------------
def remove_imports_and_comments(c_code: str) -> str:
    code_no_imports = re.sub(r'^\s*#.*$', '', c_code, flags=re.MULTILINE)
    code_no_multiline_comments = re.sub(r'/\*.*?\*/', '', code_no_imports, flags=re.DOTALL)
    code_no_singleline_comments = re.sub(r'//.*$', '', code_no_multiline_comments, flags=re.MULTILINE)
    return code_no_singleline_comments

def sanitize_source_code(src_path, out_path):
    with open(src_path, "r", encoding="utf-8") as file:
        c_code = file.read()
    cleaned_code = remove_imports_and_comments(c_code)
    with open(out_path, "w", encoding="utf-8") as file:
        file.write(cleaned_code)

# -------------------------------
# Step 2: Run cppcheck
# -------------------------------
def run_cppcheck(file_path):
    cmd = [CPPCHECK_PATH, "--enable=all", "--inconclusive", "--xml", "--xml-version=2", file_path]
    try:
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        return result.stderr
    except FileNotFoundError:
        print("❌ Cppcheck not found. Check CPPCHECK_PATH.")
        return ""

def parse_cppcheck_output(xml_str):
    issues = []
    if not xml_str.strip():
        return issues
    try:
        root = ET.fromstring(xml_str)
        for error in root.findall(".//error"):
            msg = error.get("msg", "").lower()
            if any(keyword in msg for keyword in MEMORY_KEYWORDS):
                severity = error.get("severity", "unknown")
                location = error.find("location")
                file = location.get("file") if location is not None else ""
                line = location.get("line") if location is not None else ""
                issues.append({
                    "source": "cppcheck",
                    "msg": msg,
                    "severity": severity,
                    "file": file,
                    "line": line
                })
    except ET.ParseError as e:
        print("⚠️ Failed to parse cppcheck output:", e)
    return issues

# -------------------------------
# Step 3: Custom memory pattern detection using pycparser
# -------------------------------
class MemoryChecker(c_ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_FuncCall(self, node):
        func_name = self._get_func_name(node)
        if func_name in UNSAFE_FUNCTIONS:
            self.issues.append({
                "source": "custom",
                "msg": f"Unsafe function used: {func_name}",
                "severity": "warning",
                "file": STRIPPED_C_FILE,
                "line": node.coord.line
            })
        self.generic_visit(node)

    def _get_func_name(self, node):
        return node.name.name if isinstance(node.name, c_ast.ID) else ""

def analyze_custom(file_path):
    try:
        ast = parse_file(file_path, use_cpp=False)
        print("✅ pycparser successfully parsed the AST.")
    except Exception as e:
        print("⚠️ pycparser failed:", e)
        return []
    checker = MemoryChecker()
    checker.visit(ast)
    return checker.issues

# -------------------------------
# Step 4: Report printing and saving
# -------------------------------
def print_report(issues):
    if not issues:
        print("✅ No memory corruption issues found.")
        return
    print("\n🛑 Memory Corruption Vulnerabilities Detected")
    print("-" * 60)
    for issue in issues:
        print(f"[{issue['source'].upper()}] {issue['file']}:{issue['line']} – {issue['msg']}")
    print("-" * 60)

def save_json(issues, filename="filtered_memory_report.json"):
    with open(filename, 'w') as f:
        json.dump(issues, f, indent=4)
    print(f"✅ JSON report saved to: {filename}")

# -------------------------------
# Step 5: Main Analyzer
# -------------------------------
def analyze():
    print(f"🔍 Analyzing {ORIGINAL_C_FILE}...\n")
    sanitize_source_code(ORIGINAL_C_FILE, STRIPPED_C_FILE)
    cpp_issues = parse_cppcheck_output(run_cppcheck(ORIGINAL_C_FILE))
    custom_issues = analyze_custom(STRIPPED_C_FILE)
    return cpp_issues + custom_issues

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    issues = analyze()
    print_report(issues)
    save_json(issues)
    if os.path.exists(STRIPPED_C_FILE):
        os.remove(STRIPPED_C_FILE)
