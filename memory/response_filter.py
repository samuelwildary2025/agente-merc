"""
Utility to filter internal data from client responses.
Ensures that timestamps and other internal metadata are not exposed to clients.
"""

import re
from typing import Any, Dict, List


def strip_internal_metadata(content: str) -> str:
    """
    Remove internal metadata from response content.
    Specifically removes timestamp information that should not be exposed to clients.
    
    Args:
        content: Raw response content that may contain internal metadata
        
    Returns:
        Cleaned content with internal metadata removed
    """
    if not content:
        return content
    
    # Remove timestamp references from responses
    # Pattern matches things like "_timestamp": "2024-01-15T10:30:00" or similar
    content = re.sub(r'"_timestamp"\s*:\s*"[^"]*"', '', content)
    content = re.sub(r'_timestamp\s*=\s*[^,\s}]*', '', content)
    
    # Remove any remaining timestamp patterns that might appear in responses
    # ISO format timestamps: 2024-01-15T10:30:00.000Z or similar
    content = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z?', '', content)
    
    # Clean up any resulting empty objects or extra commas
    content = re.sub(r',\s*,', ',', content)  # Remove double commas
    content = re.sub(r'\{\s*,\s*\}', '{}', content)  # Fix empty objects
    content = re.sub(r'\[\s*,\s*\]', '[]', content)  # Fix empty arrays
    
    return content.strip()


def sanitize_agent_response(response_data: Any) -> Any:
    """
    Sanitize agent response to remove internal metadata.
    
    Args:
        response_data: Raw response data from agent (could be string, dict, or list)
        
    Returns:
        Sanitized response with internal data removed
    """
    if isinstance(response_data, str):
        return strip_internal_metadata(response_data)
    
    elif isinstance(response_data, dict):
        # Create a copy to avoid modifying original
        sanitized = {}
        for key, value in response_data.items():
            # Skip internal keys
            if key.startswith('_') or key == 'timestamp':
                continue
            
            # Recursively sanitize nested data
            if isinstance(value, (dict, list, str)):
                sanitized[key] = sanitize_agent_response(value)
            else:
                sanitized[key] = value
        
        return sanitized
    
    elif isinstance(response_data, list):
        return [sanitize_agent_response(item) for item in response_data]
    
    else:
        # For other types (numbers, booleans, None), return as-is
        return response_data


def prepare_client_response(agent_output: str) -> str:
    """
    Prepare final response for client consumption.
    Ensures no internal metadata is exposed.
    
    Args:
        agent_output: Raw output from the agent
        
    Returns:
        Clean response ready for client
    """
    if not agent_output:
        return agent_output
    
    # First sanitize the content
    sanitized = sanitize_agent_response(agent_output)
    
    # Ensure it's a string for final output
    if isinstance(sanitized, (dict, list)):
        # Convert to string but ensure it's readable
        import json
        try:
            return json.dumps(sanitized, ensure_ascii=False, indent=None)
        except:
            return str(sanitized)
    
    return str(sanitized)