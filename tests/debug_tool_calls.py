#!/usr/bin/env python3
"""
Debug script to see exactly which tools ChatGPT calls
"""

import os
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Set this: export OPENAI_API_KEY='your-key'
)

def debug_chat_with_tools(user_question):
    """
    Debug ChatGPT tool calls with detailed logging
    """
    
    # Your MCP server URL
    MCP_SERVER_URL = "https://gptintegration-drr8jasbc-vijays-projects-83d7f1fb.vercel.app"
    
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
    
    def call_mcp_tool(tool_name, arguments):
        """
        Call your MCP server tool with logging
        """
        import requests
        
        print(f"🔧 CALLING MCP TOOL: {tool_name}")
        print(f"   Arguments: {json.dumps(arguments, indent=2)}")
        
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
            tool_result = result["result"]["content"][0]["text"]
            print(f"   ✅ Tool Result: {tool_result}")
            return tool_result
        else:
            error_msg = f"Error: {result}"
            print(f"   ❌ Tool Error: {error_msg}")
            return error_msg
    
    # Start conversation
    messages = [
        {
            "role": "user",
            "content": user_question
        }
    ]
    
    print(f"🤖 USER QUESTION: {user_question}")
    print("=" * 60)
    
    try:
        # Get ChatGPT response with tool calls
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        print(f"💬 ChatGPT Response: {message.content}")
        
        # Handle tool calls
        if message.tool_calls:
            print(f"\n🔧 TOOL CALLS DETECTED: {len(message.tool_calls)}")
            print("-" * 40)
            
            for i, tool_call in enumerate(message.tool_calls, 1):
                tool_name = tool_call.function.name
                tool_args = eval(tool_call.function.arguments)  # Parse JSON
                
                print(f"\n{i}. TOOL CALL #{i}:")
                print(f"   Tool Name: {tool_name}")
                print(f"   Call ID: {tool_call.id}")
                print(f"   Arguments: {json.dumps(tool_args, indent=2)}")
                
                # Call your MCP server
                result = call_mcp_tool(tool_name, tool_args)
                
                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Get final response from ChatGPT
            print(f"\n🔄 Getting final response from ChatGPT...")
            final_response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                tools=tools
            )
            
            print(f"\n💬 FINAL CHATGPT RESPONSE:")
            print(f"   {final_response.choices[0].message.content}")
        else:
            print("\n❌ No tool calls detected")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure to set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")

def test_various_questions():
    """
    Test different types of questions to see which tools are called
    """
    
    test_questions = [
        "What's the weather in Tokyo?",
        "Calculate 25 * 4 + 10",
        "What's the sentiment of this text: 'I love this product!'",
        "Search for PDF files about project management",
        "What's the weather in London and calculate 15 * 8?",
        "Analyze the sentiment of 'This is terrible' and search for documents",
        "How many words are in this sentence: 'Hello world this is a test'"
    ]
    
    print("🧪 TESTING VARIOUS QUESTIONS")
    print("=" * 60)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*20} TEST {i} {'='*20}")
        debug_chat_with_tools(question)
        print(f"\n{'='*50}")

if __name__ == "__main__":
    print("🔍 ChatGPT Tool Call Debugger")
    print("=" * 60)
    
    # Test a specific question
    test_question = input("Enter a question to test (or press Enter for default): ").strip()
    if not test_question:
        test_question = "What's the weather in Paris and calculate 10 + 5?"
    
    debug_chat_with_tools(test_question)
    
    # Uncomment to test multiple questions
    # test_various_questions()
