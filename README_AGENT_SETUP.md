# Aha! MCP Server - Agent Setup Guide

🤖 **For AI Agents & VS Code Environments** - Quick setup guide for using Aha! MCP tools directly in VS Code.

## Prerequisites ✅

- ✅ Aha! MCP Server installed and configured
- ✅ `aha_config.json` with valid Aha! credentials
- ✅ Python virtual environment activated
- ✅ VS Code with MCP integration enabled

## Quick Validation

Test that MCP tools are available:

```bash
# Verify MCP server responds
@mcp_aha_list_products limit=3

# Test feature search
@mcp_aha_search_features query="API" limit=5

# Get specific feature
@mcp_aha_get_feature DNAC-10991
```

## 🛠️ Available MCP Tools

### Feature Management
- `@mcp_aha_get_feature` - Get detailed feature information
- `@mcp_aha_search_features` - Search features with filters
- `@mcp_aha_create_feature` - Create new features  
- `@mcp_aha_update_feature` - Update existing features
- `@mcp_aha_update_feature_status` - Change feature status
- `@mcp_aha_add_feature_tags` - Add/replace feature tags

### Product & Release Management
- `@mcp_aha_list_products` - List all products
- `@mcp_aha_list_features_by_release` - Features in a release
- `@mcp_aha_list_features_by_epic` - Features in an epic

### User Management
- `@mcp_aha_list_users` - List users in the workspace
- `@mcp_aha_get_current_user` - Get current authenticated user info

### Ideas & Feedback
- `@mcp_aha_get_related_ideas` - Search customer ideas

## 🎯 Common AI Agent Tasks

### Feature Discovery
```
@mcp_aha_search_features query="security API" status="Planning"
@mcp_aha_search_features assigned_to_user="john.doe@company.com" limit=10
@mcp_aha_list_features_by_release RELEASE-2024-Q1
```

### Feature Management
```
@mcp_aha_create_feature name="Enhanced Security" description="New API security controls"
@mcp_aha_update_feature_status DNAC-1234 "In Development"
@mcp_aha_add_feature_tags DNAC-1234 "security,api,priority"
```

### Reporting & Analysis
```
@mcp_aha_search_features tags="bug,critical"
@mcp_aha_get_related_ideas query="mobile app"
@mcp_aha_list_products limit=5
```

## 🔧 Troubleshooting

### MCP Tools Not Available
1. Check VS Code settings contain MCP server configuration
2. Restart VS Code after configuration changes
3. Verify `aha_config.json` exists with valid credentials
4. Restart MCP servers if new tools were added:
   ```bash
   # Kill existing MCP server processes
   pkill -f aha_mcp_server.py
   
   # Restart VS Code to reload MCP configuration
   # New tools will be available after restart
   ```

### API Authentication Errors (403)
1. Validate API key in `aha_config.json`
2. Check user permissions in Aha! workspace
3. Test connectivity: `curl -H "Authorization: Bearer YOUR_KEY" https://DOMAIN.aha.io/api/v1/products`

### Feature Creation Fails
- Features must be created under a release using `release_id`
- Use `@mcp_aha_list_products` to find available releases first
- Ensure all required fields are provided

### Quick Health Check
```bash
# From the MCP server directory
source aha-mcp-env/bin/activate
python -c "
from aha_mcp_server import load_config, AhaAPIClient
import asyncio

async def test():
    config = load_config()
    async with AhaAPIClient(config) as client:
        data = await client.request('GET', '/products', params={'per_page': 1})
        print('✅ MCP Server healthy - API connectivity successful')

asyncio.run(test())
"
```

## 📝 Example Workflows

### Create and Track Feature
```
# 1. Find available releases
@mcp_aha_list_products limit=3

# 2. Create feature under a release
@mcp_aha_create_feature name="New Dashboard Widget" description="User-friendly analytics widget" release_id="REL-123"

# 3. Update status as work progresses  
@mcp_aha_update_feature_status DNAC-5678 "In Development"

# 4. Add relevant tags
@mcp_aha_add_feature_tags DNAC-5678 "dashboard,analytics,ui"
```

### Research Customer Requests
```
# 1. Search for related ideas
@mcp_aha_get_related_ideas query="dashboard analytics"

# 2. Find existing features
@mcp_aha_search_features query="dashboard" status="Planning"

# 3. Get detailed feature info
@mcp_aha_get_feature DNAC-1234
```

---

*This MCP server provides direct integration between AI agents and Aha! product management workflows. All tools return structured data optimized for AI consumption and decision-making.*
