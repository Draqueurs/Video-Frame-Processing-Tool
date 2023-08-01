# Video Frame Processing Tool

This is a Python script that processes video files by calculating the Mean Squared Error (MSE) between consecutive frames and saving frames that exceed a specified threshold. Additionally, the script provides functionality for sorting and organizing the processed frames based on various sorting modes.

## Video Frame Extraction Script

This script is designed to process videos in a folder by calculating the Mean Squared Error (MSE) between frames and saving frames that exceed the specified threshold. The script contains several functions, including `calculate_mse`, `preprocess_image`, `process_video`, and `process_videos_in_folder`.

### Functions

`calculate_mse(frame1, frame2):`
Calculate the Mean Squared Error (MSE) between two images.

#### Parameters:

- `frame1` (numpy.ndarray): First image (in grayscale).
- `frame2` (numpy.ndarray): Second image (in grayscale).
- 
#### Returns:

- `float`: The Mean Squared Error between the two images.

`preprocess_image(frame):`
Preprocess an image by converting to grayscale, cropping, and binarizing.

#### Parameters:

- `frame` (numpy.ndarray): Input image (in color).

#### Returns:

- `numpy.ndarray`: The preprocessed image (in grayscale and binarized).

`process_video(video_path, output_folder, threshold=-1, duration=-1):`
Process a video by calculating the MSE between frames and saving frames that exceed the threshold.

#### Parameters:

- `video_path` (str): Path of the video to be processed.
- `output_folder` (str): Output folder path to save frames.
- `threshold (float)`: Threshold for Mean Squared Error.
- `duration` (float): Real duration of the video in seconds.

`process_videos_in_folder(folder_path, output_folder, threshold, duration):`
Process all videos in a folder using the 'process_video' function.

Parameters:

folder_path (str): Path of the folder containing the videos.
output_folder (str): Output folder path to save frames.
threshold (float): Threshold for Mean Squared Error.
duration (float): Real duration of the videos in seconds.
Usage
To use the script, you can provide command-line arguments to specify the folder containing the videos, the output folder to save frames, the threshold for the Mean Squared Error, and the real duration of the videos (optional). The script uses argparse for parsing command-line arguments.

Here's the command-line usage:
