import streamlit as st
import matplotlib.pyplot as plt
from orchestrator import run_multi_agent_pipeline

st.title("GitHub Analytics")

user_query = st.text_area("Enter your analytics question:", height=100)
if st.button("Run") and user_query.strip():
    result = run_multi_agent_pipeline(user_query=user_query)

    st.subheader("Final Python code:")
    st.code(result["code"], language="python")

    st.subheader("Execution Result:")
    if result["execution_error"]:
        st.error(result["execution_error"])
    else:
        st.write(result["execution_result"])
        fig = plt.gcf()
        if fig and len(fig.get_axes()) > 0:
            st.pyplot(fig)
            plt.clf()

st.markdown("---")
st.write("Tables: github_issues, github_repos, github_pulls, github_commits")