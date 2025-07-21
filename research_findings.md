# Aha! MCP Server Research Findings

## Aha! API Overview

### Authentication
- **API Key**: Generated through Aha! user interface (Settings > Personal > Developer > Generate API key)
- **OAuth2**: Preferred method for external applications
- **Base URL**: `https://<yourcompany>.aha.io/api/v1/`
- **Authorization Header**: `Authorization: Bearer <api_key_or_token>`

### Features API Endpoints

#### Core Operations
- **List Features**: `GET /features`
- **Get Specific Feature**: `GET /features/{id}`
- **Create Feature**: `POST /features`
- **Update Feature**: `PUT /features/{id}`
- **Delete Feature**: `DELETE /features/{id}`

#### Search and Filter Operations
- **List Features in Product**: `GET /products/{product_id}/features`
- **List Features in Release**: `GET /releases/{release_id}/features`
- **List Features in Epic**: `GET /epics/{epic_id}/features`
- **List Features by Goal**: `GET /goals/{goal_id}/features`
- **List Features by Initiative**: `GET /initiatives/{initiative_id}/features`

#### Advanced Operations
- **Update Feature Custom Fields**: `PUT /features/{id}/custom_fields`
- **Update Feature Tags**: `PUT /features/{id}/tags`
- **Update Feature Score**: `PUT /features/{id}/score`
- **Update Feature Progress**: `PUT /features/{id}/progress`
- **Update Feature Release**: `PUT /features/{id}/release`
- **Update Feature Epic**: `PUT /features/{id}/epic`
- **Update Feature Goals**: `PUT /features/{id}/goals`
- **Update Feature Watchers**: `PUT /features/{id}/watchers`
- **Convert Feature to Epic**: `POST /features/{id}/convert_to_epic`

### API Features
- **Pagination**: Supports `page` and `per_page` parameters (max 200 per page)
- **Field Selection**: Use `fields` parameter to customize response fields
- **Rate Limiting**: 300 requests/minute, 20 requests/second
- **Custom Fields**: Supported for all feature operations
- **Email Suppression**: Use `disable_mailers=true` to prevent notifications

## MCP Server Architecture

### Core Concepts
1. **Tools**: Functions that can be called by LLMs (with user approval)
2. **Resources**: File-like data that can be read by clients
3. **Prompts**: Pre-written templates for specific tasks

### Python Implementation Structure
- **FastMCP**: Simplified framework for building MCP servers
- **Tool Decorators**: `@mcp.tool()` decorator for defining tools
- **Transport**: Supports stdio, HTTP, and WebSocket transports
- **Error Handling**: Built-in error handling and validation

### Key Components
1. **Server Initialization**: `FastMCP("server_name")`
2. **Tool Definition**: Functions decorated with `@mcp.tool()`
3. **Type Hints**: Required for parameter validation
4. **Async Support**: Full async/await support
5. **Server Execution**: `mcp.run(transport='stdio')`

## Implementation Plan

### Required Tools for Aha! MCP Server
1. **search_features**: Search features by various criteria
2. **get_feature**: Get detailed information about a specific feature
3. **create_feature**: Create a new feature
4. **update_feature**: Update an existing feature
5. **delete_feature**: Delete a feature
6. **list_features_by_release**: List features in a specific release
7. **list_features_by_epic**: List features in a specific epic
8. **update_feature_status**: Update feature workflow status
9. **add_feature_tags**: Add tags to a feature
10. **update_feature_score**: Update feature scoring

### Configuration Requirements
- Aha! domain (company subdomain)
- API key or OAuth2 credentials
- Default product/workspace context

