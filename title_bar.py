#!/usr/bin/env python3
"""Add a consistent title bar to a thumbnail.
"""
import pygame
import os

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

    # Create text surfaces
    text1, rect1 = font1.render(line1, (255, 255, 255))
    text2, rect2 = font2.render(line2, (255, 255, 255))

    # Get image dimensions
    image_width, image_height = image.get_size()

    # Calculate text positions
    text1_x = (image_width - rect1.width) // 2
    text1_y = image_height - 60

    text2_x = (image_width - rect2.width) // 2
    text2_y = image_height - 30

    # Create a surface for the overlay at the bottom with varying opacity
    overlay_height = 260
    overlay_surface = pygame.Surface((image_width, overlay_height), pygame.SRCALPHA)

    for alpha in range(128, 256, 2):  # Opacity from 50% to 100% (128 to 255)
        overlay_surface.set_alpha(alpha)
        overlay_surface.fill((0, 0, 0, alpha))

        # Create a copy of the initial image to overlay on
        image_copy = image.copy()

        # Blit the overlay onto the image copy
        image_copy.blit(overlay_surface, (0, image_height - overlay_height))

        # Blit the original image onto the image copy
        image_copy.blit(image, (0, 0))

        # Blit the original first line and the second line onto the image copy
        image_copy.blit(text1, (text1_x, text1_y))
        image_copy.blit(text2, (text2_x, text2_y))

        # Save the image copy as the output image
        pygame.image.save(image_copy, output_image_path)

        # Delay to show the image for a short duration (adjust as needed)
        pygame.time.delay(30)  # 30 milliseconds

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    input_image_path = "path/to/your/image.jpg"
    output_image_path = "path/to/your/output_image.jpg"
    line1 = "First line of text"
    line2 = "Second line of text"
    font_path1 = "path/to/your/font1.otf"  # Replace with the path to your first font file
    font_size1 = 36
    font_path2 = "path/to/your/font2.otf"  # Replace with the path to your second font file
    font_size2 = 24

    add_text_overlay(input_image_path, output_image_path, line1, line2, font_path1, font_size1, font_path2, font_size2)


