import os
import sys
import json

def resource_path(rel_path: str) -> str:
    """兼容直接运行与 PyInstaller 打包后的资源路径"""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)

def get_config_path() -> str:
    candidates = [
        # 优先查找Resources文件夹中的config.json（macOS .app打包）
        resource_path(os.path.join("Resources", "config.json")),
        # PyInstaller打包时的路径
        resource_path("config.json"),
        # 其他可能的路径
        resource_path(os.path.join("rollcall-bot_XMU", "config.json")),
        # 直接运行时的路径
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"),
    ]
    for p in candidates:
        if os.path.exists(p):
            print(f"[DEBUG] 找到config.json: {p}")
            return p
    raise FileNotFoundError(f"config.json not found. tried:\n" + "\n".join(candidates))