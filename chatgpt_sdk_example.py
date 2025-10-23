#!/usr/bin/env python3
"""
Simple ChatGPT SDK example with MCP tools integration
"""

import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Set this: export OPENAI_API_KEY='your-key'
)

def chat_with_tools():
    """
    Example of using ChatGPT with your MCP tools
    """
    
    # Define your MCP tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "weather",
                "description": "Get current weather information for any location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city or location to get weather for"
                        },
                        "units": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "default": "celsius"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Perform mathematical calculations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to evaluate"
                        }
                    },
                    "required": ["expression"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "text_analysis",
                "description": "Analyze text for sentiment, word count, or summary",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to analyze"
                        },
                        "analysis_type": {
                            "type": "string",
                            "enum": ["sentiment", "word_count", "summary"],
                            "default": "sentiment"
                        }
                    },
                    "required": ["text"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "file_search",
                "description": "Search for files in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for files"
                        },
                        "file_type": {
                            "type": "string",
                            "description": "Optional file type filter"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    ]
    
    # Your MCP server URL
    MCP_SERVER_URL = "https://gptintegration-gkhz75qlq-vijays-projects-83d7f1fb.vercel.app"
    
    def call_mcp_tool(tool_name, arguments):
        """
        Call your MCP server tool
        """
        import requests
        
        response = requests.post(
            f"{MCP_SERVER_URL}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
        )
        
        result = response.json()
        if "result" in result:
            return result["result"]["content"][0]["text"]
        else:
            return f"Error: {result}"
    
    # Example conversation
    messages = [
        {
            "role": "user",
            "content": "What's the weather in London and calculate 25 * 4?"
        }
    ]
    
    print("🤖 ChatGPT with MCP Tools Example")
    print("=" * 40)
    
    try:
        # Get ChatGPT response with tool calls
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        print(f"User: {messages[0]['content']}")
        print(f"ChatGPT: {message.content}")
        
        # Handle tool calls
        if message.tool_calls:
            print("\n🔧 Tool calls detected:")
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = eval(tool_call.function.arguments)  # Parse JSON
                
                print(f"  - Calling {tool_name} with args: {tool_args}")
                
                # Call your MCP server
                result = call_mcp_tool(tool_name, tool_args)
                print(f"  - Result: {result}")
                
                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Get final response from ChatGPT
            final_response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                tools=tools
            )
            
            print(f"\nFinal ChatGPT Response: {final_response.choices[0].message.content}")
    
    except Exception as e:
        print(f"Error: {e}")
        print("\n💡 Make sure to set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")

if __name__ == "__main__":
    chat_with_tools()
