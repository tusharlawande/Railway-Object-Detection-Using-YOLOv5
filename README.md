# Railway Object Detection Using YOLOv5

## Overview
This project utilizes YOLOv5 (a pre-trained object detection model) to identify specific railway-related objects in a video. It processes a given railway track video, detects various railway objects, and generates a CSV file with detailed results and a summary report. The objects are identified based on predefined categories like poles, signs, stones, etc.

## Requirements

- **Python 3.x**: Ensure you have Python 3.x installed.
- **Libraries**: Install the required Python libraries using pip:
  
  ```bash
  pip install torch opencv-python pandas
  ```

- **YOLOv5**: The code uses YOLOv5 for object detection, which can be loaded directly using the PyTorch hub.

## Installation

1. Clone or download the project files to your local machine.
2. Install the required Python packages as mentioned in the requirements section.
3. Place your railway track video in the same directory or specify the correct path to it in the script.

## Files in this Project

- **`railway_track_video.mp4`**: The input video that will be analyzed for railway object detection.
- **`railway_detections.csv`**: Contains detailed detection data (frame number, timestamp, object detected, confidence level, and bounding box coordinates).
- **`railway_detection_summary.txt`**: A summary report of the detections made during the video analysis.

## How It Works

1. **Input Video**: The video is opened and analyzed frame by frame.
2. **Object Detection**: YOLOv5 detects objects in each frame.
3. **Mapping Railway Objects**: Custom mappings are defined to recognize specific railway objects.
4. **Confidence Threshold**: Detections with a confidence score greater than 0.6 are stored.
5. **Output**:
   - **CSV File**: Stores detailed detection data.
   - **Summary File**: Provides a brief report of detected objects.

## Configuration

- **Video File**: The input video should be at `railway_track_video.mp4`. Update the script if needed.
- **Output Files**:
  - **CSV File**: Saves detection details (`railway_detections.csv`).
  - **Summary File**: Saves the detection summary (`railway_detection_summary.txt`).

## Script Overview

### `detect_railway_objects`
Processes the video frame by frame, runs object detection using YOLOv5, and collects detected objects with confidence > 0.6.

### `save_and_summarize`
Saves detection results in a CSV file and generates a summary text file.

### `main`
Ensures the video exists, processes it, and calls the detection functions.

## Running the Script

```bash
python railway_object_detection.py
```

## Output

### `railway_detections.csv`

| frame | timestamp_sec | object      | confidence | x    | y    | width | height |
|-------|--------------|------------|------------|------|------|-------|--------|
| 1     | 0.03         | Pole-OHE   | 0.85       | 150  | 120  | 50    | 100    |
| 2     | 0.07         | Sign Board | 0.90       | 200  | 180  | 60    | 110    |

### `railway_detection_summary.txt`

```
Railway Track Object Detection Report
Total Detections: 150
Unique Objects Spotted: 5

Breakdown:
Pole: 50
Sign: 40
Fence: 20
Stone: 15
Object: 25
```

## Notes
- The confidence threshold (0.6) can be adjusted in the script.
- The model can be switched to **YOLOv5m** or **YOLOv5l** for better accuracy.

## Contributing
To contribute:
- Fork the repository.
- Make your changes.
- Open a pull request with a description of your modifications.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

