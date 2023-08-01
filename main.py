"""
Process Videos Script

This script is designed to process videos from a folder, calculate the Mean Squared Error between frames, and save the frames if the error exceeds a threshold. The script supports various sorting modes for the saved frames.

Functions:
    main():
        Main function to process videos based on command-line arguments.

Usage:
    python main.py -o original_folder_path -d destination_folder_path -t threshold -s sort_mode -r number_of_frame_per_folder -n number_of_folder -c

Arguments:
    -o, --original-folder-path:
        Path of the folder containing the videos.

    -d, --destination-folder-path:
        Output folder path to save frames.

    -t, --threshold:
        Threshold for Mean Squared Error (default: -1).

    -D, --duration:
        Real duration of the videos in seconds (default: -1).

    -s, --sort-mode:
        Sorting mode(s) for the images.

    -r, --number-of-frame-per-folder:
        Number of frames per folder (default: 4).

    -n, --number-of-folder:
        Number of subfolders (default: 0).

    -c, --clear:
        Clear the original folder after processing (default: False).
"""

import argparse
import os
import shutil
from utils import (
    create_folders, create_images_sorted_folders,
    get_all_images, process_videos_in_folder, sort_images_rec
)


def main():
    """
    Main function to process videos based on command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Open videos from a folder, calculate the Mean Squared Error between frames, and save the frame if the error exceeds a threshold.")
    parser.add_argument("-o", "--original-folder-path", help="Path of the folder containing the videos.")
    parser.add_argument("-d", "--destination-folder-path", default=None, help="Output folder path to save frames.")
    parser.add_argument("-t", "--threshold", type=float, default=-1., help="Threshold for Mean Squared Error.")
    parser.add_argument("-D", "--duration", type=float, default=-1., help="Real duration of the videos in seconds.")
    parser.add_argument("-s", "--sort-mode", nargs='+', help="Sorting mode for the images.")
    parser.add_argument("-r", "--number-of-frame-per-folder", type=int, default=4, help="Number of frame per folder.")
    parser.add_argument("-n", "--number-of-folder", type=int, default=0, help="Number of subfolders.")
    parser.add_argument("-c", "--clear", default=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    # Check if the original-folder-path option is empty
    if not args.original_folder_path:
        print("Error: The '-o' option is required. Please provide the path of the folder containing the videos.")
        return  # Exit the program

    # Check if the sort-mode option is empty
    if not args.sort_mode:
        print("Error: The '-s' option is required. Please provide one or more sorting modes.")
        return  # Exit the program

    clear = args.clear

    original_folder_path = args.original_folder_path
    if args.destination_folder_path is not None:
        destination_folder_path_frames = os.path.join(args.destination_folder_path, 'frames')
    else:
        destination_folder_path_frames = os.path.join(os.path.dirname(original_folder_path), 'frames')
    print(destination_folder_path_frames)
    threshold = args.threshold
    duration = args.duration

    process_videos_in_folder(original_folder_path, destination_folder_path_frames, threshold, duration)

    original_folder_path = destination_folder_path_frames
    if args.destination_folder_path is not None:
        destination_folder_path_sort = os.path.join(args.destination_folder_path, 'sort_frames')
    else:
        destination_folder_path_sort = os.path.join(os.path.dirname(original_folder_path), 'sort_frames')
    args_mode = args.sort_mode
    args_mode.append('')
    sort_mode = []
    sort_mode_specs = {}
    i = 0
    while i < len(args_mode) - 1:
        if args_mode[i + 1].isdigit():
            sort_mode.append(args_mode[i])
            sort_mode_specs[args_mode[i]] = int(args_mode[i + 1])
            i += 2
        else:
            sort_mode.append(args_mode[i])
            i += 1
    if not sort_mode_specs:
        sort_mode_specs = None

    image_list = get_all_images(original_folder_path, sort_mode_specs)

    if sort_mode is not None:
        images = sort_images_rec(image_list, sort_mode)
        if images is not None:

            if destination_folder_path_sort:
                create_images_sorted_folders(images, destination_folder_path_sort)
                if clear:
                    shutil.rmtree(original_folder_path)
                print("Images sorted successfully.")
            else:
                print("Test mode: Images were not moved.")

    original_folder_path = destination_folder_path_sort
    if args.destination_folder_path is not None:
        destination_folder_path_equalize = os.path.join(args.destination_folder_path, 'equalize_frames')
    else:
        destination_folder_path_equalize = os.path.join(os.path.dirname(original_folder_path), 'equalize_frames')

    images_per_folder = args.number_of_frame_per_folder
    number_folder = args.number_of_folder

    create_folders(original_folder_path, destination_folder_path_equalize, images_per_folder, number_folder)
    if clear:
        shutil.rmtree(original_folder_path)


if __name__ == "__main__":
    main()
