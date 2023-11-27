#!/usr/bin/python3
"""Draw a title box on a cover image for my channel"""

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '0'
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TITLE_COLOR = (255, 244, 102)
TITLE_SHADOW = BLACK
SUBTITLE_COLOR = (240, 240, 240)
SUBTITLE_SHADOW = BLACK


def render_textbox(surface, font_path1, font_path2, vertical_offset, title, subtitle):
    # Set the fonts
    font1 = pygame.freetype.Font(font_path1, font_size1)
    font2 = pygame.freetype.Font(font_path2, font_size2)

    # Create text surfaces
    text1, rect1 = font1.render(title, TITLE_COLOR)
    text2, rect2 = font2.render(subtitle, SUBTITLE_COLOR)

    # Calculate text positions
    leading_x = 100
    line_spacing = 91

    text1_x = leading_x
    text1_y = vertical_offset + line_spacing * 0.75

    text2_x = leading_x
    text2_y = text1_y + line_spacing

    font1.render_to(surface, (text1_x + 8, text1_y + 8), title, TITLE_SHADOW, size=font_size1)
    font1.render_to(surface, (text1_x, text1_y), title, TITLE_COLOR, size=font_size1)

    font2.render_to(surface, (text2_x + 8, text2_y + 8), subtitle, SUBTITLE_SHADOW, size=font_size2)
    font2.render_to(surface, (text2_x, text2_y), subtitle, SUBTITLE_COLOR, size=font_size2)


def render_gradient(surface, y_offset, width, height, start_alpha, end_alpha):
    delta_alpha = end_alpha - start_alpha
    for y in range(height):
        overlay = pygame.Surface((width, 1), pygame.SRCALPHA)
        overlay.set_alpha(start_alpha + (delta_alpha * y / height))
        overlay.fill(BLACK)
        surface.blit(overlay, (0, y_offset + y))


def add_text_overlay(input_image_path, output_image_path, line1, line2, font_path1, font_size1, font_path2, font_size2):
    # Initialize Pygame
    pygame.init()

    # Set a dummy display mode to avoid "No video mode has been set" error
    dummy_size = (1, 1)
    pygame.display.set_mode(dummy_size)

    # Load the initial image
    image = pygame.image.load(input_image_path).convert_alpha()

    # Get image dimensions
    image_width, image_height = image.get_size()

    # Create a surface for the overlay at the bottom with varying opacity
    overlay_height = 260
    title_box_y_offset = image_height - overlay_height

    gradient_start = 100
    gradient_end = 255
    render_gradient(image, title_box_y_offset, image_width, overlay_height, gradient_start, gradient_end)

    render_textbox(image, font_path1, font_path2, title_box_y_offset, line1, line2)

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
    font_size1 = 91
    font_path2 = "path/to/your/font2.otf"  # Replace with the path to your second font file
    font_size2 = 45

    add_text_overlay(input_image_path, output_image_path, line1, line2, font_path1, font_size1, font_path2, font_size2)

