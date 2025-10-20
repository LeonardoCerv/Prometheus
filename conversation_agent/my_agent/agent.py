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
    state_key = "user_memory_slot"

    try:
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

# --- Tool 3: Stores a conversation summary point ---

def store_summary_point(summary_point: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Stores a key point from the conversation for later summarization.
    
    Args:
        summary_point: A brief note about what was discussed.
        tool_context: The context object provided by the ADK framework.
    """
    state_key = "conversation_points"
    
    try:
        # Get existing points or create new list
        points = tool_context.state.get(state_key, [])
        
        # Add new point
        points.append(summary_point)
        
        # Save back to state
        tool_context.state[state_key] = points
        
        print(f"\n*** DEBUG: Added conversation point: {summary_point} ***\n")
        
        return {"status": "OK", "message": "Point noted for summary"}
        
    except Exception as e:
        print(f"\n*** DEBUG: Error storing summary point: {e} ***\n")
        return {"status": "Error", "message": f"Error storing point: {e}"}

# --- Tool 4: Retrieves conversation summary ---

def get_conversation_summary(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Retrieves all stored conversation points to create a summary.
    
    Args:
        tool_context: The context object provided by the ADK framework.
    """
    state_key = "conversation_points"
    
    try:
        points = tool_context.state.get(state_key, [])
        
        if not points:
            print(f"\n*** DEBUG: No conversation points found ***\n")
            return {
                "status": "Empty", 
                "message": "No conversation points have been stored yet.",
                "points": []
            }
        
        print(f"\n*** DEBUG: Retrieved {len(points)} conversation points ***\n")
        
        return {
            "status": "Success",
            "point_count": len(points),
            "points": points
        }
        
    except Exception as e:
        print(f"\n*** DEBUG: Error getting summary: {e} ***\n")
        return {"status": "Error", "message": f"Error retrieving summary: {e}"}

# --- Wrap Tools ---
remember_tool = FunctionTool(remember_thing)
recall_tool = FunctionTool(recall_thing)
store_summary_tool = FunctionTool(store_summary_point)
get_summary_tool = FunctionTool(get_conversation_summary)

# --- Define The Agent ---
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant that can remember, recall, and summarize conversations.',
    
    instruction=(
        "You are a helpful, observant, and conversational assistant. "
        "Pay close attention to the entire conversation history to understand "
        "what the user is talking about. "
        "Answer their follow-up questions using the context from previous messages.\n\n"
        "IMPORTANT: Throughout the conversation, periodically use 'store_summary_point' to note "
        "key topics discussed (e.g., 'User asked for jokes', 'Discussed weather'). "
        "Store these notes naturally as the conversation progresses, not all at once.\n\n"
        "You also have special tools:\n"
        "- Use 'remember_thing' ONLY when the user explicitly asks you to 'remember' a specific fact.\n"
        "- Use 'recall_thing' ONLY when the user explicitly asks you to 'recall' or 'what did I tell you about'.\n"
        "- Use 'store_summary_point' periodically during conversation to note topics discussed.\n"
        "- Use 'get_conversation_summary' when the user asks for a summary of the conversation. "
        "Then present the points in a clear, narrative format."
    ),
    tools=[
        remember_tool,
        recall_tool,
        store_summary_tool,
        get_summary_tool
    ],
)