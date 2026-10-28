#!/usr/bin/env python3
# 构建脚本：Vercel 部署时用 VERCEL_URL 覆盖 site_url，本地/GitHub 部署保持原配置
import os
import re
import subprocess
import sys

YML = os.path.join(os.path.dirname(__file__), "mkdocs.yml")
OUT = os.path.join(os.path.dirname(__file__), "site")


def patch_site_url():
    vercel_url = os.environ.get("VERCEL_URL")  # 形如 300cs.vercel.app（无协议）
    if not vercel_url:
        return  # 本地 / GitHub Pages 部署：保持 mkdocs.yml 里的 site_url 不动
    site_url = "https://" + vercel_url
    with open(YML, "r", encoding="utf-8") as f:
        txt = f.read()
    # 仅替换第一处 site_url 行
    txt, n = re.subn(
        r'(?m)^site_url:.*$',
        f"site_url: {site_url}",
        txt,
        count=1,
    )
    if n:
        with open(YML, "w", encoding="utf-8") as f:
            f.write(txt)
        print(f"[build] site_url 已覆盖为 {site_url}")


if __name__ == "__main__":
    patch_site_url()
    cmd = [sys.executable, "-m", "mkdocs", "build", "-d", OUT]
    print("[build] 执行:", " ".join(cmd))
    subprocess.check_call(cmd)
