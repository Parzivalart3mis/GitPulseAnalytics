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

        1) Connects to Postgres using:

        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="spm_db",
            user="postgres",
            password="admin"
        )

        2) Loads the relevant table(s) into pandas DataFrame(s).
        3) Answers the user query: "{user_query}"
        4) Displays results in Streamlit:
        - Text: st.write(...) or st.markdown(...)
        - Tables: st.dataframe(...) or st.table(...)
        - Charts: matplotlib/plotly/seaborn via st.pyplot(fig) or st.plotly_chart(fig); do NOT call plt.show().
        - Only generate charts when the user explicitly asks for a chart; otherwise return text/table outputs.
        5) If forecasting:
        - Use Prophet for issues (import as: from prophet import Prophet).
        - Use statsmodels (ARIMA/SARIMA) for commits or pull requests.
        - Forecast 30 days ahead.
        - For closed issues use closed_at; for created issues use created_at.
        - For per-repo forecasting: fit once per repo, predict, then plot with model.plot(forecast) inside the loop.
        - When creating per-repo forecast outputs, do:
          • Create a pandas Series per repo: forecast.set_index('ds')['yhat'].rename('forecasted_closed_issues_<sanitized_repo>' or 'forecasted_created_issues_<sanitized_repo>').
          • Append these Series to a list (not DataFrames).
          • Finally, use pd.concat(series_list, axis=1) to align by the 'ds' index (this prevents duplicate 'ds' columns).
          • Do NOT include 'ds' as a column in the concatenated object; it should be the index only.
          • Sort the index and consider fillna(0) if appropriate for display.
        - Sanitize repo names for column naming: replace all non-alphanumeric characters with underscores (e.g., using Python's re.sub). Import re if needed.
        6) No placeholders, no pseudo-code. Do NOT use input() or any file I/O.
        7) Import all required libraries (pandas, psycopg2, streamlit, plotting libs, etc.).

        Return ONLY executable Python code.
        """
    )
    prompt = PromptTemplate.from_template(system_prompt)
    final_prompt = prompt.format(user_query=user_query)
    # LLM generate code string
    code = llm.invoke(final_prompt)
    return code
