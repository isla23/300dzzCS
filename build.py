#!/usr/bin/env python3
# 构建脚本：
# 1) Vercel 构建机是 PEP668 外部管理环境，不能直接 pip install，这里自建 venv
# 2) venv 里装 requirements，再用 venv 的 python 跑 mkdocs
# 3) 部署到 Vercel 时把 site_url 覆盖为当前 VERCEL_URL；GitHub/本地保持原值
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
YML = os.path.join(ROOT, "mkdocs.yml")
OUT = os.path.join(ROOT, "site")


def venv_python():
    if sys.platform.startswith("win"):
        return os.path.join(ROOT, ".venv", "Scripts", "python.exe")
    return os.path.join(ROOT, ".venv", "bin", "python")


def setup_venv():
    vpy = venv_python()
    if not os.path.exists(vpy):
        print("[build] 创建 venv ...")
        subprocess.check_call([sys.executable, "-m", "venv", os.path.join(ROOT, ".venv")])
    print("[build] 在 venv 中安装依赖 ...")
    subprocess.check_call([vpy, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([vpy, "-m", "pip", "install", "-r", os.path.join(ROOT, "requirements.txt")])
    return vpy


def patch_site_url():
    vercel_url = os.environ.get("VERCEL_URL")  # 形如 300cs.vercel.app（无协议）
    if not vercel_url:
        return  # 本地 / GitHub Pages 部署：保持 mkdocs.yml 里的 site_url 不动
    site_url = "https://" + vercel_url
    with open(YML, "r", encoding="utf-8") as f:
        txt = f.read()
    txt, n = re.subn(r'(?m)^site_url:.*$', f"site_url: {site_url}", txt, count=1)
    if n:
        with open(YML, "w", encoding="utf-8") as f:
            f.write(txt)
        print(f"[build] site_url 已覆盖为 {site_url}")


if __name__ == "__main__":
    patch_site_url()
    vpy = setup_venv()
    cmd = [vpy, "-m", "mkdocs", "build", "-d", OUT]
    print("[build] 执行:", " ".join(cmd))
    subprocess.check_call(cmd)
