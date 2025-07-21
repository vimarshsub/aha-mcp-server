#!/usr/bin/env python3
"""
Example usage scripts for Aha! MCP Server

This file contains practical examples of how to use the Aha! MCP Server
for common product management workflows.
"""

import asyncio
import json
from typing import Dict, Any

# Note: These examples assume you have an MCP client library
# In practice, you would use these commands through Claude Desktop
# or another MCP-compatible client

class AhaMCPExamples:
    """Example workflows using the Aha! MCP Server"""
    
    def __init__(self, mcp_client):
        """Initialize with an MCP client instance"""
        self.client = mcp_client
    
    async def example_1_feature_discovery(self):
        """Example 1: Discover and analyze features in a release"""
        print("=== Example 1: Feature Discovery ===")
        
        # Search for features in a specific release
        release_features = await self.client.call_tool(
            "list_features_by_release",
            {"release_id": "REL-2024-Q1", "limit": 20}
        )
        print("Release Features:")
        print(release_features)
        
        # Search for high-priority features
        priority_features = await self.client.call_tool(
            "search_features",
            {"tags": "high-priority", "limit": 10}
        )
        print("\nHigh Priority Features:")
        print(priority_features)
        
        # Search for features by assignee
        john_features = await self.client.call_tool(
            "search_features",
            {"assignee": "john.doe", "status": "In Progress"}
        )
        print("\nJohn's In-Progress Features:")
        print(john_features)
    
    async def example_2_feature_creation_workflow(self):
        """Example 2: Complete feature creation workflow"""
        print("=== Example 2: Feature Creation Workflow ===")
        
        # Create a new feature with comprehensive metadata
        new_feature = await self.client.call_tool(
            "create_feature",
            {
                "name": "Advanced Search Functionality",
                "description": "Implement advanced search with filters, sorting, and faceted navigation",
                "release_id": "REL-2024-Q2",
                "assignee": "sarah.johnson",
                "tags": "search,ui,enhancement",
                "custom_fields": json.dumps({
                    "effort_estimate": 13,
                    "business_value": "High",
                    "technical_complexity": "Medium"
                })
            }
        )
        print("Created Feature:")
        print(new_feature)
        
        # Extract feature ID from response (in practice, you'd parse this)
        feature_id = "APP-NEW"  # This would be extracted from the response
        
        # Update the feature with additional information
        updated_feature = await self.client.call_tool(
            "update_feature",
            {
                "feature_id": feature_id,
                "status": "Ready for Development",
                "custom_fields": json.dumps({
                    "start_date": "2024-02-01",
                    "target_completion": "2024-02-28"
                })
            }
        )
        print("\nUpdated Feature:")
        print(updated_feature)
    
    async def example_3_release_planning(self):
        """Example 3: Release planning and management"""
        print("=== Example 3: Release Planning ===")
        
        # Get all features in the upcoming release
        release_features = await self.client.call_tool(
            "list_features_by_release",
            {"release_id": "REL-2024-Q2", "include_completed": False}
        )
        print("Incomplete Features in Q2 Release:")
        print(release_features)
        
        # Search for features that might be at risk
        blocked_features = await self.client.call_tool(
            "search_features",
            {"status": "Blocked", "release_id": "REL-2024-Q2"}
        )
        print("\nBlocked Features:")
        print(blocked_features)
        
        # Search for features without assignees
        unassigned_features = await self.client.call_tool(
            "search_features",
            {"assignee": "", "release_id": "REL-2024-Q2"}
        )
        print("\nUnassigned Features:")
        print(unassigned_features)
    
    async def example_4_epic_management(self):
        """Example 4: Epic and feature hierarchy management"""
        print("=== Example 4: Epic Management ===")
        
        # List all features in a major epic
        epic_features = await self.client.call_tool(
            "list_features_by_epic",
            {"epic_id": "EPIC-USER-EXPERIENCE"}
        )
        print("Features in User Experience Epic:")
        print(epic_features)
        
        # Search for features across multiple epics
        auth_features = await self.client.call_tool(
            "search_features",
            {"query": "authentication", "limit": 15}
        )
        print("\nAuthentication-related Features:")
        print(auth_features)
    
    async def example_5_feature_lifecycle_management(self):
        """Example 5: Managing feature lifecycle and status updates"""
        print("=== Example 5: Feature Lifecycle Management ===")
        
        # Update multiple features to move them through the workflow
        feature_updates = [
            {"feature_id": "APP-123", "status": "In Progress"},
            {"feature_id": "APP-124", "status": "Ready for Review"},
            {"feature_id": "APP-125", "status": "In Testing"}
        ]
        
        for update in feature_updates:
            result = await self.client.call_tool(
                "update_feature_status",
                update
            )
            print(f"Updated {update['feature_id']}: {result}")
        
        # Add tags to categorize features
        await self.client.call_tool(
            "add_feature_tags",
            {
                "feature_id": "APP-123",
                "tags": "sprint-5,backend,api"
            }
        )
        
        # Update feature scores for prioritization
        priority_updates = [
            {"feature_id": "APP-123", "score": 95},
            {"feature_id": "APP-124", "score": 78},
            {"feature_id": "APP-125", "score": 82}
        ]
        
        for update in priority_updates:
            result = await self.client.call_tool(
                "update_feature_score",
                update
            )
            print(f"Updated score for {update['feature_id']}: {result}")
    
    async def example_6_reporting_and_analysis(self):
        """Example 6: Generate reports and analyze feature data"""
        print("=== Example 6: Reporting and Analysis ===")
        
        # Get detailed information about specific features
        feature_details = []
        feature_ids = ["APP-123", "APP-124", "APP-125"]
        
        for feature_id in feature_ids:
            detail = await self.client.call_tool(
                "get_feature",
                {"feature_id": feature_id}
            )
            feature_details.append(detail)
            print(f"\nDetailed info for {feature_id}:")
            print(detail)
        
        # Search for features by different criteria for analysis
        security_features = await self.client.call_tool(
            "search_features",
            {"tags": "security", "limit": 50}
        )
        print("\nSecurity Features Analysis:")
        print(security_features)
        
        # Performance features analysis
        performance_features = await self.client.call_tool(
            "search_features",
            {"query": "performance", "limit": 30}
        )
        print("\nPerformance Features Analysis:")
        print(performance_features)
    
    async def example_7_bulk_operations(self):
        """Example 7: Bulk operations for efficiency"""
        print("=== Example 7: Bulk Operations ===")
        
        # Bulk tag updates for a sprint
        sprint_features = ["APP-130", "APP-131", "APP-132", "APP-133"]
        
        for feature_id in sprint_features:
            await self.client.call_tool(
                "add_feature_tags",
                {
                    "feature_id": feature_id,
                    "tags": "sprint-6,q2-2024"
                }
            )
            print(f"Added sprint tags to {feature_id}")
        
        # Bulk status updates for completed features
        completed_features = ["APP-120", "APP-121", "APP-122"]
        
        for feature_id in completed_features:
            await self.client.call_tool(
                "update_feature_status",
                {
                    "feature_id": feature_id,
                    "status": "Done"
                }
            )
            print(f"Marked {feature_id} as Done")
    
    async def example_8_error_handling(self):
        """Example 8: Proper error handling patterns"""
        print("=== Example 8: Error Handling ===")
        
        try:
            # Attempt to get a non-existent feature
            result = await self.client.call_tool(
                "get_feature",
                {"feature_id": "INVALID-999"}
            )
            print("Unexpected success:", result)
        except Exception as e:
            print(f"Expected error for invalid feature: {e}")
        
        try:
            # Attempt to delete without confirmation
            result = await self.client.call_tool(
                "delete_feature",
                {"feature_id": "APP-123", "confirm": False}
            )
            print("Deletion result:", result)
        except Exception as e:
            print(f"Expected error for unconfirmed deletion: {e}")
        
        try:
            # Attempt to create feature with invalid custom fields
            result = await self.client.call_tool(
                "create_feature",
                {
                    "name": "Test Feature",
                    "custom_fields": "invalid json"
                }
            )
            print("Unexpected success:", result)
        except Exception as e:
            print(f"Expected error for invalid JSON: {e}")

