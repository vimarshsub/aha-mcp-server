#!/usr/bin/env python3
"""
Aha! MCP Server

A Model Context Protocol server that provides tools for interacting with Aha! product management platform.
Supports searching, creating, and editing features in Aha!.

Author: MCP Server Generator
Version: 1.0.0
"""

import os
import json
import asyncio
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("aha-server")

# Configuration
@dataclass
class AhaConfig:
    """Configuration for Aha! API connection"""
    domain: str
    api_key: str
    default_product: Optional[str] = None
    rate_limit_delay: float = 0.2
    timeout: int = 30
    
    @property
    def base_url(self) -> str:
        return f"https://{self.domain}/api/v1"

# Global configuration instance
config: Optional[AhaConfig] = None

def load_config() -> AhaConfig:
    """Load configuration from environment variables or config file"""
    global config
    
    if config is not None:
        return config
    
    # Try to load from environment variables first
    domain = os.getenv('AHA_DOMAIN')
    api_key = os.getenv('AHA_API_KEY')
    
    # Try to load from config file if env vars not available
    if not domain or not api_key:
        try:
            with open('aha_config.json', 'r') as f:
                config_data = json.load(f)
                domain = config_data.get('aha_domain')
                api_key = config_data.get('api_key')
        except FileNotFoundError:
            pass
    
    if not domain or not api_key:
        raise ValueError(
            "Aha! configuration not found. Please set AHA_DOMAIN and AHA_API_KEY environment variables "
            "or create an aha_config.json file with 'aha_domain' and 'api_key' fields."
        )
    
    config = AhaConfig(
        domain=domain,
        api_key=api_key,
        default_product=os.getenv('AHA_DEFAULT_PRODUCT'),
        rate_limit_delay=float(os.getenv('AHA_RATE_LIMIT_DELAY', '0.2')),
        timeout=int(os.getenv('AHA_TIMEOUT', '30'))
    )
    
    return config

class AhaAPIClient:
    """HTTP client for Aha! API interactions"""
    
    def __init__(self, config: AhaConfig):
        self.config = config
        self.session: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        self.session = httpx.AsyncClient(
            base_url=self.config.base_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "Aha-MCP-Server/1.0.0"
            },
            timeout=self.config.timeout
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an API request with error handling"""
        if not self.session:
            raise RuntimeError("API client not initialized. Use async context manager.")
        
        # Add rate limiting delay
        await asyncio.sleep(self.config.rate_limit_delay)
        
        try:
            response = await self.session.request(method, endpoint, **kwargs)
            response.raise_for_status()
            
            # Debug: Check what we're getting
            content_type = response.headers.get('content-type', '')
            if 'json' not in content_type:
                raise Exception(f"Expected JSON response, got content-type: {content_type}")
            
            json_data = response.json()
            if not isinstance(json_data, dict):
                raise Exception(f"Expected dict, got {type(json_data)}: {json_data}")
            
            return json_data
        except httpx.HTTPStatusError as e:
            await self._handle_http_error(e)
        except httpx.RequestError as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"API Error: {str(e)}")
    
    async def _handle_http_error(self, error: httpx.HTTPStatusError):
        """Handle HTTP errors with user-friendly messages"""
        status_code = error.response.status_code
        
        if status_code == 401:
            raise Exception("Authentication failed. Please check your API key.")
        elif status_code == 403:
            raise Exception("Permission denied. You don't have access to this resource.")
        elif status_code == 404:
            raise Exception("Resource not found. Please check the ID or reference number.")
        elif status_code == 429:
            raise Exception("Rate limit exceeded. Please wait a moment and try again.")
        elif status_code >= 500:
            raise Exception("Aha! server error. Please try again later.")
        else:
            try:
                error_data = error.response.json()
                error_message = error_data.get('message', str(error))
            except:
                error_message = str(error)
            raise Exception(f"API error: {error_message}")

def format_feature_summary(feature: Dict[str, Any]) -> str:
    """Format a feature for summary display"""
    ref_num = feature.get('reference_num', 'N/A')
    name = feature.get('name', 'Unnamed Feature')
    
    # Safely get workflow status
    workflow_status = feature.get('workflow_status')
    if isinstance(workflow_status, dict):
        status = workflow_status.get('name', 'Unknown')
    elif isinstance(workflow_status, str):
        status = workflow_status
    else:
        status = 'Unknown'
    
    # Check multiple possible assignee field names including nested ones
    assignee_fields = ['assigned_to_user', 'assignee', 'assigned_to', 'owner']
    assignee = 'Unassigned'
    
    # Check top-level fields
    for field in assignee_fields:
        value = feature.get(field)
        if value:
            if isinstance(value, dict):
                # If it's a user object, extract name or email
                assignee = value.get('name') or value.get('email') or str(value)
                break
            elif isinstance(value, str):
                # If it's already a string (email or name)
                assignee = value
                break
    
    # Check nested fields like requirements.assigned_to_user
    if assignee == 'Unassigned':
        requirements = feature.get('requirements', {})
        if requirements and isinstance(requirements, dict):
            req_assignee = requirements.get('assigned_to_user')
            if req_assignee:
                if isinstance(req_assignee, dict):
                    assignee = req_assignee.get('name') or req_assignee.get('email') or str(req_assignee)
                elif isinstance(req_assignee, str):
                    assignee = req_assignee
    
    # Safely get release
    release_data = feature.get('release')
    if isinstance(release_data, dict):
        release = release_data.get('name', 'No Release')
    elif isinstance(release_data, str):
        release = release_data
    else:
        release = 'No Release'
    
    tags = []
    if 'tags' in feature and feature['tags']:
        if isinstance(feature['tags'], list):
            tags = [tag.get('name', '') if isinstance(tag, dict) else str(tag) for tag in feature['tags'] if tag]
    
    return f"""Feature: {ref_num} - {name}
