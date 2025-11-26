# writer_agent.py
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def get_code_from_prompt(user_query):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        openai_api_key=OPENAI_API_KEY,
    )
    system_prompt = (
        "You are a Python and SQL data analyst with access to the following PostgreSQL tables and schemas:\n\n"
        "Table: github_issues\n"
        "  repo VARCHAR(50)\n"
        "  number INTEGER\n"
        "  title TEXT\n"
        "  state VARCHAR(10)\n"
        "  created_at TIMESTAMP\n"
        "  closed_at TIMESTAMP\n"
        "  labels TEXT\n\n"
        "Table: github_repos\n"
        "  repo VARCHAR(50) PRIMARY KEY\n"
        "  stars INTEGER\n"
        "  forks INTEGER\n\n"
        "Table: github_pulls\n"
        "  repo VARCHAR(50)\n"
        "  number INTEGER\n"
        "  title TEXT\n"
        "  state VARCHAR(10)\n"
        "  created_at TIMESTAMP\n"
        "  merged_at TIMESTAMP\n"
        "  closed_at TIMESTAMP\n"
        "  user_login TEXT\n"
        "  labels TEXT\n\n"
        "Table: github_commits\n"
        "  repo VARCHAR(50)\n"
        "  sha VARCHAR(50) PRIMARY KEY\n"
        "  author_login TEXT\n"
        "  committed_at TIMESTAMP\n"
        "  message TEXT\n\n"
        "For every user analytics question, generate ONLY the complete executable Python code with all necessary imports. "
        "For time series forecasting, always use 'from prophet import Prophet'; do not use 'fbprophet'."
        "The code must run as-is, without missing variables, functions, or steps. "
        "Visualizations: generate code for line chart, pie chart, bar chart, or stack-bar chart using matplotlib or pandas plotting as requested. Do NOT call plt.show(); simply produce the Figure, as the host application will display it using st.pyplot().\n"
        "using pandas and psycopg2. Your code must use this connection:\n"
        "conn = psycopg2.connect(\n"
        "    dbname='spm_db',\n"
        "    user='postgres',\n"
        "    password='admin',\n"
        "    host='localhost',\n"
        "    port=5432\n"
        ")\n"
        "Do NOT use input() or file I/O. Output only clean executable Python code (no comments, markdown, or explanation).\n"
        "The Python code must be 100 percenet complete and runnable, with all imports, all parentheses closed, all code blocks finished, and no incomplete lines. Do not end the code mid-line. Never return truncated code. Output all lines required, especially at the end of the block.\n"
        "User prompt: {user_query}"
    )
    prompt = PromptTemplate.from_template(system_prompt)
    final_prompt = prompt.format(user_query=user_query)
    # LLM generate code string
    code = llm.invoke(final_prompt)
    return code
