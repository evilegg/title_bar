import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def add_text_overlay(input_image_path, output_image_path, line1, line2, font_path1, font_size1, font_path2, font_size2):
    # Initialize Pygame
    pygame.init()

    # Set a dummy display mode to avoid "No video mode has been set" error
    dummy_size = (1, 1)
    pygame.display.set_mode(dummy_size)

    # Load the initial image
    image = pygame.image.load(input_image_path).convert_alpha()

    # Set the fonts
    font1 = pygame.freetype.Font(font_path1, font_size1)
    font2 = pygame.freetype.Font(font_path2, font_size2)

    # Get image dimensions
    image_width, image_height = image.get_size()

    # Create text surfaces
    text1, rect1 = font1.render(line1, (255, 255, 255))
    text2, rect2 = font2.render(line2, (255, 255, 255))


    # Create a surface for the overlay at the bottom with varying opacity
    overlay_height = 200
    overlay_surface = pygame.Surface((image_width, overlay_height), pygame.SRCALPHA)

    # Calculate text positions
    text1_x = 0
    text1_y = image_height - overlay_height

    text2_x = 0
    text2_y = image_height - overlay_height + 80

    font1.render_to(image, (text1_x + 16, text1_y + 16), line1, BLACK, size=font_size1)
    font1.render_to(image, (text1_x, text1_y), line1, WHITE, size=font_size1)

    font2.render_to(image, (text2_x + 8, text2_y + 8), line2, BLACK, size=font_size2)
    font2.render_to(image, (text2_x, text2_y), line2, WHITE, size=font_size2)

    # Save the image copy as the output image
    pygame.image.save(image, output_image_path)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    input_image_path = "path/to/your/image.jpg"
    output_image_path = "path/to/your/output_image.jpg"
    line1 = "First line of text"
    line2 = "Second line of text"
    font_path1 = "path/to/your/font1.otf"  # Replace with the path to your first font file
    font_size1 = 90
    font_path2 = "path/to/your/font2.otf"  # Replace with the path to your second font file
    font_size2 = 48

    add_text_overlay(input_image_path, output_image_path, line1, line2, font_path1, font_size1, font_path2, font_size2)

