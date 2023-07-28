import os
import cv2
import numpy as np
from tqdm import tqdm

def get_total_video_count(folder_path):
    """
    Get the total number of videos in the specified folder.

    Args:
        folder_path (str): Path to the folder containing the videos.

    Returns:
        int: Total number of videos in the folder.
    """
    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi'))]
    return len(video_files)

def rotate_video_frames(input_folder, output_folder):
    """
    Rotate video frames in the input folder and save them to the output folder.

    Args:
        input_folder (str): Path to the folder containing the input videos.
        output_folder (str): Path to the folder where rotated videos will be saved.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the total number of videos to process
    total_videos = get_total_video_count(input_folder)

    # List of video files in the input folder
    video_files = [f for f in os.listdir(input_folder) if f.endswith(('.mp4', '.avi'))]

    for video_file in tqdm(video_files, desc="Processing videos", unit="video", total=total_videos):
        video_path = os.path.join(input_folder, video_file)
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Unable to open the video: {video_path}")
            continue

        # Get the original dimensions of the video
        crop_ratio = 0.1
        WIDTH = 1280
        HEIGHT = 720
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width_prime = height
        height_prime = width
        width_2prime = width_prime
        height_2prime = (1 - crop_ratio) * height_prime
        r = height_2prime / width_2prime
        height_3prime = HEIGHT
        width_3prime = int(height_3prime / r)
        width_r = int((WIDTH - width_3prime) / 2)

        # Create the output file with the same structure as the input file
        output_path = os.path.join(output_folder, video_file)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_size = (1280, 720)
        out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar = tqdm(total=num_frames, desc=f"Processing {video_file}", unit="frame")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Crop 20% of the image from the top
            cropped_frame = frame[:, :width - int(width * crop_ratio)]

            # Rotate the image 90 degrees counterclockwise
            rotated_frame = cv2.rotate(cropped_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Resize the image with the new height while maintaining the aspect ratio
            resized_frame = cv2.resize(rotated_frame, (width_3prime, height_3prime))

            new_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
            new_frame[:, width_r:width_r + width_3prime, :] = resized_frame

            # Write the rotated frame to the output file
            out.write(new_frame)

            progress_bar.update(1)  # Update the progress bar for each frame
            # Note: You can also add a delay here to slow down the real-time display if necessary

        # Close the cap and out objects
        cap.release()
        out.release()

        progress_bar.close()  # Close the progress bar for the current video

    print("Video rotation is complete.")

if __name__ == "__main__":
    input_folder = "C:/Users/tcochou/Desktop/sandground/2023_07_17/VideosArmaine_S23/original/1"
    output_folder = "C:/Users/tcochou/Desktop/sandground/2023_07_17/VideosArmaine_S23/original/1_rotated"
    rotate_video_frames(input_folder, output_folder)