# Natural Language Examples for Claude Desktop Users
CLAUDE_EXAMPLES = """
# Natural Language Examples for Claude Desktop

Once you have the Aha! MCP Server connected to Claude Desktop, you can use these natural language commands:

## Feature Discovery
- "Search for all features related to authentication"
- "Show me features assigned to John that are in progress"
- "List all high-priority features in the Q2 2024 release"
- "Find features tagged with 'security' and 'api'"

## Feature Creation
- "Create a new feature called 'Two-Factor Authentication' and assign it to Sarah"
- "Create a feature for 'Password Reset Functionality' in the Q2 release with high priority"
- "Add a new feature 'API Rate Limiting' with description 'Implement rate limiting for all API endpoints'"

## Feature Updates
- "Update feature APP-123 status to 'In Progress'"
- "Change the assignee of feature APP-124 to John Doe"
- "Add tags 'sprint-5' and 'backend' to feature APP-125"
- "Update the score of feature APP-126 to 85"

## Release Management
- "Show me all incomplete features in release REL-2024-Q2"
- "List features in the User Experience epic"
- "Find all blocked features in the current release"

## Reporting and Analysis
- "Get detailed information about feature APP-123"
- "Show me all features related to performance optimization"
- "List features that don't have an assignee"
- "Find features with scores above 80"

## Bulk Operations
- "Mark features APP-120, APP-121, and APP-122 as done"
- "Add 'sprint-6' tag to all features in epic EPIC-MOBILE"
- "Update all features in release REL-2024-Q1 to include 'q1-complete' tag"

## Advanced Queries
- "Show me features created this month that are assigned to the mobile team"
- "Find features in the security epic that are ready for testing"
- "List all features with custom field 'business_value' set to 'High'"
"""

def print_claude_examples():
    """Print natural language examples for Claude Desktop users"""
    print(CLAUDE_EXAMPLES)

if __name__ == "__main__":
    print("Aha! MCP Server Examples")
    print("=" * 50)
    print()
    print("This file contains example workflows for using the Aha! MCP Server.")
    print("In practice, you would use these through Claude Desktop or another MCP client.")
    print()
    print_claude_examples()

