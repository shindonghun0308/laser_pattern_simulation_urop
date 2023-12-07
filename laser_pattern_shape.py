import numpy as np
import cv2
import matplotlib.pyplot as plt

# Constants
CHOSEN_SHAPE = 'triangle'
background_width = 1200
background_height = 900

# Create canvases
canvas = np.zeros((background_height, background_width, 3), dtype=np.uint8)
contour_canvas = np.zeros((background_height, background_width), dtype=np.uint8)

# Laser pattern properties
pattern_color = (255, 255, 255)  # White color
pattern_size = 100  # Size of the laser pattern
pattern_speed = 5  # Speed of the laser pattern's movement

# Rectangle positions and sizes
rectangles = [
    {"name": "1", "x": 300, "y": 300, "width": 200, "height": 100},
    {"name": "2", "x": 300, "y": 500, "width": 200, "height": 100},
    {"name": "3", "x": 500, "y": 400, "width": 200, "height": 100},
    {"name": "4", "x": 700, "y": 300, "width": 200, "height": 100},
    {"name": "5", "x": 700, "y": 500, "width": 200, "height": 100},
]

# Actuation state initialization
rectangle_actuated = {rect["name"]: [] for rect in rectangles}

# Function to draw a circle
def draw_circle(canvas, x, y, size, color):
    cv2.circle(canvas, (x, y), size, color, thickness=2)

def get_circle_contour(x, y, size):
    contour_canvas.fill(0)
    cv2.circle(contour_canvas, (x, y), size, color=255, thickness=2)
    contours, _ = cv2.findContours(contour_canvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours[0].reshape(-1, 2).tolist()

# Function to draw a triangle
def draw_triangle(canvas, x, y, size, color):
    triangle_pts = np.array([
        [x - 4 * size, y - size],
        [x - 4 * size, y + size],
        [x + 4 * size, y],
    ])
    cv2.polylines(canvas, [triangle_pts], isClosed=True, color=color, thickness=2)

def get_triangle_contour(x, y, size):
    triangle_pts = np.array([
        [x - 4 * size, y - size],
        [x - 4 * size, y + size],
        [x + 4 * size, y],
    ])
    contour_canvas.fill(0)
    cv2.polylines(contour_canvas, [triangle_pts], isClosed=True, color=255, thickness=2)
    contours, _ = cv2.findContours(contour_canvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours[0].reshape(-1, 2).tolist()

# Main loop for moving the laser pattern across the robot's surface
pattern_x = 0

while pattern_x < background_width:
    canvas.fill(0)  # Clear the canvas on each iteration
    pattern_center_x = pattern_x
    pattern_center_y = background_height // 2

    # Get the contour based on the chosen shape
    if CHOSEN_SHAPE == 'circle':
        chosen_contour = get_circle_contour(pattern_center_x, pattern_center_y, pattern_size)
    elif CHOSEN_SHAPE == 'triangle':
        chosen_contour = get_triangle_contour(pattern_center_x, pattern_center_y, pattern_size)

    # Check intersection with each rectangle
    for rect in rectangles:
        rect_pts = np.array([
            [rect["x"], rect["y"]],
            [rect["x"] + rect["width"], rect["y"]],
            [rect["x"] + rect["width"], rect["y"] + rect["height"]],
            [rect["x"], rect["y"] + rect["height"]]
        ])

        # Check if the pattern outline intersects with the rectangle
        in_rectangle = any(
            rect_pt[0] >= np.min(rect_pts[:, 0]) and
            rect_pt[0] <= np.max(rect_pts[:, 0]) and
            rect_pt[1] >= np.min(rect_pts[:, 1]) and
            rect_pt[1] <= np.max(rect_pts[:, 1])
            for rect_pt in chosen_contour
        )

        rectangle_actuated[rect["name"]].append(1 if in_rectangle else 0)
        shape_color = (0, 255, 0) if in_rectangle else (255, 0, 0)

        # Draw the rectangle
        cv2.fillPoly(canvas, [rect_pts], shape_color)

    # Draw the chosen shape
    if CHOSEN_SHAPE == "circle":
        draw_circle(canvas, pattern_center_x, pattern_center_y, pattern_size, pattern_color)
    elif CHOSEN_SHAPE == "triangle":
        draw_triangle(canvas, pattern_center_x, pattern_center_y, pattern_size, pattern_color)

    # Show the canvas
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
