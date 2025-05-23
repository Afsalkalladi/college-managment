# teachers/utils.py
from django.core.exceptions import ValidationError
import os

# Allowed file extensions
ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.txt', '.zip', '.rar', '.xlsx', '.xls']

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes

def validate_file_extension(file):
    """
    Validate that the uploaded file has an allowed extension.
    
    Args:
        file: The uploaded file object
        
    Raises:
        ValidationError: If the file extension is not allowed
    """
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f'File type "{ext}" is not supported. '
            f'Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        )

def validate_file_size(file):
    """
    Validate that the uploaded file doesn't exceed the maximum size limit.
    
    Args:
        file: The uploaded file object
        
    Raises:
        ValidationError: If the file size exceeds the maximum allowed size
    """
    if file.size > MAX_FILE_SIZE:
        raise ValidationError(
            f'File size exceeds maximum allowed size of {MAX_FILE_SIZE/1024/1024:.1f}MB. '
            f'Your file size: {file.size/1024/1024:.1f}MB'
        )

def get_file_info(file):
    """
    Get information about an uploaded file.
    
    Args:
        file: The uploaded file object
        
    Returns:
        dict: Dictionary containing file information
    """
    if not file:
        return None
    
    return {
        'name': file.name,
        'size': file.size,
        'size_mb': f"{file.size / 1024 / 1024:.2f} MB",
        'extension': os.path.splitext(file.name)[1][1:].upper(),
        'content_type': getattr(file, 'content_type', 'Unknown')
    }

def sanitize_filename(filename):
    """
    Sanitize a filename to remove potentially harmful characters.
    
    Args:
        filename: The original filename
        
    Returns:
        str: Sanitized filename
    """
    import re
    # Remove any path components
    filename = os.path.basename(filename)
    # Remove non-alphanumeric characters except dots, hyphens, and underscores
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Remove multiple consecutive dots
    filename = re.sub(r'\.+', '.', filename)
    return filename