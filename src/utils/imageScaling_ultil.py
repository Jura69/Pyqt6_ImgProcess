import numpy as np
import cv2
from typing import Tuple

def image_scaling(image: np.ndarray, max_width: int = 650, max_height: int = 650) -> np.ndarray:
    """
    Scale an image to fit within specified dimensions while maintaining aspect ratio.
    
    Args:
        image (np.ndarray): Input image to scale
        max_width (int): Maximum width for the scaled image
        max_height (int): Maximum height for the scaled image
        
    Returns:
        np.ndarray: Scaled image
        
    Raises:
        ValueError: If input image is invalid
    """
    if image is None or image.size == 0:
        raise ValueError("Invalid input image")
        
    height, width = image.shape[:2]
    
    # Calculate scaling factors
    scale_x = max_width / width
    scale_y = max_height / height
    scale = min(scale_x, scale_y)
    
    # Calculate new dimensions
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # Create transformation matrix
    transformation_matrix = np.float32([
        [scale, 0, 0], 
        [0, scale, 0]
    ])
    
    # Apply scaling transformation
    scaled_image = cv2.warpAffine(image, transformation_matrix, (new_width, new_height))
    return scaled_image 