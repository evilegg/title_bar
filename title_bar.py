#!/usr/bin/env python3
"""Draw a title box on a cover image for episodes in my YT streams.

For now we assume a 1920x1080 image to use as the cover.
We want to add a simple overlay to give it a little more professional a look.

Not trying to spend too much time on it, though as I'm not looking for high
production values.
"""

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
    font1 = pygame.freetype.Font(title_font, title_font_size)
    font2 = pygame.freetype.Font(subtitle_font, subtitle_font_size)

    # Create text surfaces
    text1, rect1 = font1.render(title, TITLE_COLOR)
    text2, rect2 = font2.render(subtitle, SUBTITLE_COLOR)

    # Calculate text positions
    leading_x = title_font_size
    line_spacing = title_font_size

    text1_y = vertical_offset + line_spacing * 0.75
    text2_y = text1_y + line_spacing

    font1.render_to(surface, (leading_x + 8, text1_y + 8), title, TITLE_SHADOW, size=title_font_size)
    font1.render_to(surface, (leading_x, text1_y), title, TITLE_COLOR, size=title_font_size)

    font2.render_to(surface, (leading_x + 8, text2_y + 8), subtitle, SUBTITLE_SHADOW, size=subtitle_font_size)
    font2.render_to(surface, (leading_x, text2_y), subtitle, SUBTITLE_COLOR, size=subtitle_font_size)


def render_gradient(surface, y_offset, width, height, start_alpha, end_alpha):
    """Behind the text is a dark radiant box."""
    delta_alpha = end_alpha - start_alpha
    for y in range(height):
        overlay = pygame.Surface((width, 1), pygame.SRCALPHA)
        overlay.set_alpha(start_alpha + (delta_alpha * y / height))
        overlay.fill(BLACK)
        surface.blit(overlay, (0, y_offset + y))


@click.command()
@click.argument('input_image', type=click.Path(exists=True))
@click.option('--title',
              help='The title and subtitle in one command line option, separate with "|"')
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
def main(input_image, title, title_font, title_font_size, subtitle_font, subtitle_font_size):

    output_ext = os.path.splitext(input_image)[-1]
    output_fname = f'{title}{output_ext.lower()}'

    subtitle = ''
    if '|' in title:
        title, subtitle = title.split(' | ')

    # Argument validation
    title_font = title_font or fonts.MINECRAFT_BOLD
    subtitle_font = subtitle_font or fonts.MINECRAFT_ITALIC

    # Initialize pygame and set a dummy display mode to avoid "No video mode has been set" error
    pygame.init()
    dummy_size = (1, 1)
    pygame.display.set_mode(dummy_size)

    # Load the initial image and get its dimensions
    image = pygame.image.load(input_image).convert_alpha()
    image_width, image_height = image.get_size()

    # Create a surface for the overlay at the bottom with varying opacity
    overlay_height = 260
    title_box_y_offset = image_height - overlay_height

    gradient_start = 100
    gradient_end = 255
    render_gradient(image, title_box_y_offset, image_width, overlay_height, gradient_start, gradient_end)

    render_textbox(image, title_font, subtitle_font, title_box_y_offset, title, title_font_size, subtitle, subtitle_font_size)

    # Save the image copy as the output image
    pygame.image.save(image, output_fname)

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()

