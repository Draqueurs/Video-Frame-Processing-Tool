# Video Frame Processing Tool

This script is designed to process videos from a folder, calculate the Mean Squared Error between frames, and save the frames if the error exceeds a threshold. The script supports various sorting modes for the saved frames.

## Functions:

- `main()`: Main function to process videos based on command-line arguments.

## Usage:

```bash
python main.py -o original_folder_path -d destination_folder_path -t threshold -s sort_mode -r number_of_frame_per_folder -n number_of_folder -c
```

## Arguments:

- `-o, --original-folder-path`: Path of the folder containing the videos.
- `-d, --destination-folder-path`: Output folder path to save frames.
- `-t, --threshold`: Threshold for Mean Squared Error (default: -1).
- `-D, --duration`: Real duration of the videos in seconds (default: -1).
- `-s, --sort-mode`: Sorting mode(s) for the images.
- `-r, --number-of-frame-per-folder`: Number of frames per folder (default: 4).
- `-n, --number-of-folder`: Number of subfolders (default: 0).
- `-c, --clear`: Clear the original folder after processing (default: False).

## How to use:

1) Ensure that your videos are named in the required format:
   `{id_box}_{id_cam}_{YYYY}-{MM}-{DD}_{hh}-{mm}-{ss}.avi`
3) Open a terminal or command prompt.
4) Change the current working directory to the location of the script.
5) Use the command-line arguments to specify the input and output options.

## Examples:

- Process videos from the "input_videos" folder, calculate MSE, save frames to "output_frames" folder, and sort frames by "mode1" and "mode2":

```bash
python main.py -o input_videos -d output_frames -t 0.5 -s mode1 mode2
```

- Process videos from the "input_videos" folder, calculate MSE, save frames to "output_frames" folder, sort frames by "mode1", and create 5 frames per subfolder:

```bash
python main.py -o input_videos -d output_frames -t 0.5 -s mode1 -r 5 -n 5
```

- Process videos from the "input_videos" folder, calculate MSE, save frames to "output_frames" folder, sort frames by "mode1", create 10 frames per subfolder, and clear the original folder after processing:

```bash
python main.py -o input_videos -d output_frames -t 0.5 -s mode1 -r 10 -n 5 -c
```

- Process videos from the "input_videos" folder, calculate MSE, save frames to "output_frames" folder, sort frames by "mode1" with value 4 and "mode2", create 10 frames per subfolder, and clear the original folder after processing:

```bash
python main.py -o input_videos -d output_frames -t 0.5 -s mode1 4 mode2 -r 10 -n 5 -c
```

Please note that the script requires the utils module, so make sure it is available in the same directory as the script or in your Python environment.
