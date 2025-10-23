# GPT Integration Tools - Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           USER REQUEST FLOW                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   USER INPUT    │    │   USER INPUT    │    │   USER INPUT    │
│                 │    │                 │    │                 │
│ "What's the     │    │ "Calculate      │    │ "Analyze this   │
│ weather in      │    │ 25 * 4 + 10"    │    │ text sentiment" │
│ New York?"      │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                      │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CHATGPT       │    │    CURSOR       │    │   WEB UI        │
│                 │    │                 │    │                 │
│ • OpenAI API    │    │ • Local Editor  │    │ • Browser       │
│ • MCP Protocol  │    │ • MCP Client    │    │ • Direct HTTP   │
│ • Tool Calling  │    │ • Stdio Transport│   │ • REST API      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            TRANSPORT LAYER                                     │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTTP/HTTPS    │    │   STDIO PIPE    │    │   HTTP/HTTPS    │
│                 │    │                 │    │                 │
│ • JSON-RPC 2.0  │    │ • JSON-RPC 2.0  │    │ • REST API      │
│ • MCP Protocol  │    │ • MCP Protocol  │    │ • JSON Response │
│ • POST Requests │    │ • stdin/stdout  │    │ • GET/POST      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            SERVER LAYER                                        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  VERCEL HOSTED  │    │  LOCAL HOSTED   │    │  PROXY SERVER   │
│                 │    │                 │    │                 │
│ • FastAPI App   │    │ • Python Script │    │ • Python Script │
│ • MCP Endpoint  │    │ • Stdio Server  │    │ • HTTP Client   │
│ • Tool Router   │    │ • Tool Router   │    │ • Request Proxy │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            TOOL EXECUTION LAYER                                │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  WEATHER TOOL   │    │ CALCULATOR TOOL │    │TEXT ANALYSIS    │    │ FILE SEARCH     │
│                 │    │                 │    │     TOOL        │    │     TOOL        │
│ • Location API  │    │ • Math Parser   │    │ • Sentiment     │    │ • File System   │
│ • Weather Data  │    │ • Expression    │    │ • Word Count    │    │ • Search Query  │
│ • Temperature   │    │ • Calculation   │    │ • Summary       │    │ • File Types    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │                       │
         ▼                       ▼                       ▼                       ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            RESPONSE LAYER                                      │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  TOOL RESULT    │    │  MCP RESPONSE   │    │  USER RESPONSE  │
│                 │    │                 │    │                 │
│ • Weather Data  │    │ • JSON-RPC 2.0  │    │ • Natural Text  │
│ • Calculation   │    │ • Content Array │    │ • Formatted     │
│ • Analysis      │    │ • Error Handling│    │ • Contextual    │
│ • File List     │    │ • Status Codes  │    │ • Interactive   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USER OUTPUT                                       │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CHATGPT       │    │    CURSOR       │    │   WEB UI        │
│                 │    │                 │    │                 │
│ "The weather in │    │ "Weather in     │    │ "Weather in     │
│ New York is     │    │ New York: 22°C, │    │ New York: 22°C, │
│ 22°C and sunny  │    │ Sunny"          │    │ Sunny"          │
│ with 45%        │    │                 │    │                 │
│ humidity."      │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Detailed Component Flow

### 1. ChatGPT Integration Flow
```
User → ChatGPT → HTTP POST → Vercel MCP Server → Tool Execution → Response → ChatGPT → User
```

### 2. Cursor Integration Flow (Local)
```
User → Cursor → Stdio Pipe → Local MCP Server → Tool Execution → Response → Cursor → User
```

### 3. Cursor Integration Flow (Proxy)
```
User → Cursor → Stdio Pipe → Proxy Server → HTTP POST → Vercel MCP Server → Tool Execution → Response → Proxy → Cursor → User
```

## Key Components

### Host Layer
- **Vercel**: Cloud hosting platform
- **Local Machine**: Development environment
- **Proxy Server**: Bridge between stdio and HTTP

### Client Layer
- **ChatGPT**: OpenAI's conversational AI
- **Cursor**: Code editor with MCP support
- **Web UI**: Browser-based interface

### Server Layer
- **FastAPI App**: Main application server
- **MCP Server**: Protocol implementation
- **Tool Router**: Request routing logic

### Tool Layer
- **Weather Tool**: Location-based weather data
- **Calculator Tool**: Mathematical operations
- **Text Analysis Tool**: Sentiment, word count, summary
- **File Search Tool**: File system queries

## Protocol Details

### MCP (Model Context Protocol)
- **Transport**: HTTP/HTTPS or stdio
- **Format**: JSON-RPC 2.0
- **Methods**: initialize, tools/list, tools/call
- **Error Handling**: Standard JSON-RPC error codes

### Tool Execution
- **Input Validation**: Schema-based validation
- **Processing**: Tool-specific logic
- **Output Format**: Standardized content array
- **Error Handling**: Graceful error responses

## Deployment Architecture

### Production (Vercel)
```
Internet → Vercel CDN → FastAPI App → Tool Execution → Response
```

### Development (Local)
```
Cursor → Local Process → Tool Execution → Response
```

### Hybrid (Proxy)
```
Cursor → Local Proxy → Vercel → Tool Execution → Response
```
