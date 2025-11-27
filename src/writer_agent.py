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
        """
        You are a Python and SQL data analyst with access to the following PostgreSQL tables and schemas:

        Table: github_issues
        repo VARCHAR(50)
        number INTEGER
        title TEXT
        state VARCHAR(10)
        created_at TIMESTAMP
        closed_at TIMESTAMP
        labels TEXT

        Table: github_repos
        repo VARCHAR(50) PRIMARY KEY
        stars INTEGER
        forks INTEGER

        Table: github_pulls
        repo VARCHAR(50)
        number INTEGER
        title TEXT
        state VARCHAR(10)
        created_at TIMESTAMP
        merged_at TIMESTAMP
        closed_at TIMESTAMP
        user_login TEXT
        labels TEXT

        Table: github_commits
        repo VARCHAR(50)
        sha VARCHAR(50) PRIMARY KEY
        author_login TEXT
        committed_at TIMESTAMP
        message TEXT

        DATABASE CONNECTION:
        Use this exact connection setup:
        conn = psycopg2.connect(
            dbname='spm_db',
            user='postgres',
            password='admin',
            host='localhost',
            port=5432
        )

        CORE REQUIREMENTS:
        1. Load relevant table(s) into pandas DataFrame(s)
        2. Answer the user query: "{user_query}"
        3. Output textual/table results OR generate charts (matplotlib/plotly/seaborn)
        4. Contains NO placeholders and NO pseudo-code
        5. Display results in Streamlit using st.dataframe() or st.table() (NEVER use print())
        6. Give only details requested - plot graphs ONLY when explicitly asked
        7. Always rename forecast columns to unique names (e.g., forecasted_commits) to avoid conflicts
        8. Do NOT attempt database insertions for forecast output; just display it
        9. For time series forecasting, use 'from prophet import Prophet' (NOT 'fbprophet')

        OUTPUT TYPE RULES:

        1. TEXTUAL QUERIES:
        - Output ONLY text using st.write() or st.markdown()
        - NO charts, plots, or figures
        - Display results clearly using pandas DataFrame with st.dataframe()

        2. TABULAR QUERIES:
        - Output a clean table using st.dataframe() or st.table()
        - Do NOT generate charts unless explicitly requested

        3. CHART/GRAPH QUERIES:
        - Output figure using matplotlib, plotly, or seaborn (using Streamlit for display is allowed)
        - Use st.pyplot(fig) or st.pyplot() or st.pyplot(plt) for matplotlib/seaborn
        - Use st.plotly_chart(fig) for plotly
        - Do NOT call plt.show()
        - Chart should directly answer the query

        4. FORECAST QUERIES:
        - For issues created/closed: Use Prophet
        - For commits or pull requests: Use statsmodels (ARIMA/SARIMA)
        - Forecast for the next 30 days
        - Plot forecast with proper x/y labels and title
        - Display forecast DataFrame using st.dataframe()

        STATSMODELS FORECASTING WORKFLOW:
        1. Identify correct table:
        - Pull requests → 'github_pulls' table
        - Commits → 'github_commits' table
        - Issues created/closed → 'github_issues' table

        2. For each repository:
        - Filter data for that repository
        - Convert date column to datetime
        - Set as DatetimeIndex
        - Resample daily: df.resample('D').sum().fillna(0)

        3. Fit SARIMAX model for 30-day forecast
        4. Create forecast DataFrame with columns: ['date', 'forecasted_<metric>']
        where <metric> is commits, pull_requests, or issues
        5. Display results using st.dataframe()
        6. If query is textual/tabular, do NOT generate plots
        7. If query explicitly asks for chart, plot using matplotlib or plotly
        8. Do NOT insert/update any tables in database

        CODE REQUIREMENTS:
        - Generate ONLY complete executable Python code with all necessary imports
        - Code must run as-is without missing variables, functions, or steps
        - Do NOT use input() or file I/O
        - Output only clean executable Python code (no comments, markdown, or explanation)
        - Code must be 100% complete and runnable with all imports, all parentheses closed, all code blocks finished, and no incomplete lines
        - Do not end code mid-line or return truncated code
        - Output all lines required, especially at the end of the block
        - If using Streamlit outputs or charts, ensure `import streamlit as st` is included
        "User prompt: {user_query}"
        """
    )
    prompt = PromptTemplate.from_template(system_prompt)
    final_prompt = prompt.format(user_query=user_query)
    # LLM generate code string
    code = llm.invoke(final_prompt)
    return code

