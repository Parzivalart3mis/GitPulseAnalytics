# executor_agent.py
import os
from langchain_experimental.utilities import PythonREPL

def execute_generated_code(code):
    python_tool = PythonREPL()
    output = python_tool.run(code)
    return output
