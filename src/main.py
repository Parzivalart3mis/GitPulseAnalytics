import streamlit as st
import matplotlib.pyplot as plt
from orchestrator import run_multi_agent_pipeline

st.title("GitHub Analytics (Multi-Agent Pipeline)")

user_query = st.text_area("Enter your analytics question:", height=100)
max_iters = st.slider("Max review iterations", min_value=1, max_value=5, value=3, step=1)
if st.button("Run Agents") and user_query.strip():
    result = run_multi_agent_pipeline(user_query=user_query, max_iterations=max_iters)

    st.subheader("Review Feedback Log")
    if result["review_feedback_log"]:
        for i, fb in enumerate(result["review_feedback_log"], start=1):
            st.markdown(f"- Iteration {i} feedback:")
            st.code(fb)
    else:
        st.write("No review feedback; code approved on first pass.")

    st.subheader("Final Python code:")
    st.code(result["code"], language="python")

    if result["approved"]:
        st.subheader("Execution Result:")
        if result["execution_error"]:
            st.error(result["execution_error"])
        else:
            st.write(result["execution_result"])
            fig = plt.gcf()
            if fig and len(fig.get_axes()) > 0:
                st.pyplot(fig)
                plt.clf()
    else:
        st.error("Code was not approved after the maximum review iterations. Please adjust your question and try again.")

st.markdown("---")
st.write("Tables: github_issues, github_repos, github_pulls, github_commits")