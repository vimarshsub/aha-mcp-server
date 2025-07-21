# API Reference - Aha! MCP Server

Complete reference for all tools and parameters available in the Aha! MCP Server.

## Tool Overview

| Tool | Purpose | Required Parameters | Optional Parameters |
|------|---------|-------------------|-------------------|
| `search_features` | Search features | None | query, product_id, release_id, epic_id, status, assignee, tags, limit |
| `get_feature` | Get feature details | feature_id | None |
| `create_feature` | Create new feature | name | description, release_id, epic_id, assignee, tags, custom_fields |
| `update_feature` | Update existing feature | feature_id | name, description, status, assignee, release_id, epic_id, custom_fields |
| `delete_feature` | Delete feature | feature_id, confirm | None |
| `list_features_by_release` | List features in release | release_id | include_completed, limit |
| `list_features_by_epic` | List features in epic | epic_id | limit |
| `update_feature_status` | Update feature status | feature_id, status | None |
| `add_feature_tags` | Add/replace feature tags | feature_id, tags | replace |
| `update_feature_score` | Update feature score | feature_id, score | None |

## Detailed Tool Reference

### search_features

Search for features across the Aha! workspace with flexible filtering.

**Syntax:**
```
search_features(query?, product_id?, release_id?, epic_id?, status?, assignee?, tags?, limit?)
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | No | None | Text search query for feature names and descriptions |
| `product_id` | string | No | None | Filter by specific product ID |
| `release_id` | string | No | None | Filter by specific release ID |
| `epic_id` | string | No | None | Filter by specific epic ID |
| `status` | string | No | None | Filter by workflow status |
| `assignee` | string | No | None | Filter by assigned user |
| `tags` | string | No | None | Filter by tags (comma-separated) |
| `limit` | integer | No | 20 | Maximum results (1-200) |

**Examples:**
```
# Basic text search
search_features(query="authentication")

# Search with multiple filters
search_features(query="login", status="In Progress", assignee="john.doe")

# Search by release
search_features(release_id="REL-2024-Q1", limit=50)

# Search by tags
search_features(tags="security,authentication")
```

**Response Format:**
```
Found X feature(s):

Feature: APP-123 - Two-Factor Authentication
Status: In Progress
Assignee: John Doe
Release: 2024 Q1 Release
Tags: security, authentication

Feature: APP-124 - Password Reset
Status: Ready for Review
Assignee: Jane Smith
Release: 2024 Q1 Release
Tags: security, user-management
```

### get_feature

Retrieve comprehensive details about a specific feature.

**Syntax:**
```
get_feature(feature_id)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `feature_id` | string | Yes | Feature ID or reference number (e.g., "APP-123") |

**Examples:**
```
# Get feature by reference number
get_feature(feature_id="APP-123")

# Get feature by ID
get_feature(feature_id="5938362174479841842")
```

**Response Format:**
```
Feature: APP-123 - Two-Factor Authentication
Description: Implement 2FA for enhanced account security
Status: In Progress
Assignee: John Doe
Release: 2024 Q1 Release
Epic: User Security Epic
Progress: 65%
Score: 85
Tags: security, authentication, high-priority
Created: 2024-01-15T10:30:00Z
Updated: 2024-01-20T14:45:00Z

Custom Fields:
- Effort Estimate: 8 story points
- Business Value: High
- Technical Risk: Medium
```

### create_feature

Create a new feature with comprehensive metadata.

**Syntax:**
```
create_feature(name, description?, release_id?, epic_id?, assignee?, tags?, custom_fields?)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Feature name |
| `description` | string | No | Detailed feature description |
| `release_id` | string | No | Release to assign feature to |
| `epic_id` | string | No | Epic to assign feature to |
| `assignee` | string | No | User to assign feature to |
| `tags` | string | No | Tags to add (comma-separated) |
| `custom_fields` | string | No | Custom field values as JSON string |

**Examples:**
```
# Basic feature creation
create_feature(name="Single Sign-On Integration")

# Feature with full metadata
create_feature(
  name="OAuth 2.0 Implementation",
  description="Implement OAuth 2.0 authentication flow",
  release_id="REL-2024-Q2",
  assignee="john.doe",
  tags="authentication,oauth,security"
)

# Feature with custom fields
create_feature(
  name="API Rate Limiting",
  custom_fields='{"effort_estimate": 5, "business_value": "High"}'
)
```

**Response Format:**
```
Successfully created feature: APP-125 - OAuth 2.0 Implementation

Feature: APP-125 - OAuth 2.0 Implementation
Description: Implement OAuth 2.0 authentication flow
Status: New
Assignee: John Doe
Release: 2024 Q2 Release
Epic: No Epic
Progress: 0%
Score: No Score
Tags: authentication, oauth, security
Created: 2024-01-21T09:15:00Z
Updated: 2024-01-21T09:15:00Z
```

### update_feature

Update an existing feature with new information.

**Syntax:**
```
update_feature(feature_id, name?, description?, status?, assignee?, release_id?, epic_id?, custom_fields?)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `feature_id` | string | Yes | Feature ID or reference number |
| `name` | string | No | New feature name |
| `description` | string | No | New feature description |
| `status` | string | No | New workflow status |
| `assignee` | string | No | New assignee |
| `release_id` | string | No | New release assignment |
| `epic_id` | string | No | New epic assignment |
| `custom_fields` | string | No | Custom field updates as JSON |

