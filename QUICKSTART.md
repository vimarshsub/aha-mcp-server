# Quick Start Guide - Aha! MCP Server

Get up and running with the Aha! MCP Server in under 5 minutes.

## Prerequisites

- Python 3.8+
- Aha! account with API access
- Claude Desktop or compatible MCP client

## Step 1: Get Your Aha! API Key

1. Log into your Aha! account
2. Go to **Settings** → **Personal** → **Developer**
3. Click **"Generate API key"**
4. Copy the generated key (you'll need this in Step 3)

## Step 2: Download and Install

```bash
# Download the server files
curl -O https://raw.githubusercontent.com/your-repo/aha-mcp-server/main/aha_mcp_server.py
curl -O https://raw.githubusercontent.com/your-repo/aha-mcp-server/main/requirements.txt

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure Credentials

**Option A: Environment Variables (Recommended)**
```bash
export AHA_DOMAIN="yourcompany.aha.io"
export AHA_API_KEY="your_api_key_from_step_1"
```

**Option B: Configuration File**
```bash
# Create config file
cat > aha_config.json << EOF
{
  "aha_domain": "yourcompany.aha.io",
  "api_key": "your_api_key_from_step_1"
}
EOF
```

## Step 4: Test the Server

```bash
# Test the server
python aha_mcp_server.py
```

If configured correctly, the server will start without errors.

## Step 5: Connect to Claude Desktop

Add this to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "aha": {
      "command": "python",
      "args": ["/full/path/to/aha_mcp_server.py"],
      "env": {
        "AHA_DOMAIN": "yourcompany.aha.io",
        "AHA_API_KEY": "your_api_key_from_step_1"
      }
    }
  }
}
```

## Step 6: Try It Out!

In Claude Desktop, try these commands:

- "Search for features with 'login' in the name"
- "Create a new feature called 'Password Reset'"
- "List all features in release REL-2024-Q1"
- "Update feature APP-123 status to 'In Progress'"

## Common Issues

**"Authentication failed"**
- Double-check your API key and domain
- Ensure your API key hasn't been revoked

**"Module not found"**
- Run `pip install -r requirements.txt`
- Check your Python version (3.8+ required)

**"Server won't start"**
- Verify your configuration file syntax
- Check file permissions

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore all available tools and parameters
- Set up advanced configuration options
- Join the community for support and best practices

## Need Help?

- Check the [Troubleshooting Guide](README.md#troubleshooting-guide)
- Review [Common Use Cases](README.md#common-use-cases)
- Report issues on GitHub

