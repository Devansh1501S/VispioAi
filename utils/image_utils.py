import io
import logging
from PIL import Image, ImageOps
from typing import Tuple, Optional
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_image(image: Image.Image) -> bool:
    """
    Validate if the image is valid and can be processed.
    
    Args:
        image: PIL Image object
        
    Returns:
        True if image is valid, False otherwise
    """
    try:
        # Check if image object exists
        if image is None:
            logger.error("Image object is None")
            return False
        
        # Check minimum dimensions
        width, height = image.size
        if width < 10 or height < 10:
            logger.warning(f"Image too small: {width}x{height}")
            return False
        
        # Check maximum dimensions (100MP limit)
        if width * height > 100_000_000:
            logger.warning(f"Image too large: {width}x{height}")
            return False
        
        # Check if image has valid mode
        valid_modes = ['RGB', 'RGBA', 'L', 'P', '1']
        if image.mode not in valid_modes:
            logger.warning(f"Unsupported image mode: {image.mode}")
            return False
        
        # Try to load image data to ensure it's not corrupted
        try:
            image.load()
        except Exception as load_error:
            logger.error(f"Failed to load image data: {str(load_error)}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Image validation failed: {str(e)}")
        return False

def resize_image(image: Image.Image, max_size: Tuple[int, int] = (1024, 1024)) -> Image.Image:
    """
    Resize image while maintaining aspect ratio.
    
    Args:
        image: PIL Image object
        max_size: Maximum dimensions (width, height)
        
    Returns:
        Resized PIL Image object
    """
    try:
        # Convert to RGB if necessary
        if image.mode in ['RGBA', 'P']:
            # Create white background for transparency
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[-1])
            else:
                background.paste(image)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Calculate new dimensions maintaining aspect ratio
        original_width, original_height = image.size
        max_width, max_height = max_size
        
        # Calculate scaling factor
        width_ratio = max_width / original_width
        height_ratio = max_height / original_height
        scale_factor = min(width_ratio, height_ratio, 1.0)  # Don't upscale
        
        if scale_factor < 1.0:
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            
            # Use high-quality resampling
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.info(f"Image resized from {original_width}x{original_height} to {new_width}x{new_height}")
        
        return image
        
    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")
        return image  # Return original image if resize fails

def optimize_image_for_api(image: Image.Image, max_file_size_mb: float = 4.0) -> bytes:
    """
    Optimize image for API upload by adjusting quality and size.
    
    Args:
        image: PIL Image object
        max_file_size_mb: Maximum file size in MB
        
    Returns:
        Optimized image as bytes
    """
    try:
        max_file_size_bytes = int(max_file_size_mb * 1024 * 1024)
        
        # Start with high quality
        quality = 95
        
        while quality >= 20:
            # Convert image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
            img_bytes = img_byte_arr.getvalue()
            
            # Check file size
            if len(img_bytes) <= max_file_size_bytes:
                logger.info(f"Image optimized to {len(img_bytes)} bytes with quality {quality}")
                return img_bytes
            
            # Reduce quality for next iteration
            quality -= 10
        
        # If still too large, resize the image
        resized_image = resize_image(image, max_size=(800, 600))
        img_byte_arr = io.BytesIO()
        resized_image.save(img_byte_arr, format='JPEG', quality=80, optimize=True)
        img_bytes = img_byte_arr.getvalue()
        
        logger.info(f"Image resized and optimized to {len(img_bytes)} bytes")
        return img_bytes
        
    except Exception as e:
        logger.error(f"Error optimizing image: {str(e)}")
        # Fallback: return original image as JPEG with medium quality
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=70)
        return img_byte_arr.getvalue()

def get_image_info(image: Image.Image) -> dict:
    """
    Get detailed information about an image.
    
    Args:
        image: PIL Image object
        
    Returns:
        Dictionary containing image information
    """
    try:
        width, height = image.size
        mode = image.mode
        format_name = getattr(image, 'format', 'Unknown')
        
        # Calculate file size estimate
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        estimated_size = len(img_byte_arr.getvalue())
        
        # Get color information
        has_transparency = mode in ['RGBA', 'LA'] or 'transparency' in image.info
        
        info = {
            'width': width,
            'height': height,
            'mode': mode,
            'format': format_name,
            'estimated_size_bytes': estimated_size,
            'estimated_size_mb': round(estimated_size / (1024 * 1024), 2),
            'aspect_ratio': round(width / height, 2),
            'total_pixels': width * height,
            'has_transparency': has_transparency
        }
        
        return info
        
    except Exception as e:
        logger.error(f"Error getting image info: {str(e)}")
        return {
            'error': str(e),
            'width': 0,
            'height': 0,
            'mode': 'Unknown',
            'format': 'Unknown'
        }

def convert_to_jpeg_bytes(image: Image.Image, quality: int = 85) -> bytes:
    """
    Convert PIL Image to JPEG bytes.
    
    Args:
        image: PIL Image object
        quality: JPEG quality (1-100)
        
    Returns:
        Image as JPEG bytes
    """
    try:
        # Ensure RGB mode for JPEG
        if image.mode != 'RGB':
            if image.mode in ['RGBA', 'P']:
                # Handle transparency by adding white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[-1])
                else:
                    background.paste(image)
                image = background
            else:
                image = image.convert('RGB')
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
        return img_byte_arr.getvalue()
        
    except Exception as e:
        logger.error(f"Error converting to JPEG bytes: {str(e)}")
        raise Exception(f"Failed to convert image to JPEG: {str(e)}")

def create_thumbnail(image: Image.Image, size: Tuple[int, int] = (150, 150)) -> Image.Image:
    """
    Create a thumbnail of the image.
    
    Args:
        image: PIL Image object
        size: Thumbnail size (width, height)
        
    Returns:
        Thumbnail as PIL Image object
    """
    try:
        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        return thumbnail
        
    except Exception as e:
        logger.error(f"Error creating thumbnail: {str(e)}")
        return image  # Return original image if thumbnail creation fails
