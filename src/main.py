import streamlit as st
import matplotlib.pyplot as plt
from orchestrator import run_multi_agent_pipeline

def get_review_color(score: int) -> str:
    if score >= 80:
        return "#4CAF50"
    elif score >= 60:
        return "#FFC107"
    else:
        return "#F44336" 

st.title("GitHub Analytics")

user_query = st.text_area("Enter your analytics question:", height=100)
if st.button("Run") and user_query.strip():
    with st.spinner('Generating and executing code...'):
        result = run_multi_agent_pipeline(user_query=user_query)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Review Status", result["review_status"])
    with col2:
        score = result["review_score"]
        st.metric("Code Quality Score", f"{score}/100")
    
    st.progress(score / 100, "Code Quality")
    
    st.subheader("Generated Python Code:")
    st.code(result["code"], language="python")

    st.subheader("Execution Result:")
    if result["execution_error"]:
        st.error(f"Error during execution: {result['execution_error']}")
    else:
        if result["execution_result"] is not None:
            st.write(result["execution_result"])
        
        fig = plt.gcf()
        if fig and len(fig.get_axes()) > 0:
            st.pyplot(fig)
            plt.clf()
        elif not result["execution_result"] and not result["execution_error"]:
            st.info("The code executed successfully.")

st.markdown("---")
st.caption("Note: The system will execute the generated code regardless of the review status.")
st.write("Tables: github_issues, github_repos, github_pulls, github_commits")