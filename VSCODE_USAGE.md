# Aha! MCP Server - VS Code Usage Guide

This guide assumes the Aha! MCP server is already installed and configured in your VS Code environment.

## 🚀 Quick Start

The Aha! MCP server is integrated with VS Code and provides direct access to Aha! features through AI chat interfaces like GitHub Copilot Chat.

### Available MCP Tools

You can use these tools directly in VS Code by calling them with the `@` prefix:

#### Feature Management
- `@mcp_aha_get_feature` - Get detailed feature information
- `@mcp_aha_search_features` - Search features with filters
- `@mcp_aha_create_feature` - Create new features
- `@mcp_aha_update_feature` - Update existing features
- `@mcp_aha_update_feature_status` - Change feature status
- `@mcp_aha_add_feature_tags` - Add tags to features

#### Product & Release Management
- `@mcp_aha_list_products` - List all products
- `@mcp_aha_list_features_by_release` - Get features in a release
- `@mcp_aha_list_features_by_epic` - Get features in an epic

#### Ideas & Feedback
- `@mcp_aha_get_related_ideas` - Search customer ideas

## 📋 Common Use Cases

### 1. Find Feature Information
```
@mcp_aha_get_feature ABC-10991
```

### 2. Search Features by Criteria
```
@mcp_aha_search_features query="API security" status="Planning" limit=10
```

### 3. Create a New Feature
```
@mcp_aha_create_feature name="New Authentication Feature" description="Enhanced security controls" release_id="RELEASE_ID"
```

### 4. Update Feature Status
```
@mcp_aha_update_feature_status DABCNAC-3080 "In Development"
```

### 5. Find Features by Assignee
```
@mcp_aha_search_features assignee="John Doe"
```

### 6. List Products
```
@mcp_aha_list_products limit=10
```

### 7. Get Features in a Release
```
@mcp_aha_list_features_by_release ABC-3.2.1
```

### 8. Search Customer Ideas
```
@mcp_aha_get_related_ideas query="mobile app"
```

## 💬 Natural Language Usage

You can also interact with Aha! using natural language in GitHub Copilot Chat:

- "Show me all features assigned to John Doe"
- "Create a new feature for API rate limiting in the security release"
- "What's the status of feature ABC-10991?"
- "Find all features related to authentication"
- "Update the status of ABC-3080 to In Development"

## 🔍 Feature Search Filters

When using `@mcp_aha_search_features`, you can filter by:

- **query**: Text search in name/description
- **product_id**: Specific product
- **release_id**: Specific release
- **epic_id**: Specific epic
- **status**: Workflow status (e.g., "Planning", "In Development", "Shipped")
- **assignee**: Person assigned to the feature
- **tags**: Feature tags (comma-separated)
- **limit**: Maximum number of results (default: 20)

## 🎯 Pro Tips

1. **Feature Creation**: Always specify a `release_id` when creating features
2. **Search Optimization**: Use specific queries for better results
3. **Status Updates**: Use exact status names from your Aha! workflow
4. **Batch Operations**: Use search first, then update multiple features
5. **Error Handling**: If a tool fails, check the error message for guidance

## ⚡ Quick Reference Commands

```bash
# Get feature details
@mcp_aha_get_feature FEATURE_ID

# Search features
@mcp_aha_search_features query="search term" status="status"

# Create feature (requires release_id)
@mcp_aha_create_feature name="Feature Name" description="Description" release_id="RELEASE_ID"

# Update status
@mcp_aha_update_feature_status FEATURE_ID "New Status"

# List products
@mcp_aha_list_products

# Get release features
@mcp_aha_list_features_by_release RELEASE_ID
```

## 🔧 Troubleshooting

### MCP Tools Not Working?
1. Restart VS Code
2. Check that the MCP server is running
3. Verify your `aha_config.json` has valid credentials

### Getting 403 Errors?
1. Check your API key in `aha_config.json`
2. Verify permissions in your Aha! workspace
3. Test connectivity with: `@mcp_aha_list_products`

### Feature Creation Failing?
1. Ensure you're providing a valid `release_id`
2. Check that all required fields are included
3. Verify you have create permissions in Aha!

### Can't Find Features?
1. Try broader search terms
2. Check if features exist in the expected product
3. Use `@mcp_aha_list_products` to see available products

## 📚 Additional Resources

- For installation and setup: See main `README.md`
- For agent setup in new environments: See `README_AGENT_SETUP.md`
- For API details: See `API_REFERENCE.md`

---

*This MCP server enables seamless integration between VS Code and Aha!, making product management workflows more efficient through AI-powered interactions.*
