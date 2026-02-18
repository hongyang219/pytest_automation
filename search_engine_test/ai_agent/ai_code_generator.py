from ai_utils import get_project_context
from prompts import *
from ai_config import *


client, MODEL = initialize_client(llm_type="local")
FILE_PATH = "../tests/draft/test_search2_draft.py"

SYSTEM_PROMPT = sp_case_design


def generate_test_from_comments(file_path, po_file):
    """
    功能 1: 根据文件中的注释生成代码
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 获取项目上下文 (RAG)
    project_context = get_project_context(po_file)

    prompt = f"""
    【项目代码上下文】:
    {project_context}

    【当前测试文件内容 (包含注释需求)】:
    {content}

    【任务】
    请读取上述测试文件中的注释 (TODO 或 docstring)，完善具体的测试用例代码。
    
    【实现原则】
    必须使用pytest的各种装饰器来生成测试函数
    保留原有的 import 和结构，仅补充函数的具体实现。
    如果有需要的package，添加对应的import。
    为每一个步骤添加对应的注释。
    Let's think step by step.
    """

    print(f"🤖 Agent 正在使用{MODEL}思考并编写代码...")
    # noinspection PyTypeChecker
    response = client.chat.completions.create(
        model=MODEL,
        # extra_body={"thinking": {"type": "enabled"}},
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    generated_code = response.choices[0].message.content

    # 将生成的代码写入新文件，避免覆盖原文件
    new_file = file_path.replace(".py", "_generated.py")
    with open(new_file, "w", encoding="utf-8") as f:
        f.write(generated_code)

    print(f"✅ 代码已生成: {new_file}")


def suggest_negative_cases(file_path, po_file):
    """
    功能 2: 扩展测试覆盖率，生成异常场景
    """
    with open(file_path, "r", encoding="utf-8") as f:
        existing_code = f.read()

    project_context = get_project_context(po_file)

    prompt = f"""
    【项目代码上下文】:
    {project_context}

    【现有测试用例】:
    {existing_code}

    【任务】:
    作为一名追求高质量的 QA，请分析现有的测试用例。
    请编写若干（<=3个）新的“异常场景 (Negative Test Cases)”或“边界值测试”。
    例如：输入错误的用户名、密码为空、输入超长字符等。
    请直接输出新增的测试函数代码即可。
    """

    print("🤖 Agent 正在分析并设计异常用例...")
    # noinspection PyTypeChecker
    response = client.chat.completions.create(
        model=MODEL,
        # extra_body={"thinking": {"type": "enabled"}},
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    new_cases = response.choices[0].message.content

    # 将新用例追加到原文件末尾 (或者存入新文件)
    output_file = file_path.replace(".py", "_extended.py")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(existing_code + "\n\n# === AI Generated Negative Cases ===\n" + new_cases)

    print(f"✅ 扩展用例已生成: {output_file}")


# === 使用入口 ===
if __name__ == "__main__":
    # 场景 1: 根据注释写代码
    generate_test_from_comments(file_path=FILE_PATH, po_file="baidu_pageobjects.py")

    # 场景 2: 扩展异常测试
    pass