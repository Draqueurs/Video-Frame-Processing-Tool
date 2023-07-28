import os
import cv2
import numpy as np
import argparse
from tqdm import tqdm

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

def process_video(video_path, output_folder, threshold=-1):
    """
    Process a video by calculating the Mean Squared Error between frames and saving frames that exceed the threshold.

    Parameters:
        video_path (str): Path of the video to be processed.
        output_folder (str): Output folder path to save frames.
        threshold (float): Threshold for Mean Squared Error.
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

    for i in range(len(mse_values)):
        if mse_values[i] > threshold:
            cap.set(cv2.CAP_PROP_POS_FRAMES, i + 1)
            _, frame = cap.read()
            output_path = os.path.join(output_folder, f"{video_name}_{i + 1}.jpg")
            cv2.imwrite(output_path, frame)

    cap.release()

def process_videos_in_folder(folder_path, output_folder, threshold):
    """
    Process all videos in a folder using the 'process_video' function.

    Parameters:
        folder_path (str): Path of the folder containing the videos.
        output_folder (str): Output folder path to save frames.
        threshold (float): Threshold for Mean Squared Error.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi'))]

    for video_file in tqdm(video_files, desc="Extract frames", unit="video"):
        video_path = os.path.join(folder_path, video_file)
        process_video(video_path, output_folder, threshold)

def main():
    """
    Main function to process videos based on command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Open videos from a folder, calculate the Mean Squared Error between frames, and save the frame if the error exceeds a threshold.")
    parser.add_argument("-o", "--original-folder-path", help="Path of the folder containing the videos.")
    parser.add_argument("-d", "--destination-folder-path", default=None, help="Output folder path to save frames.")
    parser.add_argument("-t", "--threshold", type=float, default=-1., help="Threshold for Mean Squared Error.")
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

    process_videos_in_folder(original_folder_path, destination_folder_path, threshold)

if __name__ == "__main__":
    main()
