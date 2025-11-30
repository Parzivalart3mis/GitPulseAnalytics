from typing import Dict, Any, Tuple
from writer_agent import get_code_from_prompt
from executor_agent import execute_generated_code
from reviewer_agent import review_code


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

    review_score, review_status = review_code(code, user_query)
    
    exec_result = None
    exec_error = None
    try:
        exec_result = execute_generated_code(code)
    except Exception as e:
        exec_error = str(e)

    return {
        "code": code,
        "review_score": review_score,
        "review_status": review_status,
        "execution_result": exec_result,
        "execution_error": exec_error,
    }
