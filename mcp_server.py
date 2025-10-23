#!/usr/bin/env python3
"""
Proper MCP Server Implementation for ChatGPT Apps Integration
Implements the Model Context Protocol with Server-Sent Events
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServer:
    def __init__(self):
        self.tools = {
            "weather": {
                "name": "weather",
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
            "calculator": {
                "name": "calculator",
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
            "text-analysis": {
                "name": "text-analysis",
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
            "file-search": {
                "name": "file-search",
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
        }

    async def handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request"""
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "GPT Integration Tools",
                    "version": "1.0.0"
                }
            }
        }

    async def handle_tools_list(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list request"""
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "tools": list(self.tools.values())
            }
        }

    async def handle_tools_call(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        params = request.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        try:
            if tool_name == "weather":
                result = await self._weather_tool(arguments)
            elif tool_name == "calculator":
                result = await self._calculator_tool(arguments)
            elif tool_name == "text-analysis":
                result = await self._text_analysis_tool(arguments)
            elif tool_name == "file-search":
                result = await self._file_search_tool(arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")

            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result["text"]
                        }
                    ],
                    "isError": False
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Tool execution error: {str(e)}"
                }
            }

    async def _weather_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Weather tool implementation"""
        location = args.get("location", "Unknown")
        units = args.get("units", "celsius")
        
        # Simulate weather data
        temperature = random.randint(15, 30)
        condition = random.choice(["Sunny", "Cloudy", "Rainy", "Partly Cloudy"])
        humidity = random.randint(40, 80)
        wind_speed = random.randint(5, 20)
        
        temp_symbol = "°C" if units == "celsius" else "°F"
        
        return {
            "text": f"Weather in {location}: {temperature}{temp_symbol}, {condition}. Humidity: {humidity}%, Wind: {wind_speed} km/h"
        }

    async def _calculator_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Calculator tool implementation"""
        expression = args.get("expression", "")
        
        try:
            # Simple calculator (in production, use a proper math parser)
            result = eval(expression)
            return {
                "text": f"{expression} = {result}"
            }
        except Exception as e:
            return {
                "text": f"Error calculating '{expression}': {str(e)}"
            }

    async def _text_analysis_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Text analysis tool implementation"""
        text = args.get("text", "")
        analysis_type = args.get("analysis_type", "sentiment")
        
        if analysis_type == "sentiment":
            # Simple sentiment analysis
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
            
            return {
                "text": f"Sentiment Analysis: {sentiment} (Positive: {positive_count}, Negative: {negative_count})"
            }
        elif analysis_type == "word_count":
            word_count = len(text.split())
            return {
                "text": f"Word Count: {word_count} words"
            }
        elif analysis_type == "summary":
            words = text.split()
            if len(words) > 10:
                summary = " ".join(words[:10]) + "..."
            else:
                summary = text
            return {
                "text": f"Summary: {summary}"
            }
        else:
            return {
                "text": f"Unknown analysis type: {analysis_type}"
            }

    async def _file_search_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """File search tool implementation"""
        query = args.get("query", "")
        file_type = args.get("file_type")
        
        # Simulate file search
        mock_files = [
            f"document_{query}_1.txt",
            f"report_{query}_2024.pdf",
            f"data_{query}.csv",
            f"notes_{query}.md"
        ]
        
        if file_type:
            mock_files = [f for f in mock_files if f.endswith(f".{file_type}")]
        
        result = f"Found {len(mock_files)} files matching '{query}'"
        if file_type:
            result += f" with type '{file_type}'"
        
        return {
            "text": result + f"\nFiles: {', '.join(mock_files)}"
        }

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP request"""
        method = request.get("method")
        
        if method == "initialize":
            return await self.handle_initialize(request)
        elif method == "tools/list":
            return await self.handle_tools_list(request)
        elif method == "tools/call":
            return await self.handle_tools_call(request)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

# Global MCP server instance
mcp_server = MCPServer()
