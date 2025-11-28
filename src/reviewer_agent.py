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
    issues = _static_checks(code, user_query)
    if issues:
        feedback = "\n".join(issues)
        return False, feedback
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
    )
    system_and_prompt = (
        "You are a precise Python code reviewer for a data analytics agent. "
        "Review for syntax, completeness, and logical correctness relative to the user question. "
        "Constraints and policies:\n"
        "- Database: must use psycopg2 with the exact provided connection string.\n"
        "- I/O: do not use input() or any file I/O (open()).\n"
        "- Plotting: plt.show() is not allowed. Using matplotlib/plotly/seaborn is allowed.\n"
        "  Streamlit display is allowed via st.write, st.dataframe, st.table, st.pyplot(fig) or st.pyplot() or st.pyplot(plt), and st.plotly_chart(fig).\n"
        "  Do not treat st.pyplot(plt) as an indirect call to plt.show(); it is acceptable.\n"
        "  Do NOT reject simply for using Streamlit display functions.\n"
        "- Forecasting libraries are only required when the user explicitly asks for forecasting. Do not require Prophet or statsmodels otherwise.\n"
        "- Prophet usage must follow best practices: fit once per repo (model = Prophet(); model.fit(df)), then forecast = model.predict(future), then fig = model.plot(forecast). Do not use Prophet().plot(forecast).\n"
        "- When the user asks for created issues, the code must use created_at (not closed_at).\n"
        "- Per-repo plotting should occur inside the per-repo loop to avoid referencing out-of-scope variables.\n"
        "- Displaying per-repo DataFrames separately is acceptable; do not require concatenation across repos unless requested.\n"
        "- Prefer correctness and executability. Lack of an explicit connection close or context manager is not grounds for rejection.\n\n"
        f"User question:\n{user_query}\n\n"
        f"Code to review:\n{code}\n\n"
        "Respond with either exactly:\n"
        "APPROVED\n"
        "or\n"
        "REJECTED\n<one-per-line concise issues>\n"
    )
    resp = llm.invoke(system_and_prompt)
    text = getattr(resp, "content", str(resp))
    up = text.upper()
    if "APPROVED" in up and "REJECT" not in up:
        return True, ""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    feedback = "\n".join(lines)
    return False, feedback
