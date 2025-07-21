# Aha! MCP Server

A comprehensive Model Context Protocol (MCP) server that provides seamless integration between Large Language Models and the Aha! product management platform. This server enables AI assistants to search, create, and edit features in Aha! through natural language interactions.

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

## Architecture

The server follows a modular architecture designed for maintainability and extensibility:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│  Aha! MCP Server │◄──►│   Aha! API      │
│  (Claude, etc.) │    │                  │    │                 │
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

## Available Tools

The server provides 10 comprehensive tools for feature management:



### 1. search_features

Search for features across your Aha! workspace with flexible filtering options.

**Parameters:**
- `query` (optional): Text search query to match feature names and descriptions
- `product_id` (optional): Filter results to a specific product
- `release_id` (optional): Filter results to a specific release
- `epic_id` (optional): Filter results to a specific epic
- `status` (optional): Filter by workflow status
- `assignee` (optional): Filter by assigned user
- `tags` (optional): Filter by tags (comma-separated list)
- `limit` (optional): Maximum number of results to return (default: 20, max: 200)

**Example Usage:**
```
Search for features with "login" in the name that are assigned to John and have "security" tag
```

### 2. get_feature

Retrieve detailed information about a specific feature including all metadata, custom fields, and relationships.

**Parameters:**
- `feature_id` (required): Feature ID or reference number (e.g., "APP-123")

**Example Usage:**
```
Get detailed information about feature APP-123
```

### 3. create_feature

Create a new feature in Aha! with comprehensive metadata and relationships.

**Parameters:**
- `name` (required): Feature name
- `description` (optional): Detailed feature description
- `release_id` (optional): Release to assign the feature to
- `epic_id` (optional): Epic to assign the feature to
- `assignee` (optional): User to assign the feature to
- `tags` (optional): Tags to add (comma-separated)
- `custom_fields` (optional): Custom field values as JSON string

**Example Usage:**
```
Create a new feature called "Two-Factor Authentication" with description "Implement 2FA for enhanced security" and assign it to release REL-2024-Q1
```

### 4. update_feature

Update an existing feature with new information, status changes, or relationship modifications.

**Parameters:**
- `feature_id` (required): Feature ID or reference number
- `name` (optional): New feature name
- `description` (optional): New feature description
- `status` (optional): New workflow status
- `assignee` (optional): New assignee
- `release_id` (optional): New release assignment
- `epic_id` (optional): New epic assignment
- `custom_fields` (optional): Custom field updates as JSON string

**Example Usage:**
```
Update feature APP-123 to change status to "In Progress" and assign to Sarah
```

### 5. delete_feature

Safely delete a feature from Aha! with confirmation requirement to prevent accidental deletions.

**Parameters:**
- `feature_id` (required): Feature ID or reference number
- `confirm` (required): Must be set to `true` to confirm deletion

**Example Usage:**
```
Delete feature APP-456 (confirm=true)
```

### 6. list_features_by_release

List all features associated with a specific release for release planning and tracking.

**Parameters:**
- `release_id` (required): Release ID or reference number
- `include_completed` (optional): Include completed features (default: true)
- `limit` (optional): Maximum number of results (default: 50)

**Example Usage:**
```
List all features in release REL-2024-Q2
```

### 7. list_features_by_epic

List all features associated with a specific epic for epic management and progress tracking.

**Parameters:**
- `epic_id` (required): Epic ID or reference number
- `limit` (optional): Maximum number of results (default: 50)

**Example Usage:**
```
List all features in epic EPIC-USER-MANAGEMENT
```

### 8. update_feature_status

Update the workflow status of a feature for progress tracking and workflow management.

**Parameters:**
- `feature_id` (required): Feature ID or reference number
- `status` (required): New workflow status

**Example Usage:**
```
Update feature APP-789 status to "Ready for Review"
```

### 9. add_feature_tags

Add or replace tags on a feature for improved organization and filtering.

**Parameters:**
- `feature_id` (required): Feature ID or reference number
- `tags` (required): Tags to add (comma-separated)
- `replace` (optional): Replace existing tags instead of adding (default: false)

**Example Usage:**
```
Add tags "security, authentication" to feature APP-123
```

### 10. update_feature_score

Update the priority score of a feature for prioritization and planning.

**Parameters:**
- `feature_id` (required): Feature ID or reference number
- `score` (required): New score value (numeric)

**Example Usage:**
```
Update feature APP-456 score to 85
```

## Common Use Cases

### Product Planning Workflow

The Aha! MCP Server excels in supporting comprehensive product planning workflows. Product managers can leverage the natural language interface to quickly assess feature landscapes, make strategic decisions, and communicate plans effectively.

