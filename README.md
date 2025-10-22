# MCP Server for ChatGPT Apps SDK

A Model Context Protocol (MCP) server built with FastAPI and Python that integrates with ChatGPT's new Apps SDK. This server provides sample tools with custom UI components that can be rendered inline within ChatGPT conversations.

## Features

- **Weather Tool**: Get current weather information for any location
- **Calculator Tool**: Perform mathematical calculations
- **Text Analysis Tool**: Analyze text for sentiment, word count, or summary
- **File Search Tool**: Search for files in the system
- **Custom UI Components**: Beautiful, responsive widgets for each tool output
- **CORS Configuration**: Properly configured for ChatGPT integration
- **Health Check**: Built-in health monitoring endpoint

## Project Structure

```
gptintegration/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── components/           # UI components directory
│   ├── weather-widget.html
│   ├── calculator-widget.html
│   ├── text-analysis-widget.html
│   └── file-search-widget.html
├── .env                  # Environment variables (create this)
└── README.md            # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
# Optional: Add any environment variables here
# For example:
# WEATHER_API_KEY=your_weather_api_key_here
# DEBUG=True
```

### 3. Run the Server

#### Development Mode
```bash
python app.py
```

#### Production Mode with Uvicorn
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at `http://localhost:8000`

### 4. Test the Server

Visit these endpoints to verify everything is working:

- **Health Check**: `http://localhost:8000/health`
- **Tools Manifest**: `http://localhost:8000/mcp/tools`
- **API Documentation**: `http://localhost:8000/docs`

## ChatGPT Integration

### 1. Expose Your Server

For local development, use ngrok to expose your server:

```bash
# Install ngrok if you haven't already
# https://ngrok.com/

# Expose your local server
ngrok http 8000
```

Copy the public URL (e.g., `https://abc123.ngrok.io`)

### 2. Configure ChatGPT App

1. Go to [ChatGPT Apps SDK](https://platform.openai.com/apps-sdk)
2. Create a new app
3. Add your server URL as the MCP server endpoint
4. The tools will be automatically discovered from the `/mcp/tools` endpoint

### 3. Available Tools

#### Weather Tool
- **Endpoint**: `POST /tools/weather`
- **Parameters**:
  - `location` (required): City or location name
  - `units` (optional): "celsius" or "fahrenheit" (default: "celsius")

#### Calculator Tool
- **Endpoint**: `POST /tools/calculator`
- **Parameters**:
  - `expression` (required): Mathematical expression to evaluate

#### Text Analysis Tool
- **Endpoint**: `POST /tools/text-analysis`
- **Parameters**:
  - `text` (required): Text to analyze
  - `analysis_type` (optional): "sentiment", "word_count", or "summary" (default: "sentiment")

#### File Search Tool
- **Endpoint**: `POST /tools/file-search`
- **Parameters**:
  - `query` (required): Search query for files
  - `file_type` (optional): File type filter (e.g., "txt", "pdf")

## API Endpoints

### Tool Endpoints
- `POST /tools/weather` - Get weather information
- `POST /tools/calculator` - Perform calculations
- `POST /tools/text-analysis` - Analyze text
- `POST /tools/file-search` - Search files

### Utility Endpoints
- `GET /health` - Health check
- `GET /mcp/tools` - MCP tools manifest
- `GET /widget/{component_name}` - Serve UI components
- `GET /docs` - API documentation (Swagger UI)

## Customization

### Adding New Tools

1. **Define the input schema** in `app.py`:
```python
class YourToolInput(BaseModel):
    parameter1: str = Field(..., description="Description of parameter1")
    parameter2: Optional[str] = Field(None, description="Description of parameter2")
```

2. **Create the tool endpoint**:
```python
@app.post("/tools/your-tool")
async def your_tool(input_data: YourToolInput):
    # Your tool logic here
    return {
        "content": [{"type": "text", "text": "Your response"}],
        "structuredContent": {"key": "value"},
        "_meta": {
            "openai/outputTemplate": "ui://widget/your-widget.html",
            "openai/toolInvocation/invoking": "Processing...",
            "openai/toolInvocation/invoked": "Completed."
        }
    }
```

3. **Create a UI component** in `components/your-widget.html`
4. **Add to tools manifest** in the `/mcp/tools` endpoint

### Styling UI Components

The UI components use modern CSS with:
- Glassmorphism design with backdrop blur
- Gradient backgrounds
- Responsive grid layouts
- Smooth animations
- Dark theme optimized for ChatGPT

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Using Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Using Cloud Platforms
- **Heroku**: Add a `Procfile` with `web: uvicorn app:app --host 0.0.0.0 --port $PORT`
- **Railway**: Deploy directly from GitHub
- **DigitalOcean App Platform**: Use the Python buildpack
- **AWS/GCP/Azure**: Use container services or serverless functions

## Security Considerations

- The server includes CORS configuration for ChatGPT domains
- Input validation using Pydantic models
- Error handling with appropriate HTTP status codes
- Consider adding authentication for production use

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your server URL is added to the CORS origins list
2. **Component Not Found**: Check that UI components are in the `components/` directory
3. **Tool Not Working**: Verify the tool is listed in `/mcp/tools` endpoint
4. **Port Already in Use**: Change the port in the uvicorn command

### Debug Mode

Enable debug mode by setting environment variable:
```bash
export DEBUG=True
python app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the ChatGPT Apps SDK documentation
3. Open an issue in the repository
# gpt-integration-tools
