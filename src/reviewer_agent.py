import os
import re
from langchain_openai import ChatOpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def _static_checks(code: str, user_query: str):
    issues = []
    try:
        compile(code, "<review>", "exec")
    except SyntaxError as e:
        issues.append(f"SyntaxError at line {e.lineno}: {e.msg}")
    if "from fbprophet" in code or "import fbprophet" in code:
        issues.append("Uses fbprophet; must use 'from prophet import Prophet'.")
    if "plt.show(" in code:
        issues.append("Calls plt.show(); it must not be called.")
    if "input(" in code:
        issues.append("Uses input(); interactive input is not allowed.")
    if re.search(r"\bopen\(.*\)", code):
        issues.append("Uses file I/O; it is not allowed.")
    if "psycopg2.connect(" not in code:
        issues.append("Missing psycopg2.connect() database connection per spec.")
    if "from prophet import Prophet" not in code and "Prophet(" in code:
        issues.append("Prophet is used but not imported as 'from prophet import Prophet'.")
    if "st." in code and "import streamlit as st" not in code:
        issues.append("Uses Streamlit APIs but missing 'import streamlit as st'.")
    if "Prophet().plot(" in code:
        issues.append("Incorrect Prophet plotting; use model.plot(forecast) after fitting the model.")
    lq = (user_query or "").lower()
    if "created" in lq and "created_at" not in code and "closed_at" in code:
        issues.append("User asked for created issues, but code uses closed_at. Use created_at for created issues.")
    return issues

def review_code(code: str, user_query: str):
    """
    Review the generated code and return a score and status.
    
    Args:
        code (str): The generated code to review
        user_query (str): The original user query that generated this code
        
    Returns:
        tuple: (score: int, status: str) where:
            - score: A number between 0-100 indicating code quality
            - status: Either "ACCEPTED" or "REJECTED"
    """
    issues = _static_checks(code, user_query)
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
    )
    
    system_prompt = """
    You are a code quality evaluator. Review the code and user query, then provide:
    1. A score from 0-100 based on code quality, correctness, and alignment with requirements
    2. A status of either "ACCEPTED" or "REJECTED"
    
    Format your response exactly as:
    SCORE: [0-100]
    STATUS: [ACCEPTED/REJECTED]
    """
    
    response = llm.invoke(f"{system_prompt}\n\nUser Query: {user_query}\n\nCode:\n{code}")
    response_text = getattr(response, "content", str(response)).strip()
    
    score = 50 
    status = "ACCEPTED" 
    
    lines = [line.strip() for line in response_text.split('\n') if line.strip()]
    for line in lines:
        if line.upper().startswith("SCORE:"):
            try:
                score = int(line.split(":")[1].strip())
                score = max(0, min(100, score))
            except (ValueError, IndexError):
                pass
        elif line.upper().startswith("STATUS:"):
            status = line.split(":")[1].strip().upper()
            if status not in ["ACCEPTED", "REJECTED"]:
                status = "ACCEPTED" 
    
    if issues and score > 70:
        score = 70
    
    if score < 50:
        status = "REJECTED"
    
    return score, status
