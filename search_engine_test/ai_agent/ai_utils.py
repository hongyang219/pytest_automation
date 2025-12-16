# 这是一个工具模块
import os


def get_project_context(file):
    """
    RAG 的核心：检索项目的上下文信息。
    对于小项目，直接读取关键文件内容作为 Prompt 的一部分。
    """
    context = ""

    # 1. 读取 conftest.py，让 AI 知道有哪些 fixture (比如 browser)
    if os.path.exists("conftest.py"):
        with open("conftest.py", "r", encoding="utf-8") as f:
            context += f"### 文件: conftest.py\n{f.read()}\n\n"

    # 2. 读取 Page Objects，让 AI 知道页面有哪些操作方法
    # 如login_page.py
    po_path = f"../page_objects/{file}"
    if os.path.exists(po_path):
        with open(po_path, "r", encoding="utf-8") as f:
            context += f"### 文件: {po_path}\n{f.read()}\n\n"

    return context