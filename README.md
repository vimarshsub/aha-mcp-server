# Aha! MCP Server

A comprehensive Model Context Protocol (MCP) server that provides seamless integration between Large Language Models and the Aha! product management platform. This server enables AI assistants to search, create, and edit features in Aha! through natural language interactions.

## 🤖 For AI Agents: Complete Setup Guide

### Prerequisites
- Access to this workspace in VS Code
- User has provided Aha! domain and API key
- Python 3.8+ available in the environment

### Step-by-Step Setup Instructions

**1. Initialize the Environment**
```bash
# Navigate to the project directory
cd /Users/vimarsh/Documents/GitHub/aha-mcp-server

# Create and activate virtual environment
python3 -m venv aha-mcp-env
source aha-mcp-env/bin/activate  # On Windows: aha-mcp-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

**2. Create Configuration File**
Ask the user for their Aha! credentials, then create:
```bash
cat > aha_config.json << 'EOF'
{
  "aha_domain": "USER_PROVIDED_DOMAIN.aha.io",
  "api_key": "USER_PROVIDED_API_KEY", 
  "default_product": "USER_PROVIDED_PRODUCT_ID"
}
EOF
```

**3. Test the Installation**
```bash
# Test API connectivity
python -c "
import asyncio
from aha_mcp_server import load_config, AhaAPIClient

async def test():
    config = load_config()
    async with AhaAPIClient(config) as client:
        data = await client.request('GET', '/products', params={'per_page': 1})
        print('✅ API connectivity successful')
        print(f'Found {len(data.get(\"products\", []))} product(s)')

asyncio.run(test())
"
```

**4. Configure VS Code MCP Integration**
The MCP server is already configured in VS Code. Verify with:
```json
// VS Code settings.json should contain:
{
  "mcp": {
    "servers": {
      "aha": {
        "command": "/Users/vimarsh/Documents/GitHub/aha-mcp-server/aha-mcp-env/bin/python",
        "args": ["/Users/vimarsh/Documents/GitHub/aha-mcp-server/aha_mcp_server.py"],
        "cwd": "/Users/vimarsh/Documents/GitHub/aha-mcp-server"
      }
    }
  }
}
```

### Quick Validation Commands

**Test MCP Tools Directly:**
```
# Get feature details
@mcp_aha_get_feature DNAC-10991

# Search features  
@mcp_aha_search_features query="API" limit=5

# List products
@mcp_aha_list_products limit=10
```

### Common Agent Troubleshooting

**Issue: MCP tools not available**
- Restart VS Code after configuration changes
- Check that `aha_config.json` exists and has valid credentials
- Verify virtual environment is activated

**Issue: 403 Forbidden errors**
- Validate API key in `aha_config.json`
- Check user permissions in Aha! workspace
- Test with curl: `curl -H "Authorization: Bearer YOUR_API_KEY" https://DOMAIN.aha.io/api/v1/products`

**Issue: Feature creation fails**
- Features must be created under a release using `/releases/{release_id}/features` endpoint
- Use `mcp_aha_list_products` to find available releases first

---

## Overview

The Aha! MCP Server bridges the gap between AI-powered tools and product management workflows by exposing Aha!'s feature management capabilities through the standardized Model Context Protocol. Built with Python and the FastMCP framework, this server provides robust, production-ready tools for managing product features, releases, and epics.

### Key Features

- **Comprehensive Feature Management**: Search, create, update, and delete features with full support for custom fields, tags, and assignments
- **Advanced Search Capabilities**: Filter features by product, release, epic, status, assignee, and tags with flexible query options
- **Batch Operations**: Efficiently manage multiple features across releases and epics
- **Real-time Integration**: Direct API integration with Aha! ensures data consistency and immediate updates
- **Error Handling**: Robust error handling with user-friendly messages and actionable guidance
- **Security**: Secure API key management with support for environment variables and configuration files
- **Performance Optimized**: Built-in rate limiting, connection pooling, and efficient data formatting
- **Native MCP Integration**: Direct tool calling support in VS Code and Claude Desktop

## Architecture

The server follows a modular architecture designed for maintainability and extensibility:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Aha! MCP Server │◄──►│   Aha! API      │
│ (VS Code/Claude)│    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Configuration   │
                       │  & Credentials   │
                       └──────────────────┘
```

### Core Components

1. **Configuration Manager**: Handles Aha! domain and API key configuration with support for multiple configuration sources
2. **API Client**: Manages HTTP requests to Aha! REST API with automatic error handling and rate limiting
3. **Tool Handlers**: Individual functions for each MCP tool with comprehensive parameter validation
4. **Error Handler**: Centralized error handling with user-friendly messages and recovery suggestions
5. **Data Formatter**: Formats Aha! API responses for optimal LLM consumption and human readability

## Installation

### Prerequisites

- Python 3.8 or higher
- Active Aha! account with API access
- Valid Aha! API key
- VS Code with GitHub Copilot (for MCP integration)

### Quick Installation

```bash
# Clone or download the server files
git clone https://github.com/your-username/aha-mcp-server.git
cd aha-mcp-server

# Install dependencies
pip install -r requirements.txt