When planning a new product release, you can start by searching for features across different criteria to understand the current state of development. For example, searching for features by status helps identify bottlenecks and resource allocation needs. The search functionality supports complex queries that combine multiple filters, enabling sophisticated analysis of feature portfolios.

Creating new features becomes streamlined through natural language descriptions that automatically populate appropriate fields and relationships. The server intelligently handles feature creation with proper validation and error handling, ensuring data integrity while maintaining workflow efficiency.

### Release Management

Release management becomes significantly more efficient with the MCP server's batch operations and relationship management capabilities. Release managers can quickly list all features in a release, assess completion status, and make necessary adjustments to scope and timeline.

The ability to update feature assignments and statuses in bulk through natural language commands dramatically reduces the administrative overhead typically associated with release management. Progress tracking becomes real-time and accurate, with immediate visibility into feature completion rates and potential blockers.

### Epic and Feature Hierarchy Management

Managing complex feature hierarchies across epics becomes intuitive with the server's relationship management tools. Product teams can easily visualize and modify the relationships between epics and features, ensuring proper organization and dependency management.

The server supports sophisticated queries that traverse feature hierarchies, enabling analysis of epic completion rates, feature distribution, and resource allocation across major initiatives. This capability is particularly valuable for large-scale product development efforts with multiple interconnected components.

## Error Handling and Troubleshooting

The Aha! MCP Server implements comprehensive error handling designed to provide clear, actionable feedback for common issues while maintaining system stability and security.

### Authentication Errors

Authentication failures typically occur due to invalid or expired API keys. The server provides specific guidance for resolving authentication issues:

- **Invalid API Key**: Verify that your API key is correctly configured and hasn't been revoked in Aha!
- **Expired Token**: Generate a new API key through the Aha! interface
- **Domain Mismatch**: Ensure your Aha! domain is correctly specified in the configuration

### Permission Errors

Permission-related errors indicate that your API key doesn't have sufficient privileges for the requested operation. Common scenarios include:

- **Read-Only Access**: Your API key may only have read permissions
- **Product-Specific Restrictions**: Some operations may be restricted to specific products or workspaces
- **User Role Limitations**: The user associated with the API key may lack necessary permissions

### Rate Limiting

The server implements intelligent rate limiting to respect Aha!'s API constraints while maintaining optimal performance. When rate limits are encountered:

- **Automatic Retry**: The server automatically implements appropriate delays
- **Backoff Strategy**: Progressive delays prevent overwhelming the API
- **User Notification**: Clear messages indicate when rate limiting is active

### Data Validation Errors

Input validation errors provide specific guidance for correcting parameter issues:

- **Required Parameters**: Clear indication of missing required fields
- **Format Validation**: Specific guidance for parameter format requirements
- **Relationship Validation**: Verification of feature relationships and dependencies

## Performance Optimization

The Aha! MCP Server is designed for optimal performance in production environments with several key optimizations:

### Connection Management

The server implements efficient HTTP connection pooling to minimize connection overhead and improve response times. Persistent connections are maintained across multiple requests, reducing latency and improving overall throughput.

### Response Caching

Strategic caching of frequently accessed data reduces API calls and improves response times. The caching strategy balances data freshness with performance, ensuring users receive current information while minimizing unnecessary API requests.

### Batch Operations

Where possible, the server groups related operations to reduce the total number of API calls required. This approach is particularly effective for bulk updates and large-scale data retrieval operations.

### Field Selection Optimization

The server automatically optimizes API requests by requesting only necessary fields, reducing response payload size and improving transfer speeds. This optimization is particularly beneficial for large feature sets and detailed queries.

## Security Considerations

Security is a fundamental consideration in the design and implementation of the Aha! MCP Server. The server implements multiple layers of security controls to protect sensitive data and ensure secure operation.

### Credential Management

API keys are handled with strict security protocols:

- **Environment Variable Support**: Credentials can be stored in environment variables to avoid file-based storage
- **Configuration File Security**: When using configuration files, appropriate file permissions should be set
- **No Logging**: API keys are never logged or exposed in error messages
- **Secure Transmission**: All API communications use HTTPS encryption

### Input Validation

All user inputs undergo comprehensive validation to prevent injection attacks and ensure data integrity:

- **Parameter Validation**: All parameters are validated against expected types and formats
- **SQL Injection Prevention**: Input sanitization prevents malicious query construction
- **Cross-Site Scripting Protection**: Output encoding prevents XSS vulnerabilities
- **Data Type Enforcement**: Strict type checking prevents type confusion attacks

### Error Message Sanitization

Error messages are carefully crafted to provide useful information without exposing sensitive system details:

