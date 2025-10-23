#!/usr/bin/env python3
"""
MCP Proxy Server - Forwards Cursor MCP requests to Vercel endpoint
"""

import asyncio
import json
import sys
import logging
import requests
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Your Vercel MCP server URL
VERCEL_MCP_URL = "https://gptintegration-gkhz75qlq-vijays-projects-83d7f1fb.vercel.app/mcp"

class MCPProxyServer:
    def __init__(self):
        self.vercel_url = VERCEL_MCP_URL

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Forward MCP request to Vercel endpoint"""
        try:
            # Log the request
            logger.info(f"Forwarding request to Vercel: {request.get('method', 'unknown')}")
            
            # Forward the request to Vercel
            response = requests.post(
                self.vercel_url,
                json=request,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Cursor-MCP-Proxy/1.0"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Vercel response: {result.get('result', {}).get('serverInfo', {}).get('name', 'unknown') if request.get('method') == 'initialize' else 'tool response'}")
                return result
            else:
                logger.error(f"Vercel error: {response.status_code} - {response.text}")
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32603,
                        "message": f"Vercel server error: {response.status_code}"
                    }
                }
                
        except requests.exceptions.Timeout:
            logger.error("Vercel request timeout")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Request timeout to Vercel server"
                }
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Vercel request error: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Network error: {str(e)}"
                }
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

async def main():
    """Main MCP proxy server loop using stdio transport"""
    server = MCPProxyServer()
    
    # Read from stdin and write to stdout
    while True:
        try:
            # Read JSON-RPC request from stdin
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            request = json.loads(line.strip())
            
            # Handle the request by forwarding to Vercel
            response = await server.handle_request(request)
            
            # Write JSON-RPC response to stdout
            print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(main())
