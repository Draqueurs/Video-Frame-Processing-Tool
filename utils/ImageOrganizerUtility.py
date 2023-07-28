import os
import shutil
import argparse
from collections import defaultdict
from tqdm import tqdm

def is_image(file_path):
    """
    Check if a file is an image based on its extension.

    Parameters:
        file_path (str): The path of the file to check.

    Returns:
        bool: True if the file is an image, False otherwise.
    """
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in image_extensions

def is_targeted(file_path, targets):
    """
    Check if the file matches the given targets.

    Parameters:
        file_path (str): The path of the file to check.
        targets (dict): A dictionary containing specific criteria to match against the file.

    Returns:
        bool: True if the file matches all the specified targets, False otherwise.
    """
    # Iterate through the target keys and their corresponding values
    for key, value in targets.items():
        # Extract the relevant part of the file name based on the key (e.g., 'box', 'cam', etc.)
        if key == 'box':
            target_value = int(os.path.basename(file_path).split('_')[0])
        elif key == 'cam':
            target_value = int(os.path.basename(file_path).split('_')[1])
        elif key == 'year':
            target_value = int(os.path.basename(file_path).split('_')[2].split('-')[0])
        elif key == 'month':
            target_value = int(os.path.basename(file_path).split('_')[2].split('-')[1])
        elif key == 'day':
            target_value = int(os.path.basename(file_path).split('_')[2].split('-')[2])
        elif key == 'hour':
            target_value = int(os.path.basename(file_path).split('_')[3].split('-')[0])
        elif key == 'minute':
            target_value = int(os.path.basename(file_path).split('_')[3].split('-')[1])
        elif key == 'second':
            target_value = int(os.path.basename(file_path).split('_')[3].split('-')[2].split('.')[0])

        # Check if the extracted target value matches the provided target value
        if value != target_value:
            return False

    # If all target checks pass, return True indicating the file matches all specified targets
    return True
    
def get_all_images(directory, targets=None):
    """
    Retrieve a list of all image files (png, jpg, jpeg, gif, bmp, tiff) in a given directory and its subdirectories.

    Parameters:
        directory (str): The absolute path of the root directory to search for images.

    Returns:
        list: A list of absolute file paths of all image files found in the directory and its subdirectories.
    """
    image_files = []
    for root, _, files in tqdm(os.walk(directory), desc="Searching for images", unit=" files"):
        if targets is None:
            for file in files:
                file_path = os.path.join(root, file)
                if is_image(file_path):
                    image_files.append(file_path)
        else:
            for file in files:
                file_path = os.path.join(root, file)
                if is_image(file_path):
                    if is_targeted(file_path, targets):
                        image_files.append(file_path)
    return image_files

def sort_images_by_key(images, key_func):
    """
    Sort a list of image files into groups based on a given key function.

    Parameters:
        images (list): A list of absolute file paths of image files to be sorted.
        key_func (function): A function that takes an image file path as input and returns the grouping key.

    Returns:
        dict: A dictionary where keys are the grouping keys returned by the key_func,
              and values are lists of image file paths belonging to each group.
    """
    output = defaultdict(list)
    for image in images:
        idx = key_func(image)
        output[idx].append(image)
    return output

def sort_images_rec(images, modes):
    """
    Recursively sort a list of image files based on multiple sorting modes.

    Parameters:
        images (list): A list of absolute file paths of image files to be sorted.
        modes (list): A list of sorting modes to be applied in order.

    Returns:
        dict: A nested dictionary where keys are the grouping keys for each mode,
              and values are either another nested dictionary (for deeper levels of sorting)
              or lists of image file paths, representing the sorted groups at each level.
    """
    if not modes:
        return images

    # Dictionary mapping sorting modes to their corresponding functions
    sorting_functions = {
        'box': lambda image: 'box_' + os.path.basename(image).split('_')[0],
        'cam': lambda image: 'cam_' + os.path.basename(image).split('_')[1],
        'year': lambda image: 'year_' + os.path.basename(image).split('_')[2].split('-')[0],
        'month': lambda image: 'month_' + os.path.basename(image).split('_')[2].split('-')[1],
        'day': lambda image: 'day_' + os.path.basename(image).split('_')[2].split('-')[2],
        'hour': lambda image: 'hour_' + os.path.basename(image).split('_')[3].split('-')[0],
        'minute': lambda image: 'minute_' + os.path.basename(image).split('_')[3].split('-')[1],
        'second': lambda image: 'second_' + os.path.basename(image).split('_')[3].split('-')[2].split('.')[0],
    }

    # Get the sorting function for the current mode
    sorting_function = sorting_functions.get(modes[0])
    if sorting_function is None:
        print(f"The sorting mode '{modes[0]}' is not valid.")
        return None

    # Sort images based on the current mode
    sorted_images = sort_images_by_key(images, sorting_function)

    if len(modes) > 1:
        # If there are more sorting modes, apply recursion to sort the groups at deeper levels
        for key, value in sorted_images.items():
            sorted_images[key] = sort_images_rec(value, modes[1:])

    return sorted_images

def create_images_sorted_folders(images_sorted, prev_path=''):
    """
    Create sorted folders and copy images into them based on the provided sorted image dictionary.

    Parameters:
        images_sorted (dict): A dictionary representing the sorted groups of image file paths.
        prev_path (str): The path of the parent directory for the current level of sorting.

    Returns:
        None
    """
    total_images = sum(len(value) if isinstance(value, list) else 1 for value in images_sorted.values())

    with tqdm(total=total_images, desc="Copying and sorting images", unit=" images") as pbar:
        for key, value in images_sorted.items():
            path = os.path.join(prev_path, key)
            os.makedirs(path, exist_ok=True)
            if isinstance(value, list):
                for image in value:
                    shutil.copy2(image, path)
                    pbar.update(1)
            else:
                create_images_sorted_folders(value, path)

def main():
    parser = argparse.ArgumentParser(description="Retrieve all images from a folder and its subfolders.")
    parser.add_argument("-o", "--original-folder-path", help="Absolute path of the folder containing the images.")
    parser.add_argument("-d", "--destination-folder-path", default='', help="Absolute path of the folder for the sorted images.")
    parser.add_argument("-s", "--sort-mode", nargs='+', help="Sorting mode for the images.")
    args = parser.parse_args()

    # Check if the original-folder-path option is empty
    if not args.original_folder_path:
        print("Error: The '-o' option is required. Please provide the path of the folder containing the videos.")
        return  # Exit the program

    # Check if the sort-mode option is empty
    if not args.sort_mode:
        print("Error: The '-s' option is required. Please provide one or more sorting modes.")
        return  # Exit the program

    original_folder_path = args.original_folder_path
    if args.destination_folder_path is not None:
        destination_folder_path = os.path.join(args.destination_folder_path, 'sort_frames')
    else:
        destination_folder_path = os.path.join(os.path.dirname(original_folder_path), 'sort_frames')
    args_mode = args.sort_mode
    args_mode.append('')
    sort_mode = []
    sort_mode_specs = {}
    i = 0
    while i < len(args_mode)-1:
        if args_mode[i+1].isdigit():
            sort_mode.append(args_mode[i])
            sort_mode_specs[args_mode[i]] = int(args_mode[i+1])
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

            if destination_folder_path:
                create_images_sorted_folders(images, destination_folder_path)
                print("Images sorted successfully.")
            else:
                print("Test mode: Images were not moved.")

if __name__ == "__main__":
    main()