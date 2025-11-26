import streamlit as st
from writer_agent import get_code_from_prompt
from executor_agent import execute_generated_code
import matplotlib.pyplot as plt

st.title("GitHub Analytics (Modular Agent Pipeline)")

user_query = st.text_area("Enter your analytics question:", height=100)
if st.button("Run Agent") and user_query.strip():
    # Step 1: Writer agent – LLM generates Python code
    llm_message = get_code_from_prompt(user_query)
    # Extract 'content' attribute if present (for AIMessage), else use as string
    code = getattr(llm_message, "content", llm_message)
    # Remove markdown formatting if present
    code = code.strip()
    if code.startswith("```python"):
        code = code[9:]
    elif code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-6]
    code = code.strip()
    st.subheader("Generated Python code:")
    st.code(code, language="python")

    # Step 2: Executor agent – runs generated code
    try:
        result = execute_generated_code(code)
        st.subheader("Execution Result:")
        st.write(result)
        # Display any active matplotlib figure (if code produced a plot)
        fig = plt.gcf()
        if fig and len(fig.get_axes()) > 0:
            st.pyplot(fig)
            plt.clf()
    except Exception as e:
        st.error(f"Execution error: {e}")

st.markdown("---")
st.write("Tables: github_issues, github_repos, github_pulls, github_commits")