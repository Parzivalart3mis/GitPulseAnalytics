from typing import Dict, Any
from writer_agent import get_code_from_prompt
from executor_agent import execute_generated_code


def _extract_code(text: str) -> str:
    s = text.strip()
    if s.startswith("```python"):
        s = s[9:]
    elif s.startswith("```"):
        s = s[3:]
    if s.endswith("```"):
        s = s[:-3]
    return s.strip()


def run_multi_agent_pipeline(user_query: str) -> Dict[str, Any]:
    llm_message = get_code_from_prompt(user_query)
    code = getattr(llm_message, "content", llm_message)
    code = _extract_code(code)

    exec_result = None
    exec_error = None
    try:
        exec_result = execute_generated_code(code)
    except Exception as e:
        exec_error = str(e)

    return {
        "code": code,
        "execution_result": exec_result,
        "execution_error": exec_error,
    }
