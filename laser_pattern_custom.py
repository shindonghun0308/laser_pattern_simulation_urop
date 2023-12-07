import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Constants
background_width = 1200
background_height = 900
vertical_translation = 0  # vertically translate your laser pattern (positive means pattern is lowered down)

# Initial settings
INPUT_IMAGE_PATH = 'Picture 1.png'
OUTPUT_IMAGE_PATH = INPUT_IMAGE_PATH[:-4] + '_resized.png'
TARGET_HEIGHT = 400  # change size of the laser pattern accordingly

# Function to resize the image
def resize_image(input_path, output_path, target_height):
    with Image.open(input_path) as img:
        width_percent = (target_height / float(img.size[1]))
        target_width = int((float(img.size[0]) * float(width_percent)))
        resized_img = img.resize((target_width, target_height), Image.BICUBIC)
        resized_img.save(output_path)

# Resize the image
resize_image(INPUT_IMAGE_PATH, OUTPUT_IMAGE_PATH, TARGET_HEIGHT)

# Load resized image
image = cv2.imread(OUTPUT_IMAGE_PATH)

# Rectangle positions and sizes
rectangles = [
    {"name": "1", "x": 300, "y": 300, "width": 200, "height": 100},
    {"name": "2", "x": 300, "y": 500, "width": 200, "height": 100},
    {"name": "3", "x": 500, "y": 400, "width": 200, "height": 100},
    {"name": "4", "x": 700, "y": 300, "width": 200, "height": 100},
    {"name": "5", "x": 700, "y": 500, "width": 200, "height": 100},
]

# Actuation state initialization
actuation_data = {rect["name"]: [] for rect in rectangles}

# Function to get contour coordinates
def get_contour_coordinates(image):
    ignore_pixels = 2
    image_height, image_width, _ = image.shape
    roi = image[ignore_pixels:image_height-ignore_pixels, ignore_pixels:image_width-ignore_pixels]
    gray_resized_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_resized_roi, 50, 150)
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_coordinates = [[int(x), int(y)] for contour in contours for x, y in contour[:, 0]]
    return contour_coordinates

# Get contour coordinates
contour_coordinates = get_contour_coordinates(image)

# Canvas initialization
canvas = np.zeros((background_height, background_width, 3), dtype=np.uint8)

# Centroid calculation
centroid_x = int(np.mean(np.array(contour_coordinates)[:, 0]).round())
centroid_y = int(np.mean(np.array(contour_coordinates)[:, 1]).round())

# Adjust contour coordinates
contour_coordinates = [[x[0] - centroid_x, x[1] + vertical_translation + background_height // 2 - centroid_y] for x in contour_coordinates]

# Laser pattern initialization
pattern_x = 0
pattern_speed = 5

# Actuation state initialization
actuation_data = {rect["name"]: [] for rect in rectangles}

# Main loop for laser pattern movement
while pattern_x < background_width:
    canvas.fill(0)
    contour_coordinates = [[x[0] + pattern_speed, x[1]] for x in contour_coordinates]

    # Drawing rectangles and contours on the canvas
    for rect in rectangles:
        rect_pts = np.array([
            [rect["x"], rect["y"]],
            [rect["x"] + rect["width"], rect["y"]],
            [rect["x"] + rect["width"], rect["y"] + rect["height"]],
            [rect["x"], rect["y"] + rect["height"]]
        ])
        in_rectangle = any(
            np.min(rect_pts[:, 0]) <= rect_pt[0] <= np.max(rect_pts[:, 0]) and
            np.min(rect_pts[:, 1]) <= rect_pt[1] <= np.max(rect_pts[:, 1])
            for rect_pt in contour_coordinates
        )

        actuation_data[rect["name"]].append(1 if in_rectangle else 0)
        shape_color = (0, 255, 0) if in_rectangle else (255, 0, 0)
        cv2.fillPoly(canvas, [rect_pts], shape_color)

    cv2.drawContours(canvas, [np.array(contour_coordinates)], -1, (255, 255, 255), 2)

    # Show the canvas
    cv2.imshow("Laser Pattern", canvas)
    cv2.waitKey(10)

    # Move the laser pattern to the right
    pattern_x += pattern_speed

# Close all windows
cv2.destroyAllWindows()

# Plot actuation data
time_points = list(range(len(actuation_data["1"])))
plt.figure(figsize=(12, 8))

for i, rect in enumerate(rectangles):
    plt.subplot(2, 3, i + 1)
    plt.plot(time_points, actuation_data[rect["name"]], label=f'Rectangle {rect["name"]} Actuated')
    plt.xlabel('Time')
    plt.ylabel('Actuated State (1/0)')
    plt.title(f'Actuation in Rectangle {rect["name"]}')

plt.tight_layout()
plt.show()

# Write actuation data to a text file
output_file_path = "actuation_data.txt"
with open(output_file_path, 'w') as file:
    for key, values in actuation_data.items():
        file.write(f'{key}: {values}\n')

# Confirm that the file has been written
print(f"Output has been written to {output_file_path}")
