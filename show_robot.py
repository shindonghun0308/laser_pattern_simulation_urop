import numpy as np
import cv2
import matplotlib.pyplot as plt

CHOSEN_SHAPE = 'triangle'
# Define the dimensions of the background
background_width = 1200
background_height = 900

# Create an empty canvas (black background)
canvas = np.zeros((background_height, background_width, 3), dtype=np.uint8)
contour_canvas = np.zeros((background_height, background_width), dtype=np.uint8)

# Define the properties of the laser pattern (size, color, speed)
pattern_color = (255, 255, 255)  # White color
pattern_size = 200  # Size of the laser pattern
pattern_speed = 5  # Speed of the laser pattern's movement


# Define the positions and sizes of the five rectangles
rectangles = [
    {"name": "1", "x": 300, "y": 300, "width": 200, "height": 100},
    {"name": "2", "x": 300, "y": 500, "width": 200, "height": 100},
    {"name": "3", "x": 500, "y": 400, "width": 200, "height": 100},
    {"name": "4", "x": 700, "y": 300, "width": 200, "height": 100},
    {"name": "5", "x": 700, "y": 500, "width": 200, "height": 100},
]

# Initialize the actuation state for all rectangles to 0
rectangle_actuated = {rect["name"]: [] for rect in rectangles}

# Function to draw a circle
def draw_circle(canvas, x, y, size, color):
    cv2.circle(canvas, (x, y), size, color, thickness=2)

def get_circle_contour(x, y, size):
    contour_canvas.fill(0)  # Clear the contour canvas
    cv2.circle(contour_canvas, (x, y), size, color=255, thickness=2)
    contours, _ = cv2.findContours(contour_canvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_coordinates = []
    for contour in contours:
        contour_coordinates.extend(contour.reshape(-1, 2).tolist())
    return contour_coordinates

#-------------------------------------------------------------------------_#
def draw_triangle(canvas, x, y, size, color):
    triangle_pts = np.array([
        [x, y - size],  # Top vertex
        [x - size, y + size],  # Bottom-left vertex
        [x + size, y + size],  # Bottom-right vertex
    ])
    cv2.polylines(canvas, [triangle_pts], isClosed=True, color=color, thickness=2)

def get_triangle_contour(x, y, size):
    triangle_pts = np.array([
        [x, y - size],  # Top vertex
        [x - size, y + size],  # Bottom-left vertex
        [x + size, y + size],  # Bottom-right vertex
    ])
    contour_canvas.fill(0)
    cv2.polylines(contour_canvas, [triangle_pts], isClosed=True, color=255, thickness=2)
    contours, _ = cv2.findContours(contour_canvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_coordinates = []
    for contour in contours:
        contour_coordinates.extend(contour.reshape(-1, 2).tolist())
    return contour_coordinates



# Main loop for moving the laser pattern across the robot's surface
pattern_x = 0

while pattern_x < background_width:
    # Clear the canvas on each iteration
    canvas.fill(0)

    # Calculate the axis of the laser pattern moving (vertical center)
    pattern_center_x = pattern_x
    pattern_center_y = background_height // 2

    # Check if the laser pattern intersects with the area of each rectangle
    for rect in rectangles:
        # Create the vertices of the rectangle as a polygon
        rect_pts = np.array([
            [rect["x"], rect["y"]],
            [rect["x"] + rect["width"], rect["y"]],
            [rect["x"] + rect["width"], rect["y"] + rect["height"]],
            [rect["x"], rect["y"] + rect["height"]]
        ])

        # if CHOSEN_SHAPE == 'circle':
        #     chosen_contour = get_circle_contour(pattern_center_x, pattern_center_y, pattern_size)
        # if CHOSEN_SHAPE == 'triangle':
        #     chosen_contour = get_triangle_contour(pattern_center_x, pattern_center_y, pattern_size)
            

        # Check if the pattern outline intersects with the rectangle
        in_rectangle = 0 

        rectangle_actuated[rect["name"]].append(1 if in_rectangle else 0)
        if in_rectangle:
            shape_color = (0, 255, 0)
        else:
            shape_color = (255, 0, 0)

        # Draw the rectangle
        cv2.fillPoly(canvas, [rect_pts], shape_color)

    # Show the canvas (you can replace this with actual robot actuation)
    cv2.imshow("Laser Pattern", canvas)
    cv2.waitKey(10)  # Adjust the delay as needed

    # Move the laser pattern to the right
    pattern_x += pattern_speed

# Close the OpenCV window
cv2.destroyAllWindows()

# Plot the actuated state over time for each rectangle
time_points = list(range(len(rectangle_actuated["1"])))

plt.figure(figsize=(12, 8))

for i, rect in enumerate(rectangles):
    plt.subplot(2, 3, i + 1)  # Adjust the layout based on the number of rectangles
    plt.plot(time_points, rectangle_actuated[rect["name"]], label=f'Rectangle {rect["name"]} Actuated')
    plt.xlabel('Time')
    plt.ylabel('Actuated State (1/0)')
    plt.title(f'Actuation in Rectangle {rect["name"]}')

plt.tight_layout()
plt.show()

print(rectangle_actuated)
