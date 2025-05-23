# PyQt6 Image Processor

A simple image processing application built with PyQt6 and OpenCV.

## Features

- Image upload and display
- Multiple image processing operations:
  - Rotation 
  - Cropping 
  - Lowpass filter
- Real-time preview
- Modern and intuitive interface

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
   - Click "Upload Image" to select an image
   - Choose a transformation from the dropdown
   - Adjust parameters using the controls
   - Click "Process Image" to apply the transformation

## Requirements

- Python 3.11
- PyQt6
- OpenCV
- NumPy