# Configure your Aha! credentials (see Configuration section)
cp aha_config.json.example aha_config.json
# Edit aha_config.json with your credentials
```

### Development Installation

```bash
# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest tests/
```

## Configuration

The server supports multiple configuration methods for maximum flexibility:

### Method 1: Environment Variables (Recommended)

```bash
export AHA_DOMAIN="yourcompany.aha.io"
export AHA_API_KEY="your_api_key_here"
export AHA_DEFAULT_PRODUCT="optional_default_product_id"
export AHA_RATE_LIMIT_DELAY="0.2"
export AHA_TIMEOUT="30"
```

### Method 2: Configuration File

Create an `aha_config.json` file in the server directory:

```json
{
  "aha_domain": "yourcompany.aha.io",
  "api_key": "your_api_key_here",
  "default_product": "optional_default_product_id",
  "rate_limit_delay": 0.2,
  "timeout": 30
}
```

### Obtaining Your API Key

1. Log into your Aha! account
2. Navigate to Settings → Personal → Developer
3. Click "Generate API key"
4. Copy the generated key and use it in your configuration

## Usage

### Running the Server

```bash
# Run the MCP server
python aha_mcp_server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Connecting to Claude Desktop

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "aha": {
      "command": "python",
      "args": ["/path/to/aha_mcp_server.py"],
      "env": {
        "AHA_DOMAIN": "yourcompany.aha.io",
        "AHA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ Available MCP Tools

The Aha! MCP Server provides the following tools for AI agents and users:

### Feature Management Tools
- `mcp_aha_get_feature` - Get detailed feature information
- `mcp_aha_search_features` - Search features with advanced filters
- `mcp_aha_create_feature` - Create new features
- `mcp_aha_update_feature` - Update existing features
- `mcp_aha_delete_feature` - Delete features (with confirmation)
- `mcp_aha_update_feature_status` - Update feature workflow status
- `mcp_aha_update_feature_score` - Update feature scoring
- `mcp_aha_add_feature_tags` - Add or replace feature tags

### Product & Release Management Tools
- `mcp_aha_list_products` - List all available products
- `mcp_aha_list_features_by_release` - Get features in a specific release
- `mcp_aha_list_features_by_epic` - Get features in a specific epic

### Ideas & Customer Feedback Tools
- `mcp_aha_get_related_ideas` - Search for customer ideas and feedback

### 🎯 Common Use Cases for AI Agents

**Feature Discovery:**
```
@mcp_aha_search_features query="API security" status="Planning"
@mcp_aha_get_feature DNAC-10991
```

**Feature Management:**
```
@mcp_aha_create_feature name="New Security Feature" description="Enhanced API security controls"
@mcp_aha_update_feature_status DNAC-3080 "In Development"
```

**Reporting & Analysis:**
```
@mcp_aha_search_features assignee="Pratik Patel"
@mcp_aha_list_features_by_release CatC-3.2.1
```

## 🔧 Troubleshooting for AI Agents

### Common Issues and Solutions

**1. MCP Tools Not Available**
```bash
# Check if MCP server is configured in VS Code settings.json
# Verify the paths are correct and python environment is activated
source aha-mcp-env/bin/activate
python aha_mcp_server.py --help  # Should show MCP server info
```

**2. Authentication Errors (403 Forbidden)**
```bash
# Verify API key in aha_config.json
# Check if user has proper permissions in Aha! workspace
curl -H "Authorization: Bearer YOUR_API_KEY" https://ciscospinfra.aha.io/api/v1/products
```

**3. Feature Creation Fails**
- Features must be created under a specific release
- Use `POST /api/v1/releases/{release_id}/features` endpoint
- Ensure all mandatory fields are provided

**4. MCP Server Not Responding**
```bash
# Restart the MCP server
pkill -f aha_mcp_server.py
cd /path/to/aha-mcp-server
source aha-mcp-env/bin/activate
python aha_mcp_server.py
```

### Environment Validation Script

```bash
#!/bin/bash
# Validate MCP setup
echo "🔍 Validating Aha MCP Server Setup..."

# Check Python environment
if [ -d "aha-mcp-env" ]; then
    echo "✅ Virtual environment found"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Check configuration
if [ -f "aha_config.json" ]; then
    echo "✅ Configuration file found"
else
    echo "❌ Configuration file missing"
    exit 1
fi

# Test API connectivity
source aha-mcp-env/bin/activate
python -c "
from aha_mcp_server import load_config, AhaAPIClient
import asyncio

async def test():
    config = load_config()
    async with AhaAPIClient(config) as client:
        data = await client.request('GET', '/products', params={'per_page': 1})
        print('✅ API connectivity successful')

asyncio.run(test())
"

echo "🎉 Aha MCP Server validation complete!"
```

## Overview

The Aha! MCP Server bridges the gap between AI-powered tools and product management workflows by exposing Aha!'s feature management capabilities through the standardized Model Context Protocol. Built with Python and the FastMCP framework, this server provides robust, production-ready tools for managing product features, releases, and epics.

### Key Features

- **Comprehensive Feature Management**: Search, create, update, and delete features with full support for custom fields, tags, and assignments
- **Advanced Search Capabilities**: Filter features by product, release, epic, status, assignee, and tags with flexible query options
- **Batch Operations**: Efficiently manage multiple features across releases and epics
- **Real-time Integration**: Direct API integration with Aha! ensures data consistency and immediate updates
- **Error Handling**: Robust error handling with user-friendly messages and actionable guidance
- **Security**: Secure API key management with support for environment variables and configuration files
- **Performance Optimized**: Built-in rate limiting, connection pooling, and efficient data formatting
- **Native MCP Integration**: Direct tool calling support in VS Code and Claude Desktop

## Architecture

The server follows a modular architecture designed for maintainability and extensibility:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Aha! MCP Server │◄──►│   Aha! API      │
│ (VS Code/Claude)│    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Configuration   │
                       │  & Credentials   │
                       └──────────────────┘
```

### Core Components

1. **Configuration Manager**: Handles Aha! domain and API key configuration with support for multiple configuration sources
2. **API Client**: Manages HTTP requests to Aha! REST API with automatic error handling and rate limiting
3. **Tool Handlers**: Individual functions for each MCP tool with comprehensive parameter validation
4. **Error Handler**: Centralized error handling with user-friendly messages and recovery suggestions
5. **Data Formatter**: Formats Aha! API responses for optimal LLM consumption and human readability

## Installation

### Prerequisites

- Python 3.8 or higher
- Active Aha! account with API access
- Valid Aha! API key
- VS Code with GitHub Copilot (for MCP integration)

### Quick Installation

```bash
# Clone or download the server files
git clone https://github.com/your-username/aha-mcp-server.git
cd aha-mcp-server

# Install dependencies
pip install -r requirements.txt

# Configure your Aha! credentials (see Configuration section)
cp aha_config.json.example aha_config.json
# Edit aha_config.json with your credentials
```

### Development Installation

```bash
# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest tests/
```

## Configuration

The server supports multiple configuration methods for maximum flexibility:

### Method 1: Environment Variables (Recommended)

```bash
export AHA_DOMAIN="yourcompany.aha.io"
export AHA_API_KEY="your_api_key_here"
export AHA_DEFAULT_PRODUCT="optional_default_product_id"
export AHA_RATE_LIMIT_DELAY="0.2"
export AHA_TIMEOUT="30"
```

### Method 2: Configuration File

Create an `aha_config.json` file in the server directory:

```json
{
  "aha_domain": "yourcompany.aha.io",
  "api_key": "your_api_key_here",
  "default_product": "optional_default_product_id",
  "rate_limit_delay": 0.2,
  "timeout": 30
}
```

### Obtaining Your API Key

1. Log into your Aha! account
2. Navigate to Settings → Personal → Developer
3. Click "Generate API key"
4. Copy the generated key and use it in your configuration

## Usage

### Running the Server

```bash
# Run the MCP server
python aha_mcp_server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Connecting to Claude Desktop

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "aha": {
      "command": "python",
      "args": ["/path/to/aha_mcp_server.py"],
      "env": {
        "AHA_DOMAIN": "yourcompany.aha.io",
        "AHA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ Available MCP Tools

The Aha! MCP Server provides the following tools for AI agents and users:

### Feature Management Tools
- `mcp_aha_get_feature` - Get detailed feature information
- `mcp_aha_search_features` - Search features with advanced filters
- `mcp_aha_create_feature` - Create new features
- `mcp_aha_update_feature` - Update existing features
- `mcp_aha_delete_feature` - Delete features (with confirmation)
- `mcp_aha_update_feature_status` - Update feature workflow status
- `mcp_aha_update_feature_score` - Update feature scoring
- `mcp_aha_add_feature_tags` - Add or replace feature tags

### Product & Release Management Tools
- `mcp_aha_list_products` - List all available products
- `mcp_aha_list_features_by_release` - Get features in a specific release
- `mcp_aha_list_features_by_epic` - Get features in a specific epic

### Ideas & Customer Feedback Tools
- `mcp_aha_get_related_ideas` - Search for customer ideas and feedback

### 🎯 Common Use Cases for AI Agents

**Feature Discovery:**
```
@mcp_aha_search_features query="API security" status="Planning"
@mcp_aha_get_feature DNAC-10991
```

**Feature Management:**
```
@mcp_aha_create_feature name="New Security Feature" description="Enhanced API security controls"
@mcp_aha_update_feature_status DNAC-3080 "In Development"
```

**Reporting & Analysis:**
```
@mcp_aha_search_features assignee="Pratik Patel"
@mcp_aha_list_features_by_release CatC-3.2.1
```

## 🔧 Troubleshooting for AI Agents

### Common Issues and Solutions

**1. MCP Tools Not Available**
```bash
# Check if MCP server is configured in VS Code settings.json
# Verify the paths are correct and python environment is activated
source aha-mcp-env/bin/activate
python aha_mcp_server.py --help  # Should show MCP server info
```

**2. Authentication Errors (403 Forbidden)**
```bash
# Verify API key in aha_config.json
# Check if user has proper permissions in Aha! workspace
curl -H "Authorization: Bearer YOUR_API_KEY" https://ciscospinfra.aha.io/api/v1/products
```

**3. Feature Creation Fails**
- Features must be created under a specific release
- Use `POST /api/v1/releases/{release_id}/features` endpoint
- Ensure all mandatory fields are provided

**4. MCP Server Not Responding**
```bash
# Restart the MCP server
pkill -f aha_mcp_server.py
cd /path/to/aha-mcp-server
source aha-mcp-env/bin/activate
python aha_mcp_server.py
```

### Environment Validation Script

```bash
#!/bin/bash
# Validate MCP setup
echo "🔍 Validating Aha MCP Server Setup..."

# Check Python environment
if [ -d "aha-mcp-env" ]; then
    echo "✅ Virtual environment found"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Check configuration
if [ -f "aha_config.json" ]; then
    echo "✅ Configuration file found"
else
    echo "❌ Configuration file missing"
    exit 1
fi

# Test API connectivity
source aha-mcp-env/bin/activate
python -c "
from aha_mcp_server import load_config, AhaAPIClient
import asyncio

async def test():
    config = load_config()
    async with AhaAPIClient(config) as client:
        data = await client.request('GET', '/products', params={'per_page': 1})
        print('✅ API connectivity successful')

asyncio.run(test())
"

echo "🎉 Aha MCP Server validation complete!"
```

## Overview

The Aha! MCP Server bridges the gap between AI-powered tools and product management workflows by exposing Aha!'s feature management capabilities through the standardized Model Context Protocol. Built with Python and the FastMCP framework, this server provides robust, production-ready tools for managing product features, releases, and epics.

### Key Features

- **Comprehensive Feature Management**: Search, create, update, and delete features with full support for custom fields, tags, and assignments
- **Advanced Search Capabilities**: Filter features by product, release, epic, status, assignee, and tags with flexible query options
- **Batch Operations**: Efficiently manage multiple features across releases and epics
- **Real-time Integration**: Direct API integration with Aha! ensures data consistency and immediate updates
- **Error Handling**: Robust error handling with user-friendly messages and actionable guidance
- **Security**: Secure API key management with support for environment variables and configuration files
- **Performance Optimized**: Built-in rate limiting, connection pooling, and efficient data formatting
- **Native MCP Integration**: Direct tool calling support in VS Code and Claude Desktop

## Architecture

The server follows a modular architecture designed for maintainability and extensibility:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Aha! MCP Server │◄──►│   Aha! API      │
│ (VS Code/Claude)│    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Configuration   │
                       │  & Credentials   │
                       └──────────────────┘
```

### Core Components

1. **Configuration Manager**: Handles Aha! domain and API key configuration with support for multiple configuration sources
2. **API Client**: Manages HTTP requests to Aha! REST API with automatic error handling and rate limiting
3. **Tool Handlers**: Individual functions for each MCP tool with comprehensive parameter validation
4. **Error Handler**: Centralized error handling with user-friendly messages and recovery suggestions
5. **Data Formatter**: Formats Aha! API responses for optimal LLM consumption and human readability

## Installation

### Prerequisites

- Python 3.8 or higher
- Active Aha! account with API access
- Valid Aha! API key
- VS Code with GitHub Copilot (for MCP integration)

### Quick Installation

```bash
# Clone or download the server files
git clone https://github.com/your-username/aha-mcp-server.git
cd aha-mcp-server

# Install dependencies
pip install -r requirements.txt

# Configure your Aha! credentials (see Configuration section)
cp aha_config.json.example aha_config.json
# Edit aha_config.json with your credentials
```

### Development Installation

```bash
# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest tests/
```

## Configuration

The server supports multiple configuration methods for maximum flexibility:

### Method 1: Environment Variables (Recommended)

```bash
export AHA_DOMAIN="yourcompany.aha.io"
export AHA_API_KEY="your_api_key_here"
export AHA_DEFAULT_PRODUCT="optional_default_product_id"
export AHA_RATE_LIMIT_DELAY="0.2"
export AHA_TIMEOUT="30"
```

### Method 2: Configuration File

Create an `aha_config.json` file in the server directory:

```json
{
  "aha_domain": "yourcompany.aha.io",
  "api_key": "your_api_key_here",
  "default_product": "optional_default_product_id",
  "rate_limit_delay": 0.2,
  "timeout": 30
}
```

### Obtaining Your API Key

1. Log into your Aha! account
2. Navigate to Settings → Personal → Developer
3. Click "Generate API key"
4. Copy the generated key and use it in your configuration

## Usage

### Running the Server

```bash
# Run the MCP server
python aha_mcp_server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Connecting to Claude Desktop

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "aha": {
      "command": "python",
      "args": ["/path/to/aha_mcp_server.py"],
      "env": {
        "AHA_DOMAIN": "yourcompany.aha.io",
        "AHA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ Available MCP Tools

The Aha! MCP Server provides the following tools for AI agents and users:

### Feature Management Tools
- `mcp_aha_get_feature` - Get detailed feature information
- `mcp_aha_search_features` - Search features with advanced filters
- `mcp_aha_create_feature` - Create new features
- `mcp_aha_update_feature` - Update existing features
- `mcp_aha_delete_feature` - Delete features (with confirmation)
- `mcp_aha_update_feature_status` - Update feature workflow status
- `mcp_aha_update_feature_score` - Update feature scoring
- `mcp_aha_add_feature_tags` - Add or replace feature tags

### Product & Release Management Tools
- `mcp_aha_list_products` - List all available products
- `mcp_aha_list_features_by_release` - Get features in a specific release
- `mcp_aha_list_features_by_epic` - Get features in a specific epic

### Ideas & Customer Feedback Tools
- `mcp_aha_get_related_ideas` - Search for customer ideas and feedback

### 🎯 Common Use Cases for AI Agents

**Feature Discovery:**
```
@mcp_aha_search_features query="API security" status="Planning"
@mcp_aha_get_feature DNAC-10991
```

**Feature Management:**
```
@mcp_aha_create_feature name="New Security Feature" description="Enhanced API security controls"
@mcp_aha_update_feature_status DNAC-3080 "In Development"
```

**Reporting & Analysis:**
```
@mcp_aha_search_features assignee="Pratik Patel"
@mcp_aha_list_features_by_release CatC-3.2.1
```

## 🔧 Troubleshooting for AI Agents

### Common Issues and Solutions

**1. MCP Tools Not Available**
```bash
# Check if MCP server is configured in VS Code settings.json
# Verify the paths are correct and python environment is activated
source aha-mcp-env/bin/activate
python aha_mcp_server.py --help  # Should show MCP server info
```

**2. Authentication Errors (403 Forbidden)**
```bash
# Verify API key in aha_config.json
# Check if user has proper permissions in Aha! workspace
curl -H "Authorization: Bearer YOUR_API_KEY" https://ciscospinfra.aha.io/api/v1/products
```

**3. Feature Creation Fails**
- Features must be created under a specific release
- Use `POST /api/v1/releases/{release_id}/features` endpoint
- Ensure all mandatory fields are provided

**4. MCP Server Not Responding**
```bash
# Restart the MCP server
pkill -f aha_mcp_server.py
cd /path/to/aha-mcp-server
source aha-mcp-env/bin/activate
python aha_mcp_server.py
```

### Environment Validation Script

```bash
#!/bin/bash
# Validate MCP setup
echo "🔍 Validating Aha MCP Server Setup..."

# Check Python environment
if [ -d "aha-mcp-env" ]; then
    echo "✅ Virtual environment found"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Check configuration
if [ -f "aha_config.json" ]; then
    echo "✅ Configuration file found"
else
    echo "❌ Configuration file missing"
    exit 1
fi

# Test API connectivity
source aha-mcp-env/bin/activate
python -c "
from aha_mcp_server import load_config, AhaAPIClient
import asyncio

async def test():
    config = load_config()
    async with AhaAPIClient(config) as client:
        data = await client.request('GET', '/products', params={'per_page': 1})
        print('✅ API connectivity successful')

asyncio.run(test())
"

echo "🎉 Aha MCP Server validation complete!"
```

## Overview

The Aha! MCP Server bridges the gap between AI-powered tools and product management workflows by exposing Aha!'s feature management capabilities through the standardized Model Context Protocol. Built with Python and the FastMCP framework, this server provides robust, production-ready tools for managing product features, releases, and epics.

### Key Features

- **Comprehensive Feature Management**: Search, create, update, and delete features with full support for custom fields, tags, and assignments
- **Advanced Search Capabilities**: Filter features by product, release, epic, status, assignee, and tags with flexible query options
- **Batch Operations**: Efficiently manage multiple features across releases and epics
- **Real-time Integration**: Direct API integration with Aha! ensures data consistency and immediate updates
- **Error Handling**: Robust error handling with user-friendly messages and actionable guidance
- **Security**: Secure API key management with support for environment variables and configuration files
- **Performance Optimized**: Built-in rate limiting, connection pooling, and efficient data formatting
- **Native MCP Integration**: Direct tool calling support in VS Code and Claude Desktop

## Architecture

The server follows a modular architecture designed for maintainability and extensibility:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Aha! MCP Server │◄──►│   Aha! API      │
│ (VS Code/Claude)│    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Configuration   │
                       │  & Credentials   │
                       └──────────────────┘
```

### Core Components

1. **Configuration Manager**: Handles Aha! domain and API key configuration with support for multiple configuration sources
2. **API Client**: Manages HTTP requests to Aha! REST API with automatic error handling and rate limiting
3. **Tool Handlers**: Individual functions for each MCP tool with comprehensive parameter validation
4. **Error Handler**: Centralized error handling with user-friendly messages and recovery suggestions
5. **Data Formatter**: Formats Aha! API responses for optimal LLM consumption and human readability

## Installation

### Prerequisites

- Python 3.8 or higher
- Active Aha! account with API access
- Valid Aha! API key
- VS Code with GitHub Copilot (for MCP integration)

### Quick Installation

```bash
# Clone or download the server files
git clone https://github.com/your-username/aha-mcp-server.git
cd aha-mcp-server

# Install dependencies
pip install -r requirements.txt

# Configure your Aha! credentials (see Configuration section)
cp aha_config.json.example aha_config.json
# Edit aha_config.json with your credentials
```

### Development Installation

```bash
# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest tests/
```

## Configuration

The server supports multiple configuration methods for maximum flexibility:

### Method 1: Environment Variables (Recommended)

```bash
export AHA_DOMAIN="yourcompany.aha.io"
export AHA_API_KEY="your_api_key_here"
export AHA_DEFAULT_PRODUCT="optional_default_product_id"
export AHA_RATE_LIMIT_DELAY="0.2"
export AHA_TIMEOUT="30"
```

### Method 2: Configuration File

Create an `aha_config.json` file in the server directory:

```json
{
  "aha_domain": "yourcompany.aha.io",
  "api_key": "your_api_key_here",
  "default_product": "optional_default_product_id",
  "rate_limit_delay": 0.2,
  "timeout": 30
}
```

### Obtaining Your API Key

1. Log into your Aha! account
2. Navigate to Settings → Personal → Developer
3. Click "Generate API key"
4. Copy the generated key and use it in your configuration

## Usage

### Running the Server

```bash
# Run the MCP server
python aha_mcp_server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Connecting to Claude Desktop

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "aha": {
      "command": "python",
      "args": ["/path/to/aha_mcp_server.py"],
      "env": {
        "AHA_DOMAIN": "yourcompany.aha.io",
        "AHA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ Available MCP Tools

The Aha! MCP Server provides the following tools for AI agents and users:

### Feature Management Tools
- `mcp_aha_get_feature` - Get detailed feature information
- `mcp_aha_search_features` - Search features with advanced filters
- `mcp_aha_create_feature` - Create new features
- `mcp_aha_update_feature` - Update existing features
- `mcp_aha_delete_feature` - Delete features (with confirmation)
- `mcp_aha_update_feature_status` - Update feature workflow status
- `mcp_aha_update_feature_score` - Update feature scoring
- `mcp_aha_add_feature_tags` - Add or replace feature tags

### Product & Release Management Tools
- `mcp_aha_list_products` - List all available products
- `mcp_aha_list_features_by_release` - Get features in a specific release
- `mcp_aha_list_features_by_epic` - Get features in a specific epic

### Ideas & Customer Feedback Tools
- `mcp_aha_get_related_ideas` - Search for customer ideas and feedback

### 🎯 Common Use Cases for AI Agents

**Feature Discovery:**
```
@mcp_aha_search_features query="API security" status="Planning"
@mcp_aha_get_feature DNAC-10991
```

**Feature Management:**
```
@mcp_aha_create_feature name="New Security Feature" description="Enhanced API security controls"
@mcp_aha_update_feature_status DNAC-3080 "In Development"
```

**Reporting & Analysis:**
```
@mcp_aha_search_features assignee="Pratik Patel"
@mcp_aha_list_features_by_release CatC-3.2.1
```

## 🔧 Troubleshooting for AI Agents

### Common Issues and Solutions

**1. MCP Tools Not Available**
```bash
# Check if MCP server is configured in VS Code settings.json
# Verify the paths are correct and python environment is activated
source aha-mcp-env/bin/activate
python aha_mcp_server.py --help  # Should show MCP server info
```

**2. Authentication Errors (403 Forbidden)**
```bash
# Verify API key in aha_config.json
# Check if user has proper permissions in Aha! workspace
curl -H "Authorization: Bearer YOUR_API_KEY" https://ciscospinfra.aha.io/api/v1/products
```

**3. Feature Creation Fails**
- Features must be created under a specific release
- Use `POST /api/v1/releases/{release_id}/features` endpoint
- Ensure all mandatory fields are provided

**4. MCP Server Not Responding**
```bash
# Restart the MCP server
pkill -f aha_mcp_server.py
cd /path/to/aha-mcp-server
source aha-mcp-env/bin/activate
python aha_mcp_server.py
```

### Environment Validation Script

```bash
#!/bin/bash
# Validate MCP setup
echo "🔍 Validating Aha MCP Server Setup..."

# Check Python environment
if [ -d "aha-mcp-env" ]; then
    echo "✅ Virtual environment found"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Check configuration
if [ -f "aha_config.json" ]; then
    echo "✅ Configuration file found"
else
    echo "❌ Configuration file missing"
    exit 1
fi

# Test API connectivity
source aha-mcp-env/bin/activate
python -c "
from aha_mcp_server import load_config, AhaAPIClient
import asyncio

async def test():
    config = load_config()
    async with AhaAPIClient(config) as client:
        data = await client.request('GET', '/products', params={'per_page': 1})
        print('✅ API connectivity successful')

asyncio.run(test())
"

echo "🎉 Aha MCP Server validation complete!"
```

## Overview

The Aha! MCP Server bridges the gap between AI-powered tools and product management workflows by exposing Aha!'s feature management capabilities through the standardized Model Context Protocol. Built with Python and the FastMCP framework, this server provides robust, production-ready tools for managing product features, releases, and epics.

### Key Features

- **Comprehensive Feature Management**: Search, create, update, and delete features with full support for custom fields, tags, and assignments
- **Advanced Search Capabilities**: Filter features by product, release, epic, status, assignee, and tags with flexible query options
- **Batch Operations**: Efficiently manage multiple features across releases and epics
- **Real-time Integration**: Direct API integration with Aha! ensures data consistency and immediate updates
- **Error Handling**: Robust error handling with user-friendly messages and actionable guidance
- **Security**: Secure API key management with support for environment variables and configuration files
- **Performance Optimized**: Built-in rate limiting, connection pooling, and efficient data formatting
- **Native MCP Integration**: Direct tool calling support in VS Code and Claude Desktop

## Architecture

The server follows a modular architecture designed for maintainability and extensibility:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Aha! MCP Server │◄──►│   Aha! API      │
│ (VS Code/Claude)│    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Configuration   │
                       │  & Credentials   │
                       └──────────────────┘
```

### Core Components

1. **Configuration Manager**: Handles Aha! domain and API key configuration with support for multiple configuration sources
2. **API Client**: Manages HTTP requests to Aha! REST API with automatic error handling and rate limiting
3. **Tool Handlers**: Individual functions for each MCP tool with comprehensive parameter validation
4. **Error Handler**: Centralized error handling with user-friendly messages and recovery suggestions
5. **Data Formatter**: Formats Aha! API responses for optimal LLM consumption and human readability

## Installation

### Prerequisites

- Python 3.8 or higher
- Active Aha! account with API access
- Valid Aha! API key
- VS Code with GitHub Copilot (for MCP integration)

### Quick Installation

```bash
# Clone or download the server files
git clone https://github.com/your-username/aha-mcp-server.git
cd aha-mcp-server

# Install dependencies
pip install -r requirements.txt

# Configure your Aha! credentials (see Configuration section)
cp aha_config.json.example aha_config.json
# Edit aha_config.json with your credentials
```

### Development Installation

```bash
# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest tests/
```

## Configuration

The server supports multiple configuration methods for maximum flexibility:

### Method 1: Environment Variables (Recommended)

```bash
export AHA_DOMAIN="yourcompany.aha.io"
export AHA_API_KEY="your_api_key_here"
export AHA_DEFAULT_PRODUCT="optional_default_product_id"
export AHA_RATE_LIMIT_DELAY="0.2"
export AHA_TIMEOUT="30"
```

### Method 2: Configuration File

Create an `aha_config.json` file in the server directory:

```json
{
  "aha_domain": "yourcompany.aha.io",
  "api_key": "your_api_key_here",
  "default_product": "optional_default_product_id",
  "rate_limit_delay": 0.2,
  "timeout": 30
}
```

### Obtaining Your API Key

1. Log into your Aha! account
2. Navigate to Settings → Personal → Developer
3. Click "Generate API key"
4. Copy the generated key and use it in your configuration

## Usage

### Running the Server

```bash
# Run the MCP server
python aha_mcp_server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Connecting to Claude Desktop

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "aha": {
      "command": "python",
      "args": ["/path/to/aha_mcp_server.py"],
      "env": {
        "AHA_DOMAIN": "yourcompany.aha.io",
        "AHA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ Available MCP Tools

The Aha! MCP Server provides the following tools for AI agents and users:

### Feature Management Tools
- `mcp_aha_get_feature` - Get detailed feature information
- `mcp_aha_search_features` - Search features with advanced filters
- `mcp_aha_create_feature` - Create new features
- `mcp_aha_update_feature` - Update existing features
- `mcp_aha_delete_feature` - Delete features (with confirmation)
- `mcp_aha_update_feature_status` - Update feature workflow status
- `mcp_aha_update_feature_score` - Update feature scoring
- `mcp_aha_add_feature_tags` - Add or replace feature tags

### Product & Release Management Tools
- `mcp_aha_list_products` - List all available products
- `mcp_aha_list_features_by_release` - Get features in a specific release
- `mcp_aha_list_features_by_epic` - Get features in a specific epic

### Ideas & Customer Feedback Tools
- `mcp_aha_get_related_ideas` - Search for customer ideas and feedback

### 🎯 Common Use Cases for AI Agents

**Feature Discovery:**
```
@mcp_aha_search_features query="API security" status="Planning"
@mcp_aha_get_feature DNAC-10991
```

**Feature Management:**
```
@mcp_aha_create_feature name="New Security Feature" description="Enhanced API security controls"
@mcp_aha_update_feature_status DNAC-3080 "In Development"
```

**Reporting & Analysis:**
```
@mcp_aha_search_features assignee="Pratik Patel"
@mcp_aha_list_features_by_release CatC-3.2.1
```

## 🔧 Troubleshooting for AI Agents

### Common Issues and Solutions

**1. MCP Tools Not Available**
```bash
# Check if MCP server is configured in VS Code settings.json
# Verify the paths are correct and python environment is activated
source aha-mcp-env/bin/activate
python aha_mcp_server.py --help  # Should show MCP server info
```

**2. Authentication Errors (403 Forbidden)**
```bash
# Verify API key in aha_config.json
# Check if user has proper permissions in Aha! workspace
curl -H "Authorization: Bearer YOUR_API_KEY" https://ciscospinfra.aha.io/api/v1/products
```

**3. Feature Creation Fails**
- Features must be created under a specific release
- Use `POST /api/v1/releases/{release_id}/features` endpoint
- Ensure all mandatory fields are provided

**4. MCP Server Not Responding**
```bash
# Restart the MCP server
pkill -f aha_mcp_server.py
cd /path/to/aha-mcp-server
source aha-mcp-env/bin/activate
python aha_mcp_server.py
```

### Environment Validation Script

```bash
#!/bin/bash
# Validate MCP setup
echo "🔍 Validating Aha MCP Server Setup..."

# Check Python environment
if [ -d "aha-mcp-env" ]; then
    echo "✅ Virtual environment found"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Check configuration
if [ -f "aha_config.json" ]; then
    echo "✅ Configuration file found"
else
    echo "❌ Configuration file missing"
    exit 1
fi

# Test API connectivity
source aha-mcp-env/bin/activate
python -c "
from aha_mcp_server import load_config, AhaAPIClient
import asyncio

async def test():
    config = load_config()
    async with AhaAPIClient(config) as client:
        data = await client.request('GET', '/products', params={'per_page': 1})
        print('✅ API connectivity successful')

asyncio.run(test())
"

echo "🎉 Aha MCP Server validation complete!"
```

## Overview

The Aha! MCP Server bridges the gap between AI-powered tools and product management workflows by exposing Aha!'s feature management capabilities through the standardized Model Context Protocol. Built with Python and the FastMCP framework, this server provides robust, production-ready tools for managing product features, releases, and epics.

### Key Features

- **Comprehensive Feature Management**: Search, create, update, and delete features with full support for custom fields, tags, and assignments
- **Advanced Search Capabilities**: Filter features by product, release, epic, status, assignee, and tags with flexible query options
- **Batch Operations**: Efficiently manage multiple features across releases and epics
- **Real-time Integration**: Direct API integration with Aha! ensures data consistency and immediate updates
- **Error Handling**: Robust error handling with user-friendly messages and actionable guidance
- **Security**: Secure API key management with support for environment variables and configuration files
- **Performance Optimized**: Built-in rate limiting, connection pooling, and efficient data formatting
- **Native MCP Integration**: Direct tool calling support in VS Code and Claude Desktop

## Architecture

The server follows a modular architecture designed for maintainability and extensibility:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Aha! MCP Server │◄──►│   Aha! API      │
│ (VS Code/Claude)│    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Configuration   │
                       │  & Credentials   │
                       └──────────────────┘
```

### Core Components

1. **Configuration Manager**: Handles Aha! domain and API key configuration with support for multiple configuration sources
2. **API Client**: Manages HTTP requests to Aha! REST API with automatic error handling and rate limiting
3. **Tool Handlers**: Individual functions for each MCP tool with comprehensive parameter validation
4. **Error Handler**: Centralized error handling with user-friendly messages and recovery suggestions
5. **Data Formatter**: Formats Aha! API responses for optimal LLM consumption and human readability

## Installation

### Prerequisites

- Python 3.8 or higher
- Active Aha! account with API access
- Valid Aha! API key
- VS Code with GitHub Copilot (for MCP integration)

### Quick Installation

```bash
# Clone or download the server files
git clone https://github.com/your-username/aha-mcp-server.git
cd aha-mcp-server

# Install dependencies
pip install -r requirements.txt

# Configure your Aha! credentials (see Configuration section)
cp aha_config.json.example aha_config.json
# Edit aha_config.json with your credentials
```

### Development Installation

```bash
# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest tests/
```

## Configuration

The server supports multiple configuration methods for maximum flexibility:

### Method 1: Environment Variables (Recommended)

```bash
export AHA_DOMAIN="yourcompany.aha.io"
export AHA_API_KEY="your_api_key_here"
export AHA_DEFAULT_PRODUCT="optional_default_product_id"
export AHA_RATE_LIMIT_DELAY="0.2"
export AHA_TIMEOUT="30"
```

### Method 2: Configuration File

Create an `aha_config.json` file in the server directory:

```json
{
  "aha_domain": "yourcompany.aha.io",
  "api_key": "your_api_key_here",
  "default_product": "optional_default_product_id",
  "rate_limit_delay": 0.2,
  "timeout": 30
}
```

### Obtaining Your API Key

1. Log into your Aha! account
2. Navigate to Settings → Personal → Developer
3. Click "Generate API key"
4. Copy the generated key and use it in your configuration

## Usage

### Running the Server

```bash
# Run the MCP server
python aha_mcp_server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Connecting to Claude Desktop

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "aha": {
      "command": "python",
      "args": ["/path/to/aha_mcp_server.py"],
      "env": {
        "AHA_DOMAIN": "yourcompany.aha.io",
        "AHA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ Available MCP Tools

The Aha! MCP Server provides the following tools for AI agents and users:

### Feature Management Tools
- `mcp_aha_get_feature` - Get detailed feature information
- `mcp_aha_search_features` - Search features with advanced filters
- `mcp_aha_create_feature` - Create new features
- `mcp_aha_update_feature` - Update existing features
- `mcp_aha_delete_feature` - Delete features (with confirmation)
- `mcp_aha_update_feature_status` - Update feature workflow status
- `mcp_aha_update_feature_score` - Update feature scoring
- `mcp_aha_add_feature_tags` - Add or replace feature tags

### Product & Release Management Tools
- `mcp_aha_list_products` - List all available products
- `mcp_aha_list_features_by_release` - Get features in a specific release
- `mcp_aha_list_features_by_epic` - Get features in a specific epic

### Ideas & Customer Feedback Tools
- `mcp_aha_get_related_ideas` - Search for customer ideas and feedback

### 🎯 Common Use Cases for AI Agents

**Feature Discovery:**
```
@mcp_aha_search_features query="API security" status="Planning"
@mcp_aha_get_feature DNAC-10991
```

**Feature Management:**
```
@mcp_aha_create_feature name="New Security Feature" description="Enhanced API security controls"
@mcp_aha_update_feature_status DNAC-3080 "In Development"
```

**Reporting & Analysis:**
```
@mcp_aha_search_features assignee="Pratik Patel"
@mcp_aha_list_features_by_release CatC-3.2.1
```

## 🔧 Troubleshooting for AI Agents

### Common Issues and Solutions

**1. MCP Tools Not Available**
```bash
# Check if MCP server is configured in VS Code settings.json
# Verify the paths are correct and python environment is activated
source aha-mcp-env/bin/activate
python aha_mcp_server.py --help  # Should show MCP server info
```

**2. Authentication Errors (403 Forbidden)**
```bash
# Verify API key in aha_config.json
# Check if user has proper permissions in Aha! workspace
curl -H "Authorization: Bearer YOUR_API_KEY" https://ciscospinfra.aha.io/api/v1/products
```

**3. Feature Creation Fails**
- Features must be created under a specific release
- Use `POST /api/v1/releases/{release_id}/features` endpoint
- Ensure all mandatory fields are provided

**4. MCP Server Not Responding**
```bash
# Restart the MCP server
pkill -f aha_mcp_server.py
cd /path/to/aha-mcp-server
source aha-mcp-env/bin/activate
python aha_mcp_server.py
```

### Environment Validation Script

```bash
#!/bin/bash
# Validate MCP setup
echo "🔍 Validating Aha MCP Server Setup..."

# Check Python environment
if [ -d "aha-mcp-env" ]; then
    echo "✅ Virtual environment found"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Check configuration
if [ -f "aha_config.json" ]; then
    echo "✅ Configuration file found"
else
    echo "❌ Configuration file missing"
    exit 1
fi

# Test API connectivity
source aha-mcp-env/bin/activate
python -c "
from aha_mcp_server import load_config, AhaAPIClient
import asyncio

async def test():
    config = load_config()
    async with AhaAPIClient(config) as client:
        data = await client.request('GET', '/products', params={'per_page': 1})
        print('✅ API connectivity successful')

asyncio.run(test())
"

echo "🎉 Aha MCP Server validation complete!"
```

## Overview

The Aha! MCP Server bridges the gap between AI-powered tools and product management workflows by exposing Aha!'s feature management capabilities through the standardized Model Context Protocol. Built with Python and the FastMCP framework, this server provides robust, production-ready tools for managing product features, releases, and epics.

### Key Features

- **Comprehensive Feature Management**: Search, create, update, and delete features with full support for custom fields, tags, and assignments
- **Advanced Search Capabilities**: Filter features by product, release, epic, status, assignee, and tags with flexible query options
- **Batch Operations**: Efficiently manage multiple features across releases and epics
- **Real-time Integration**: Direct API integration with Aha! ensures data consistency and immediate updates
- **Error Handling**: Robust error handling with user-friendly messages and actionable guidance
- **Security**: Secure API key management with support for environment variables and configuration files
- **Performance Optimized**: Built-in rate limiting, connection pooling, and efficient data formatting
- **Native MCP Integration**: Direct tool calling support in VS Code and Claude Desktop

## Architecture

The server follows a modular architecture designed for maintainability and extensibility:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Aha! MCP Server │◄──►│   Aha! API      │
│ (VS Code/Claude)│    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Configuration   │
                       │  & Credentials   │
                       └──────────────────┘
```

### Core Components

1. **Configuration Manager**: Handles Aha! domain and API key configuration with support for multiple configuration sources
2. **API Client**: Manages HTTP requests to Aha! REST API with automatic error handling and rate limiting
3. **Tool Handlers**: Individual functions for each MCP tool with comprehensive parameter validation
4. **Error Handler**: Centralized error handling with user-friendly messages and recovery suggestions
5. **Data Formatter**: Formats Aha! API responses for optimal LLM consumption and human readability

## Installation

### Prerequisites

- Python 3.8 or higher
- Active Aha! account with API access
- Valid Aha! API key
- VS Code with GitHub Copilot (for MCP integration)

### Quick Installation

```bash
# Clone or download the server files
git clone https://github.com/your-username/aha-mcp-server.git
cd aha-mcp-server

# Install dependencies
pip install -r requirements.txt

# Configure your Aha! credentials (see Configuration section)
cp aha_config.json.example aha_config.json
# Edit aha_config.json with your credentials
```

### Development Installation

```bash
# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest tests/
```

## Configuration

The server supports multiple configuration methods for maximum flexibility:

### Method 1: Environment Variables (Recommended)

```bash
export AHA_DOMAIN="yourcompany.aha.io"
export AHA_API_KEY="your_api_key_here"
export AHA_DEFAULT_PRODUCT="optional_default_product_id"
export AHA_RATE_LIMIT_DELAY="0.2"
export AHA_TIMEOUT="30"
```

### Method 2: Configuration File

Create an `aha_config.json` file in the server directory:

```json
{
  "aha_domain": "yourcompany.aha.io",
  "api_key": "your_api_key_here",
  "default_product": "optional_default_product_id",
  "rate_limit_delay": 0.2,
  "timeout": 30
}
```

### Obtaining Your API Key

1. Log into your Aha! account
2. Navigate to Settings → Personal → Developer
3. Click "Generate API key"
4. Copy the generated key and use it in your configuration

## Usage

### Running the Server

```bash
# Run the MCP server
python aha_mcp_server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Connecting to Claude Desktop

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "aha": {
      "command": "python",
      "args": ["/path/to/aha_mcp_server.py"],
      "env": {
        "AHA_DOMAIN": "yourcompany.aha.io",
        "AHA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ Available MCP Tools

The Aha! MCP Server provides the following tools for AI agents and users:

### Feature Management Tools
- `mcp_aha_get_feature` - Get detailed feature information
- `mcp_aha_search_features` - Search features with advanced filters
- `mcp_aha_create_feature` - Create new features
- `mcp_aha_update_feature` - Update existing features
- `mcp_aha_delete_feature` - Delete features (with confirmation)
- `mcp_aha_update_feature_status` - Update feature workflow status
- `mcp_aha_update_feature_score` - Update feature scoring
- `mcp_aha_add_feature_tags` - Add or replace feature tags

### Product & Release Management Tools
- `mcp_aha_list_products` - List all available products
- `mcp_aha_list_features_by_release` - Get features in a specific release
- `mcp_aha_list_features_by_epic` - Get features in a specific epic

### Ideas & Customer Feedback Tools
- `mcp_aha_get_related_ideas` - Search for customer ideas and feedback

### 🎯 Common Use Cases for AI Agents

**Feature Discovery:**
```
@mcp_aha_search_features query="API security" status="Planning"
@mcp_aha_get_feature DNAC-10991
```

**Feature Management:**
```
@mcp_aha_create_feature name="New Security Feature" description="Enhanced API security controls"
@mcp_aha_update_feature_status DNAC-3080 "In Development"
```

**Reporting & Analysis:**
```
@mcp_aha_search_features assignee="Pratik Patel"
@mcp_aha_list_features_by_release CatC-3.2.1
```

## 🔧 Troubleshooting for AI Agents

### Common Issues and Solutions

**1. MCP Tools Not Available**
```bash
# Check if MCP server is configured in VS Code settings.json
# Verify the paths are correct and python environment is activated
source aha-mcp-env/bin/activate
python aha_mcp_server.py --help  # Should show MCP server info
```

**2. Authentication Errors (403 Forbidden)**
```bash
# Verify API key in aha_config.json
# Check if user has proper permissions in Aha! workspace
curl -H "Authorization: Bearer YOUR_API_KEY" https://ciscospinfra.aha.io/api/v1/products
```

**3. Feature Creation Fails**
- Features must be created under a specific release
- Use `POST /api/v1/releases/{release_id}/features` endpoint
- Ensure all mandatory fields are provided

**4. MCP Server Not Responding**
```bash
# Restart the MCP server
pkill -f aha_mcp_server.py
cd /path/to/aha-mcp-server
source aha-mcp-env/bin/activate
python aha_mcp_server.py
```

### Environment Validation Script

```bash
#!/bin/bash
# Validate MCP setup
echo "🔍 Validating Aha MCP Server Setup..."

# Check Python environment
if [ -d "aha-mcp-env" ]; then
    echo "✅ Virtual environment found"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Check configuration
if [ -f "aha_config.json" ]; then
    echo "✅ Configuration file found"
else
    echo "❌ Configuration file missing"
    exit 1
fi

# Test API connectivity
source aha-mcp-env/bin/activate
python -c "
from aha_mcp_server import load_config, AhaAPIClient
import asyncio

async def test():
    config = load_config()
    async with AhaAPIClient(config) as client:
        data = await client.request('GET', '/products', params={'per_page': 1})
        print('✅ API connectivity successful')

asyncio.run(test())
"

echo "🎉 Aha MCP Server validation complete!"
```

## Overview

The Aha! MCP Server bridges the gap between AI-powered tools and product management workflows by exposing Aha!'s feature management capabilities through the standardized Model Context Protocol. Built with Python and the FastMCP framework, this server provides robust, production-ready tools for managing product features, releases, and epics.

### Key Features

- **Comprehensive Feature Management**: Search, create, update, and delete features with full support for custom fields, tags, and assignments
- **Advanced Search Capabilities**: Filter features by product, release, epic, status, assignee, and tags with flexible query options
- **Batch Operations**: Efficiently manage multiple features across releases and epics
- **Real-time Integration**: Direct API integration with Aha! ensures data consistency and immediate updates
- **Error Handling**: Robust error handling with user-friendly messages and actionable guidance
- **Security**: Secure API key management with support for environment variables and configuration files
- **Performance Optimized**: Built-in rate limiting, connection pooling, and efficient data formatting
- **Native MCP Integration**: Direct tool calling support in VS Code and Claude Desktop

## Architecture

The server follows a modular architecture designed for maintainability and extensibility:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Aha! MCP Server │◄──►│   Aha! API      │
│ (VS Code/Claude)│    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Configuration   │
                       │  & Credentials   │
                       └──────────────────┘
```

### Core Components

1. **Configuration Manager**: Handles Aha! domain and API key configuration with support for multiple configuration sources
2. **API Client**: Manages HTTP requests to Aha! REST API with automatic error handling and rate limiting
3. **Tool Handlers**: Individual functions for each MCP tool with comprehensive parameter validation
4. **Error Handler**: Centralized error handling with user-friendly messages and recovery suggestions
5. **Data Formatter**: Formats Aha! API responses for optimal LLM consumption and human readability

## Installation

### Prerequisites

- Python 3.8 or higher
- Active Aha! account with API access
- Valid Aha! API key
- VS Code with GitHub Copilot (for MCP integration)

### Quick Installation

```bash
# Clone or download the server files
git clone https://github.com/your-username/aha-mcp-server.git
cd aha-mcp-server

# Install dependencies
pip install -r requirements.txt

# Configure your Aha! credentials (see Configuration section)
cp aha_config.json.example aha_config.json
# Edit aha_config.json with your credentials
```

### Development Installation

```bash
# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest tests/
```

## Configuration

The server supports multiple configuration methods for maximum flexibility:

### Method 1: Environment Variables (Recommended)

```bash
export AHA_DOMAIN="yourcompany.aha.io"
export AHA_API_KEY="your_api_key_here"
export AHA_DEFAULT_PRODUCT="optional_default_product_id"
export AHA_RATE_LIMIT_DELAY="0.2"
export AHA_TIMEOUT="30"
```

### Method 2: Configuration File

Create an `aha_config.json` file in the server directory:

```json
{
  "aha_domain": "yourcompany.aha.io",
  "api_key": "your_api_key_here",
  "default_product": "optional_default_product_id",
  "rate_limit_delay": 0.2,
  "timeout": 30
}
```

### Obtaining Your API Key

1. Log into your Aha! account
2. Navigate to Settings → Personal → Developer
3. Click "Generate API key"
4. Copy the generated key and use it in your configuration

## Usage

### Running the Server

```bash
# Run the MCP server
python aha_mcp_server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Connecting to Claude Desktop

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "aha": {
      "command": "python",
      "args": ["/path/to/aha_mcp_server.py"],
      "env": {
        "AHA_DOMAIN": "yourcompany.aha.io",
        "AHA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ Available MCP Tools

The Aha! MCP Server provides the following tools for AI agents and users:

### Feature Management Tools
- `mcp_aha_get_feature` - Get detailed feature information
- `mcp_aha_search_features` - Search features with advanced filters
- `mcp_aha_create_feature` - Create new features
- `mcp_aha_update_feature` - Update existing features
- `mcp_aha_delete_feature` - Delete features (with confirmation)
- `mcp_aha_update_feature_status` - Update feature workflow status
- `mcp_aha_update_feature_score` - Update feature scoring
- `mcp_aha_add_feature_tags` - Add or replace feature tags

### Product & Release Management Tools
- `mcp_aha_list_products` - List all available products
- `mcp_aha_list_features_by_release` - Get features in a specific release
- `mcp_aha_list_features_by_epic` - Get features in a specific epic

### Ideas & Customer Feedback Tools
- `mcp_aha_get_related_ideas` - Search for customer ideas and feedback

### 🎯 Common Use Cases for AI Agents

**Feature Discovery:**
```
@mcp_aha_search_features query="API security" status="Planning"
@mcp_aha_get_feature DNAC-10991
```

**Feature Management:**
```
@mcp_aha_create_feature name="New Security Feature" description="Enhanced API security controls"
@mcp_aha_update_feature_status DNAC-3080 "In Development"
```

**Reporting & Analysis:**
```
@mcp_aha_search_features assignee="Pratik Patel"
@mcp_aha_list_features_by_release CatC-3.2.1
```

## 🔧 Troubleshooting for AI Agents

### Common Issues and Solutions

**1. MCP Tools Not Available**
```bash
# Check if MCP server is configured in VS Code settings.json
# Verify the paths are correct and python environment is activated
source aha-mcp-env/bin/activate
python aha_mcp_server.py --help  # Should show MCP server info
```

**2. Authentication Errors (403 Forbidden)**
```bash
# Verify API key in aha_config.json
# Check if user has proper permissions in Aha! workspace
curl -H "Authorization: Bearer YOUR_API_KEY" https://ciscospinfra.aha.io/api/v1/products
```

**3. Feature Creation Fails**
- Features must be created under a specific release
- Use `POST /api/v1/releases/{release_id}/features` endpoint
- Ensure all mandatory fields are provided

**4. MCP Server Not Responding**
```bash
# Restart the MCP server
pkill -f aha_mcp_server.py
cd /path/to/aha-mcp-server
source aha-mcp-env/bin/activate
python aha_mcp_server.py
```

### Environment Validation Script

```bash
#!/bin/bash
# Validate MCP setup
echo "🔍 Validating Aha MCP Server Setup..."

# Check Python environment
if [ -d "aha-mcp-env" ]; then
    echo "✅ Virtual environment found"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Check configuration
if [ -f "aha_config.json" ]; then
    echo "✅ Configuration file found"
else
    echo "❌ Configuration file missing"
    exit 1
fi

# Test API connectivity
source aha-mcp-env/bin/activate
python -c "
from aha_mcp_server import load_config, AhaAPIClient
import asyncio

async def test():
    config = load_config()
    async with AhaAPIClient(config) as client:
        data = await client.request('GET', '/products', params={'per_page': 1})
        print('✅ API connectivity successful')

asyncio.run(test())
"

echo "🎉 Aha MCP Server validation complete!"
```

## Overview

The Aha! MCP Server bridges the gap between AI-powered tools and product management workflows by exposing Aha!'s feature management capabilities through the standardized Model Context Protocol. Built with Python and the FastMCP framework, this server provides robust, production-ready tools for managing product features, releases, and epics.

### Key Features

- **Comprehensive Feature Management**: Search, create, update, and delete features with full support for custom fields, tags, and assignments
- **Advanced Search Capabilities**: Filter features by product, release, epic, status, assignee, and tags with flexible query options
- **Batch Operations**: Efficiently manage multiple features across releases and epics
- **Real-time Integration**: Direct API integration with Aha! ensures data consistency and immediate updates
- **Error Handling**: Robust error handling with user-friendly messages and actionable guidance
- **Security**: Secure API key management with support for environment variables and configuration files
- **Performance Optimized**: Built-in rate limiting, connection pooling, and efficient data formatting
- **Native MCP Integration**: Direct tool calling support in VS Code and Claude Desktop

## Architecture

The server follows a modular architecture designed for maintainability and extensibility:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Aha! MCP Server │◄──►│   Aha! API      │
│ (VS Code/Claude)│    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Configuration   │
                       │  & Credentials   │
                       └──────────────────┘
```

### Core Components

1. **Configuration Manager**: Handles Aha! domain and API key configuration with support for multiple configuration sources
2. **API Client**: Manages HTTP requests to Aha! REST API with automatic error handling and rate limiting
3. **Tool Handlers**: Individual functions for each MCP tool with comprehensive parameter validation
4. **Error Handler**: Centralized error handling with user-friendly messages and recovery suggestions
5. **Data Formatter**: Formats Aha! API responses for optimal LLM consumption and human readability

## Installation

### Prerequisites

- Python 3.8 or higher
- Active Aha! account with API access
- Valid Aha! API key
- VS Code with GitHub Copilot (for MCP integration)

### Quick Installation

```bash
# Clone or download the server files
git clone https://github.com/your-username/aha-mcp-server.git
cd aha-mcp-server

# Install dependencies
pip install -r requirements.txt

# Configure your Aha! credentials (see Configuration section)
cp aha_config.json.example aha_config.json
# Edit aha_config.json with your credentials
```

### Development Installation

```bash
# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest tests/
```

## Configuration

The server supports multiple configuration methods for maximum flexibility:

### Method 1: Environment Variables (Recommended)

```bash
export AHA_DOMAIN="yourcompany.aha.io"
export AHA_API_KEY="your_api_key_here"
export AHA_DEFAULT_PRODUCT="optional_default_product_id"
export AHA_RATE_LIMIT_DELAY="0.2"
export AHA_TIMEOUT="30"
```

### Method 2: Configuration File

Create an `aha_config.json` file in the server directory:

```json
{
  "aha_domain": "yourcompany.aha.io",
  "api_key": "your_api_key_here",
  "default_product": "optional_default_product_id",
  "rate_limit_delay": 0.2,
  "timeout": 30
}
```

### Obtaining Your API Key

1. Log into your Aha! account
2. Navigate to Settings → Personal → Developer
3. Click "Generate API key"
4. Copy the generated key and use it in your configuration

## Usage

### Running the Server

```bash
# Run the MCP server
python aha_mcp_server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Connecting to Claude Desktop

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "aha": {
      "command": "python",
      "args": ["/path/to/aha_mcp_server.py"],
      "env": {
        "AHA_DOMAIN": "yourcompany.aha.io",
        "AHA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ Available MCP Tools

The Aha! MCP Server provides the following tools for AI agents and users:

### Feature Management Tools
- `mcp_aha_get_feature` - Get detailed feature information
- `mcp_aha_search_features` - Search features with advanced filters
- `mcp_aha_create_feature` - Create new features
- `mcp_aha_update_feature` - Update existing features
- `mcp_aha_delete_feature` - Delete features (with confirmation)
- `mcp_aha_update_feature_status` - Update feature workflow status
- `mcp_aha_update_feature_score` - Update feature scoring
- `mcp_aha_add_feature_tags` - Add or replace feature tags

### Product & Release Management Tools
- `mcp_aha_list_products` - List all available products
- `mcp_aha_list_features_by_release` - Get features in a specific release