from PIL import Image, ImageDraw
import math

def draw_hexagon(draw, center, size, color, fill=None):
    """
    Draws a hexagon on an ImageDraw object.

    :param draw: The ImageDraw object to draw on
    :param center: The (x, y) center coordinates of the hexagon
    :param size: The distance from the center to each vertex (hexagon size)
    :param color: The color of the hexagon's outline
    :param fill: The fill color of the hexagon (default is None)
    """
    x, y = center
    angle_deg = 60  # Each interior angle of a hexagon
    points = [
        (
            x + size * math.cos(math.radians(angle_deg * i)),
            y + size * math.sin(math.radians(angle_deg * i))
        ) for i in range(6)
    ]
    draw.polygon(points, outline=color, fill=fill)

def draw_hex_grid(image_path, hex_size, grid_color=(0, 0, 0), fill_color=None):
    """
    Draws a grid of adjacent hexagons directly over an existing image (such as a map).

    :param image_path: Path to the image file to draw the grid on
    :param hex_size: The size of the hexagons
    :param grid_color: The color of the hexagon outlines
    :param fill_color: The fill color of the hexagons (default is None)
    :return: An Image object with the hexagonal grid
    """
    # Load the existing image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    width, height = img.size  # Get the size of the loaded image

    # Calculate the horizontal and vertical spacing between hexagon centers
    hex_height = math.sqrt(3) * hex_size  # Height of a hexagon
    hex_width = 2 * hex_size  # Width of a hexagon
    vert_dist = hex_height * 0.75  # Vertical distance between rows (75% overlap)
    horiz_dist = hex_width  # Horizontal distance between hexagon centers

    # Start drawing hexagons at the top-left corner of the image and work down
    for row in range(0, height, int(vert_dist)):
        for col in range(0, width, int(horiz_dist)):
            # Offset every other row by half a hexagon's width
            offset_x = (hex_width / 2) if (row // int(vert_dist)) % 2 == 1 else 0
            center_x = col + offset_x
            center_y = row
            if center_x + hex_size < width and center_y + hex_size < height:
                draw_hexagon(draw, (center_x, center_y), hex_size, grid_color, fill_color)

    return img

# Usage Example
image_path = './images/world_map.jpg'
hex_size = 30
cluster_image = draw_hex_grid(image_path, hex_size)
cluster_image.show()  # Display the image
cluster_image.save("hex_grid_with_map_fixed.png")  # Save the image
