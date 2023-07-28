# Video Frame Processing Tool

This is a Python script that processes video files by calculating the Mean Squared Error (MSE) between consecutive frames and saving frames that exceed a specified threshold. Additionally, the script provides functionality for sorting and organizing the processed frames based on various sorting modes.

## Requirements

- Python 3.x
- OpenCV (cv2) library
- NumPy library
- tqdm library

You can install the required libraries using pip:
'''
pip install opencv-python numpy tqdm
'''

## Usage

'''
python script_name.py -o original_folder_path -d destination_folder_path -t threshold -s sort_mode -r number_of_frame_per_folder -n number_of_folder -c
'''

- -o, --original-folder-path: Path of the folder containing the videos.
- -d, --destination-folder-path: Output folder path to save frames (optional).
- -t, --threshold: Threshold for Mean Squared Error (default: -1).
- -s, --sort-mode: Sorting mode(s) for the images (e.g., 'box', 'cam', 'year', 'month', 'day', 'hour', 'minute', 'second').
- -r, --number-of-frame-per-folder: Number of frames per folder (default: 4).
- -n, --number-of-folder: Number of folders (default: 0).
- -c, --clear: Clear the original folder after processing (default: False).

## Description

### calculate_mse(frame1, frame2)
Calculate the Mean Squared Error (MSE) between two grayscale images.

### preprocess_image(frame)
Preprocess an image by converting it to grayscale, cropping, and binarizing it.

### process_video(video_path, output_folder, threshold)
Process a video by calculating the Mean Squared Error between frames and saving frames that exceed the specified threshold.

### process_videos_in_folder(folder_path, output_folder, threshold)
Process all videos in a folder using the 'process_video' function.

### is_image(file_path)
Check if a file is an image based on its extension.

### is_targeted(file_path, targets)
Check if the file matches the given targets (used for sorting).

### get_all_images(directory, targets=None)
Retrieve a list of all image files (png, jpg, jpeg, gif, bmp, tiff) in a given directory and its subdirectories.

### sort_images_by_key(images, key_func)
Sort a list of image files into groups based on a given key function (used for sorting).

### sort_images_rec(images, modes)
Recursively sort a list of image files based on multiple sorting modes.

### create_images_sorted_folders(images_sorted, prev_path='')
Create sorted folders and copy images into them based on the provided sorted image dictionary.

### count_images_in_subfolders(directory)
Count the number of images in each subfolder of the given directory.

### extract_images_from_subfolders(main_folder, output_folder, num_images)
Extract a specified number of images from each subfolder of the main folder and move them to the output folder.

### create_folders(main_folder, output_folder, num_images, num_folders)
Create subfolders and distribute images from the main folder into these subfolders.

### main()
Main function to process videos based on command-line arguments. Processes videos in the 'original_folder_path', sorts the frames based on the provided sorting mode(s), and saves the sorted frames in the 'destination_folder_path'. Optionally, it can clear the 'original_folder_path' after processing.

Note: If no 'destination_folder_path' is provided, the script will create subfolders 'frames', 'sort_frames', and 'equalize_frames' in the same directory as the 'original_folder_path' and store the frames accordingly.
