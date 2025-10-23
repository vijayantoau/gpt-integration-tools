#!/usr/bin/env python3
"""
FastAPI MCP Server with ChatGPT Apps Integration
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn
import os
import json
import asyncio
from datetime import datetime
import random
import time
from mcp_server import mcp_server

# Initialize FastAPI app
app = FastAPI(
    title="GPT Integration Tools",
    description="A comprehensive set of tools including weather, calculator, text analysis, and file search capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add timeout middleware
@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await asyncio.wait_for(call_next(request), timeout=10.0)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=504,
            content={"error": "Request timeout", "message": "The request took too long to process"}
        )

# Pydantic models for tool inputs
class WeatherInput(BaseModel):
    location: str
    units: str = "celsius"

class CalculatorInput(BaseModel):
    expression: str

class TextAnalysisInput(BaseModel):
    text: str
    analysis_type: str = "sentiment"

class FileSearchInput(BaseModel):
    query: str
    file_type: str = None

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "uptime": "running"
        },
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

# Serve web interface
@app.get("/")
async def serve_web_interface():
    """
    Serve the main web interface for testing tools
    """
    interface_path = "web_interface.html"
    if os.path.exists(interface_path):
        return FileResponse(interface_path, media_type="text/html")
    else:
        return JSONResponse(
            content={
                "message": "GPT Integration Tools API",
                "version": "1.0.0",
                "status": "running",
                "endpoints": {
                    "mcp": "/mcp",
                    "tools": "/mcp/tools",
                    "health": "/health",
                    "validate": "/mcp/validate"
                }
            }
        )

# Test route
@app.get("/test")
async def test_route():
    return {"message": "Test route is working!"}

# App manifest endpoint
@app.get("/manifest")
async def get_app_manifest():
    """
    Return the app manifest for ChatGPT Apps SDK
    """
    manifest_path = "app_manifest.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        return manifest
    else:
        raise HTTPException(status_code=404, detail="App manifest not found")

# MCP endpoint for ChatGPT Apps
@app.get("/mcp")
@app.post("/mcp")
async def mcp_endpoint():
    """
    Main MCP endpoint for ChatGPT Apps integration
    """
    return JSONResponse(
        content={
            "name": "GPT Integration Tools",
            "version": "1.0.0",
            "description": "A comprehensive set of tools including weather, calculator, text analysis, and file search capabilities",
            "protocol": "MCP",
            "endpoints": {
                "sse": "/mcp/sse",
                "call": "/mcp/call",
                "tools": "/mcp/tools",
                "health": "/health",
                "validate": "/mcp/validate"
            },
            "status": "ready",
            "timestamp": datetime.now().isoformat(),
            "authTypeOverride": "NONE",
            "auth_request": {
                "supported_auth": [],
                "oauth_client_params": None
            },
            "capabilities": {
                "tools": True,
                "sse": True,
                "websocket": False
            }
        },
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

# MCP tools manifest endpoint
@app.get("/mcp/tools")
async def get_tools_manifest():
    """
    Return the tools manifest for MCP
    """
    return JSONResponse(
        content={
            "tools": [
                {
                    "name": "weather",
                    "title": "Weather Information",
                    "description": "Get current weather information for any location",
                    "inputSchema": {
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
                },
                {
                    "name": "calculator",
                    "title": "Calculator",
                    "description": "Perform mathematical calculations",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression to evaluate"
                            }
                        },
                        "required": ["expression"]
                    }
                },
                {
                    "name": "text-analysis",
                    "title": "Text Analysis",
                    "description": "Analyze text for sentiment, word count, or summary",
                    "inputSchema": {
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
                },
                {
                    "name": "file-search",
                    "title": "File Search",
                    "description": "Search for files in the system",
                    "inputSchema": {
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
            ]
        },
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

# Tool execution endpoints
@app.post("/tools/weather")
async def weather_tool(input_data: WeatherInput):
    """
    Weather tool implementation
    """
    try:
        # Simulate weather data (in a real implementation, you'd call a weather API)
        weather_data = {
            "location": input_data.location,
            "temperature": random.randint(15, 30),
            "units": input_data.units,
            "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]),
            "humidity": random.randint(40, 80),
            "wind_speed": random.randint(5, 20),
            "timestamp": datetime.now().isoformat()
        }
        
        temp_symbol = "°C" if input_data.units == "celsius" else "°F"
        
        return {
            "content": [{
                "type": "text",
                "text": f"Weather in {input_data.location}: {weather_data['temperature']}{temp_symbol}, {weather_data['condition']}"
            }],
            "structuredContent": weather_data,
            "_meta": {
                "openai/outputTemplate": "ui://widget/weather-widget.html",
                "openai/toolInvocation/invoking": "Fetching weather data...",
                "openai/toolInvocation/invoked": "Weather data retrieved successfully."
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather tool error: {str(e)}")

@app.post("/tools/calculator")
async def calculator_tool(input_data: CalculatorInput):
    """
    Calculator tool implementation
    """
    try:
        # Simple calculator (in a real implementation, you'd use a proper math parser)
        result = eval(input_data.expression)
        
        return {
            "content": [{
                "type": "text",
                "text": f"{input_data.expression} = {result}"
            }],
            "structuredContent": {
                "expression": input_data.expression,
                "result": result,
                "timestamp": datetime.now().isoformat()
            },
            "_meta": {
                "openai/outputTemplate": "ui://widget/calculator-widget.html",
                "openai/toolInvocation/invoking": "Calculating...",
                "openai/toolInvocation/invoked": "Calculation completed."
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculator tool error: {str(e)}")

@app.post("/tools/text-analysis")
async def text_analysis_tool(input_data: TextAnalysisInput):
    """
    Text analysis tool implementation
    """
    try:
        text = input_data.text
        analysis_type = input_data.analysis_type
        
        if analysis_type == "sentiment":
            # Simple sentiment analysis (in a real implementation, you'd use NLP libraries)
            positive_words = ["good", "great", "excellent", "amazing", "wonderful", "love", "like", "happy"]
            negative_words = ["bad", "terrible", "awful", "hate", "dislike", "sad", "angry", "frustrated"]
            
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            if positive_count > negative_count:
                sentiment = "Positive"
            elif negative_count > positive_count:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            
            result = f"Sentiment: {sentiment}"
            
        elif analysis_type == "word_count":
            word_count = len(text.split())
            result = f"Word count: {word_count}"
            
        elif analysis_type == "summary":
            # Simple summary (in a real implementation, you'd use summarization models)
            words = text.split()
            if len(words) > 10:
                summary = " ".join(words[:10]) + "..."
            else:
                summary = text
            result = f"Summary: {summary}"
        
        return {
            "content": [{
                "type": "text",
                "text": result
            }],
            "structuredContent": {
                "text": text,
                "analysis_type": analysis_type,
                "result": result,
                "timestamp": datetime.now().isoformat()
            },
            "_meta": {
                "openai/outputTemplate": "ui://widget/text-analysis-widget.html",
                "openai/toolInvocation/invoking": "Analyzing text...",
                "openai/toolInvocation/invoked": "Analysis completed."
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text analysis tool error: {str(e)}")

@app.post("/tools/file-search")
async def file_search_tool(input_data: FileSearchInput):
    """
    File search tool implementation
    """
    try:
        # Simulate file search (in a real implementation, you'd search actual files)
        mock_files = [
            f"document_{input_data.query}_1.txt",
            f"report_{input_data.query}_2024.pdf",
            f"data_{input_data.query}.csv",
            f"notes_{input_data.query}.md"
        ]
        
        if input_data.file_type:
            mock_files = [f for f in mock_files if f.endswith(f".{input_data.file_type}")]
        
        result = f"Found {len(mock_files)} files matching '{input_data.query}'"
        if input_data.file_type:
            result += f" with type '{input_data.file_type}'"
        
        return {
            "content": [{
                "type": "text",
                "text": result
            }],
            "structuredContent": {
                "query": input_data.query,
                "file_type": input_data.file_type,
                "files": mock_files,
                "count": len(mock_files),
                "timestamp": datetime.now().isoformat()
            },
            "_meta": {
                "openai/outputTemplate": "ui://widget/file-search-widget.html",
                "openai/toolInvocation/invoking": "Searching files...",
                "openai/toolInvocation/invoked": "Search completed."
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File search tool error: {str(e)}")

# Proper MCP Server-Sent Events endpoint
@app.get("/mcp/sse")
async def mcp_sse_endpoint():
    """
    MCP Server-Sent Events endpoint for ChatGPT Apps
    """
    async def event_generator():
        # Send initial MCP initialization message
        init_message = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "GPT Integration Tools",
                    "version": "1.0.0"
                }
            },
            "id": 1
        }
        
        yield f"data: {json.dumps(init_message)}\n\n"
        
        # Keep connection alive
        while True:
            await asyncio.sleep(30)
            yield f"data: {json.dumps({'type': 'ping', 'timestamp': datetime.now().isoformat()})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
        }
    )

# MCP WebSocket-style endpoint for tool calls
@app.post("/mcp/call")
async def mcp_tool_call(request: Request):
    """
    Handle MCP tool calls via POST
    """
    try:
        body = await request.json()
        response = await mcp_server.handle_request(body)
        return JSONResponse(content=response)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
        )

# ChatGPT Apps connector validation endpoint
@app.get("/mcp/validate")
@app.post("/mcp/validate")
async def validate_connector():
    """
    Endpoint for ChatGPT Apps to validate the connector
    """
    return JSONResponse(
        content={
            "valid": True,
            "status": "ready",
            "message": "Connector is valid and ready to use",
            "timestamp": datetime.now().isoformat(),
            "protocol": "MCP",
            "endpoints": {
                "sse": "/mcp/sse",
                "call": "/mcp/call"
            }
        },
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

# OPTIONS handler for CORS preflight requests
@app.options("/mcp")
@app.options("/mcp/tools")
@app.options("/mcp/validate")
@app.options("/mcp/sse")
@app.options("/mcp/call")
async def options_handler():
    """
    Handle CORS preflight requests
    """
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "86400"
        }
    )

# Widget endpoints for UI components
@app.get("/widget/{component_name}")
async def get_widget(component_name: str):
    """
    Serve widget components for the web interface
    """
    widget_path = f"components/{component_name}.html"
    if os.path.exists(widget_path):
        return FileResponse(widget_path, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="Widget not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
