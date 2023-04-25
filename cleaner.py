import os
from PIL import Image
import json

# This program is used to rename and clean up a dataset of PNG images and associated JSON files.
# It assumes that the JSON files are still intact and copies the dataset to a new location with the files renamed.

original_images_directory = ''
new_images_directory = ''
original_jsons_directory = ''
new_jsons_directory = ''

# Find all PNG images in the original images directory
image_files = [f for f in os.listdir(original_images_directory) if (f.endswith('.PNG'))]

# Find all JSON files in the new JSONs directory
json_files = [f for f in os.listdir(new_jsons_directory) if (f.endswith('.json'))]

# Order the images in ascending order based on the filenames, which are assumed to be four-digit integers.
image_files = sorted([int(filename[0:4]) for filename in image_files])

# Return the sorted images to their original format, which includes leading zeros and the ".PNG" file extension.
image_files = [str(filename).rjust(4, '0') + '.PNG' for filename in image_files]

# Create a new dataset by looping through each image in the image files list.
for index, image_filename in enumerate(image_files):
    # Open the original image using PIL.
    image = Image.open(original_images_directory + image_filename)

    # Save the image with a new name in the new images directory with the same extension.
    image.save(new_images_directory + str(index).rjust(4, '0') + ".PNG")

    # Close the original image.
    image.close()

    # Open the associated JSON file using the first four digits of the original image's filename.
    with open(original_jsons_directory + image_filename[0:4] + '.json', 'r') as json_file:
        # Load the JSON data.
        json_data = json.load(json_file)

    # Close the JSON file.
    json_file.close()

    # Save the JSON file with a new name in the new JSONs directory using the same index as the image.
    with open(new_jsons_directory + str(index).rjust(4, '0') + '.json', 'w') as json_file:
        # Write the JSON data.
        json.dump(json_data, json_file)

    # Close the JSON file.
    json_file.close()

# The following code runs a tally of the instances of the different classes in the dataset.
# However, the program does not save this information anywhere.
# The final_labels list includes the names of the different classes,
# and the final_counts list keeps a count of the number of instances of each class.

# final_labels = ["Stop", "Cross", "Light", "Meter", "Car", "Bike"]
# final_counts = [0, 0, 0, 0, 0, 0]

# for json_filename in json_files:
#     with open(new_jsons_directory + json_filename) as json_file:
#         # Load the JSON data.
#         json_data = json.load(json_file)

#         # Extract the class label.
#         class_label = int(json_data['cat'])

#         # Increment the count for that label in the final_counts list.
#         final_counts[class_label] += 1

#     # Close the JSON file.
#     json_file.close()

# # Print the final_labels list and the final_counts list.
# print(final_labels, "\n", final_counts)