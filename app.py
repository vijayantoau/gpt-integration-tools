"""
MCP Server with FastAPI integration for ChatGPT Apps SDK
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime
import httpx

# Initialize FastAPI app
app = FastAPI(
    title="MCP Server for ChatGPT",
    description="Model Context Protocol server with sample tools",
    version="1.0.0"
)

# Configure CORS for ChatGPT integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://chatgpt.com",
        "https://chat.openai.com",
        "http://localhost:3000",  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for tool inputs
class WeatherInput(BaseModel):
    location: str = Field(..., description="The city or location to get weather for")
    units: str = Field(default="celsius", description="Temperature units: celsius or fahrenheit")

class CalculatorInput(BaseModel):
    expression: str = Field(..., description="Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')")

class TextAnalysisInput(BaseModel):
    text: str = Field(..., description="Text to analyze")
    analysis_type: str = Field(default="sentiment", description="Type of analysis: sentiment, word_count, or summary")

class FileSearchInput(BaseModel):
    query: str = Field(..., description="Search query for files")
    file_type: Optional[str] = Field(None, description="Optional file type filter (e.g., 'txt', 'pdf')")

# Sample tools implementation
@app.post("/tools/weather")
async def get_weather(input_data: WeatherInput):
    """
    Get weather information for a location
    """
    try:
        # Mock weather data - in production, you'd call a real weather API
        weather_data = {
            "location": input_data.location,
            "temperature": 22 if input_data.units == "celsius" else 72,
            "units": input_data.units,
            "condition": "Sunny",
            "humidity": 65,
            "wind_speed": 10,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "content": [{
                "type": "text", 
                "text": f"Weather in {input_data.location}: {weather_data['temperature']}°{input_data.units[0].upper()}, {weather_data['condition']}"
            }],
            "structuredContent": weather_data,
            "_meta": {
                "openai/outputTemplate": "ui://widget/weather-widget.html",
                "openai/toolInvocation/invoking": "Fetching weather data...",
                "openai/toolInvocation/invoked": "Weather data retrieved successfully."
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")

@app.post("/tools/calculator")
async def calculate(input_data: CalculatorInput):
    """
    Perform mathematical calculations
    """
    try:
        # Simple calculator - in production, use a proper math parser
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in input_data.expression):
            raise ValueError("Invalid characters in expression")
        
        result = eval(input_data.expression)
        
        calculation_data = {
            "expression": input_data.expression,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "content": [{
                "type": "text", 
                "text": f"{input_data.expression} = {result}"
            }],
            "structuredContent": calculation_data,
            "_meta": {
                "openai/outputTemplate": "ui://widget/calculator-widget.html",
                "openai/toolInvocation/invoking": "Calculating...",
                "openai/toolInvocation/invoked": "Calculation completed."
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@app.post("/tools/text-analysis")
async def analyze_text(input_data: TextAnalysisInput):
    """
    Analyze text for sentiment, word count, or summary
    """
    try:
        text = input_data.text
        analysis_type = input_data.analysis_type
        
        if analysis_type == "word_count":
            word_count = len(text.split())
            char_count = len(text)
            analysis_result = {
                "word_count": word_count,
                "character_count": char_count,
                "analysis_type": analysis_type
            }
            result_text = f"Word count: {word_count}, Character count: {char_count}"
            
        elif analysis_type == "sentiment":
            # Simple sentiment analysis (in production, use a proper NLP library)
            positive_words = ["good", "great", "excellent", "amazing", "wonderful", "fantastic"]
            negative_words = ["bad", "terrible", "awful", "horrible", "disappointing"]
            
            text_lower = text.lower()
            positive_score = sum(1 for word in positive_words if word in text_lower)
            negative_score = sum(1 for word in negative_words if word in text_lower)
            
            if positive_score > negative_score:
                sentiment = "positive"
            elif negative_score > positive_score:
                sentiment = "negative"
            else:
                sentiment = "neutral"
                
            analysis_result = {
                "sentiment": sentiment,
                "positive_score": positive_score,
                "negative_score": negative_score,
                "analysis_type": analysis_type
            }
            result_text = f"Sentiment: {sentiment} (positive: {positive_score}, negative: {negative_score})"
            
        else:  # summary
            words = text.split()
            if len(words) > 20:
                summary = " ".join(words[:20]) + "..."
            else:
                summary = text
            analysis_result = {
                "summary": summary,
                "original_length": len(words),
                "analysis_type": analysis_type
            }
            result_text = f"Summary: {summary}"
        
        analysis_result["timestamp"] = datetime.now().isoformat()
        
        return {
            "content": [{
                "type": "text", 
                "text": result_text
            }],
            "structuredContent": analysis_result,
            "_meta": {
                "openai/outputTemplate": "ui://widget/text-analysis-widget.html",
                "openai/toolInvocation/invoking": "Analyzing text...",
                "openai/toolInvocation/invoked": "Analysis completed."
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.post("/tools/file-search")
async def search_files(input_data: FileSearchInput):
    """
    Search for files in the system
    """
    try:
        # Mock file search - in production, implement actual file system search
        mock_files = [
            {"name": "document1.txt", "path": "/documents/document1.txt", "size": 1024, "modified": "2024-01-15"},
            {"name": "report.pdf", "path": "/reports/report.pdf", "size": 2048, "modified": "2024-01-14"},
            {"name": "data.json", "path": "/data/data.json", "size": 512, "modified": "2024-01-13"},
        ]
        
        # Filter files based on query and file type
        filtered_files = []
        for file in mock_files:
            if input_data.query.lower() in file["name"].lower():
                if input_data.file_type is None or file["name"].endswith(f".{input_data.file_type}"):
                    filtered_files.append(file)
        
        search_result = {
            "query": input_data.query,
            "file_type_filter": input_data.file_type,
            "files": filtered_files,
            "total_found": len(filtered_files),
            "timestamp": datetime.now().isoformat()
        }
        
        result_text = f"Found {len(filtered_files)} files matching '{input_data.query}'"
        if input_data.file_type:
            result_text += f" with type '{input_data.file_type}'"
        
        return {
            "content": [{
                "type": "text", 
                "text": result_text
            }],
            "structuredContent": search_result,
            "_meta": {
                "openai/outputTemplate": "ui://widget/file-search-widget.html",
                "openai/toolInvocation/invoking": "Searching files...",
                "openai/toolInvocation/invoked": "Search completed."
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

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
        return {"message": "Web interface not found. Please ensure web_interface.html exists."}

# Test route
@app.get("/test")
async def test_route():
    return {"message": "Test route is working!"}

# Serve UI components
@app.get("/widget/{component_name}")
async def serve_component(component_name: str):
    """
    Serve UI components for ChatGPT rendering
    """
    component_path = f"components/{component_name}"
    if os.path.exists(component_path):
        return FileResponse(component_path, media_type="text/html+skybridge")
    else:
        raise HTTPException(status_code=404, detail="Component not found")

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

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
async def mcp_endpoint():
    """
    Main MCP endpoint for ChatGPT Apps integration
    """
    return {
        "name": "GPT Integration Tools",
        "version": "1.0.0",
        "description": "A comprehensive set of tools including weather, calculator, text analysis, and file search capabilities",
        "endpoints": {
            "tools": "/mcp/tools",
            "health": "/health"
        }
    }

# MCP tools manifest endpoint
@app.get("/mcp/tools")
async def get_tools_manifest():
    """
    Return the MCP tools manifest for ChatGPT integration
    """
    tools_manifest = {
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
    }
    return tools_manifest

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
