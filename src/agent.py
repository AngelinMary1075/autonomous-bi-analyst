import httpx
import json
import re
from src.tools import TOOLS_MANIFEST

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """You are an Autonomous Business Intelligence Analyst.
You have access to the following tools:
- execute_sql_query: Use this to fetch numbers, sales records, and run aggregations. Expects a valid SQL statement.
- generate_revenue_chart: Use this when the user explicitly asks for a visual chart or plot. Takes no arguments.

You must follow a strict ReAct loop format:
Thought: Reflect on what data you need to answer the question.
Action: tool_name(argument_if_any)
Observation: The output from the tool will be provided to you here.
... (this Thought/Action/Observation can repeat)
Final Answer: Provide your final executive business insights and recommendations based strictly on your observations.

Begin!"""

def call_ollama(prompt: str) -> str:
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0}  # Low temperature for analytical consistency
    }
    with httpx.Client(timeout=120.0) as client:
        response = client.post(OLLAMA_URL, json=payload)
        return response.json().get("response", "")

def run_bi_agent(user_query: str) -> dict:
    agent_history = f"{SYSTEM_PROMPT}\n\nUser Question: {user_query}\n"
    
    # Allow up to 4 reasoning steps to prevent infinite loops
    for step in range(4):
        response = call_ollama(agent_history)
        agent_history += response
        
        print(f"--- [Agent Step {step+1}] ---\n{response}\n")
        
        if "Final Answer:" in response:
            final_answer = response.split("Final Answer:")[-1].strip()
            return {"status": "success", "output": final_answer}
        
        # Parse for Action pattern: tool_name(args)
        action_match = re.search(r"Action:\s*(\w+)\((.*)\)", response)
        if action_match:
            tool_name = action_match.group(1)
            tool_arg = action_match.group(2).strip("'\" ")
            
            if tool_name in TOOLS_MANIFEST:
                tool_func = TOOLS_MANIFEST[tool_name]["func"]
                # Execute tool
                observation = tool_func(tool_arg) if tool_arg else tool_func()
                agent_history += f"\nObservation: {observation}\n"
            else:
                agent_history += f"\nObservation: Error - Tool '{tool_name}' does not exist.\n"
        else:
            # If the LLM failed to format a proper Action but didn't give a Final Answer
            return {"status": "partial", "output": response}
            
    return {"status": "timeout", "output": "Agent timed out without finding a conclusive answer."}