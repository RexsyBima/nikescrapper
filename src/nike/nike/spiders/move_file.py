import os
import shutil

def move_file_to_output_folder(file_name):
    # Get the current working directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the source and destination file paths
    source_file_path = os.path.join(current_dir, file_name)
    destination_folder_path = os.path.join(current_dir, "../../../../output")

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder_path, exist_ok=True)

    # Move the file to the destination folder
    destination_file_path = os.path.join(destination_folder_path, file_name)
    shutil.move(source_file_path, destination_file_path)

if __name__ == "__main__":
    file_name = "data.csv"
    move_file_to_output_folder(file_name)