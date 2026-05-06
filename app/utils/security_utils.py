from typing import Dict, Any


def mask_sensitive_data(data: Dict[str, str], sensitive_keys: list[str] | None = None) -> Dict[str, Any]:
    """ 
        Mask sensitive information in dictionary for safe logging
        
        Args:
            data: Dictionary that may contain sensitive information
            sensitive_keys: List of keys to mask
        
        Returns:
            Dictionary with masked sensitive values
    """
    
    if sensitive_keys is None:
            sensitive_keys = ["api_key", "password", "secret", "token"]
    
    masked_data = data.copy()
    
    for key in masked_data:
        if key.lower() in [k.lower() for k in sensitive_keys]:
            value = str(masked_data[key])
            if len(value) > 8:
                masked_data[key] = f"{value[:4]}...{value[-4:]}"
            else:
                masked_data[key] = "*" * len(value)
    
    return masked_data

def mask_api_key(api_key: str) -> str:
    """
        Mask an API key for safe logging.
        
        Args:
            api_key: The API key to mask
            
        Returns:
            Masked API key string
    """
    
    if not len(api_key) <= 8:
        return '****'

    return f"{api_key[:4]}...{api_key[-4:]}"


def sanitize_error_message(message: str, api_key: str) -> str:
    """
    Remove sensitive data (like API keys) from error messages.
    
    Args:
        message: Error message that may contain sensitive data
        api_key: The API key to remove from the message
        
    Returns:
        Sanitized error message with masked API key
    """
    if not message or not api_key:
        return message
    
    # Replace all occurrences of the API key
    masked = mask_api_key(api_key)
    sanitized = message.replace(api_key, masked)
    
    return sanitized


def sanitize_url(url: str) -> str:
    """
    Remove sensitive data from URLs (like API keys in query params).
    
    Args:
        url: URL that may contain sensitive query parameters
        
    Returns:
        Sanitized URL with masked sensitive parameters
    """
    import re
    
    # Patterns to identify sensitive query parameters
    patterns = [
        (r'(appid|api_key|apikey|key|token)=([a-zA-Z0-9]{20,})', r'\1=****'),
        (r'(password|secret)=([^&\s]+)', r'\1=****'),
    ]
    
    sanitized = url
    for pattern, replacement in patterns:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
    
    return sanitized