- **Generic Error Messages**: Internal system details are not exposed to users
- **Actionable Guidance**: Error messages provide specific steps for resolution
- **No Credential Exposure**: API keys and internal tokens are never included in error responses
- **Audit Trail**: Security-relevant events are logged for monitoring and analysis

## Advanced Configuration

The Aha! MCP Server supports advanced configuration options for enterprise deployments and specialized use cases.

### Custom Rate Limiting

Organizations with specific API rate limit requirements can customize the server's rate limiting behavior:

```json
{
  "rate_limit_delay": 0.1,
  "max_concurrent_requests": 5,
  "retry_attempts": 3,
  "backoff_multiplier": 2.0
}
```

### Timeout Configuration

Network timeout settings can be adjusted based on network conditions and performance requirements:

```json
{
  "timeout": 60,
  "connect_timeout": 10,
  "read_timeout": 30
}
```

### Logging Configuration

Comprehensive logging options support monitoring and debugging in production environments:

```json
{
  "log_level": "INFO",
  "log_format": "json",
  "log_file": "/var/log/aha-mcp-server.log",
  "enable_audit_log": true
}
```

## Integration Examples

### Claude Desktop Integration

The most common integration scenario involves connecting the Aha! MCP Server to Claude Desktop for natural language feature management.

Configuration example for Claude Desktop:

```json
{
  "mcpServers": {
    "aha": {
      "command": "python",
      "args": ["/path/to/aha_mcp_server.py"],
      "env": {
        "AHA_DOMAIN": "yourcompany.aha.io",
        "AHA_API_KEY": "your_api_key_here",
        "AHA_DEFAULT_PRODUCT": "PROD-123"
      }
    }
  }
}
```

### Custom MCP Client Integration

For organizations building custom MCP clients, the server provides a standard MCP interface that can be integrated with any compliant client implementation.

Example client connection code:

```python
import asyncio
from mcp.client import ClientSession

async def connect_to_aha_server():
    session = ClientSession()
    await session.connect("stdio", command=["python", "aha_mcp_server.py"])
    
    # List available tools
    tools = await session.list_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    # Call a tool
    result = await session.call_tool("search_features", {"query": "login"})
    print(f"Search results: {result}")
```

### Webhook Integration

For real-time synchronization scenarios, the server can be extended to support webhook notifications from Aha!:

```python
# Example webhook handler extension
@mcp.tool()
async def handle_feature_update_webhook(webhook_data: str) -> str:
    """Handle incoming webhook notifications from Aha!"""
    # Process webhook data and update local cache
    # Notify connected clients of changes
    pass
```

## Troubleshooting Guide

### Common Issues and Solutions

**Issue: "Authentication failed" error**
- **Cause**: Invalid or expired API key
- **Solution**: Verify API key in Aha! settings and update configuration
- **Prevention**: Implement API key rotation schedule

**Issue: "Rate limit exceeded" error**
- **Cause**: Too many API requests in short time period
- **Solution**: Increase rate_limit_delay in configuration
- **Prevention**: Implement request batching for bulk operations

**Issue: "Feature not found" error**
- **Cause**: Invalid feature ID or insufficient permissions
- **Solution**: Verify feature ID and check user permissions
- **Prevention**: Implement feature ID validation before API calls

**Issue: Server startup fails**
- **Cause**: Missing dependencies or configuration
- **Solution**: Install requirements and verify configuration
- **Prevention**: Use virtual environments and configuration validation

### Debug Mode

Enable debug mode for detailed troubleshooting information:

```bash
export AHA_DEBUG=true
python aha_mcp_server.py
```

Debug mode provides:
- Detailed API request/response logging
- Performance timing information
- Configuration validation details
- Error stack traces

### Log Analysis

The server generates structured logs that can be analyzed for performance and error patterns:

```bash
# View recent errors
grep "ERROR" /var/log/aha-mcp-server.log | tail -20

# Analyze API response times
grep "api_response_time" /var/log/aha-mcp-server.log | awk '{print $5}' | sort -n
```

## Contributing

We welcome contributions to the Aha! MCP Server project. Please follow these guidelines for contributing:

### Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/aha-mcp-server.git
cd aha-mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Include comprehensive docstrings for all public functions
- Maintain test coverage above 90%

### Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate tests
4. Submit a pull request with detailed description

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For support and questions:

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Comprehensive documentation available in the docs/ directory
- **Community**: Join our community discussions for help and best practices

## Changelog

### Version 1.0.0
- Initial release with core feature management tools
- Support for search, create, update, and delete operations
- Comprehensive error handling and validation
- Production-ready performance optimizations
- Complete documentation and examples

---

*Built with ❤️ by the MCP community*