Status: {status}
Assignee: {assignee}
Release: {release}
Tags: {', '.join(tags) if tags else 'None'}"""

def format_feature_detail(feature: Dict[str, Any]) -> str:
    """Format a feature for detailed display"""
    ref_num = feature.get('reference_num', 'N/A')
    name = feature.get('name', 'Unnamed Feature')
    
    # Handle description which can be a string or an object
    description_raw = feature.get('description', 'No description')
    if isinstance(description_raw, dict):
        description = description_raw.get('body', 'No description')
    else:
        description = description_raw
    
    status = feature.get('workflow_status', {}).get('name', 'Unknown')
    
    # Handle workflow status safely
    workflow_status = feature.get('workflow_status')
    if isinstance(workflow_status, dict):
        status = workflow_status.get('name', 'Unknown')
    elif isinstance(workflow_status, str):
        status = workflow_status
    else:
        status = 'Unknown'
    
    # Handle assignee with robust checking
    assignee = "Unassigned"
    assigned_to_user = feature.get('assigned_to_user')
    if assigned_to_user:
        if isinstance(assigned_to_user, dict):
            # If it's a user object, extract name or email
            assignee = assigned_to_user.get('name') or assigned_to_user.get('email') or str(assigned_to_user)
        elif isinstance(assigned_to_user, str):
            # If it's already a string (email or name)
            assignee = assigned_to_user
    elif isinstance(feature.get('assignee'), dict):
        assignee = feature.get('assignee', {}).get('name', 'Unassigned')
    elif feature.get('assignee'):
        assignee = str(feature.get('assignee'))
    
    # Handle release safely  
    release_data = feature.get('release')
    if isinstance(release_data, dict):
        release = release_data.get('name', 'No Release')
    elif isinstance(release_data, str):
        release = release_data
    else:
        release = 'No Release'
        
    # Handle epic safely
    epic_data = feature.get('epic')
    if isinstance(epic_data, dict):
        epic = epic_data.get('name', 'No Epic')
    elif isinstance(epic_data, str):
        epic = epic_data
    else:
        epic = 'No Epic'
    progress = feature.get('progress', 0)
    score = feature.get('score', 'No Score')
    
    created_at = feature.get('created_at', '')
    updated_at = feature.get('updated_at', '')
    
    tags = []
    if 'tags' in feature and feature['tags'] and isinstance(feature['tags'], list):
        tags = [tag.get('name', '') for tag in feature['tags'] if isinstance(tag, dict) and tag.get('name')]
    
    result = f"""Feature: {ref_num} - {name}