def revise_code(user_query: str, prior_code: str, feedback: str):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        openai_api_key=OPENAI_API_KEY,
    )
    system_prompt = (
        "You are a Python and SQL data analyst fixing previously generated code according to review feedback.\n\n"
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
        "DATABASE CONNECTION:\n"
        "Use this exact connection setup:\n"
        "conn = psycopg2.connect(\n"
        "    dbname='spm_db',\n"
        "    user='postgres',\n"
        "    password='admin',\n"
        "    host='localhost',\n"
        "    port=5432\n"
        ")\n\n"
        "REVISION REQUIREMENTS:\n"
        "1. Load relevant table(s) into pandas DataFrame(s)\n"
        "2. Address ALL feedback points from the review\n"
        "3. Fix errors, bugs, or logic issues identified in the feedback\n"
        "4. Output textual/table results OR generate charts (matplotlib/plotly/seaborn)\n"
        "5. Contains NO placeholders and NO pseudo-code\n"
        "6. Display results in Streamlit using st.dataframe() or st.table() (NEVER use print())\n"
        "7. Give only details requested - plot graphs ONLY when explicitly asked\n"
        "8. Always rename forecast columns to unique names (e.g., forecasted_commits) to avoid conflicts\n"
        "9. Do NOT attempt database insertions for forecast output; just display it\n"
        "10. For time series forecasting, use 'from prophet import Prophet' (NOT 'fbprophet')\n\n"
        "OUTPUT TYPE RULES:\n\n"
        "1. TEXTUAL QUERIES:\n"
        "   - Output ONLY text using st.write() or st.markdown()\n"
        "   - NO charts, plots, or figures\n"
        "   - Display results clearly using pandas DataFrame with st.dataframe()\n\n"
        "2. TABULAR QUERIES:\n"
        "   - Output a clean table using st.dataframe() or st.table()\n"
        "   - Do NOT generate charts unless explicitly requested\n\n"
        "3. CHART/GRAPH QUERIES:\n"
        "   - Output figure using matplotlib, plotly, or seaborn\n"
        "   - Use st.pyplot(fig) for matplotlib/seaborn\n"
        "   - Use st.plotly_chart(fig) for plotly\n"
        "   - Do NOT call plt.show()\n"
        "   - Chart should directly answer the query\n\n"
        "4. FORECAST QUERIES:\n"
        "   - For issues created/closed: Use Prophet\n"
        "   - For commits or pull requests: Use statsmodels (ARIMA/SARIMA)\n"
        "   - Forecast for the next 30 days\n"
        "   - Plot forecast with proper x/y labels and title\n"
        "   - Display forecast DataFrame using st.dataframe()\n\n"
        "STATSMODELS FORECASTING WORKFLOW:\n"
        "1. Identify correct table:\n"
        "   - Pull requests → 'github_pulls' table\n"
        "   - Commits → 'github_commits' table\n"
        "   - Issues created/closed → 'github_issues' table\n\n"
        "2. For each repository:\n"
        "   - Filter data for that repository\n"
        "   - Convert date column to datetime\n"
        "   - Set as DatetimeIndex\n"
        "   - Resample daily: df.resample('D').sum().fillna(0)\n\n"
        "3. Fit SARIMAX model for 30-day forecast\n"
        "4. Create forecast DataFrame with columns: ['date', 'forecasted_<metric>']\n"
        "   where <metric> is commits, pull_requests, or issues\n"
        "5. Display results using st.dataframe()\n"
        "6. If query is textual/tabular, do NOT generate plots\n"
        "7. If query explicitly asks for chart, plot using matplotlib or plotly\n"
        "8. Do NOT insert/update any tables in database\n\n"
        "CODE REQUIREMENTS:\n"
        "- Generate ONLY complete executable Python code with all necessary imports\n"
        "- Code must run as-is without missing variables, functions, or steps\n"
        "- Do NOT use input() or file I/O\n"
        "- Output only clean executable Python code (no comments, markdown, or explanation)\n"
        "- Code must be 100% complete and runnable with all imports, all parentheses closed, all code blocks finished, and no incomplete lines\n"
        "- Do not end code mid-line or return truncated code\n"
        "- Output all lines required, especially at the end of the block\n"
        "- If using Streamlit outputs or charts, ensure `import streamlit as st` is included\n\n"
        "User prompt: {user_query}\n"
        "Review feedback to address: {feedback}\n"
        "Prior code to revise follows:\n{prior_code}"
    )
    prompt = PromptTemplate.from_template(system_prompt)
    final_prompt = prompt.format(user_query=user_query, feedback=feedback, prior_code=prior_code)
    code = llm.invoke(final_prompt)
    return code
