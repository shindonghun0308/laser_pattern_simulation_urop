from PIL import Image

# Constants
INPUT_IMAGE_PATH = 'Testing.png'
OUTPUT_IMAGE_PATH = f"{INPUT_IMAGE_PATH[:-4]}_resized.png"
TARGET_HEIGHT = 1500

def resize_image(input_path, output_path, target_height):
    # Open the image file
    with Image.open(input_path) as img:
        # Calculate the proportional width based on the target height
        width_percent = target_height / float(img.size[1])
        target_width = int(float(img.size[0]) * width_percent)

        # Resize the image
        resized_img = img.resize((target_width, target_height), Image.BICUBIC)

        # Save the resized image
        resized_img.save(output_path)

# Perform image resizing
resize_image(INPUT_IMAGE_PATH, OUTPUT_IMAGE_PATH, TARGET_HEIGHT)
