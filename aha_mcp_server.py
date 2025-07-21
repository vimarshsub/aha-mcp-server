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
            return response.json()
        except httpx.HTTPStatusError as e:
            await self._handle_http_error(e)
        except httpx.RequestError as e:
            raise Exception(f"Network error: {str(e)}")
    
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
    status = feature.get('workflow_status', {}).get('name', 'Unknown')
    assignee = feature.get('assigned_to_user', {}).get('name', 'Unassigned')
    release = feature.get('release', {}).get('name', 'No Release')
    
    tags = []
    if 'tags' in feature and feature['tags']:
        tags = [tag.get('name', '') for tag in feature['tags'] if tag.get('name')]
    
    return f"""Feature: {ref_num} - {name}
Status: {status}
Assignee: {assignee}
Release: {release}
Tags: {', '.join(tags) if tags else 'None'}"""

def format_feature_detail(feature: Dict[str, Any]) -> str:
    """Format a feature for detailed display"""
    ref_num = feature.get('reference_num', 'N/A')
    name = feature.get('name', 'Unnamed Feature')
    description = feature.get('description', 'No description')
    status = feature.get('workflow_status', {}).get('name', 'Unknown')
    assignee = feature.get('assigned_to_user', {}).get('name', 'Unassigned')
    release = feature.get('release', {}).get('name', 'No Release')
    epic = feature.get('epic', {}).get('name', 'No Epic')
    progress = feature.get('progress', 0)
    score = feature.get('score', 'No Score')
    
    created_at = feature.get('created_at', '')
    updated_at = feature.get('updated_at', '')
    
    tags = []
    if 'tags' in feature and feature['tags']:
        tags = [tag.get('name', '') for tag in feature['tags'] if tag.get('name')]
    
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
    if custom_fields:
        result += "\n\nCustom Fields:"
        for field in custom_fields:
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
    assignee: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 20
) -> str:
    """Search for features across the Aha! workspace.
    
    Args:
        query: Text search query
        product_id: Filter by product ID
        release_id: Filter by release ID
        epic_id: Filter by epic ID
        status: Filter by workflow status
        assignee: Filter by assignee
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
        if assignee:
            params['assignee'] = assignee
        if tags:
            params['tags'] = tags
        
        async with AhaAPIClient(config) as client:
            data = await client.request('GET', endpoint, params=params)
            
            features = data.get('features', [])
            if not features:
                return "No features found matching the search criteria."
            
            # Format results
            results = []
            for feature in features[:limit]:
                results.append(format_feature_summary(feature))
            
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
    """Get detailed information about a specific feature.
    
    Args:
        feature_id: Feature ID or reference number
    """
    try:
        config = load_config()
        
        async with AhaAPIClient(config) as client:
            data = await client.request('GET', f"/features/{feature_id}")
            
            feature = data.get('feature', data)
            return format_feature_detail(feature)
            
    except Exception as e:
        return f"Error retrieving feature: {str(e)}"

@mcp.tool()
async def create_feature(
    name: str,
    description: Optional[str] = None,
    release_id: Optional[str] = None,
    epic_id: Optional[str] = None,
    assignee: Optional[str] = None,
    tags: Optional[str] = None,
    custom_fields: Optional[str] = None
) -> str:
    """Create a new feature in Aha!.
    
    Args:
        name: Feature name
        description: Feature description
        release_id: Release to assign the feature to
        epic_id: Epic to assign the feature to
        assignee: User to assign the feature to
        tags: Tags to add (comma-separated)
        custom_fields: Custom field values as JSON string
    """
    try:
        config = load_config()
        
        # Build feature data
        feature_data = {
            'feature': {
                'name': name
            }
        }
        
        if description:
            feature_data['feature']['description'] = description
        if release_id:
            feature_data['feature']['release_id'] = release_id
        if epic_id:
            feature_data['feature']['epic_id'] = epic_id
        if assignee:
            feature_data['feature']['assigned_to_user'] = assignee
        
        # Handle tags
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            feature_data['feature']['tags'] = tag_list
        
        # Handle custom fields
        if custom_fields:
            try:
                custom_fields_data = json.loads(custom_fields)
                feature_data['feature']['custom_fields'] = custom_fields_data
            except json.JSONDecodeError:
                return "Error: custom_fields must be valid JSON"
        
        async with AhaAPIClient(config) as client:
            data = await client.request('POST', '/features', json=feature_data)
            
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

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

