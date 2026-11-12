from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def ensure_dir(path: str | Path) -> Path:
    """确保目录存在（不存在则递归创建），并返回该 Path。"""
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    return target


def resolve_path(*parts: str | Path) -> Path:
    """将相对路径片段拼接为基于项目根目录的绝对路径。"""
    return PROJECT_ROOT.joinpath(*parts)
