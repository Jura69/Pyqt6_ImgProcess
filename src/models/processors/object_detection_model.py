import numpy as np
import cv2
from typing import Dict, Any, Tuple, List
from models.base_model import BaseModel

class ObjectDetectionModel(BaseModel):
    """
    Model for object detection using Canny edge detection and contour finding.
    
    This processor detects objects in images by:
    1. Applying Gaussian blur for noise reduction
    2. Using Canny edge detection to find edges
    3. Finding contours from the edges
    4. Drawing bounding boxes around detected objects
    5. Optionally showing object numbering and area information
    """
    
    def __init__(self) -> None:
        """Initialize object detection model with default parameters."""
        self.threshold1: int = 30
        self.threshold2: int = 150
        self.gaussian_kernel: int = 5
        self.show_numbering: bool = True
        self.show_area: bool = True
        self.min_contour_area: float = 100.0
        self.bounding_box_color: Tuple[int, int, int] = (0, 255, 0)  # Green in RGB
        self.text_color: Tuple[int, int, int] = (0, 255, 0)  # Green in RGB
    
    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Process the image by detecting objects and drawing bounding boxes.
        
        Args:
            image (np.ndarray): Input image to process
            
        Returns:
            np.ndarray: Image with bounding boxes drawn around detected objects
        """
        if not self.validate_image(image):
            return image
        
        # Make a copy to avoid modifying the original
        result_image = image.copy()
        
        # Convert to grayscale for edge detection
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray_image = image.copy()
        
        # Apply Canny edge detection
        edges = self._canny_edge_detection(gray_image, self.threshold1, self.threshold2)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by minimum area
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > self.min_contour_area]
        
        # Draw bounding boxes
        result_image = self._draw_bounding_boxes(result_image, filtered_contours)
        
        # Calculate centroids and areas for text overlay
        if filtered_contours and (self.show_numbering or self.show_area):
            centroids = self._calculate_centroids(filtered_contours)
            
            if self.show_numbering:
                result_image = self._draw_object_numbering(result_image, centroids)
            
            if self.show_area:
                areas = self._calculate_areas(filtered_contours)
                result_image = self._draw_area_text(result_image, centroids, areas)
        
        return result_image
    
    def _canny_edge_detection(self, image: np.ndarray, threshold1: int, threshold2: int) -> np.ndarray:
        """
        Perform Canny edge detection with Gaussian blur preprocessing.
        
        Args:
            image (np.ndarray): Grayscale input image
            threshold1 (int): First threshold for edge detection
            threshold2 (int): Second threshold for edge detection
            
        Returns:
            np.ndarray: Binary edge image
        """
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (self.gaussian_kernel, self.gaussian_kernel), 0)
        
        # Apply Canny edge detection
        edges = cv2.Canny(blurred, threshold1, threshold2)
        
        return edges
    
    def _draw_bounding_boxes(self, image: np.ndarray, contours: List[np.ndarray]) -> np.ndarray:
        """
        Draw bounding boxes around the detected contours.
        
        Args:
            image (np.ndarray): Input image to draw on
            contours (List[np.ndarray]): List of contours to draw boxes around
            
        Returns:
            np.ndarray: Image with bounding boxes drawn
        """
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), self.bounding_box_color, 2)
        
        return image
    
    def _calculate_centroids(self, contours: List[np.ndarray]) -> List[Tuple[int, int]]:
        """
        Calculate the centroids of detected objects.
        
        Args:
            contours (List[np.ndarray]): List of contours
            
        Returns:
            List[Tuple[int, int]]: List of centroid coordinates (x, y)
        """
        centroids = []
        for contour in contours:
            M = cv2.moments(contour)
            if M['m00'] != 0:  # Avoid division by zero
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                centroids.append((cx, cy))
            else:
                # Use bounding box center if moments calculation fails
                x, y, w, h = cv2.boundingRect(contour)
                centroids.append((x + w // 2, y + h // 2))
        
        return centroids
    
    def _calculate_areas(self, contours: List[np.ndarray]) -> List[float]:
        """
        Calculate areas of the detected objects.
        
        Args:
            contours (List[np.ndarray]): List of contours
            
        Returns:
            List[float]: List of contour areas
        """
        return [cv2.contourArea(contour) for contour in contours]
    
    def _draw_object_numbering(self, image: np.ndarray, centroids: List[Tuple[int, int]]) -> np.ndarray:
        """
        Draw numbering on detected objects at their centroids.
        
        Args:
            image (np.ndarray): Input image to draw on
            centroids (List[Tuple[int, int]]): List of centroid coordinates
            
        Returns:
            np.ndarray: Image with object numbers drawn
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.7
        thickness = 2
        
        for i, (cx, cy) in enumerate(centroids):
            cv2.putText(image, str(i + 1), (cx, cy), font, scale, self.text_color, thickness)
        
        return image
    
    def _draw_area_text(self, image: np.ndarray, centroids: List[Tuple[int, int]], areas: List[float]) -> np.ndarray:
        """
        Draw area information on detected objects.
        
        Args:
            image (np.ndarray): Input image to draw on
            centroids (List[Tuple[int, int]]): List of centroid coordinates
            areas (List[float]): List of areas corresponding to each centroid
            
        Returns:
            np.ndarray: Image with area text drawn
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.5
        thickness = 2
        
        for (cx, cy), area in zip(centroids, areas):
            # Offset text slightly below the centroid to avoid overlap with numbering
            text_position = (cx - 20, cy + 20)
            cv2.putText(image, str(int(area)), text_position, font, scale, self.text_color, thickness)
        
        return image
    
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Set object detection parameters.
        
        Args:
            parameters (Dict[str, Any]): Parameter values to set
            
        Raises:
            ValueError: If parameters are invalid
        """
        try:
            if "threshold1" in parameters:
                self.threshold1 = int(parameters["threshold1"])
                if self.threshold1 < 0 or self.threshold1 > 255:
                    raise ValueError("threshold1 must be between 0 and 255")
            
            if "threshold2" in parameters:
                self.threshold2 = int(parameters["threshold2"])
                if self.threshold2 < 0 or self.threshold2 > 255:
                    raise ValueError("threshold2 must be between 0 and 255")
            
            if "gaussian_kernel" in parameters:
                kernel_size = int(parameters["gaussian_kernel"])
                if kernel_size < 1 or kernel_size % 2 == 0:
                    raise ValueError("gaussian_kernel must be a positive odd number")
                self.gaussian_kernel = kernel_size
            
            if "min_contour_area" in parameters:
                self.min_contour_area = float(parameters["min_contour_area"])
                if self.min_contour_area < 0:
                    raise ValueError("min_contour_area must be non-negative")
            
            if "show_numbering" in parameters:
                self.show_numbering = bool(parameters["show_numbering"])
            
            if "show_area" in parameters:
                self.show_area = bool(parameters["show_area"])
                
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid object detection parameters: {e}")
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get current object detection parameters.
        
        Returns:
            Dict[str, Any]: Current parameter values
        """
        return {
            "threshold1": self.threshold1,
            "threshold2": self.threshold2,
            "gaussian_kernel": self.gaussian_kernel,
            "min_contour_area": self.min_contour_area,
            "show_numbering": self.show_numbering,
            "show_area": self.show_area
        }
    
    def get_name(self) -> str:
        """
        Get the display name of this processor.
        
        Returns:
            str: Display name
        """
        return "Object Detection" 