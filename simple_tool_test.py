#!/usr/bin/env python3
"""
Simple example showing how to verify tool calls
"""

import requests
import json

def test_tool_call_flow():
    """
    Show the complete flow of a tool call
    """
    
    MCP_SERVER_URL = "https://gptintegration-4l8whbu5h-vijays-projects-83d7f1fb.vercel.app"
    
    print("🔍 TOOL CALL VERIFICATION EXAMPLE")
    print("=" * 50)
    
    # Example: User asks "What's the weather in Tokyo?"
    user_question = "What's the weather in Tokyo?"
    print(f"👤 User asks: {user_question}")
    
    # ChatGPT would decide to call the weather tool
    print(f"\n🤖 ChatGPT decides to call: weather tool")
    
    # Show the tool call that would be made
    tool_call = {
        "name": "weather",
        "arguments": {
            "location": "Tokyo",
            "units": "celsius"
        }
    }
    
    print(f"🔧 Tool call details:")
    print(f"   Tool: {tool_call['name']}")
    print(f"   Arguments: {json.dumps(tool_call['arguments'], indent=2)}")
    
    # Make the actual call to your MCP server
    print(f"\n📡 Calling MCP server...")
    
    response = requests.post(
        f"{MCP_SERVER_URL}/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_call["name"],
                "arguments": tool_call["arguments"]
            }
        }
    )
    
    result = response.json()
    
    if "result" in result:
        tool_result = result["result"]["content"][0]["text"]
        print(f"✅ Tool result: {tool_result}")
        
        # ChatGPT would then use this result in its response
        print(f"\n💬 ChatGPT's final response would be:")
        print(f"   'The weather in Tokyo is {tool_result.split(': ')[1] if ': ' in tool_result else tool_result}'")
    else:
        print(f"❌ Error: {result}")

def show_tool_mapping():
    """
    Show which questions trigger which tools
    """
    
    print(f"\n📋 TOOL MAPPING GUIDE")
    print("=" * 50)
    
    mappings = [
        {
            "question_type": "Weather questions",
            "examples": [
                "What's the weather in London?",
                "How's the weather in Tokyo?",
                "Is it sunny in Paris?"
            ],
            "tool_called": "weather",
            "parameters": "location, units (optional)"
        },
        {
            "question_type": "Math/Calculation questions",
            "examples": [
                "Calculate 25 * 4",
                "What's 100 + 50?",
                "Solve 15 * 8 - 20"
            ],
            "tool_called": "calculator",
            "parameters": "expression"
        },
        {
            "question_type": "Text analysis questions",
            "examples": [
                "What's the sentiment of this text?",
                "Count the words in this sentence",
                "Summarize this paragraph"
            ],
            "tool_called": "text_analysis",
            "parameters": "text, analysis_type (sentiment/word_count/summary)"
        },
        {
            "question_type": "File search questions",
            "examples": [
                "Search for PDF files",
                "Find documents about project",
                "Look for .txt files"
            ],
            "tool_called": "file_search",
            "parameters": "query, file_type (optional)"
        }
    ]
    
    for mapping in mappings:
        print(f"\n🔧 {mapping['question_type']}")
        print(f"   Tool: {mapping['tool_called']}")
        print(f"   Parameters: {mapping['parameters']}")
        print(f"   Examples:")
        for example in mapping['examples']:
            print(f"     - '{example}'")

if __name__ == "__main__":
    test_tool_call_flow()
    show_tool_mapping()
