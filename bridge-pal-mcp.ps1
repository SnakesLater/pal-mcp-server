<#
.SYNOPSIS
Windows PowerShell bridge script for PAL MCP Server Docker deployment

.DESCRIPTION
This script provides a Windows-compatible bridge between Docker MCP server
and local MCP clients. It handles Docker container management and provides
stdio interface for MCP clients.

.PARAMETER Start
    Start the PAL MCP Docker container

.PARAMETER Stop
    Stop the PAL MCP Docker container

.PARAMETER Restart
    Restart the PAL MCP Docker container

.PARAMETER Logs
    Follow container logs

.PARAMETER Status
    Show container status

.PARAMETER Exec
    Execute server directly in container (for MCP clients)

.PARAMETER Build
    Build Docker image

.PARAMETER Force
    Force rebuild of Docker image

.PARAMETER Follow
    Follow logs after starting

.EXAMPLE
    .\bridge-pal-mcp.ps1 -Start
    Start the PAL MCP Docker container

    .\bridge-pal-mcp.ps1 -Exec
    Execute server in container (for MCP clients)

    .\bridge-pal-mcp.ps1 -Logs
    Follow container logs

.NOTES
    Author: GiGiDKR
    Date: 2025-01-20
    Requires: Docker Desktop, PowerShell 5.1+
#>

[CmdletBinding()]
param(
    [switch]$Start,
    [switch]$Stop,
    [switch]$Restart,
    [switch]$Logs,
    [switch]$Status,
    [switch]$Exec,
    [switch]$Build,
    [switch]$Force,
    [switch]$Follow
)

$ErrorActionPreference = "Stop"

# Configuration
$ContainerName = "pal-mcp-server"
$ImageName = "pal-mcp-server:latest"
$EnvFile = ".env"
$DockerComposeFile = "docker-compose.yml"

# Colors
$Green = [ConsoleColor]::Green
$Yellow = [ConsoleColor]::Yellow
$Red = [ConsoleColor]::Red
$Cyan = [ConsoleColor]::Cyan
$White = [ConsoleColor]::White

function Write-Info { Write-Host "ℹ $args" -ForegroundColor $Cyan }
function Write-Success { Write-Host "✓ $args" -ForegroundColor $Green }
function Write-Warning { Write-Host "⚠ $args" -ForegroundColor $Yellow }
function Write-Error { Write-Host "✗ $args" -ForegroundColor $Red }
function Write-Step { Write-Host "`n=== $args ===" -ForegroundColor $White }

function Test-Docker {
    if (!(Get-Command "docker" -ErrorAction SilentlyContinue)) {
        Write-Error "Docker not found. Please install Docker Desktop."
        return $false
    }
    
    try {
        $null = docker version 2>$null
        Write-Success "Docker is running"
        return $true
    }
    catch {
        Write-Error "Docker is not running. Please start Docker Desktop."
        return $false
    }
}

function Test-Files {
    if (!(Test-Path $DockerComposeFile)) {
        Write-Error "docker-compose.yml not found"
        return $false
    }
    
    if (!(Test-Path $EnvFile)) {
        Write-Warning ".env file not found. Creating default..."
        Create-DefaultEnv
    }
    
    return $true
}

function Create-DefaultEnv {
    $defaultEnv = @"
# API Keys - Replace with your actual keys
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
XAI_API_KEY=your_xai_api_key_here
DIAL_API_KEY=your_dial_api_key_here
DIAL_API_HOST=your_dial_api_host_here
DIAL_API_VERSION=your_dial_api_version_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
CUSTOM_API_URL=your_custom_api_url_here
CUSTOM_API_KEY=your_custom_api_key_here
CUSTOM_MODEL_NAME=your_custom_model_name_here

# Server Configuration
DEFAULT_MODEL=auto
LOG_LEVEL=INFO
LOG_MAX_SIZE=10MB
LOG_BACKUP_COUNT=5
DEFAULT_THINKING_MODE_THINKDEEP=high

# Optional Advanced Settings
#DISABLED_TOOLS=
#MAX_MCP_OUTPUT_TOKENS=
#TZ=UTC
"@
    
    $defaultEnv | Out-File -FilePath $EnvFile -Encoding UTF8
    Write-Success "Default .env file created"
}

function Test-APIKeys {
    if (!(Test-Path $EnvFile)) { return $false }
    
    $envContent = Get-Content $EnvFile
    $hasValidKey = $false
    
    foreach ($line in $envContent) {
        if ($line -match '^([^#][^=]*?)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim() -replace '^["'']|["'']$', ''
            
            if ($value -ne "your_${key.ToLower()}_here" -and $value.Length -gt 10) {
                Write-Success "Found valid $key"
                $hasValidKey = $true
            }
        }
    }
    
    return $hasValidKey
}

