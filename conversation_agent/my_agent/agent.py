from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool, ToolContext
from typing import Dict, Any

# --- Tool 1: Remembers a fact (Writes to State) ---

def remember_thing(thing_to_remember: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Stores a piece of information in the session state.
    
    Args:
        thing_to_remember: The string of text to remember.
        tool_context: The context object provided by the ADK framework.
    """
    # Use a key to save the data in the context's state
    # We can make up any key we want, e.g., "user_memory_slot"
    state_key = "user_memory_slot"
    
    try:
        tool_context.state[state_key] = thing_to_remember
        
        print(f"\n*** DEBUG: Saved to state (key='{state_key}'): {thing_to_remember} ***\n")
        
        return {"status": "OK", "message": f"I will remember: {thing_to_remember}"}
        
    except Exception as e:
        print(f"\n*** DEBUG: Error saving to state: {e} ***\n")
        return {"status": "Error", "message": f"I had trouble remembering that: {e}"}

# --- Tool 2: Recalls a fact (Reads from State) ---

def recall_thing(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Retrieves a piece of information from the session state.
    
    Args:
        tool_context: The context object provided by the ADK framework.
    """
    state_key = "user_memory_slot" # Must be the same key used to save

    try:
        # Use .get() to safely read the data from the context's state
        recalled_info = tool_context.state.get(state_key)
        
        if recalled_info:
            print(f"\n*** DEBUG: Recalled from state (key='{state_key}'): {recalled_info} ***\n")
            return {"status": "Found", "recalled_message": recalled_info}
        else:
            print(f"\n*** DEBUG: Nothing found in state for key '{state_key}' ***\n")
            return {"status": "Not Found", "message": "I don't seem to have anything remembered."}

    except Exception as e:
        print(f"\n*** DEBUG: Error reading from state: {e} ***\n")
        return {"status": "Error", "message": f"I had trouble recalling: {e}"}

# --- Wrap Tools ---
remember_tool = FunctionTool(remember_thing)
recall_tool = FunctionTool(recall_thing)

# --- Define The Agent ---
# The 'adk run' command will automatically find this 'root_agent' variable.
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant that can remember and recall information.',
    
    # --- THIS IS THE PART TO CHANGE ---
    instruction=(
        "You are a helpful, observant, and conversational assistant. "
        "Pay close attention to the entire conversation history to understand "
        "what the user is talking about. "
        "Answer their follow-up questions using the context from previous messages.\n\n"
        "You also have special tools: "
        "- Use 'remember_thing' ONLY when the user explicitly asks you to 'remember' a specific fact."
        "- Use 'recall_thing' ONLY when the user explicitly asks you to 'recall' or 'what did I tell you about'."
    ),
    tools=[
        remember_tool,
        recall_tool
    ],
)