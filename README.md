# Signal Data Explorer

## Overview

The Signal Data Explorer is an interactive web application designed for visualizing and analyzing complex signal data from ZIP files containing CSV data. It offers a powerful and user-friendly interface for exploring multi-channel, multi-segment signal data sets, allowing users to select and analyze specific portions of the data with precision.

This tool is particularly effective for working with oscilloscope segmented memory data, enabling efficient analysis of long-duration captures with intermittent signals of interest across multiple channels. The application also supports selecting files directly from a GitHub repository, providing a convenient way to access and analyze signal data stored in remote locations.

## Live Demo

You can try out the Signal Data Explorer without any installation here:

**[https://seg-mem-explorer-demo.onrender.com](https://seg-mem-explorer-demo.onrender.com)**

Feel free to explore the features and functionality of the application directly in your web browser.

## Features

- Support for ZIP files containing multiple CSV data files
- GitHub file selection feature for accessing signal data from remote repositories
- Interactive selection of files, frames (segments), records, and channels
- Multi-axis plotting capabilities for comparing different data channels
- Dynamic updating of data visualization based on user selections
- Responsive layout adapting to various screen sizes
- Integrated signal processing utilities for advanced data analysis
- Support for oscilloscope segmented memory data, allowing analysis of multiple waveform segments captured over extended time periods
- Customizable Y-axis placement for optimal data comparison
- Theme switching between light and dark modes for comfortable viewing

## Installation

### Prerequisites

- Python 3.11 or higher
- pipenv

### Setting up the environment

1. Clone the repository:
   ```
   git clone https://github.com/ionutms/seg_mem_explorer_demo.git
   cd seg_mem_explorer_demo
   ```

2. Create a virtual environment and install dependencies using pipenv:
   ```
   pipenv install
   ```

3. Activate the virtual environment:
   ```
   pipenv shell
   ```

4. Run the application:
   ```
   python app.py
   ```

The application should now be running on `http://localhost:8050` (or another port if specified).

## Usage

1. Upload a ZIP file containing CSV signal data using the drag-and-drop area or file selector.
2. Use the range sliders to select specific files within the ZIP archive.
3. Adjust the frames slider to navigate between different segments of the data.
4. Use the records slider to focus on specific portions within each frame.
5. Select the data channels you wish to visualize using the data sets slider.
6. Customize the Y-axis placement for each channel using the radio buttons.
7. Click the 'View selected data' button to generate the visualization.
8. Interact with the multi-axis plot to explore relationships between channels.
9. Use the zoom and pan tools to investigate areas of interest in detail.
10. Toggle between light and dark themes for optimal viewing.

## Components

The Signal Data Explorer consists of several key components:

- File upload area for CSV and ZIP files
- Range sliders for selecting specific files, frames, records, and channels
- Interactive graph for data visualization
- Theme switch for toggling between light and dark modes

## Screenshots

Here are some key screenshots of the Signal Data Explorer in action:

1. Home Page

<img src="/docs/images/home-page-800x600.png" alt="Signal Data Explorer home page" width="100%" max-width="800px">

*The home page of the Signal Data Explorer, showing the main navigation hub with links to all available pages.*

2. Main Interface

<img src="/docs/images/main-interface-file-source-area-800x600.png" alt="Signal Data Explorer main interface file source area" width="100%" max-width="800px">

<img src="/docs/images/main-interface-control-panels-area-800x600.png" alt="Signal Data Explorer main interface control panels area" width="100%" max-width="800px">

*The main interface of the Signal Data Explorer, showing the file upload area and control panels.*

3. Data Visualization

<img src="/docs/images/data-visualization-800x600.png" alt="Multi-channel signal data visualization" width="100%" max-width="800px">

*An example of multi-channel signal data visualization with customized Y-axis placement.*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


