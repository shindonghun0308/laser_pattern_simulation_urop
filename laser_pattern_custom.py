import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

background_width = 1200
background_height = 900
vertical_translation = 0 #vertically translate your laser pattern (positive means pattern is lowered down)



######################## INITIAL SETTING ###########################
INPUT_IMAGE_PATH = 'Picture 1.png'
OUTPUT_IMAGE_PATH = INPUT_IMAGE_PATH[:-4] + '_resized.png'
TARGET_HEIGHT = 400 # change size of the laser pattern accordingly
########################################


def resize_image(input_path, output_path, target_height):
    # Open the image file
    with Image.open(input_path) as img:
        # Calculate the proportional width based on the target height
        width_percent = (target_height / float(img.size[1]))
        target_width = int((float(img.size[0]) * float(width_percent)))

        # Resize the image
        resized_img = img.resize((target_width, target_height), Image.BICUBIC)

        # Save the resized image
        resized_img.save(output_path)


resize_image(INPUT_IMAGE_PATH, OUTPUT_IMAGE_PATH, TARGET_HEIGHT)

image = cv2.imread(OUTPUT_IMAGE_PATH)

# Define the positions and sizes of the five rectangles
rectangles = [
    {"name": "1", "x": 300, "y": 300, "width": 200, "height": 100},
    {"name": "2", "x": 300, "y": 500, "width": 200, "height": 100},
    {"name": "3", "x": 500, "y": 400, "width": 200, "height": 100},
    {"name": "4", "x": 700, "y": 300, "width": 200, "height": 100},
    {"name": "5", "x": 700, "y": 500, "width": 200, "height": 100},
]

# Initialize the actuation state for all rectangles to 0
actuation_data = {rect["name"]: [] for rect in rectangles}

def get_contour_coordinates(image):
    # Ignore 2-pixel width closest to the end of the input picture
    ignore_pixels = 2
    image_height, image_width, _ = image.shape
    roi = image[ignore_pixels:image_height-ignore_pixels, ignore_pixels:image_width-ignore_pixels]

    # Diagonal resizing factor for contours

    # Convert the resized ROI to grayscale
    gray_resized_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Apply edge detection using Canny
    edges = cv2.Canny(gray_resized_roi, 50, 150)

    # Increase the thickness of the edges slightly using dilation
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract contour coordinates as a list
    contour_coordinates = []
    for contour in contours:
        for point in contour:
            x, y = point[0]
            # Adjust coordinates based on the ignored pixels and resizing factor
            x = int(x) 
            y = int(y) 
            contour_coordinates.append([x, y])

    return contour_coordinates

contour_coordinates = get_contour_coordinates(image)

canvas = np.zeros((background_height, background_width, 3), dtype=np.uint8)

centroid_x = int(np.mean(np.array(contour_coordinates)[:, 0]).round())
centroid_y = int(np.mean(np.array(contour_coordinates)[:, 1]).round())
# print("Centroid coordinates: ({}, {})".format(centroid_x, centroid_y))

contour_coordinates = [[x[0] - centroid_x, x[1] + vertical_translation + background_height //2 - centroid_y] for x in contour_coordinates]

pattern_x = 0
pattern_speed = 5
# Initialize the actuation state for all rectangles to 0
actuation_data = {rect["name"]: [] for rect in rectangles}

while pattern_x < background_width:
    # Clear the canvas on each iteration
    canvas.fill(0)
    # canvas = np.zeros((background_height, background_width), dtype=np.uint8)
    contour_coordinates = [[x[0] + pattern_speed, x[1]] for x in contour_coordinates]
    for rect in rectangles:
        rect_pts = np.array([
            [rect["x"], rect["y"]],
            [rect["x"] + rect["width"], rect["y"]],
            [rect["x"] + rect["width"], rect["y"] + rect["height"]],
            [rect["x"], rect["y"] + rect["height"]]
        ])
        in_rectangle = any(
            rect_pt[0] >= np.min(rect_pts[:, 0]) and
            rect_pt[0] <= np.max(rect_pts[:, 0]) and
            rect_pt[1] >= np.min(rect_pts[:, 1]) and
            rect_pt[1] <= np.max(rect_pts[:, 1])
            for rect_pt in contour_coordinates
        )

        actuation_data[rect["name"]].append(1 if in_rectangle else 0)
        if in_rectangle:
            shape_color = (0, 255, 0)
        else:
            shape_color = (255, 0, 0)
        cv2.fillPoly(canvas, [rect_pts], shape_color)

    cv2.drawContours(canvas, [np.array(contour_coordinates)], -1, (255, 255, 255), 2)

    # Show the canvas (you can replace this with actual robot actuation)
    cv2.imshow("Laser Pattern", canvas)
    cv2.waitKey(10)  # Adjust the delay as needed

    # Move the laser pattern to the right
    pattern_x += pattern_speed

cv2.destroyAllWindows()

time_points = list(range(len(actuation_data["1"])))

plt.figure(figsize=(12, 8))

for i, rect in enumerate(rectangles):
    plt.subplot(2, 3, i + 1)  # Adjust the layout based on the number of rectangles
    plt.plot(time_points, actuation_data[rect["name"]], label=f'Rectangle {rect["name"]} Actuated')
    plt.xlabel('Time')
    plt.ylabel('Actuated State (1/0)')
    plt.title(f'Actuation in Rectangle {rect["name"]}')

plt.tight_layout()
plt.show()

output_file_path = "actuation_data.txt"

# Write the output to a text file
with open(output_file_path, 'w') as file:
    for key, values in actuation_data.items():
        file.write(f'{key}: {values}\n')

# Confirm that the file has been written
print(f"Output has been written to {output_file_path}")