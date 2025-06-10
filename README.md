# PyQt6 Image Processor

A comprehensive image processing application built with PyQt6 and OpenCV, featuring advanced computer vision and signal processing capabilities.

## Features

- **Image Upload & Display** - Load and preview images with intuitive interface
- **Real-time Processing** - Live parameter adjustment with instant feedback
- **Modern UI** - Clean, responsive interface with grouped controls
- **Multiple Processing Operations:**

### 🎯 **Object Detection**
- **Canny Edge Detection** - Advanced edge detection with dual thresholds
- **Contour Analysis** - Automatic object boundary detection
- **Bounding Box Visualization** - Visual object localization
- **Object Numbering** - Sequential object identification
- **Area Calculation** - Automatic area measurement for detected objects
- **Configurable Parameters** - Adjustable Canny thresholds, Gaussian blur, minimum area filtering

### 🔄 **Geometric Transformations**
- **Rotation** - Precise angle rotation with interpolation options
- **Cropping** - Interactive region selection and extraction
- **Flipping** - Horizontal and vertical image mirroring

### 🔧 **Frequency Domain Processing**
- **Fourier Transform Analysis** - Complete FFT-based frequency domain processing
- **Multiple Filter Types:**
  - **Lowpass** - Noise reduction and image smoothing
  - **Highpass** - Edge enhancement and sharpening
  - **Bandpass** - Selective frequency range filtering
  - **Notch** - Periodic noise removal
- **Filter Shapes:**
  - **Ideal** - Sharp cutoff filters
  - **Butterworth** - Configurable steepness (order 1-10)
  - **Gaussian** - Smooth, natural filtering
- **Spectrum Visualization** - Magnitude and phase spectrum display
- **Advanced Controls** - Dual cutoff frequencies, log transform options

### 📊 **Spatial Domain Filtering**
- **Lowpass Filters** - Multiple algorithms for noise reduction:
  - Gaussian blur with configurable sigma
  - Box filter with kernel size control
  - Bilateral filter for edge-preserving smoothing
- **Highpass Filters** - Image sharpening and enhancement:
  - **Unsharp Masking** - Professional sharpening technique
  - **Laplacian Filter** - Direct edge enhancement
  - **High Boost Filter** - Amplified sharpening
  - **Custom Kernels** - 3x3 and 5x5 predefined sharpening matrices
- **Parameter Control** - Strength, sigma, boost factor adjustments

## Installation

### 1. Install Conda

#### Windows:
1. Download Miniconda for Windows from [Miniconda website](https://docs.conda.io/en/latest/miniconda.html)
2. Run the installer and follow the instructions
3. Open "Anaconda Prompt" from Start Menu
4. Verify installation:
```bash
conda --version
```

#### macOS:
1. Download Miniconda for macOS from [Miniconda website](https://docs.conda.io/en/latest/miniconda.html)
2. Open Terminal and navigate to the download directory
3. Run the installer:
```bash
bash Miniconda3-latest-MacOSX-x86_64.sh
```
4. Follow the prompts and restart Terminal
5. Verify installation:
```bash
conda --version
```

### 2. Clone and Setup Project

1. Clone the repository:
```bash
git clone https://github.com/Jura69/Pyqt6_ImgProcess.git
cd PyQt6-Project
```

2. Create and activate the conda environment:
```bash
# Create environment from environment.yml
conda env create -f environment.yml
conda activate pyqt6_app
```

## Usage

1. Make sure you are in the project root directory (where the `src` folder is located)

2. Run the application:
```bash
python src/main.py
```

3. Use the interface:
   - **Upload Image** - Click to select an image file
   - **Select Processor** - Choose from dropdown menu:
     - Rotation (angle adjustment)
     - Crop (region selection)
     - Flip (horizontal/vertical)
     - Lowpass Filter (noise reduction)
     - Highpass Filter (sharpening)
     - Object Detection (computer vision)
     - Fourier Transform (frequency analysis)
   - **Adjust Parameters** - Use sliders, spinboxes, and checkboxes
   - **Process Image** - Apply transformations with real-time preview
   - **Save Result** - Export processed images

## Advanced Features

### 🎛️ **Dynamic UI Controls**
- **Context-Sensitive Interface** - Controls adapt to selected processor
- **Real-time Synchronization** - Sliders and spinboxes stay in sync
- **Parameter Validation** - Automatic range checking and error prevention
- **Visual Feedback** - Success/error messages and processing indicators

### 🔬 **Computer Vision Capabilities**
- **Edge Detection** - Hysteresis thresholding for optimal edge continuity
- **Contour Processing** - Hierarchical contour analysis with area filtering
- **Morphological Operations** - Advanced shape analysis and cleanup
- **Statistical Analysis** - Object counting, area measurement, centroid calculation

### 📐 **Frequency Domain Analysis**
- **FFT Processing** - Optimized Fast Fourier Transform implementation
- **Spectrum Visualization** - Magnitude and phase spectrum display
- **Filter Design** - Multiple filter shapes and customizable parameters
- **Noise Removal** - Periodic and random noise reduction techniques

### 🎨 **Image Enhancement**
- **Adaptive Filtering** - Content-aware processing algorithms
- **Edge-Preserving Smoothing** - Advanced bilateral filtering
- **Multi-scale Processing** - Pyramid-based enhancement techniques
- **Quality Preservation** - Float64 precision for minimal quality loss

## Architecture

- **MVC Pattern** - Model-View-Controller architecture for maintainability
- **Modular Design** - Easy to extend with new processors
- **Signal-Slot Communication** - Efficient event-driven updates
- **Memory Optimization** - Smart image copying and resource management

## Requirements

- Python 3.11+
- PyQt6 >= 6.0.0
- OpenCV >= 4.5.0
- NumPy >= 1.20.0


