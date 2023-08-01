"""
Video Frame Extraction Script

This script is designed to process videos in a folder by calculating the Mean Squared Error (MSE) between frames and
saving frames that exceed the specified threshold. The script contains several functions, including
`calculate_mse`, `preprocess_image`, `process_video`, and `process_videos_in_folder`.

Functions:
    calculate_mse(frame1, frame2):
        Calculate the Mean Squared Error (MSE) between two images.

    preprocess_image(frame):
        Preprocess an image by converting to grayscale, cropping, and binarizing.

    process_video(video_path, output_folder, threshold=-1, duration=-1):
        Process a video by calculating the MSE between frames and saving frames that exceed the threshold.

    process_videos_in_folder(folder_path, output_folder, threshold, duration):
        Process all videos in a folder using the 'process_video' function.

The script uses the argparse module to parse command-line arguments, allowing users to specify the path of the folder
containing the videos, the output folder path to save frames, the threshold for the Mean Squared Error, and the real
duration of the videos in seconds. The main() function is responsible for parsing the arguments and calling the
process_videos_in_folder() function with the provided arguments. If the required argument (-o) for the folder path is not
provided, it displays an error message and exits the program.

The script reads video files from the given folder path, calculates the Mean Squared Error between consecutive frames,
and saves frames where the error exceeds the specified threshold. It then creates an output folder to store the extracted
frames, and the frames are saved as JPEG images with filenames indicating the original video name and the frame number.
"""

import os
import cv2
import numpy as np
import argparse
from tqdm import tqdm
from datetime import datetime, timedelta


def calculate_mse(frame1, frame2):
    """
    Calculate the Mean Squared Error (MSE) between two images.

    Parameters:
        frame1 (numpy.ndarray): First image (in grayscale).
        frame2 (numpy.ndarray): Second image (in grayscale).

    Returns:
        float: The Mean Squared Error between the two images.
    """
    squared_diff = (frame1 - frame2) ** 2
    mse = np.mean(squared_diff)
    return mse


def preprocess_image(frame):
    """
    Preprocess an image by converting to grayscale, cropping, and binarizing.

    Parameters:
        frame (numpy.ndarray): Input image (in color).

    Returns:
        numpy.ndarray: The preprocessed image (in grayscale and binarized).
    """
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    height, width = gray_frame.shape[:2]
    crop_width = int(width * 0.25)
    crop_height = int(height * 0)
    frame_cropped = gray_frame[crop_height:height - crop_height, crop_width:width - crop_width]

    median_value = np.median(frame_cropped)

    _, binary_frame = cv2.threshold(frame_cropped, median_value, 255, cv2.THRESH_BINARY)

    return binary_frame


def process_video(video_path, output_folder, threshold=-1, duration=-1):
    """
    Process a video by calculating the Mean Squared Error between frames and saving frames that exceed the threshold.

    Parameters:
        video_path (str): Path of the video to be processed.
        output_folder (str): Output folder path to save frames.
        threshold (float): Threshold for Mean Squared Error.
        duration (float): Real duration of the video in seconds.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Unable to open the video: {video_path}")
        return

    mse_values = []
    _, prev_frame = cap.read()
    pp_prev_frame = preprocess_image(prev_frame)
    frame_count = 0

    video_name = os.path.splitext(os.path.basename(video_path))[0]

    if duration > 0:
        interval = int(duration / (int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) + 1))

        box_cam_name = '_'.join(video_name.split('_')[:2])
        date_and_time = datetime.strptime('_'.join(video_name.split('_')[2:]), "%Y-%m-%d_%H-%M-%S")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        pp_frame = preprocess_image(frame)
        mse = calculate_mse(pp_prev_frame, pp_frame)
        mse_values.append(mse)

        pp_prev_frame = pp_frame.copy()
        frame_count += 1

    if threshold == -1:
        threshold = sum(mse_values) / len(mse_values)

    for i, mse_value in enumerate(mse_values):
        if mse_value > threshold:
            cap.set(cv2.CAP_PROP_POS_FRAMES, i + 1)
            _, frame = cap.read()
            if duration > 0:
                time_change = timedelta(seconds=(i + 1) * interval)
                new_date_and_time = date_and_time + time_change
                output_path = os.path.join(output_folder, box_cam_name + '_' + new_date_and_time.strftime("%Y-%m-%d_%H-%M-%S") + '.jpg')
            else:
                output_path = os.path.join(output_folder, f'{video_name}_{i + 1}.jpg')
            cv2.imwrite(output_path, frame)

    cap.release()


def process_videos_in_folder(folder_path, output_folder, threshold, duration):
    """
    Process all videos in a folder using the 'process_video' function.

    Parameters:
        folder_path (str): Path of the folder containing the videos.
        output_folder (str): Output folder path to save frames.
        threshold (float): Threshold for Mean Squared Error.
        duration (float): Real duration of the videos in seconds.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi'))]

    for video_file in tqdm(video_files, desc="Extract frames", unit="video"):
        video_path = os.path.join(folder_path, video_file)
        process_video(video_path, output_folder, threshold, duration)


def main():
    """
    Main function to process videos based on command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Open videos from a folder, calculate the Mean Squared Error between frames, and save the frame if "
                    "the error exceeds a threshold."
    )
    parser.add_argument("-o", "--original-folder-path", help="Path of the folder containing the videos.")
    parser.add_argument("-d", "--destination-folder-path", default=None, help="Output folder path to save frames.")
    parser.add_argument("-t", "--threshold", type=float, default=-1., help="Threshold for Mean Squared Error.")
    parser.add_argument("-D", "--duration", type=float, default=-1., help="Real duration of the videos in seconds.")
    args = parser.parse_args()

    # Check if the original-folder-path option is empty
    if not args.original_folder_path:
        print("Error: The '-o' option is required. Please provide the path of the folder containing the videos.")
        return  # Exit the program

    original_folder_path = args.original_folder_path
    if args.destination_folder_path is not None:
        destination_folder_path = os.path.join(args.destination_folder_path, 'frames')
    else:
        destination_folder_path = os.path.join(os.path.dirname(original_folder_path), 'frames')
    threshold = args.threshold
    duration = args.duration

    process_videos_in_folder(original_folder_path, destination_folder_path, threshold, duration)


if __name__ == "__main__":
    main()