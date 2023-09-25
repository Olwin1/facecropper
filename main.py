import os

from PIL import Image
import face_recognition

def get_first_level_subdirectories(path):
    try:
        # Get a list of all items (files and directories) in the given path
        items = os.listdir(path)
        
        # Filter the items to keep only directories
        subdirectories = [item for item in items if os.path.isdir(os.path.join(path, item))]
        
        return subdirectories
    except OSError as e:
        print(f"Error: {e}")
        return []


def get_all_files_in_directory(directory_path):
    try:
        # Initialize an empty list to store the file names and their creation times
        file_list = []

        # Walk through the directory and its subdirectories
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Get the creation time of each file and store it in a tuple with the file path
                file_creation_time = os.path.getctime(file_path)
                file_list.append((file, file_creation_time))

        # Sort the file list by creation time
        file_list.sort(key=lambda x: x[1])

        # Extract the sorted file paths from the list
        sorted_file_paths = [file_info[0] for file_info in file_list]

        return sorted_file_paths

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


unknown_images = []
def crop_to_aspect_ratio(image_path, output_path, target_ratio):
    try:
        # Open the image using Pillow
        image = Image.open(image_path)
        loaded_face = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(loaded_face)
        if len(face_locations) == 0:
            unknown_images.append(image_path)
            return
        top, right, bottom, left = face_locations[0]
        center_x = (left + right) / 2
        center_y = (top + bottom) / 2
        print("Center of the face detected at:", (center_x, center_y))



        # Get the current width and height of the image
        width, height = image.size

        # Calculate the target width and height for the specified aspect ratio
        target_width = int(min(width, height * target_ratio))
        target_height = int(min(height, width / target_ratio))

        # Calculate the coordinates for the cropping box centered around (center_x, center_y)
        left = int(center_x - target_width / 2)
        top = int(center_y - target_height / 2)
        right = int(center_x + target_width / 2)
        bottom = int(center_y + target_height / 2)

        # Ensure that the cropping box stays within the bounds of the image
        left = max(0, left)
        top = max(0, top)
        right = min(width, right)
        bottom = min(height, bottom)

        # Crop the image using the calculated coordinates
        cropped_image = image.crop((left, top, right, bottom))

        # Save the cropped image
        cropped_image.save(output_path)
        print(f"Image cropped and saved to {output_path}")

    except Exception as e:
        print(f"Error: {e} \n On file: {image_path}")

# Specify the input image path, output image path, and target aspect ratio

target_aspect_ratio = 3 / 4  # You can change this to your desired aspect ratio


isExist = os.path.exists("./cropped")
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs("./cropped")


# Specify the directory path for which you want to get first-level subdirectories
directory_path = "./"

# Call the function to get the first-level subdirectories
subdirectories = get_first_level_subdirectories(directory_path)

# Print the list of first-level subdirectories
print("First-level subdirectories:")
for subdirectory in subdirectories:
    print(subdirectory)
# Call the function to get all files in the directory

for subdirectory in subdirectories:
    if subdirectory != 'cropped':
        isExist = os.path.exists(f"./cropped/{subdirectory}")
        if not isExist:

            # Create a new directory because it does not exist
            os.makedirs(f"./cropped/{subdirectory}")

        files = get_all_files_in_directory(subdirectory)

        # Print the list of file paths
        print(f"All files in the directory {subdirectory}:")
        for file in files:
            # Call the function to crop the image
            crop_to_aspect_ratio(f"./{subdirectory}/{file}", f"./cropped/{subdirectory}/{file}", target_aspect_ratio)
if len(unknown_images) > 0:
    print("Images that could not be auto-cropped:")
    for i in unknown_images:
        print(i)
    print("Cropped images can be found in cropped folder")