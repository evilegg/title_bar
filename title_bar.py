#!/usr/bin/python3
"""Draw a title box on a cover image for my channel"""

import base64
from io import StringIO
import os

import click
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '0'
import fonts
import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TITLE_COLOR = (255, 244, 102)
TITLE_SHADOW = BLACK
SUBTITLE_COLOR = (240, 240, 240)
SUBTITLE_SHADOW = BLACK


def render_textbox(surface, title_font, subtitle_font, vertical_offset, title, title_font_size, subtitle, subtitle_font_size):
    # Set the fonts
    font1 = pygame.freetype.Font(title_font or fonts.MINECRAFT_BOLD, title_font_size)
    font2 = pygame.freetype.Font(subtitle_font or fonts.MINECRAFT_ITALIC, subtitle_font_size)

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

    font1.render_to(surface, (text1_x + 8, text1_y + 8), title, TITLE_SHADOW, size=title_font_size)
    font1.render_to(surface, (text1_x, text1_y), title, TITLE_COLOR, size=title_font_size)

    font2.render_to(surface, (text2_x + 8, text2_y + 8), subtitle, SUBTITLE_SHADOW, size=subtitle_font_size)
    font2.render_to(surface, (text2_x, text2_y), subtitle, SUBTITLE_COLOR, size=subtitle_font_size)


def render_gradient(surface, y_offset, width, height, start_alpha, end_alpha):
    """Behind the text is a dark radiant box."""
    delta_alpha = end_alpha - start_alpha
    for y in range(height):
        overlay = pygame.Surface((width, 1), pygame.SRCALPHA)
        overlay.set_alpha(start_alpha + (delta_alpha * y / height))
        overlay.fill(BLACK)
        surface.blit(overlay, (0, y_offset + y))
        

@click.command()
@click.option('--input-image', '-i',
              type=click.Path(exists=True),
              default="path/to/your/image.jpg",
              help='Path to the input image file.')
@click.option('--output-image', '-o',
              type=click.Path(),
              help='Path to the output image file.')
@click.option('--title', '-t',
              default='This episode',
              help='The title of this episode.')
@click.option('--subtitle', '-s',
              default='',
              help='Useful sub-title')
@click.option('--title-font',
              type=click.File('rb'),
              help='Path to an optional font file to use for the title.')
@click.option('--subtitle-font',
              type=click.File('rb'),
              help='Path to an optional font file to use for the subtitle.')
@click.option('--title-font-size',
              type=int,
              default=90,
              help='Font size for the title.')
@click.option('--subtitle_font_size',
              type=int,
              default=45,
              help='Font size for the subtitle.')
def main(input_image, output_image, title, subtitle, title_font, title_font_size, subtitle_font, subtitle_font_size):
    # Initialize Pygame
    pygame.init()

    # Set a dummy display mode to avoid "No video mode has been set" error
    dummy_size = (1, 1)
    pygame.display.set_mode(dummy_size)

    # Load the initial image
    image = pygame.image.load(input_image).convert_alpha()

    # Get image dimensions
    image_width, image_height = image.get_size()

    # Create a surface for the overlay at the bottom with varying opacity
    overlay_height = 260
    title_box_y_offset = image_height - overlay_height

    gradient_start = 100
    gradient_end = 255
    render_gradient(image, title_box_y_offset, image_width, overlay_height, gradient_start, gradient_end)

    render_textbox(image, title_font, subtitle_font, title_box_y_offset, title, title_font_size, subtitle, subtitle_font_size)

    # Save the image copy as the output image
    if not output_image:
        print(output_image)
        path_fragments = os.path.splitext(input_image)
        output_image = ''.join((path_fragments[0], '-output', path_fragments[1]))

    pygame.image.save(image, output_image)

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()

