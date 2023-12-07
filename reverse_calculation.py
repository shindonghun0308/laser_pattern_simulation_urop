import numpy as np
import cv2
import matplotlib.pyplot as plt

# Constants
background_width = 1200
background_height = 900
pattern_color = (255, 255, 255)  # White color
pattern_speed = 5

# Create an empty canvas
canvas = np.zeros((background_height, background_width, 3), dtype=np.uint8)
loaded_canvas = np.zeros((background_height, background_width, 3), dtype=np.uint8)

# Read actuation data from a text file
input_file_path = "actuation_data.txt"
actuation_data = {}

with open(input_file_path, 'r') as file:
    lines = file.readlines()

for line in lines:
    key, values_str = line.strip().split(':')
    values = [int(val) for val in values_str.strip().strip('[]').split(',')]
    actuation_data[key.strip()] = values

# Define the positions and sizes of the five rectangles
rectangles = [
    {"name": "1", "x": 300, "y": 300, "width": 200, "height": 100},
    {"name": "2", "x": 300, "y": 500, "width": 200, "height": 100},
    {"name": "3", "x": 500, "y": 400, "width": 200, "height": 100},
    {"name": "4", "x": 700, "y": 300, "width": 200, "height": 100},
    {"name": "5", "x": 700, "y": 500, "width": 200, "height": 100},
]

# Function to draw a line between two points
def draw_line(canvas, start_point, end_point, color):
    cv2.line(canvas, start_point, end_point, color, thickness=2)

# Iterate through rectangles and generate laser pattern
for rect_name, actuations in actuation_data.items():
    # Get the rectangle based on the name
    rectangle = next(rect for rect in rectangles if rect["name"] == rect_name)
    
    # Iterate through actuations to generate line segments
    for i in range(len(actuations) - 1):
        start_point = (rectangle["x"] + i * 10, rectangle["y"])
        end_point = (rectangle["x"] + (i + 1) * 10, rectangle["y"])
        # Check if laser is on
        if actuations[i] == 1:
            draw_line(canvas, start_point, end_point, pattern_color)

# Display the generated laser pattern
plt.imshow(canvas)
plt.show()

# Main loop for moving the loaded laser pattern across the robot's surface
pattern_x = -background_width

while pattern_x < background_width:
    # Clear the loaded canvas on each iteration
    loaded_canvas.fill(0)

    # Iterate through rectangles and generate loaded laser pattern
    for rect_name, actuations in actuation_data.items():
        # Get the rectangle based on the name
        rectangle = next(rect for rect in rectangles if rect["name"] == rect_name)

        # Iterate through actuations to generate line segments
        for i in range(len(actuations) - 1):
            start_point = (rectangle["x"] + pattern_x + i * 5, rectangle["y"])
            end_point = (rectangle["x"] + pattern_x + (i + 1) * 5, rectangle["y"])

            # Check if laser is on
            if actuations[i] == 1:
                draw_line(loaded_canvas, start_point, end_point, pattern_color)

    # Display the loaded pattern
    cv2.imshow("Loaded Laser Pattern", loaded_canvas)
    cv2.waitKey(10)  # Adjust the delay as needed

    # Move the loaded pattern to the right
    pattern_x += pattern_speed

# Close the OpenCV window
cv2.destroyAllWindows()
