import numpy as np
import cv2
from typing import Dict, Any, Literal
from models.base_model import BaseModel

class HighpassModel(BaseModel):
    """
    Model for highpass filtering and image sharpening operations.
    
    This processor enhances image sharpness using various highpass filter techniques:
    1. Laplacian Filter - Direct edge enhancement
    2. Unsharp Masking - Subtracts blurred version from original
    3. High Boost Filter - Amplified unsharp masking
    4. Custom Kernel - User-defined sharpening kernels
    """
    
    def __init__(self) -> None:
        """Initialize highpass model with default parameters."""
        self.filter_type: Literal["laplacian", "unsharp_mask", "high_boost", "custom"] = "unsharp_mask"
        self.strength: float = 1.0  # Filter strength multiplier
        self.gaussian_sigma: float = 1.0  # For unsharp masking blur
        self.boost_factor: float = 1.5  # For high boost filter
        self.kernel_size: int = 3  # For custom kernels
        self.preserve_brightness: bool = True  # Maintain original brightness
        
    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Process the image using selected highpass filter.
        
        Args:
            image (np.ndarray): Input image to sharpen
            
        Returns:
            np.ndarray: Sharpened image
        """
        if not self.validate_image(image):
            return image
        
        # Convert to float for better precision
        image_float = image.astype(np.float64)
        
        if self.filter_type == "laplacian":
            result = self._apply_laplacian_filter(image_float)
        elif self.filter_type == "unsharp_mask":
            result = self._apply_unsharp_mask(image_float)
        elif self.filter_type == "high_boost":
            result = self._apply_high_boost_filter(image_float)
        elif self.filter_type == "custom":
            result = self._apply_custom_kernel(image_float)
        else:
            result = image_float
        
        # Ensure values are in valid range and convert back to uint8
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return result
    
    def _apply_laplacian_filter(self, image: np.ndarray) -> np.ndarray:
        """
        Apply Laplacian filter for edge enhancement.
        
        Args:
            image (np.ndarray): Input image in float format
            
        Returns:
            np.ndarray: Sharpened image
        """
        # Define Laplacian kernel
        laplacian_kernel = np.array([[0, -1, 0],
                                   [-1, 4, -1],
                                   [0, -1, 0]], dtype=np.float64)
        
        if len(image.shape) == 3:
            # Apply to each channel separately
            result = np.zeros_like(image)
            for channel in range(image.shape[2]):
                # Apply Laplacian filter
                filtered = cv2.filter2D(image[:, :, channel], -1, laplacian_kernel)
                # Add filtered result to original with strength control
                result[:, :, channel] = image[:, :, channel] + self.strength * filtered
        else:
            # Grayscale image
            filtered = cv2.filter2D(image, -1, laplacian_kernel)
            result = image + self.strength * filtered
        
        return result
    
    def _apply_unsharp_mask(self, image: np.ndarray) -> np.ndarray:
        """
        Apply unsharp masking for image sharpening.
        
        Formula: sharpened = original + strength * (original - blurred)
        
        Args:
            image (np.ndarray): Input image in float format
            
        Returns:
            np.ndarray: Sharpened image
        """
        # Create Gaussian blur
        kernel_size = max(3, int(6 * self.gaussian_sigma) | 1)  # Ensure odd kernel size
        blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), self.gaussian_sigma)
        
        # Calculate unsharp mask
        mask = image - blurred
        
        # Apply sharpening
        result = image + self.strength * mask
        
        return result
    
    def _apply_high_boost_filter(self, image: np.ndarray) -> np.ndarray:
        """
        Apply high boost filter (amplified unsharp masking).
        
        Formula: sharpened = boost_factor * original - blurred
        
        Args:
            image (np.ndarray): Input image in float format
            
        Returns:
            np.ndarray: Sharpened image
        """
        # Create Gaussian blur
        kernel_size = max(3, int(6 * self.gaussian_sigma) | 1)  # Ensure odd kernel size
        blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), self.gaussian_sigma)
        
        # Apply high boost formula
        result = self.boost_factor * image - blurred
        
        # Apply strength control
        result = image + self.strength * (result - image)
        
        return result
    
    def _apply_custom_kernel(self, image: np.ndarray) -> np.ndarray:
        """
        Apply custom sharpening kernel.
        
        Args:
            image (np.ndarray): Input image in float format
            
        Returns:
            np.ndarray: Sharpened image
        """
        if self.kernel_size == 3:
            # 3x3 sharpening kernel
            kernel = np.array([[0, -1, 0],
                             [-1, 5, -1],
                             [0, -1, 0]], dtype=np.float64)
        elif self.kernel_size == 5:
            # 5x5 sharpening kernel
            kernel = np.array([[-1, -1, -1, -1, -1],
                             [-1,  2,  2,  2, -1],
                             [-1,  2,  8,  2, -1],
                             [-1,  2,  2,  2, -1],
                             [-1, -1, -1, -1, -1]], dtype=np.float64) / 8
        else:
            # Default to 3x3 if invalid size
            kernel = np.array([[0, -1, 0],
                             [-1, 5, -1],
                             [0, -1, 0]], dtype=np.float64)
        
        # Apply strength to kernel
        center = kernel.shape[0] // 2
        kernel[center, center] = 1 + self.strength * (kernel[center, center] - 1)
        kernel = kernel * self.strength + np.eye(kernel.shape[0]) * (1 - self.strength)
        
        if len(image.shape) == 3:
            # Apply to each channel separately
            result = np.zeros_like(image)
            for channel in range(image.shape[2]):
                result[:, :, channel] = cv2.filter2D(image[:, :, channel], -1, kernel)
        else:
            # Grayscale image
            result = cv2.filter2D(image, -1, kernel)
        
        return result
    
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Set highpass filter parameters.
        
        Args:
            parameters (Dict[str, Any]): Parameter values to set
            
        Raises:
            ValueError: If parameters are invalid
        """
        try:
            if "filter_type" in parameters:
                filter_type = parameters["filter_type"]
                if filter_type not in ["laplacian", "unsharp_mask", "high_boost", "custom"]:
                    raise ValueError("Invalid filter type")
                self.filter_type = filter_type
            
            if "strength" in parameters:
                self.strength = float(parameters["strength"])
                if self.strength < 0 or self.strength > 5.0:
                    raise ValueError("strength must be between 0 and 5.0")
            
            if "gaussian_sigma" in parameters:
                self.gaussian_sigma = float(parameters["gaussian_sigma"])
                if self.gaussian_sigma < 0.1 or self.gaussian_sigma > 10.0:
                    raise ValueError("gaussian_sigma must be between 0.1 and 10.0")
            
            if "boost_factor" in parameters:
                self.boost_factor = float(parameters["boost_factor"])
                if self.boost_factor < 1.0 or self.boost_factor > 5.0:
                    raise ValueError("boost_factor must be between 1.0 and 5.0")
            
            if "kernel_size" in parameters:
                kernel_size = int(parameters["kernel_size"])
                if kernel_size not in [3, 5]:
                    raise ValueError("kernel_size must be 3 or 5")
                self.kernel_size = kernel_size
            
            if "preserve_brightness" in parameters:
                self.preserve_brightness = bool(parameters["preserve_brightness"])
                
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid highpass filter parameters: {e}")
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get current highpass filter parameters.
        
        Returns:
            Dict[str, Any]: Current parameter values
        """
        return {
            "filter_type": self.filter_type,
            "strength": self.strength,
            "gaussian_sigma": self.gaussian_sigma,
            "boost_factor": self.boost_factor,
            "kernel_size": self.kernel_size,
            "preserve_brightness": self.preserve_brightness
        }
    
    def get_name(self) -> str:
        """
        Get the display name of this processor.
        
        Returns:
            str: Display name
        """
        return "Highpass Filter" 