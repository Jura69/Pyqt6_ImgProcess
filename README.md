# PyQt6 Image Processor

A simple image processing application built with PyQt6 and OpenCV.

## Features

- Image upload and display
- Multiple image processing operations:
  - Rotation with matrix transformation
  - Cropping with improved UI
- Real-time preview
- Modern and intuitive interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Jura69/Pyqt6_ImgProcess.git
cd PyQt6-Project
```

2. Create and activate a conda environment:
```bash
conda env create -f environment.yml
conda activate pyqt6_app
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Use the interface:
   - Click "Upload Image" to select an image
   - Choose a transformation from the dropdown
   - Adjust parameters using the controls
   - Click "Process Image" to apply the transformation

## Requirements

- Python 3.11
- PyQt6
- OpenCV
- NumPy

## Project Structure

```
.
├── main.py                 # Main application
├── image_processors/       # Image processing modules
│   ├── base_processor.py   # Base processor class
│   ├── processor_factory.py # Processor factory
│   └── processors/         # Individual processors
│       ├── rotation_processor.py
│       └── crop_processor.py
└── environment.yml         # Conda environment file
```
