import re
from typing import List, Dict, Any
from email_validator import validate_email as email_validator, EmailNotValidError

def validate_email(email: str) -> bool:
    """Validate email format"""
    try:
        email_validator(email)
        return True
    except EmailNotValidError:
        return False

def validate_password(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 8:
        return False
    
    # Check for uppercase letter
    if not re.search(r"[A-Z]", password):
        return False
    
    # Check for lowercase letter
    if not re.search(r"[a-z]", password):
        return False
    
    # Check for digit
    if not re.search(r"\d", password):
        return False
    
    # Check for special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    
    return True

def validate_username(username: str) -> bool:
    """Validate username format"""
    if len(username) < 3 or len(username) > 50:
        return False
    
    # Only allow alphanumeric characters and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False
    
    return True

def validate_phone_number(phone: str) -> bool:
    """Validate phone number format"""
    # Remove all non-digit characters
    digits_only = re.sub(r"\D", "", phone)
    
    # Check if it's a valid length (10-15 digits)
    if len(digits_only) < 10 or len(digits_only) > 15:
        return False
    
    return True

def validate_url(url: str) -> bool:
    """Validate URL format"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None

def validate_hex_color(color: str) -> bool:
    """Validate hex color format"""
    hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    return hex_pattern.match(color) is not None

def validate_rgb_color(rgb: List[int]) -> bool:
    """Validate RGB color values"""
    if len(rgb) != 3:
        return False
    
    for value in rgb:
        if not isinstance(value, int) or value < 0 or value > 255:
            return False
    
    return True

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """Validate file extension"""
    if not filename:
        return False
    
    extension = filename.split('.')[-1].lower()
    return extension in [ext.lower() for ext in allowed_extensions]

def validate_file_size(file_size: int, max_size: int) -> bool:
    """Validate file size"""
    return file_size <= max_size

def validate_image_dimensions(width: int, height: int, min_width: int = 100, min_height: int = 100) -> bool:
    """Validate image dimensions"""
    return width >= min_width and height >= min_height

def validate_wardrobe_item_data(item_data: Dict[str, Any]) -> List[str]:
    """Validate wardrobe item data"""
    errors = []
    
    # Check required fields
    required_fields = ["category", "subcategory", "colors", "style"]
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate category
    if "category" in item_data:
        valid_categories = ["top", "bottom", "dress", "shoes", "accessories", "outerwear", "underwear"]
        if item_data["category"] not in valid_categories:
            errors.append(f"Invalid category. Must be one of: {', '.join(valid_categories)}")
    
    # Validate colors
    if "colors" in item_data and isinstance(item_data["colors"], list):
        for color in item_data["colors"]:
            if not isinstance(color, str) or not color.strip():
                errors.append("Invalid color format")
                break
    
    # Validate style
    if "style" in item_data:
        valid_styles = ["casual", "formal", "sporty", "bohemian", "minimalist", "vintage", "modern", "ethnic"]
        if item_data["style"] not in valid_styles:
            errors.append(f"Invalid style. Must be one of: {', '.join(valid_styles)}")
    
    return errors

def validate_outfit_data(outfit_data: Dict[str, Any]) -> List[str]:
    """Validate outfit data"""
    errors = []
    
    # Check required fields
    required_fields = ["name", "items", "occasion", "season"]
    for field in required_fields:
        if field not in outfit_data or not outfit_data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate items
    if "items" in outfit_data and isinstance(outfit_data["items"], list):
        if len(outfit_data["items"]) == 0:
            errors.append("Outfit must have at least one item")
    
    # Validate occasion
    if "occasion" in outfit_data:
        valid_occasions = ["work", "casual", "formal", "party", "sport", "travel", "date", "wedding"]
        if outfit_data["occasion"] not in valid_occasions:
            errors.append(f"Invalid occasion. Must be one of: {', '.join(valid_occasions)}")
    
    # Validate season
    if "season" in outfit_data:
        valid_seasons = ["spring", "summer", "fall", "winter", "all_season"]
        if outfit_data["season"] not in valid_seasons:
            errors.append(f"Invalid season. Must be one of: {', '.join(valid_seasons)}")
    
    return errors

def validate_pagination_params(page: int, limit: int) -> List[str]:
    """Validate pagination parameters"""
    errors = []
    
    if page < 1:
        errors.append("Page must be greater than 0")
    
    if limit < 1 or limit > 100:
        errors.append("Limit must be between 1 and 100")
    
    return errors

def validate_sort_params(sort_by: str, sort_order: str) -> List[str]:
    """Validate sort parameters"""
    errors = []
    
    valid_sort_fields = ["created_at", "updated_at", "name", "price", "rating", "wear_count"]
    if sort_by not in valid_sort_fields:
        errors.append(f"Invalid sort field. Must be one of: {', '.join(valid_sort_fields)}")
    
    if sort_order not in ["asc", "desc"]:
        errors.append("Sort order must be 'asc' or 'desc'")
    
    return errors

def sanitize_string(text: str, max_length: int = 1000) -> str:
    """Sanitize string input"""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text

def validate_date_range(start_date: str, end_date: str) -> List[str]:
    """Validate date range"""
    errors = []
    
    try:
        from datetime import datetime
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        if start >= end:
            errors.append("Start date must be before end date")
        
        # Check if date range is not too large (e.g., more than 1 year)
        if (end - start).days > 365:
            errors.append("Date range cannot exceed 1 year")
            
    except ValueError:
        errors.append("Invalid date format. Use ISO 8601 format")
    
    return errors
