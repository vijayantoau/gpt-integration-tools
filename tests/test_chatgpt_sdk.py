#!/usr/bin/env python3
"""
Test script for ChatGPT SDK integration with MCP tools
"""

import os
from openai import OpenAI

# Your MCP server URL
MCP_SERVER_URL = "https://gptintegration-4l8whbu5h-vijays-projects-83d7f1fb.vercel.app"

def test_chatgpt_with_tools():
    """
    Test ChatGPT SDK with MCP tools integration
    """
    
    # Initialize OpenAI client
    # You'll need to set your OpenAI API key
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")  # Set this environment variable
    )
    
    print("🤖 Testing ChatGPT SDK with MCP Tools")
    print("=" * 50)
    
    # Test 1: Weather Tool
    print("\n🌤️  Testing Weather Tool...")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user", 
                    "content": "What's the weather like in Paris? Use the weather tool."
                }
            ],
            tools=[{
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
                                "default": "celsius",
                                "description": "Temperature units"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }],
            tool_choice="auto"
        )
        
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"Error testing weather tool: {e}")
    
    # Test 2: Calculator Tool
    print("\n🧮 Testing Calculator Tool...")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user", 
                    "content": "Calculate 25 * 4 + 10 using the calculator tool."
                }
            ],
            tools=[{
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
            }],
            tool_choice="auto"
        )
        
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"Error testing calculator tool: {e}")
    
    # Test 3: Text Analysis Tool
    print("\n📝 Testing Text Analysis Tool...")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user", 
                    "content": "Analyze the sentiment of this text: 'I absolutely love this amazing product! It is wonderful and makes me so happy.' Use the text analysis tool."
                }
            ],
            tools=[{
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
                                "default": "sentiment",
                                "description": "Type of analysis to perform"
                            }
                        },
                        "required": ["text"]
                    }
                }
            }],
            tool_choice="auto"
        )
        
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"Error testing text analysis tool: {e}")

def test_mcp_server_directly():
    """
    Test MCP server directly (without ChatGPT SDK)
    """
    import requests
    import json
    
    print("\n🔧 Testing MCP Server Directly")
    print("=" * 50)
    
    # Test MCP initialize
    print("\n1. Testing MCP Initialize...")
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1.0.0"}
                }
            }
        )
        result = response.json()
        print(f"✅ Initialize successful: {result['result']['serverInfo']['name']}")
    except Exception as e:
        print(f"❌ Initialize failed: {e}")
    
    # Test tools list
    print("\n2. Testing Tools List...")
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
        )
        result = response.json()
        tools = result['result']['tools']
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool['name']}: {tool['description']}")
    except Exception as e:
        print(f"❌ Tools list failed: {e}")
    
    # Test each tool
    tools_to_test = [
        {
            "name": "weather",
            "arguments": {"location": "Tokyo", "units": "celsius"}
        },
        {
            "name": "calculator", 
            "arguments": {"expression": "15 * 8 - 20"}
        },
        {
            "name": "text_analysis",
            "arguments": {"text": "This is amazing!", "analysis_type": "sentiment"}
        },
        {
            "name": "file_search",
            "arguments": {"query": "document", "file_type": "pdf"}
        }
    ]
    
    for i, tool_test in enumerate(tools_to_test, 3):
        print(f"\n{i}. Testing {tool_test['name']} tool...")
        try:
            response = requests.post(
                f"{MCP_SERVER_URL}/mcp",
                json={
                    "jsonrpc": "2.0",
                    "id": i,
                    "method": "tools/call",
                    "params": {
                        "name": tool_test["name"],
                        "arguments": tool_test["arguments"]
                    }
                }
            )
            result = response.json()
            if "result" in result:
                print(f"✅ {tool_test['name']}: {result['result']['content'][0]['text']}")
            else:
                print(f"❌ {tool_test['name']} failed: {result}")
        except Exception as e:
            print(f"❌ {tool_test['name']} failed: {e}")

if __name__ == "__main__":
    print("🚀 GPT Integration Tools - ChatGPT SDK Test")
    print("=" * 60)
    
    # Test MCP server directly first
    test_mcp_server_directly()
    
    # Test with ChatGPT SDK (requires API key)
    print("\n" + "=" * 60)
    print("📋 To test with ChatGPT SDK:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
    print("2. Uncomment the line below to run ChatGPT SDK tests")
    print("3. Run: python3 test_chatgpt_sdk.py")
    
    # Uncomment the line below to test with ChatGPT SDK
    # test_chatgpt_with_tools()