function Get-ContainerStatus {
    try {
        $status = docker ps --filter "name=$ContainerName" --format "{{.Status}}" 2>$null
        if ($status) {
            return $status
        }
        else {
            $exists = docker ps -a --filter "name=$ContainerName" --format "{{.Names}}" 2>$null
            if ($exists) {
                return "stopped"
            }
            else {
                return "not_found"
            }
        }
    }
    catch {
        return "error"
    }
}

function Start-Container {
    Write-Step "Starting PAL MCP Docker Container"
    
    # Stop existing container
    Write-Info "Stopping existing container..."
    docker-compose down 2>$null | Out-Null
    
    # Start services
    Write-Info "Starting services..."
    docker-compose up -d
    
    # Wait for health check
    Write-Info "Waiting for service to be healthy..."
    $maxAttempts = 30
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        $status = Get-ContainerStatus
        if ($status -match "healthy|running") {
            Write-Success "Container is healthy"
            break
        }
        Write-Info "Waiting... ($($attempt + 1)/$maxAttempts)"
        Start-Sleep -Seconds 2
        $attempt++
    }
    
    if ($attempt -eq $maxAttempts) {
        Write-Error "Container failed to become healthy"
        docker-compose logs $ContainerName
        return $false
    }
    
    Write-Success "PAL MCP Docker container started"
    return $true
}

function Stop-Container {
    Write-Step "Stopping PAL MCP Docker Container"
    docker-compose down
    Write-Success "Container stopped"
}

function Restart-Container {
    Write-Step "Restarting PAL MCP Docker Container"
    docker-compose restart $ContainerName
    Write-Success "Container restarted"
}

function Show-Status {
    Write-Step "Container Status"
    docker-compose ps
}

function Follow-Logs {
    Write-Step "Following Container Logs"
    docker-compose logs -f $ContainerName
}

function Exec-Server {
    Write-Step "Executing PAL MCP Server in Container"
    
    # Check if container is running
    $status = Get-ContainerStatus
    if ($status -notmatch "healthy|running") {
        Write-Warning "Container not running. Starting..."
        if (!(Start-Container)) {
            Write-Error "Failed to start container"
            return
        }
    }
    
    # Execute server in container
    Write-Info "Executing server in container..."
    docker exec -i $ContainerName python server.py
}

function Build-Image {
    Write-Step "Building Docker Image"
    
    if ($Force) {
        Write-Info "Removing existing image..."
        docker rmi $ImageName 2>$null | Out-Null
    }
    
    Write-Info "Building image..."
    docker build -t $ImageName .
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Docker image built successfully"
    }
    else {
        Write-Error "Failed to build Docker image"
        return $false
    }
    
    return $true
}

function Show-Usage {
    Write-Host @"
PAL MCP Docker Bridge Script

USAGE:
    .\bridge-pal-mcp.ps1 [OPTIONS]

OPTIONS:
    -Start      Start the PAL MCP Docker container
    -Stop       Stop the PAL MCP Docker container
    -Restart    Restart the PAL MCP Docker container
    -Logs       Follow container logs
    -Status     Show container status
    -Exec       Execute server in container (for MCP clients)
    -Build      Build Docker image
    -Force      Force rebuild of Docker image
    -Follow     Follow logs after starting

EXAMPLES:
    .\bridge-pal-mcp.ps1 -Start
    .\bridge-pal-mcp.ps1 -Exec
    .\bridge-pal-mcp.ps1 -Logs
    .\bridge-pal-mcp.ps1 -Build -Force

MCP Client Integration:
    This script provides the bridge for MCP clients to connect to
    the Docker container. Use -Exec for stdio communication.

    Example MCP client configuration:
    {
        "command": "powershell",
        "args": ["-File", "bridge-pal-mcp.ps1", "-Exec"]
    }
"@
}

# Main execution
function Main {
    if ($Start) {
        if (!(Test-Docker)) { exit 1 }
        if (!(Test-Files)) { exit 1 }
        if (!(Test-APIKeys)) {
            Write-Warning "No valid API keys found. Please configure .env file."
        }
        if (!(Start-Container)) { exit 1 }
        if ($Follow) { Follow-Logs }
    }
    elseif ($Stop) {
        if (!(Test-Docker)) { exit 1 }
        Stop-Container
    }
    elseif ($Restart) {
        if (!(Test-Docker)) { exit 1 }
        Restart-Container
    }
    elseif ($Logs) {
        if (!(Test-Docker)) { exit 1 }
        Follow-Logs
    }
    elseif ($Status) {
        if (!(Test-Docker)) { exit 1 }
        Show-Status
    }
    elseif ($Exec) {
        if (!(Test-Docker)) { exit 1 }
        if (!(Test-Files)) { exit 1 }
        Exec-Server
    }
    elseif ($Build) {
        if (!(Test-Docker)) { exit 1 }
        if (!(Test-Files)) { exit 1 }
        if (!(Build-Image)) { exit 1 }
    }
    else {
        Show-Usage
    }
}

# Execute main function
Main