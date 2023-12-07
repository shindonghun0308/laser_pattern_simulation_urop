# Laser Pattern Simulation for UROP

## Overview

This project is part of the Undergraduate Research Opportunities Program (UROP) at NUS, focusing on developing an automated system for light-driven soft robots using liquid crystal elastomers materials. The primary goal is to simulate light pattern actuations on the robot, incorporating fixed shapes like circles and triangles, as well as custom shapes defined through connected lines of vertices or other customized forms.

## Modules

### laser_pattern_shape.py

This module simulates light pattern actuations for circle and triangle shapes. To use:

- For a circle, set `CHOSEN_SHAPE = 'circle'` and adjust `pattern_size` for the radius.
- For a triangle, set `CHOSEN_SHAPE = 'triangle'` and define vertex positions within the `get_contour_triangle` and `draw_triangle` functions, adjusting the `pattern_size`.
- Set `pattern_speed` to control the speed of the pattern crossing the robot.
- Run the code to visualize the simulation and actuation plot.
- Actuation data is saved to `circle_actuation_data.txt` and `triangle_actuation_data.txt` for each shape.

### laser_pattern_custom.py

This module simulates custom-shaped laser patterns. To use:

- Draw the initial shape using tools like PowerPoint with a distinct colored background.
- Set the path to this picture in the `INPUT_IMAGE_PATH` constant variable.
- Adjust the resizing factor with `TARGET_HEIGHT` for the initial shape.
- Run the code to visualize the simulation and actuation plot.
- The resized shape is saved as a PNG file.

### Reverse_calculation.py

This module assists in reverse calculation, recreating light patterns from the `actuation_data.txt` file. To use:

- Set the path to the actuation data file in the `input_file_path` variable.
- Manually edit the `actuation_data.txt` file if needed, created by running `laser_pattern_shape.py` or `laser_pattern_custom.py`.

## Dependencies

- OpenCV for image processing and simulation
- NumPy for numerical operations.
- Matplotlib for plotting.
- PIL (Python Imaging Library) for image resizing tasks.
