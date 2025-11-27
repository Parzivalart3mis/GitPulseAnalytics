from typing import Dict, Any, List, Tuple
from writer_agent import get_code_from_prompt, revise_code
from reviewer_agent import review_code
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


def run_multi_agent_pipeline(user_query: str, max_iterations: int = 3) -> Dict[str, Any]:
    review_feedback_log: List[str] = []
    llm_message = get_code_from_prompt(user_query)
    code = getattr(llm_message, "content", llm_message)
    code = _extract_code(code)

    approved = False
    for _ in range(max_iterations):
        ok, feedback = review_code(code, user_query)
        if ok:
            approved = True
            break
        review_feedback_log.append(feedback)
        revised_msg = revise_code(user_query=user_query, prior_code=code, feedback=feedback)
        code = getattr(revised_msg, "content", revised_msg)
        code = _extract_code(code)

    exec_result = None
    exec_error = None
    if approved:
        try:
            exec_result = execute_generated_code(code)
        except Exception as e:
            exec_error = str(e)

    return {
        "approved": approved,
        "code": code,
        "review_feedback_log": review_feedback_log,
        "execution_result": exec_result,
        "execution_error": exec_error,
    }
