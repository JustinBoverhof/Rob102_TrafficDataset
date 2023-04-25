from PIL import Image
import xml.etree.ElementTree as ET
import json


def parse_Xml_DATA(path):
    path = path
    tree = ET.parse(path)

    root = tree.getroot()
    Class = ()
    cords = ()

    objects = root.findall("object")
    for obj in objects:
        Class += (obj.find("name").text,)
        box = obj.find("bndbox")
        cords += (int(box.find("xmin").text),)
        cords += (int(box.find("ymin").text),)
        cords += (int(box.find("xmax").text),)
        cords += (int(box.find("ymax").text),)

    return Class, cords


def parse_Json_COCO_step1(path, path_to, ids):
    c = 0
    with open(path, 'r') as file:
        data = json.load(file)
    file.close()

    print(data.keys())
    name = str(data["annotations"][0]['image_id']).rjust(12, "0")
    print(name)
    print(data["annotations"][0]['category_id'])
    print(data["annotations"][0]['bbox'])

    for i in range(len(data["annotations"])):
        Id = data["annotations"][i]['category_id']
        if (Id in ids == False):
            continue
        box = data["annotations"][i]['bbox']
        name = str(data["annotations"][i]['image_id']).rjust(12, "0")
        Dict = {
            "from": "Coco 2017",
            "img_id": name,
            "cat_id": Id,
            "bnd_box": box,
        }
        with open(path_to + str(c) + ".json", "w") as file:
            json.dump(Dict, file)
        file.close()
        c += 1


def parse_Json_data(path):
    with open(path, "r") as file:
        data = json.load(file)
    file.close()
    origin = data['img_id']
    Class = ()
    Class += (str(data["cat_id"]),)
    cords = ()
    cords += (int(data['bnd_box'][0]),)
    cords += (int(data['bnd_box'][1]),)
    cords += (cords[0]+int(data['bnd_box'][2]),)
    cords += (cords[1]+int(data['bnd_box'][3]),)

    return Class, cords, data['img_id'], origin


# Define a function to crop an image to a square based on specified coordinates
def squareImage(img_path, save_path, coords, verify=False):
    # Open the image using the Image module
    img = Image.open(img_path)
    
    # Extract the top-left and bottom-right coordinates from the 'coords' parameter
    top_left = coords[0:2]
    bottom_right = coords[2:4]
    
    # Calculate the width and height of the desired crop
    crop_width = bottom_right[0] - top_left[0]
    crop_height = bottom_right[1] - top_left[1]
    
    # Get the width and height of the original image
    img_width, img_height = img.size
    
    # Calculate the maximum possible size of the square crop
    max_crop_size = min(img_width, img_height)
    
    # Calculate the size of the crop based on the larger dimension of the image and the specified coordinates
    crop_size = max(crop_width, crop_height)

    # If the calculated crop size is greater than the maximum possible crop size, use the maximum possible size instead
    if crop_size > max_crop_size:
        crop_size = max_crop_size
    
    # Calculate the middle point of the desired crop
    crop_middle = [top_left[0] + crop_width // 2, top_left[1] + crop_height // 2] 
    
    # Calculate the new top-left corner of the crop
    new_top_left = [max(crop_middle[0] - crop_size // 2, 0), max(crop_middle[1] - crop_size // 2, 0)]
    
    # If the new crop extends beyond the right or bottom edge of the image, adjust the top-left corner accordingly
    if new_top_left[0] + crop_size > img_width:
        new_top_left[0] -= (new_top_left[0] + crop_size - img_width)
    if new_top_left[1] + crop_size > img_height:
        new_top_left[1] -= (new_top_left[1] + crop_size - img_height)

    # Crop the image to the specified size and coordinates
    img = img.crop((new_top_left[0], new_top_left[1], new_top_left[0] + crop_size, new_top_left[1] + crop_size))
    
    # If the 'verify' parameter is True, display the cropped image and prompt the user to keep or discard it
    if verify:
        img.show()
        keep_image = input("Keep Image? ")
        if keep_image == 'n':
            img.close()
            return -1
    
    # Save the cropped image to a file and close the image object
    img.save(save_path)
    img.close()
    
    # Return a success status code
    return 1