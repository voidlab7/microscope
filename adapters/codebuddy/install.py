#!/usr/bin/env python3
"""
MicroScope — CodeBuddy 安装脚本

用法:
  python3 install.py              # 安装到当前项目的 .codebuddy/skills/
  python3 install.py --global     # 安装到用户级 ~/.codebuddy/skills/
  python3 install.py --uninstall  # 卸载
  python3 install.py --check      # 仅检查环境依赖

GitHub: https://github.com/voidlab7/microscope
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ── 颜色输出 ──────────────────────────────────────────

def _supports_color():
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

if _supports_color():
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
else:
    RED = GREEN = YELLOW = BLUE = BOLD = DIM = RESET = ''

def ok(msg):     print(f"  {GREEN}✅{RESET} {msg}")
def fail(msg):   print(f"  {RED}❌{RESET} {msg}")
def warn(msg):   print(f"  {YELLOW}⚠️{RESET}  {msg}")
def info(msg):   print(f"  {BLUE}ℹ️{RESET}  {msg}")
def header(msg): print(f"\n{BOLD}{msg}{RESET}")

# ── 路径常量 ──────────────────────────────────────────

SKILL_NAME = "microscope"
SKILL_DIR_NAME = SKILL_NAME  # .codebuddy/skills/microscope/

# MicroScope 源码目录（脚本所在目录的上上级）
SCRIPT_DIR = Path(__file__).resolve().parent          # adapters/codebuddy/
MICROSCOPE_ROOT = SCRIPT_DIR.parent.parent            # MicroScope/

# 源路径
AGENT_MD     = MICROSCOPE_ROOT / "agent" / "AGENT.md"
SKILLS_DIR   = MICROSCOPE_ROOT / "skills"
PROMPTS_DIR  = MICROSCOPE_ROOT / "prompts"
TEMPLATES_DIR = MICROSCOPE_ROOT / "templates"
TOOLS_DIR    = MICROSCOPE_ROOT / "tools"

# ── 环境检查 ──────────────────────────────────────────

def check_python_dependency(module_name, pip_name=None, required=False):
    """检查 Python 包是否已安装"""
    try:
        __import__(module_name)
        ok(f"{module_name}")
        return True
    except ImportError:
        label = f"{module_name} (pip install {pip_name or module_name})"
        if required:
            fail(f"{label} — 基础依赖")
        else:
            warn(f"{label} — 可选")
        return False

def check_environment():
    """检查所有环境依赖"""
    header("🔍 环境依赖检查")
    print()

    # 基础依赖
    info("基础依赖（PDF/Excel 解析）:")
    basics = [
        ("pdfplumber", "pdfplumber", True),
        ("pypdf",     "pypdf",      True),
        ("pandas",    "pandas",     True),
        ("openpyxl",  "openpyxl",   True),
        ("jinja2",    "jinja2",     True),
    ]
    basic_ok = all(check_python_dependency(m, p, r) for m, p, r in basics)

    print()
    info("OCR 引擎（图片识别，强烈建议）:")
    ocr_ok = check_python_dependency("paddleocr", "paddlepaddle paddleocr", required=False)

    print()
    if basic_ok and ocr_ok:
        ok("所有依赖已就绪，图片 OCR 将使用双引擎交叉验证")
    elif basic_ok:
        warn("PaddleOCR 未安装 → 图片 OCR 降级为仅模型视觉，无法交叉验证")
        print(f"    安装命令: {BOLD}pip install paddlepaddle paddleocr{RESET}")
    else:
        fail("缺少基础依赖，部分功能不可用")
        print(f"    安装命令: {BOLD}pip install -r tools/requirements.txt{RESET}")

    return basic_ok, ocr_ok

# ── 安装逻辑 ──────────────────────────────────────────

def get_target_dir(global_install):
    """获取安装目标目录"""
    if global_install:
        base = Path.home() / ".codebuddy" / "skills"
    else:
        # 查找项目根目录（有 .git 的目录，或当前目录）
        cwd = Path.cwd()
        while cwd != cwd.parent:
            if (cwd / ".git").exists() or (cwd / ".codebuddy").exists():
                break
            cwd = cwd.parent
        base = cwd / ".codebuddy" / "skills"
    return base / SKILL_DIR_NAME

def install(global_install=False):
    """安装 MicroScope Skill 到 CodeBuddy"""

    target = get_target_dir(global_install)
    scope = "用户级" if global_install else "项目级"

    header(f"🔬 安装 MicroScope 到 CodeBuddy ({scope})")
    print(f"  目标: {target}")
    print()

    # 检查源文件
    if not AGENT_MD.exists():
        fail(f"找不到源文件: {AGENT_MD}")
        fail("请确保在 MicroScope 仓库内运行此脚本，或先 clone:")
        print(f"  git clone https://github.com/voidlab7/microscope.git")
        sys.exit(1)

    # 创建目录
    refs_dir = target / "references"
    assets_dir = target / "assets"
    refs_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    # 1. 复制 SKILL.md
    skill_md = target / "SKILL.md"
    shutil.copy2(AGENT_MD, skill_md)
    ok(f"SKILL.md ← agent/AGENT.md")

    # 2. 复制 skills/ → references/
    if SKILLS_DIR.exists():
        for f in SKILLS_DIR.glob("*.md"):
            shutil.copy2(f, refs_dir / f.name)
            ok(f"references/{f.name} ← skills/{f.name}")

    # 3. 复制 prompts/ → references/
    if PROMPTS_DIR.exists():
        for f in PROMPTS_DIR.glob("*.md"):
            shutil.copy2(f, refs_dir / f.name)
            ok(f"references/{f.name} ← prompts/{f.name}")

    # 4. 复制 templates/ → assets/
    if TEMPLATES_DIR.exists():
        for f in TEMPLATES_DIR.glob("*.md"):
            shutil.copy2(f, assets_dir / f.name)
            ok(f"assets/{f.name} ← templates/{f.name}")

    print()
    ok(f"安装完成！共 {len(list(target.rglob('*')))} 个文件")

    # 环境检查
    print()
    basic_ok, ocr_ok = check_environment()

    # 安装依赖提示
    print()
    header("📦 安装 Python 依赖（可选）")
    print(f"  基础: {BOLD}pip install -r {TOOLS_DIR}/requirements.txt{RESET}")
    print(f"  完整: {BOLD}pip install -r {TOOLS_DIR}/requirements-full.txt{RESET}")

    # 使用说明
    print()
    header("🚀 使用方式")
    print(f"  在 CodeBuddy 中说: {BOLD}帮我分析 AI 眼镜市场{RESET}")
    print(f"  或: {BOLD}@MicroScope 做个竞品分析{RESET}")
    print(f"  触发词: 市场分析、行业调研、企业调研、竞品分析、做个调研")

    return True

def uninstall(global_install=False):
    """卸载 MicroScope Skill"""
    target = get_target_dir(global_install)
    scope = "用户级" if global_install else "项目级"

    header(f"🗑️ 卸载 MicroScope ({scope})")

    if not target.exists():
        warn(f"未找到安装: {target}")
        return

    file_count = len(list(target.rglob("*")))
    shutil.rmtree(target)
    ok(f"已删除 {target} ({file_count} 个文件)")

# ── 入口 ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="MicroScope — CodeBuddy 安装/卸载脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 install.py              # 安装到当前项目
  python3 install.py --global     # 安装到用户级（所有项目可用）
  python3 install.py --uninstall  # 卸载
  python3 install.py --check      # 仅检查环境依赖
        """
    )
    parser.add_argument("--global", action="store_true", dest="global_install",
                        help="安装到用户级 ~/.codebuddy/skills/")
    parser.add_argument("--uninstall", action="store_true",
                        help="卸载 MicroScope Skill")
    parser.add_argument("--check", action="store_true",
                        help="仅检查环境依赖，不安装")

    args = parser.parse_args()

    if args.check:
        check_environment()
    elif args.uninstall:
        uninstall(args.global_install)
    else:
        install(args.global_install)

if __name__ == "__main__":
    main()
