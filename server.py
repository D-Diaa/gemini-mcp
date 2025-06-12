"""Gemini MCP Server

Enables Collaboration with Google's Gemini AI
"""

import os
from typing import Optional
from dotenv import load_dotenv

from mcp.server import FastMCP

load_dotenv()

mcp = FastMCP("gemini", description="Gemini AI collaboration server")

# Initialize Gemini
try:
    import google.generativeai as genai
    
    # Get API key from environment or use the one provided during setup
    API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
    MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-2.5-flash-preview-05-20")
    if API_KEY == "YOUR_API_KEY_HERE":
        raise ValueError("Please set your Gemini API key in the GEMINI_API_KEY environment variable")
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
    GEMINI_AVAILABLE = True
except Exception as e:
    GEMINI_AVAILABLE = False
    GEMINI_ERROR = str(e)


def call_gemini(prompt: str, temperature: float = 0.5, system_instruction: Optional[str] = None) -> str:
    """Call Gemini and return response with enhanced error handling"""
    try:
        # Create model with system instruction if provided
        current_model = model
        if system_instruction:
            current_model = genai.GenerativeModel(
                MODEL_NAME,
                system_instruction=system_instruction
            )
        
        response = current_model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=8192,
            )
        )
        
        if not response.text:
            return "Error: Gemini returned an empty response. This may be due to content filtering or API limitations."
        
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "rate" in error_msg.lower():
            return f"Rate limit or quota exceeded. Please try again later. Details: {error_msg}"
        elif "safety" in error_msg.lower() or "filter" in error_msg.lower():
            return f"Content was filtered due to safety policies. Please rephrase your request. Details: {error_msg}"
        else:
            return f"Error calling Gemini: {error_msg}"


@mcp.tool()
def ask_gemini(prompt: str, temperature: float = 0.5, context: str = "", persona: str = "") -> str:
    """Ask Gemini a question and get the response directly in context
    
    Args:
        prompt: The question or prompt for Gemini
        temperature: Temperature for response (0.0-1.0)
        context: Additional context to provide to Gemini
        persona: Persona for Gemini to adopt (e.g., "senior architect", "security expert")
    
    Returns:
        Gemini's response as a string
    """
    if not GEMINI_AVAILABLE:
        return f"❌ Gemini not available: {GEMINI_ERROR}"
    
    # Build enhanced prompt with context and persona
    enhanced_prompt = prompt
    system_instruction = None
    
    if persona:
        system_instruction = f"You are acting as a {persona}. Respond in character with appropriate expertise and perspective."
    
    if context:
        enhanced_prompt = f"Context: {context}\n\nQuery: {prompt}"
    
    response = call_gemini(enhanced_prompt, temperature, system_instruction)
    return f"🤖 GEMINI RESPONSE:\n\n{response}"

@mcp.tool()
def server_info() -> str:
    """Get server status and error information
    
    Returns:
        Dictionary with server status information
    """
    info = {
        "server_name": "Gemini MCP Server",
        "gemini_available": GEMINI_AVAILABLE,
        "model": MODEL_NAME if GEMINI_AVAILABLE else "N/A",
    }
    
    if not GEMINI_AVAILABLE:
        info["error"] = GEMINI_ERROR
    
    # Format as readable string
    status = "✅ ONLINE" if GEMINI_AVAILABLE else "❌ OFFLINE"
    output = f"🤖 GEMINI MCP SERVER STATUS: {status}\n\n"
    
    for key, value in info.items():
        if key == "error":
            output += f"Error: {value}\n"
        else:
            output += f"{key.replace('_', ' ').title()}: {value}\n"
    
    return output


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()