Description: {description}
Status: {status}
Assignee: {assignee}
Release: {release}
Epic: {epic}
Progress: {progress}%
Score: {score}
Tags: {', '.join(tags) if tags else 'None'}
Created: {created_at}
Updated: {updated_at}"""
    
    # Add custom fields if present
    custom_fields = feature.get('custom_fields', [])
    if custom_fields and isinstance(custom_fields, list):
        result += "\n\nCustom Fields:"
        for field in custom_fields:
            if isinstance(field, dict):
                field_name = field.get('name', 'Unknown Field')
                field_value = field.get('value', 'No Value')
                result += f"\n- {field_name}: {field_value}"
    
    return result

# MCP Tools Implementation

@mcp.tool()
async def search_features(
    query: Optional[str] = None,
    product_id: Optional[str] = None,
    release_id: Optional[str] = None,
    epic_id: Optional[str] = None,
    status: Optional[str] = None,
    assigned_to_user: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 20
) -> str:
    """Search for FEATURES in the Aha! workspace. Use this tool when looking for development features, 
    requirements, or functionality that is being built or planned. Features are work items that get 
    implemented by development teams.
    
    For searching IDEAS (customer requests, feedback, suggestions), use get_related_ideas instead.
    
    Args:
        query: Text search query for feature names, descriptions, or content
        product_id: Filter by product ID
        release_id: Filter by release ID
        epic_id: Filter by epic ID
        status: Filter by workflow status (e.g., "In Development", "FCS", "Shipped")
        assigned_to_user: Filter by assignee email or user ID (e.g., "user@company.com" or user ID)
        tags: Filter by tags (comma-separated)
        limit: Maximum number of results (default: 20)
    """
    try:
        config = load_config()
        
        # Build search parameters
        params = {'per_page': min(limit, 200)}
        
        # Determine the endpoint based on filters
        if release_id:
            endpoint = f"/releases/{release_id}/features"
        elif epic_id:
            endpoint = f"/epics/{epic_id}/features"
        elif product_id:
            endpoint = f"/products/{product_id}/features"
        else:
            endpoint = "/features"
        
        # Add query parameters
        if query:
            params['q'] = query
        if status:
            params['status'] = status
        if assigned_to_user:
            params['assigned_to_user'] = assigned_to_user
        if tags:
            params['tags'] = tags
        
        async with AhaAPIClient(config) as client:
            data = await client.request('GET', endpoint, params=params)
            
            features = data.get('features', [])
            if not features:
                return "No features found matching the search criteria."
            
            # Format results - fetch full details if needed for assignee info
            results = []
            
            # Check if we need detailed info (when search includes assignee filter)
            fetch_details = assigned_to_user is not None
            
            for i, feature in enumerate(features[:limit]):
                # If we're filtering by assignee, fetch full details to show assignee info
                if fetch_details and isinstance(feature, dict) and feature.get('reference_num'):
                    try:
                        # Fetch full feature details
                        feature_detail = await client.request('GET', f"/features/{feature['reference_num']}")
                        if 'feature' in feature_detail and isinstance(feature_detail['feature'], dict):
                            feature = feature_detail['feature']
                    except Exception as e:
                        # If detailed fetch fails, use original data
                        pass
                
                # Ensure feature is still a dict before formatting
                if isinstance(feature, dict):
                    try:
                        results.append(format_feature_summary(feature))
                    except Exception as e:
                        results.append(f"Error formatting feature {feature.get('reference_num', 'unknown')}: {str(e)}")
                else:
                    results.append(f"Error: Invalid feature data type: {type(feature)} - {feature}")
            
            total_found = len(features)
            result_text = f"Found {total_found} feature(s):\n\n"
            result_text += "\n\n".join(results)
            
            if total_found > limit:
                result_text += f"\n\n(Showing first {limit} results)"
            
            return result_text
            
    except Exception as e:
        return f"Error searching features: {str(e)}"

@mcp.tool()
async def get_feature(feature_id: str) -> str:
    """Get detailed information about a specific FEATURE by its ID or reference number.
    Features are development work items, requirements, or functionality being built.
    
    Use this tool when you have a specific feature ID (e.g., "PRJ1-1234", "PRJ2-567") 
    and need complete details including assignee, status, description, custom fields, etc.
    
    For searching multiple features by text query, use search_features instead.
    For idea information, use get_related_ideas instead.
    
    Args:
        feature_id: Feature ID or reference number (e.g., "PRJ1-1234", "PRJ2-567")
    """
    try:
        config = load_config()
        
        async with AhaAPIClient(config) as client:
            data = await client.request('GET', f'/features/{feature_id}')
            
            # The API returns the feature data directly or wrapped in a 'feature' key
            feature = data.get('feature', data)
            
            return format_feature_detail(feature)
            
    except Exception as e:
        return f"Error retrieving feature {feature_id}: {str(e)}"

@mcp.tool()
async def create_feature(
    name: str,
    release_id: str,
    description: Optional[str] = None
) -> str:
    """Create a new FEATURE in Aha!. Features are development work items that get implemented 
    by engineering teams (different from ideas which are customer requests/suggestions).
    
    Args:
        name: Feature name/title
        release_id: Release to assign the feature to (REQUIRED - use list_products to find releases)
        description: Feature description or requirements
    """
    try:
        config = load_config()
        
        # Validate required release_id
        if not release_id or not release_id.strip():
            return "Error: release_id is required. Please specify which release to create the feature in. Use list_products to find available releases."
        
        # Build feature data
        feature_data = {
            'feature': {
                'name': name,
                'release_id': release_id
            }
        }
        
        if description:
            feature_data['feature']['description'] = description
        
        async with AhaAPIClient(config) as client:
            # Always use release-specific endpoint since release_id is required
            endpoint = f'/releases/{release_id}/features'
            
            data = await client.request('POST', endpoint, json=feature_data)
            
            feature = data.get('feature', data)
            ref_num = feature.get('reference_num', 'N/A')
            feature_name = feature.get('name', name)
            
            return f"Successfully created feature: {ref_num} - {feature_name}\n\n{format_feature_detail(feature)}"
            
    except Exception as e:
        return f"Error creating feature: {str(e)}"

@mcp.tool()
async def update_feature(
    feature_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    assignee: Optional[str] = None,
    release_id: Optional[str] = None,
    epic_id: Optional[str] = None,
    custom_fields: Optional[str] = None
) -> str:
    """Update an existing feature.
    
    Args:
        feature_id: Feature ID or reference number
        name: New feature name
        description: New feature description
        status: New workflow status
        assignee: New assignee
        release_id: New release assignment
        epic_id: New epic assignment
        custom_fields: Custom field updates as JSON string
    """
    try:
        config = load_config()
        
        # Build update data
        update_data = {'feature': {}}
        
        if name:
            update_data['feature']['name'] = name
        if description:
            update_data['feature']['description'] = description
        if status:
            update_data['feature']['workflow_status'] = status
        if assignee:
            update_data['feature']['assigned_to_user'] = assignee
        if release_id:
            update_data['feature']['release_id'] = release_id
        if epic_id:
            update_data['feature']['epic_id'] = epic_id
        
        # Handle custom fields
        if custom_fields:
            try:
                custom_fields_data = json.loads(custom_fields)
                update_data['feature']['custom_fields'] = custom_fields_data
            except json.JSONDecodeError:
                return "Error: custom_fields must be valid JSON"
        
        if not update_data['feature']:
            return "Error: No update fields provided"
        
        async with AhaAPIClient(config) as client:
            data = await client.request('PUT', f"/features/{feature_id}", json=update_data)
            
            feature = data.get('feature', data)
            ref_num = feature.get('reference_num', feature_id)
            feature_name = feature.get('name', 'Updated Feature')
            
            return f"Successfully updated feature: {ref_num} - {feature_name}\n\n{format_feature_detail(feature)}"
            
    except Exception as e:
        return f"Error updating feature: {str(e)}"

@mcp.tool()
async def delete_feature(feature_id: str, confirm: bool = False) -> str:
    """Delete a feature from Aha!.
    
    Args:
        feature_id: Feature ID or reference number
        confirm: Confirmation flag to prevent accidental deletion
    """
    try:
        if not confirm:
            return "Error: Deletion requires confirmation. Set confirm=True to proceed."
        
        config = load_config()
        
        async with AhaAPIClient(config) as client:
            await client.request('DELETE', f"/features/{feature_id}")
            
            return f"Successfully deleted feature: {feature_id}"
            
    except Exception as e:
        return f"Error deleting feature: {str(e)}"

@mcp.tool()
async def list_features_by_release(
    release_id: str,
    include_completed: bool = True,
    limit: int = 50
) -> str:
    """List all features in a specific release.
    
    Args:
        release_id: Release ID or reference number
        include_completed: Include completed features
        limit: Maximum number of results
    """
    try:
        config = load_config()
        
        params = {'per_page': min(limit, 200)}
        if not include_completed:
            params['exclude_completed'] = 'true'
        
        async with AhaAPIClient(config) as client:
            data = await client.request('GET', f"/releases/{release_id}/features", params=params)
            
            features = data.get('features', [])
            if not features:
                return f"No features found in release: {release_id}"
            
            # Format results
            results = []
            for feature in features[:limit]:
                results.append(format_feature_summary(feature))
            
            total_found = len(features)
            result_text = f"Found {total_found} feature(s) in release {release_id}:\n\n"
            result_text += "\n\n".join(results)
            
            if total_found > limit:
                result_text += f"\n\n(Showing first {limit} results)"
            
            return result_text
            
    except Exception as e:
        return f"Error listing features by release: {str(e)}"

@mcp.tool()
async def list_features_by_epic(epic_id: str, limit: int = 50) -> str:
    """List all features in a specific epic.
    
    Args:
        epic_id: Epic ID or reference number
        limit: Maximum number of results
    """
    try:
        config = load_config()
        
        params = {'per_page': min(limit, 200)}
        
        async with AhaAPIClient(config) as client:
            data = await client.request('GET', f"/epics/{epic_id}/features", params=params)
            
            features = data.get('features', [])
            if not features:
                return f"No features found in epic: {epic_id}"
            
            # Format results
            results = []
            for feature in features[:limit]:
                results.append(format_feature_summary(feature))
            
            total_found = len(features)
            result_text = f"Found {total_found} feature(s) in epic {epic_id}:\n\n"
            result_text += "\n\n".join(results)
            
            if total_found > limit:
                result_text += f"\n\n(Showing first {limit} results)"
            
            return result_text
            
    except Exception as e:
        return f"Error listing features by epic: {str(e)}"

@mcp.tool()
async def update_feature_status(feature_id: str, status: str) -> str:
    """Update the workflow status of a feature.
    
    Args:
        feature_id: Feature ID or reference number
        status: New workflow status
    """
    try:
        config = load_config()
        
        update_data = {
            'feature': {
                'workflow_status': status
            }
        }
        
        async with AhaAPIClient(config) as client:
            data = await client.request('PUT', f"/features/{feature_id}", json=update_data)
            
            feature = data.get('feature', data)
            ref_num = feature.get('reference_num', feature_id)
            feature_name = feature.get('name', 'Feature')
            new_status = feature.get('workflow_status', {}).get('name', status)
            
            return f"Successfully updated status for {ref_num} - {feature_name} to: {new_status}"
            
    except Exception as e:
        return f"Error updating feature status: {str(e)}"

@mcp.tool()
async def add_feature_tags(feature_id: str, tags: str, replace: bool = False) -> str:
    """Add tags to a feature.
    
    Args:
        feature_id: Feature ID or reference number
        tags: Tags to add (comma-separated)
        replace: Replace existing tags instead of adding
    """
    try:
        config = load_config()
        
        tag_list = [tag.strip() for tag in tags.split(',')]
        
        if replace:
            update_data = {
                'feature': {
                    'tags': tag_list
                }
            }
        else:
            # For adding tags, we need to get current tags first
            async with AhaAPIClient(config) as client:
                current_data = await client.request('GET', f"/features/{feature_id}")
                current_feature = current_data.get('feature', current_data)
                current_tags = [tag.get('name', '') for tag in current_feature.get('tags', [])]
                
                # Combine current and new tags
                all_tags = list(set(current_tags + tag_list))
                
                update_data = {
                    'feature': {
                        'tags': all_tags
                    }
                }
        
        async with AhaAPIClient(config) as client:
            data = await client.request('PUT', f"/features/{feature_id}", json=update_data)
            
            feature = data.get('feature', data)
            ref_num = feature.get('reference_num', feature_id)
            feature_name = feature.get('name', 'Feature')
            updated_tags = [tag.get('name', '') for tag in feature.get('tags', [])]
            
            action = "Replaced" if replace else "Added"
            return f"Successfully {action.lower()} tags for {ref_num} - {feature_name}\nCurrent tags: {', '.join(updated_tags)}"
            
    except Exception as e:
        return f"Error updating feature tags: {str(e)}"

@mcp.tool()
async def update_feature_score(feature_id: str, score: float) -> str:
    """Update the score of a feature.
    
    Args:
        feature_id: Feature ID or reference number
        score: New score value
    """
    try:
        config = load_config()
        
        update_data = {
            'feature': {
                'score': score
            }
        }
        
        async with AhaAPIClient(config) as client:
            data = await client.request('PUT', f"/features/{feature_id}", json=update_data)
            
            feature = data.get('feature', data)
            ref_num = feature.get('reference_num', feature_id)
            feature_name = feature.get('name', 'Feature')
            new_score = feature.get('score', score)
            
            return f"Successfully updated score for {ref_num} - {feature_name} to: {new_score}"
            
    except Exception as e:
        return f"Error updating feature score: {str(e)}"

@mcp.tool()
async def list_products(limit: int = 50) -> str:
    """List all products available in the Aha! workspace. 
    
    Use this tool to:
    - Discover available products and their IDs
    - Find product reference prefixes (used in feature IDs like "PRJ1-", "PRJ2-", "APP-")
    - Get product information before filtering features by product_id
    
    Args:
        limit: Maximum number of results (default: 50)
    """
    try:
        config = load_config()
        
        params = {'per_page': min(limit, 200)}
        
        async with AhaAPIClient(config) as client:
            data = await client.request('GET', '/products', params=params)
            
            products = data.get('products', [])
            if not products:
                return "No products found in the workspace."
            
            # Format results
            results = []
            for product in products:
                product_id = product.get('id', 'N/A')
                name = product.get('name', 'Unnamed Product')
                reference_prefix = product.get('reference_prefix', 'N/A')
                created_at = product.get('created_at', '')
                
                results.append(f"Product: {name} (ID: {product_id})")
                results.append(f"  Reference Prefix: {reference_prefix}")
                results.append(f"  Created: {created_at}")
                
                # Add description if available
                description = product.get('description', '')
                if description:
                    # Truncate long descriptions
                    if len(description) > 100:
                        description = description[:97] + "..."
                    results.append(f"  Description: {description}")
                
                results.append("")  # Empty line for separation
            
            total_found = len(products)
            result_text = f"Found {total_found} product(s):\n\n"
            result_text += "\n".join(results)
            
            if total_found >= limit:
                result_text += f"\n\n(Showing first {limit} results)"
            
            return result_text
            
    except Exception as e:
        return f"Error retrieving products: {str(e)}"

@mcp.tool()
async def get_related_ideas(
    query: Optional[str] = None,
    idea_id: Optional[str] = None,
    feature_id: Optional[str] = None,
    limit: int = 20
) -> str:
    """Search for and retrieve IDEAS from Aha!. Use this tool when looking for customer requests, 
    feedback, suggestions, or enhancement ideas that have been submitted to the product team.
    
    IDEAS are different from FEATURES - ideas are customer requests/suggestions, while features 
    are development work items. Use search_features for development features instead.
    
    This tool can:
    1. Search ideas by text query (most reliable method)
    2. Find ideas related to another idea 
    3. Find ideas related to a specific feature (may not always return results)
    
    Note: Feature-to-idea relationships may not be consistently available in all Aha! configurations.
    Text-based search (using 'query' parameter) is the most reliable way to find ideas.
    
    Args:
        query: Text search query to find ideas by content, title, or description (e.g., "API", "mobile", "security")
        idea_id: Specific idea ID to find related ideas for
        feature_id: Feature ID to find related ideas for (e.g., "PRJ1-123") - may not always work
        limit: Maximum number of results (default: 20)
    
    Examples:
    - Search for API-related ideas: query="API"
    - Search mobile ideas: query="mobile"
    - Find ideas for a feature: feature_id="PRJ1-123" (may return no results)
    """
    try:
        config = load_config()
        
        # Build parameters
        params = {'per_page': min(limit, 200)}
        
        # If we have a text query, use the ideas search endpoint instead of related
        if query:
            params['q'] = query
            endpoint = '/ideas'
        else:
            # Use the related ideas endpoint for specific idea/feature relationships
            if idea_id:
                params['idea_id'] = idea_id
            if feature_id:
                params['feature_id'] = feature_id
            endpoint = '/ideas/related'
        
        async with AhaAPIClient(config) as client:
            data = await client.request('GET', endpoint, params=params)
            
            ideas = data.get('ideas', [])
            if not ideas:
                return "No related ideas found."
            
            # Format results
            results = []
            for i, idea in enumerate(ideas[:limit]):
                idea_id = idea.get('id', 'N/A')
                name = idea.get('name', 'Unnamed Idea')
                reference_num = idea.get('reference_num', 'N/A')
                status = idea.get('workflow_status', {}).get('name', 'Unknown') if isinstance(idea.get('workflow_status'), dict) else 'Unknown'
                created_at = idea.get('created_at', '')
                
                # Get score if available
                score = idea.get('score', 'No Score')
                
                # Get category if available
                category = idea.get('category', {}).get('name', 'No Category') if isinstance(idea.get('category'), dict) else 'No Category'
                
                results.append(f"Idea: {reference_num} - {name}")
                results.append(f"  ID: {idea_id}")
                results.append(f"  Status: {status}")
                results.append(f"  Category: {category}")
                results.append(f"  Score: {score}")
                results.append(f"  Created: {created_at}")
                
                # Add description if available (truncated)
                description = idea.get('description', '')
                if description:
                    if isinstance(description, dict):
                        description = description.get('body', '')
                    if len(description) > 150:
                        description = description[:147] + "..."
                    results.append(f"  Description: {description}")
                
                results.append("")  # Empty line for separation
            
            total_found = len(ideas)
            result_text = f"Found {total_found} related idea(s):\n\n"
            result_text += "\n".join(results)
            
            if total_found > limit:
                result_text += f"\n\n(Showing first {limit} results)"
            
            return result_text
            
    except Exception as e:
        return f"Error retrieving related ideas: {str(e)}"

@mcp.tool()
async def list_users(
    limit: int = 20,
    query: Optional[str] = None
) -> str:
    """List users in the Aha! workspace. This tool helps find user information including 
    names, emails, and user IDs that can be used for assignee filtering.
    
    Args:
        limit: Maximum number of users to return (default: 20)
        query: Optional text search query to filter users by name or email
    """
    try:
        config = load_config()
        
        # Build search parameters
        params = {'per_page': min(limit, 200)}
        
        if query:
            params['q'] = query
        
        async with AhaAPIClient(config) as client:
            data = await client.request('GET', '/users', params=params)
            
            users = data.get('users', [])
            if not users:
                return "No users found matching the search criteria."
            
            # Format results
            results = []
            for i, user in enumerate(users[:limit]):
                user_info = []
                
                # Basic user information
                name = user.get('name', 'Unknown')
                email = user.get('email', 'No email')
                user_id = user.get('id', 'No ID')
                reference_num = user.get('reference_num', 'No reference')
                
                user_info.append(f"User: {name}")
                user_info.append(f"  Email: {email}")
                user_info.append(f"  User ID: {user_id}")
                user_info.append(f"  Reference: {reference_num}")
                
                # Additional fields if available
                if user.get('title'):
                    user_info.append(f"  Title: {user['title']}")
                
                if user.get('department'):
                    user_info.append(f"  Department: {user['department']}")
                
                if user.get('is_admin'):
                    user_info.append(f"  Admin: {user['is_admin']}")
                
                if user.get('created_at'):
                    user_info.append(f"  Created: {user['created_at']}")
                
                results.append("\n".join(user_info))
                results.append("")  # Empty line for separation
            
            total_found = len(users)
            result_text = f"Found {total_found} user(s):\n\n"
            result_text += "\n".join(results)
            
            if total_found > limit:
                result_text += f"\n\n(Showing first {limit} results)"
            
            return result_text
            
    except Exception as e:
        return f"Error listing users: {str(e)}"

@mcp.tool()
async def get_current_user() -> str:
    """Get information about the current authenticated user.
    
    This tool calls the /api/v1/me endpoint to retrieve details about the user
    associated with the current API key, including name, email, permissions, and role.
    """
    try:
        config = load_config()
        
        async with AhaAPIClient(config) as client:
            data = await client.request('GET', '/me')
            
            user = data.get('user', data)
            
            # Format user information
            results = []
            
            # Basic user information
            name = user.get('name', 'Unknown')
            email = user.get('email', 'No email')
            user_id = user.get('id', 'No ID')
            
            results.append(f"Current User: {name}")
            results.append(f"Email: {email}")
            results.append(f"User ID: {user_id}")
            
            # Additional fields if available
            if user.get('reference_num'):
                results.append(f"Reference: {user['reference_num']}")
                
            if user.get('title'):
                results.append(f"Title: {user['title']}")
                
            if user.get('department'):
                results.append(f"Department: {user['department']}")
                
            if user.get('is_admin') is not None:
                results.append(f"Admin: {user['is_admin']}")
                
            if user.get('role'):
                results.append(f"Role: {user['role']}")
                
            if user.get('created_at'):
                results.append(f"Created: {user['created_at']}")
                
            if user.get('last_active'):
                results.append(f"Last Active: {user['last_active']}")
            
            return "\n".join(results)
            
    except Exception as e:
        return f"Error retrieving current user information: {str(e)}"

if __name__ == "__main__":
    import sys
    
    # Check for help command
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        print("""
Aha! MCP Server - Model Context Protocol Integration

