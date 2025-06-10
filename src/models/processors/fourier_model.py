import numpy as np
import cv2
from typing import Dict, Any, Literal, Tuple
from models.base_model import BaseModel

class FourierModel(BaseModel):
    """
    Model for Fourier Transform image processing operations.
    
    This processor provides frequency domain analysis and filtering including:
    1. Forward/Inverse FFT - Transform between spatial and frequency domains
    2. Frequency Domain Filtering - Lowpass, Highpass, Bandpass, Notch filters
    3. Magnitude/Phase Analysis - Visualize and manipulate frequency components
    4. Noise Removal - Remove periodic noise using frequency domain techniques
    """
    
    def __init__(self) -> None:
        """Initialize Fourier model with default parameters."""
        self.operation_type: Literal["filter", "magnitude", "phase", "inverse"] = "filter"
        self.filter_type: Literal["lowpass", "highpass", "bandpass", "notch"] = "lowpass"
        self.filter_shape: Literal["ideal", "butterworth", "gaussian"] = "gaussian"
        self.cutoff_frequency: float = 50.0  # Cutoff frequency (0-100% of max frequency)
        self.cutoff_high: float = 80.0  # High cutoff for bandpass/notch
        self.butterworth_order: int = 2  # Order for Butterworth filter
        self.gaussian_sigma: float = 20.0  # Sigma for Gaussian filter
        self.show_spectrum: bool = True  # Show magnitude spectrum overlay
        self.log_transform: bool = True  # Apply log transform to spectrum display
        
        # Internal state for FFT processing
        self._fft_image: np.ndarray = None
        self._magnitude: np.ndarray = None
        self._phase: np.ndarray = None
        
    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Process the image using Fourier Transform operations.
        
        Args:
            image (np.ndarray): Input image to process
            
        Returns:
            np.ndarray: Processed image based on operation type
        """
        if not self.validate_image(image):
            return image
        
        # Convert to grayscale for FFT processing
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray_image = image.copy()
        
        # Perform FFT
        fft_image = self._forward_fft(gray_image)
        self._fft_image = fft_image
        self._magnitude = np.abs(fft_image)
        self._phase = np.angle(fft_image)
        
        if self.operation_type == "filter":
            result = self._apply_frequency_filter(fft_image, gray_image.shape)
        elif self.operation_type == "magnitude":
            result = self._create_magnitude_spectrum()
        elif self.operation_type == "phase":
            result = self._create_phase_spectrum()
        elif self.operation_type == "inverse":
            result = self._inverse_fft(fft_image)
        else:
            result = gray_image
        
        # Convert back to original format if needed
        if len(image.shape) == 3 and len(result.shape) == 2:
            # Convert grayscale result back to RGB
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
        elif len(image.shape) == 2 and len(result.shape) == 3:
            # Convert RGB result to grayscale
            result = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
            
        return result
    
    def _forward_fft(self, image: np.ndarray) -> np.ndarray:
        """
        Perform forward FFT on the image.
        
        Args:
            image (np.ndarray): Input grayscale image
            
        Returns:
            np.ndarray: Complex FFT result (shifted to center)
        """
        # Pad image to optimal size for FFT
        rows, cols = image.shape
        optimal_rows = cv2.getOptimalDFTSize(rows)
        optimal_cols = cv2.getOptimalDFTSize(cols)
        
        # Pad with zeros
        padded = np.zeros((optimal_rows, optimal_cols), dtype=np.float32)
        padded[:rows, :cols] = image.astype(np.float32)
        
        # Perform FFT
        fft = np.fft.fft2(padded)
        fft_shifted = np.fft.fftshift(fft)  # Shift zero frequency to center
        
        return fft_shifted
    
    def _inverse_fft(self, fft_image: np.ndarray) -> np.ndarray:
        """
        Perform inverse FFT to get back spatial domain image.
        
        Args:
            fft_image (np.ndarray): Complex FFT image
            
        Returns:
            np.ndarray: Reconstructed spatial domain image
        """
        # Shift back and perform inverse FFT
        fft_ishifted = np.fft.ifftshift(fft_image)
        reconstructed = np.fft.ifft2(fft_ishifted)
        reconstructed = np.abs(reconstructed)
        
        # Normalize to 0-255 range
        reconstructed = np.clip(reconstructed, 0, 255).astype(np.uint8)
        
        return reconstructed
    
    def _apply_frequency_filter(self, fft_image: np.ndarray, original_shape: Tuple[int, int]) -> np.ndarray:
        """
        Apply frequency domain filter to FFT image.
        
        Args:
            fft_image (np.ndarray): Complex FFT image
            original_shape (Tuple[int, int]): Original image dimensions
            
        Returns:
            np.ndarray: Filtered spatial domain image
        """
        rows, cols = fft_image.shape
        center_row, center_col = rows // 2, cols // 2
        
        # Create filter mask
        if self.filter_type == "lowpass":
            mask = self._create_lowpass_filter(rows, cols, center_row, center_col)
        elif self.filter_type == "highpass":
            mask = self._create_highpass_filter(rows, cols, center_row, center_col)
        elif self.filter_type == "bandpass":
            mask = self._create_bandpass_filter(rows, cols, center_row, center_col)
        elif self.filter_type == "notch":
            mask = self._create_notch_filter(rows, cols, center_row, center_col)
        else:
            mask = np.ones((rows, cols))
        
        # Apply filter
        filtered_fft = fft_image * mask
        
        # Convert back to spatial domain
        result = self._inverse_fft(filtered_fft)
        
        # Crop to original size
        result = result[:original_shape[0], :original_shape[1]]
        
        return result
    
    def _create_lowpass_filter(self, rows: int, cols: int, center_row: int, center_col: int) -> np.ndarray:
        """Create lowpass filter mask."""
        mask = np.zeros((rows, cols))
        cutoff = (self.cutoff_frequency / 100.0) * min(rows, cols) / 2
        
        if self.filter_shape == "ideal":
            for i in range(rows):
                for j in range(cols):
                    distance = np.sqrt((i - center_row)**2 + (j - center_col)**2)
                    if distance <= cutoff:
                        mask[i, j] = 1.0
        elif self.filter_shape == "butterworth":
            for i in range(rows):
                for j in range(cols):
                    distance = np.sqrt((i - center_row)**2 + (j - center_col)**2)
                    mask[i, j] = 1.0 / (1.0 + (distance / cutoff)**(2 * self.butterworth_order))
        elif self.filter_shape == "gaussian":
            for i in range(rows):
                for j in range(cols):
                    distance = np.sqrt((i - center_row)**2 + (j - center_col)**2)
                    mask[i, j] = np.exp(-(distance**2) / (2 * (cutoff/2)**2))
        
        return mask
    
    def _create_highpass_filter(self, rows: int, cols: int, center_row: int, center_col: int) -> np.ndarray:
        """Create highpass filter mask."""
        lowpass_mask = self._create_lowpass_filter(rows, cols, center_row, center_col)
        return 1.0 - lowpass_mask
    
    def _create_bandpass_filter(self, rows: int, cols: int, center_row: int, center_col: int) -> np.ndarray:
        """Create bandpass filter mask."""
        cutoff_low = (self.cutoff_frequency / 100.0) * min(rows, cols) / 2
        cutoff_high = (self.cutoff_high / 100.0) * min(rows, cols) / 2
        
        mask = np.zeros((rows, cols))
        
        if self.filter_shape == "ideal":
            for i in range(rows):
                for j in range(cols):
                    distance = np.sqrt((i - center_row)**2 + (j - center_col)**2)
                    if cutoff_low <= distance <= cutoff_high:
                        mask[i, j] = 1.0
        elif self.filter_shape == "butterworth":
            for i in range(rows):
                for j in range(cols):
                    distance = np.sqrt((i - center_row)**2 + (j - center_col)**2)
                    if distance > 0:
                        h_high = 1.0 / (1.0 + (cutoff_low / distance)**(2 * self.butterworth_order))
                        h_low = 1.0 / (1.0 + (distance / cutoff_high)**(2 * self.butterworth_order))
                        mask[i, j] = h_high * h_low
        elif self.filter_shape == "gaussian":
            for i in range(rows):
                for j in range(cols):
                    distance = np.sqrt((i - center_row)**2 + (j - center_col)**2)
                    center_freq = (cutoff_low + cutoff_high) / 2
                    bandwidth = cutoff_high - cutoff_low
                    mask[i, j] = np.exp(-((distance - center_freq)**2) / (2 * (bandwidth/4)**2))
        
        return mask
    
    def _create_notch_filter(self, rows: int, cols: int, center_row: int, center_col: int) -> np.ndarray:
        """Create notch filter mask (inverse of bandpass)."""
        bandpass_mask = self._create_bandpass_filter(rows, cols, center_row, center_col)
        return 1.0 - bandpass_mask
    
    def _create_magnitude_spectrum(self) -> np.ndarray:
        """
        Create magnitude spectrum visualization.
        
        Returns:
            np.ndarray: Magnitude spectrum image
        """
        if self._magnitude is None:
            return np.zeros((100, 100), dtype=np.uint8)
        
        magnitude = self._magnitude.copy()
        
        if self.log_transform:
            # Apply log transform for better visualization
            magnitude = np.log(magnitude + 1)
        
        # Normalize to 0-255 range
        magnitude = magnitude - np.min(magnitude)
        if np.max(magnitude) > 0:
            magnitude = magnitude / np.max(magnitude) * 255
        
        return magnitude.astype(np.uint8)
    
    def _create_phase_spectrum(self) -> np.ndarray:
        """
        Create phase spectrum visualization.
        
        Returns:
            np.ndarray: Phase spectrum image
        """
        if self._phase is None:
            return np.zeros((100, 100), dtype=np.uint8)
        
        phase = self._phase.copy()
        
        # Normalize phase to 0-255 range
        phase = (phase + np.pi) / (2 * np.pi) * 255
        
        return phase.astype(np.uint8)
    
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Set Fourier transform parameters.
        
        Args:
            parameters (Dict[str, Any]): Parameter values to set
            
        Raises:
            ValueError: If parameters are invalid
        """
        try:
            if "operation_type" in parameters:
                operation_type = parameters["operation_type"]
                if operation_type not in ["filter", "magnitude", "phase", "inverse"]:
                    raise ValueError("Invalid operation type")
                self.operation_type = operation_type
            
            if "filter_type" in parameters:
                filter_type = parameters["filter_type"]
                if filter_type not in ["lowpass", "highpass", "bandpass", "notch"]:
                    raise ValueError("Invalid filter type")
                self.filter_type = filter_type
            
            if "filter_shape" in parameters:
                filter_shape = parameters["filter_shape"]
                if filter_shape not in ["ideal", "butterworth", "gaussian"]:
                    raise ValueError("Invalid filter shape")
                self.filter_shape = filter_shape
            
            if "cutoff_frequency" in parameters:
                self.cutoff_frequency = float(parameters["cutoff_frequency"])
                if self.cutoff_frequency < 0 or self.cutoff_frequency > 100:
                    raise ValueError("cutoff_frequency must be between 0 and 100")
            
            if "cutoff_high" in parameters:
                self.cutoff_high = float(parameters["cutoff_high"])
                if self.cutoff_high < 0 or self.cutoff_high > 100:
                    raise ValueError("cutoff_high must be between 0 and 100")
            
            if "butterworth_order" in parameters:
                self.butterworth_order = int(parameters["butterworth_order"])
                if self.butterworth_order < 1 or self.butterworth_order > 10:
                    raise ValueError("butterworth_order must be between 1 and 10")
            
            if "gaussian_sigma" in parameters:
                self.gaussian_sigma = float(parameters["gaussian_sigma"])
                if self.gaussian_sigma < 1 or self.gaussian_sigma > 100:
                    raise ValueError("gaussian_sigma must be between 1 and 100")
            
            if "show_spectrum" in parameters:
                self.show_spectrum = bool(parameters["show_spectrum"])
            
            if "log_transform" in parameters:
                self.log_transform = bool(parameters["log_transform"])
                
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid Fourier transform parameters: {e}")
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get current Fourier transform parameters.
        
        Returns:
            Dict[str, Any]: Current parameter values
        """
        return {
            "operation_type": self.operation_type,
            "filter_type": self.filter_type,
            "filter_shape": self.filter_shape,
            "cutoff_frequency": self.cutoff_frequency,
            "cutoff_high": self.cutoff_high,
            "butterworth_order": self.butterworth_order,
            "gaussian_sigma": self.gaussian_sigma,
            "show_spectrum": self.show_spectrum,
            "log_transform": self.log_transform
        }
    
    def get_name(self) -> str:
        """
        Get the display name of this processor.
        
        Returns:
            str: Display name
        """
        return "Fourier Transform" 