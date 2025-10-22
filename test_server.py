#!/usr/bin/env python3
"""
Test script to verify the MCP server endpoints
"""

import requests
import json
import time
import subprocess
import sys
from threading import Thread

def test_endpoints():
    """Test all the server endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing MCP Server Endpoints...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health Check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health Check failed: {e}")
    
    # Test tools manifest
    try:
        response = requests.get(f"{base_url}/mcp/tools")
        print(f"✅ Tools Manifest: {response.status_code}")
        tools = response.json()
        print(f"   Available tools: {[tool['name'] for tool in tools['tools']]}")
    except Exception as e:
        print(f"❌ Tools Manifest failed: {e}")
    
    # Test weather tool
    try:
        weather_data = {"location": "New York", "units": "celsius"}
        response = requests.post(f"{base_url}/tools/weather", json=weather_data)
        print(f"✅ Weather Tool: {response.status_code}")
        result = response.json()
        print(f"   Location: {result['structuredContent']['location']}")
        print(f"   Temperature: {result['structuredContent']['temperature']}°C")
    except Exception as e:
        print(f"❌ Weather Tool failed: {e}")
    
    # Test calculator tool
    try:
        calc_data = {"expression": "2 + 2 * 3"}
        response = requests.post(f"{base_url}/tools/calculator", json=calc_data)
        print(f"✅ Calculator Tool: {response.status_code}")
        result = response.json()
        print(f"   Expression: {result['structuredContent']['expression']}")
        print(f"   Result: {result['structuredContent']['result']}")
    except Exception as e:
        print(f"❌ Calculator Tool failed: {e}")
    
    # Test text analysis tool
    try:
        text_data = {"text": "This is a great day!", "analysis_type": "sentiment"}
        response = requests.post(f"{base_url}/tools/text-analysis", json=text_data)
        print(f"✅ Text Analysis Tool: {response.status_code}")
        result = response.json()
        print(f"   Sentiment: {result['structuredContent']['sentiment']}")
    except Exception as e:
        print(f"❌ Text Analysis Tool failed: {e}")
    
    # Test file search tool
    try:
        search_data = {"query": "document", "file_type": "txt"}
        response = requests.post(f"{base_url}/tools/file-search", json=search_data)
        print(f"✅ File Search Tool: {response.status_code}")
        result = response.json()
        print(f"   Files found: {result['structuredContent']['total_found']}")
    except Exception as e:
        print(f"❌ File Search Tool failed: {e}")
    
    # Test widget serving
    try:
        response = requests.get(f"{base_url}/widget/weather-widget.html")
        print(f"✅ Widget Serving: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
    except Exception as e:
        print(f"❌ Widget Serving failed: {e}")
    
    print("=" * 50)
    print("Test completed!")

def start_server():
    """Start the server in a separate thread"""
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except subprocess.CalledProcessError:
        pass

if __name__ == "__main__":
    print("Starting MCP Server for testing...")
    
    # Start server in background
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    # Test endpoints
    test_endpoints()
    
    print("\nTo run the server manually:")
    print("python3 app.py")
    print("\nOr use the run script:")
    print("python3 run.py")