USAGE:
    python aha_mcp_server.py [OPTIONS]

OPTIONS:
    --help, -h, help    Show this help message and exit

DESCRIPTION:
    This MCP server provides integration between AI agents and Aha! product management.
    The server runs via stdio transport and provides the following tools:

FEATURE MANAGEMENT TOOLS:
    - mcp_aha_get_feature          Get detailed feature information
    - mcp_aha_search_features      Search features with filters  
    - mcp_aha_create_feature       Create new features
    - mcp_aha_update_feature       Update existing features
    - mcp_aha_update_feature_status Update feature workflow status
    - mcp_aha_update_feature_score Update feature scoring
    - mcp_aha_add_feature_tags     Add or replace feature tags
    - mcp_aha_delete_feature       Delete features (with confirmation)

PRODUCT & RELEASE MANAGEMENT TOOLS:
    - mcp_aha_list_products        List all available products
    - mcp_aha_list_features_by_release  Get features in a specific release
    - mcp_aha_list_features_by_epic     Get features in a specific epic
    - mcp_aha_list_users           List users in the workspace
    - mcp_aha_get_current_user     Get current authenticated user info

IDEAS & FEEDBACK TOOLS:
    - mcp_aha_get_related_ideas    Search for customer ideas and feedback

CONFIGURATION:
    The server requires aha_config.json with your Aha! credentials:
    {
        "aha_domain": "yourcompany.aha.io",
        "api_key": "your_api_key_here",
        "default_product": "optional_default_product_id"
    }

EXAMPLES:
    # Run the MCP server
    python aha_mcp_server.py
    
    # In VS Code or Claude Desktop, use tools like:
    @mcp_aha_search_features query="API security" limit=10
    @mcp_aha_get_feature DNAC-10991
    @mcp_aha_list_users limit=20

For more information, see README.md
        """)
        sys.exit(0)
    
    # Initialize and run the server
    mcp.run(transport='stdio')