**Examples:**
```
# Update status and assignee
update_feature(
  feature_id="APP-123",
  status="In Progress",
  assignee="jane.smith"
)

# Update description and custom fields
update_feature(
  feature_id="APP-124",
  description="Updated requirements based on user feedback",
  custom_fields='{"effort_estimate": 13, "priority": "High"}'
)
```

### delete_feature

Safely delete a feature with confirmation requirement.

**Syntax:**
```
delete_feature(feature_id, confirm)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `feature_id` | string | Yes | Feature ID or reference number |
| `confirm` | boolean | Yes | Must be `true` to confirm deletion |

**Examples:**
```
# Delete with confirmation
delete_feature(feature_id="APP-999", confirm=true)

# Attempt without confirmation (will fail)
delete_feature(feature_id="APP-999", confirm=false)
```

### list_features_by_release

List all features in a specific release.

**Syntax:**
```
list_features_by_release(release_id, include_completed?, limit?)
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `release_id` | string | Yes | None | Release ID or reference number |
| `include_completed` | boolean | No | true | Include completed features |
| `limit` | integer | No | 50 | Maximum results (1-200) |

**Examples:**
```
# List all features in release
list_features_by_release(release_id="REL-2024-Q1")

# List only incomplete features
list_features_by_release(
  release_id="REL-2024-Q1",
  include_completed=false
)
```

### list_features_by_epic

List all features in a specific epic.

**Syntax:**
```
list_features_by_epic(epic_id, limit?)
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `epic_id` | string | Yes | None | Epic ID or reference number |
| `limit` | integer | No | 50 | Maximum results (1-200) |

**Examples:**
```
# List all features in epic
list_features_by_epic(epic_id="EPIC-USER-AUTH")

# Limit results
list_features_by_epic(epic_id="EPIC-API-V2", limit=25)
```

### update_feature_status

Update the workflow status of a feature.

**Syntax:**
```
update_feature_status(feature_id, status)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `feature_id` | string | Yes | Feature ID or reference number |
| `status` | string | Yes | New workflow status |

**Common Status Values:**
- "New"
- "In Progress"
- "Ready for Review"
- "In Review"
- "Ready for Testing"
- "In Testing"
- "Done"
- "Shipped"

**Examples:**
```
# Move to in progress
update_feature_status(feature_id="APP-123", status="In Progress")

# Mark as complete
update_feature_status(feature_id="APP-124", status="Done")
```

### add_feature_tags

Add or replace tags on a feature.

**Syntax:**
```
add_feature_tags(feature_id, tags, replace?)
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `feature_id` | string | Yes | None | Feature ID or reference number |
| `tags` | string | Yes | None | Tags to add (comma-separated) |
| `replace` | boolean | No | false | Replace existing tags instead of adding |

**Examples:**
```
# Add tags to existing tags
add_feature_tags(
  feature_id="APP-123",
  tags="security,high-priority"
)

# Replace all tags
add_feature_tags(
  feature_id="APP-124",
  tags="authentication,oauth",
  replace=true
)
```

### update_feature_score

Update the priority score of a feature.

**Syntax:**
```
update_feature_score(feature_id, score)
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `feature_id` | string | Yes | Feature ID or reference number |
| `score` | number | Yes | New score value (typically 0-100) |

**Examples:**
```
# Set high priority score
update_feature_score(feature_id="APP-123", score=95)

# Set medium priority score
update_feature_score(feature_id="APP-124", score=65)
```

## Error Responses

All tools return user-friendly error messages when issues occur:

### Authentication Errors
```
Error: Authentication failed. Please check your API key.
```

### Permission Errors
```
Error: Permission denied. You don't have access to this resource.
```

### Not Found Errors
```
Error: Resource not found. Please check the ID or reference number.
```

### Validation Errors
```
Error: custom_fields must be valid JSON
Error: Deletion requires confirmation. Set confirm=True to proceed.
Error: No update fields provided
```

### Rate Limit Errors
```
Error: Rate limit exceeded. Please wait a moment and try again.
```

## Data Types and Formats

### Feature Reference Numbers
- Format: `[PRODUCT_PREFIX]-[NUMBER]`
- Examples: `APP-123`, `WEB-456`, `API-789`

### Date Formats
- ISO 8601 format: `2024-01-21T09:15:00Z`
- All dates are in UTC

### Custom Fields JSON Format
```json
{
  "field_name": "field_value",
  "effort_estimate": 8,
  "business_value": "High",
  "technical_risk": "Medium"
}
```

### Tag Format
- Comma-separated strings: `"tag1,tag2,tag3"`
- No spaces around commas
- Case-sensitive

## Rate Limiting

The server implements automatic rate limiting to respect Aha!'s API limits:

- **Default delay**: 0.2 seconds between requests
- **Maximum rate**: 300 requests per minute
- **Burst limit**: 20 requests per second
- **Automatic retry**: Built-in retry logic with exponential backoff

## Best Practices

### Efficient Searching
- Use specific filters to reduce result sets
- Combine multiple filters for precise results
- Use appropriate limit values to avoid large responses

### Batch Operations
- Group related updates when possible
- Use list operations to get multiple features efficiently
- Consider using search instead of individual get operations

### Error Handling
- Always check for error responses
- Implement retry logic for rate limit errors
- Validate parameters before making requests

### Performance
- Cache frequently accessed data
- Use field selection to reduce response size
- Implement connection pooling for multiple requests

