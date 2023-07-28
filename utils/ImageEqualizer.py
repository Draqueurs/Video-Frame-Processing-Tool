import os
import shutil
import argparse
from tqdm import tqdm

def count_images_in_subfolders(directory):
    """
    Count the number of images in each subfolder of the given directory.

    Parameters:
        directory (str): The path to the directory to be scanned.

    Returns:
        dict: A dictionary containing the number of images per subfolder.
    """
    image_counts = {}
    for root, dirs, files in os.walk(directory):
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        current_folder = root
        image_counts[current_folder] = len(image_files)
    return image_counts

def extract_images_from_subfolders(main_folder, output_folder, num_images):
    """
    Extract a specified number of images from each subfolder of the main folder
    and move them to the output folder.

    Parameters:
        main_folder (str): The path to the main folder containing subfolders.
        output_folder (str): The path to the output folder.
        num_images (int): The number of images to extract from each subfolder.
    """
    if not os.path.exists(main_folder):
        print("The main folder does not exist.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = []
    for item in os.listdir(main_folder):
        item_path = os.path.join(main_folder, item)
        if os.path.isdir(item_path):
            extract_images_from_subfolders(item_path, output_folder, num_images)
        else:
            if item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                images.append(item_path)
                if len(images) == num_images:
                    for image in images:
                        shutil.move(image, output_folder)
                    break
    if 0 < len(images) < num_images:
        for image in images:
            shutil.copy(image, output_folder)

def create_folders(main_folder, output_folder, num_images, num_folders):
    """
    Create subfolders and distribute images from the main folder into these subfolders.

    Parameters:
        main_folder (str): The path to the main folder containing images.
        output_folder (str): The path to the output folder for the subfolders.
        num_images (int): The number of images to place in each subfolder.
        num_folders (int): The number of subfolders to create.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images_per_subfolder = count_images_in_subfolders(main_folder)
    nombre_elements_sup_0 = 0

    for value in images_per_subfolder.values():
        if value > 0:
            nombre_elements_sup_0 += 1
    max_num_images = nombre_elements_sup_0 * num_images

    if num_folders <= 0:
        num_folders = int(max(images_per_subfolder.values()) / num_images)

    for i in tqdm(range(num_folders), desc="Creating subfolders", unit="folder"):
        new_output_path = os.path.join(output_folder, os.path.basename(output_folder)+f'_{i+1}')
        if not os.path.exists(new_output_path):
            os.makedirs(new_output_path)
        extract_images_from_subfolders(main_folder, new_output_path, num_images)
        if count_images_in_subfolders(new_output_path)[new_output_path] == max_num_images:
            shutil.move(new_output_path, new_output_path+'_full')

def main():
    """
    Main function to retrieve images from a folder and its subfolders based on the provided arguments.
    """
    parser = argparse.ArgumentParser(description="Retrieve all images from a folder and its subfolders.")
    parser.add_argument("-o", "--original-folder-path", help="Absolute path of the folder containing the images.")
    parser.add_argument("-d", "--destination-folder-path", default='', help="Absolute path of the folder for the sorted images.")
    parser.add_argument("-r", "--number-of-frame-per-folder", type=int, default=4, help="Number of frames per folder.")
    parser.add_argument("-n", "--number-of-folder", type=int, default=0, help="Number of subfolders.")
    args = parser.parse_args()

    if not args.original_folder_path:
        print("Error: The '-o' option is required. Please provide the path of the folder containing the videos.")
        return

    original_folder_path = args.original_folder_path
    destination_folder_path = args.destination_folder_path
    images_per_folder = args.number_of_frame_per_folder
    number_folder = args.number_of_folder

    create_folders(original_folder_path, destination_folder_path, images_per_folder, number_folder)

if __name__ == "__main__":
    main()
