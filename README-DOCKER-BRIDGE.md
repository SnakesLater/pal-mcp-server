# PAL MCP Server Docker Bridge

This directory contains Windows PowerShell scripts to bridge the PAL MCP Server Docker deployment with local MCP clients.

## Overview

The `bridge-pal-mcp.ps1` script provides a Windows-compatible interface between Docker containers and MCP clients. It handles:

- Docker container lifecycle management
- Stdio communication bridge for MCP clients
- Environment file management
- Health checks and status monitoring

## Prerequisites

- Docker Desktop for Windows
- PowerShell 5.1+
- PAL MCP Server Docker image

## Quick Start

### 1. Start the Docker Container

```powershell
.\bridge-pal-mcp.ps1 -Start
```

### 2. Execute Server for MCP Clients

```powershell
.\bridge-pal-mcp.ps1 -Exec
```

### 3. Follow Container Logs

```powershell
.\bridge-pal-mcp.ps1 -Logs
```

## Usage

### Command Line Options

| Option | Description |
|--------|-------------|
| `-Start` | Start the PAL MCP Docker container |
| `-Stop` | Stop the PAL MCP Docker container |
| `-Restart` | Restart the PAL MCP Docker container |
| `-Logs` | Follow container logs |
| `-Status` | Show container status |
| `-Exec` | Execute server in container (for MCP clients) |
| `-Build` | Build Docker image |
| `-Force` | Force rebuild of Docker image |
| `-Follow` | Follow logs after starting |

### Examples

```powershell
# Start container and follow logs
.\bridge-pal-mcp.ps1 -Start -Follow

# Build and start
.\bridge-pal-mcp.ps1 -Build -Force
.\bridge-pal-mcp.ps1 -Start

# Check status
.\bridge-pal-mcp.ps1 -Status

# Stop container
.\bridge-pal-mcp.ps1 -Stop
```

## MCP Client Integration

### Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pal": {
      "command": "powershell",
      "args": ["-File", "C:\\path\\to\\bridge-pal-mcp.ps1", "-Exec"],
      "type": "stdio"
    }
  }
}
```

### VSCode Configuration

Add to `settings.json`:

```json
{
  "mcp.servers.pal": {
    "command": "powershell",
    "args": ["-File", "C:\\path\\to\\bridge-pal-mcp.ps1", "-Exec"],
    "type": "stdio"
  }
}
```

### Other MCP Clients

For other MCP clients, use:

```json
{
  "command": "powershell",
  "args": ["-File", "C:\\path\\to\\bridge-pal-mcp.ps1", "-Exec"],
  "type": "stdio"
}
```

## Environment Configuration

The script automatically creates a `.env` file if it doesn't exist. Edit this file to add your API keys:

```bash
# API Keys - Replace with your actual keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
XAI_API_KEY=your_xai_api_key_here
# ... other keys
```

## Docker Management

### Building the Image

```powershell
.\bridge-pal-mcp.ps1 -Build
```

### Force Rebuild

```powershell
.\bridge-pal-mcp.ps1 -Build -Force
```

### Container Status

```powershell
.\bridge-pal-mcp.ps1 -Status
```

## Troubleshooting

### Container Won't Start

1. Check Docker Desktop is running
2. Verify `.env` file has valid API keys
3. Check logs: `.\bridge-pal-mcp.ps1 -Logs`

### MCP Client Connection Issues

1. Ensure container is running: `.\bridge-pal-mcp.ps1 -Status`
2. Test server execution: `.\bridge-pal-mcp.ps1 -Exec`
3. Verify MCP client configuration paths

### Permission Issues

Run PowerShell as Administrator when needed.

## Advanced Usage

### Custom Docker Compose

The script uses `docker-compose.yml` in the current directory. You can customize this file for your environment.

### Environment Variables

The script loads environment variables from `.env` file and passes them to the Docker container.

### Health Checks

The script performs health checks when starting containers and waits up to 60 seconds for the service to become healthy.

## Development

### Script Structure

- `Test-Docker()` - Verify Docker installation and running status
- `Test-Files()` - Check required files exist
- `Start-Container()` - Start and health-check container
- `Exec-Server()` - Execute server in container for MCP clients
- `Build-Image()` - Build Docker image

### Adding New Features

1. Add new parameters to the param block
2. Implement the function
3. Add logic to the Main function
4. Update documentation

## License

This script is part of the PAL MCP Server project.

## Support

For issues and questions:
1. Check the main PAL MCP Server documentation
2. Review Docker logs
3. Verify MCP client configuration