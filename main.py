from PIL import Image, ImageFont, ImageDraw
from unidecode import unidecode
from constants import *
import uuid


def generate(portrait_path: str = None, first_name: str = '', last_name: str = '', bounty: int = 0,
             output_poster_path: str = None, vertical_align: str = "center", horizontal_align: str = "center") -> str:
    """
    Generates a wanted poster
    :param portrait_path: The path to the portrait image
    :param first_name: The first name of the user
    :param last_name: The last name of the user
    :param bounty: The bounty of the user
    :param output_poster_path: The path to the output poster. If None, a temporary file will be created
    :param vertical_align: The vertical alignment of the portrait image (top, center, bottom)
    :param horizontal_align: The horizontal alignment of the portrait image (left, center, right)
    :return: The path to the generated wanted poster
    """

    # Open poster template
    poster_template = Image.open(BOUNTY_POSTER_TEMPLATE_PATH).convert("RGBA")
    # Get poster template size
    poster_template_width, poster_template_height = poster_template.size

    # Create a new image with the same size as the template
    new_image = Image.new("RGB", poster_template.size)

    # Get portrait image
    if portrait_path is None:
        portrait_path = BOUNTY_POSTER_NO_PHOTO_PATH

    # Open portrait image
    portrait = Image.open(portrait_path)
    # Get portrait size
    portrait_width, portrait_height = portrait.size

    # Get where profile image should be placed
    if portrait_path == BOUNTY_POSTER_NO_PHOTO_PATH:
        # Excess photo parts should be evenly cropped from top and bottom
        delta = portrait_height - BOUNTY_POSTER_IMAGE_BOX_H
        portrait_y = BOUNTY_POSTER_IMAGE_BOX_START_Y - int(delta / 2)
    else:
        # Excess photo parts should be cropped from bottom
        portrait_y = BOUNTY_POSTER_IMAGE_BOX_START_Y

    # Calculate the portrait's x coordinate based on the desired alignment
    if horizontal_align == "left":
        portrait_x = 0
    elif horizontal_align == "center":
        portrait_x = int((poster_template_width - portrait_width) / 2)
    else:  # right
        portrait_x = poster_template_width - portrait_width

    # Adjust the portrait's y coordinate based on the desired alignment
    if vertical_align == "top":
        portrait_y = 0
    elif vertical_align == "center":
        portrait_y = int((poster_template_height - portrait_height) / 2)
    else:  # bottom
        portrait_y = poster_template_height - portrait_height

    # Paste portrait into the new image
    new_image.paste(portrait, (portrait_x, portrait_y))

    # Paste poster template into the new image
    new_image.paste(poster_template, (0, 0), mask=poster_template)

    # Add name component
    full_name = get_bounty_poster_name(first_name, last_name)
    name_component: Image = get_bounty_poster_component(full_name, BOUNTY_POSTER_COMPONENT_NAME)
    new_image.paste(name_component, (0, BOUNTY_POSTER_NAME_START_Y), name_component)

    # Add belly component
    belly = '{0:,}'.format(bounty) + '-'

    belly_component: Image = get_bounty_poster_component(belly, BOUNTY_POSTER_COMPONENT_BELLY)
    new_image.paste(belly_component, (0, BOUNTY_POSTER_BELLY_START_Y), belly_component)

    # Save image

    # If output path is not specified, create a temporary file in the current directory
    if output_poster_path is None:
        output_poster_path = uuid.uuid4().hex + '.jpg'

    save_path = output_poster_path
    new_image.save(save_path)



    return save_path


def get_bounty_poster_name(first_name: str, last_name: str) -> str:
    """
    Gets the bounty poster's name of a user
    :param first_name: The user first_name to get the poster's name of
    :param last_name: The user last_name to get the poster's name of
    :return: The name to display on the bounty poster
    """

    # Normalize to ascii
    first_name = unidecode(first_name).upper().strip()
    last_name = unidecode(last_name).upper().strip()

    # Get full name
    full_name = get_full_name(first_name, last_name)

    # Add space sub if too long or D. in name
    if len(full_name) >= BOUNTY_POSTER_NAME_SPACE_SUB_MIN_LENGTH or 'D.' in full_name:
        full_name = full_name.replace(' ', BOUNTY_POSTER_NAME_SPACE_SUB_CHAR)

    # Replace 'D.' with 'D'
    full_name = full_name.replace('D.', 'D')

    return full_name


def get_bounty_poster_component(text: str, c_type: int) -> Image:
    """
    Get a component of the poster
    :param text: Text to be written
    :param c_type: Type of component (1 - name, 2 - belly)
    :return: Component image
    """

    if c_type == BOUNTY_POSTER_COMPONENT_NAME:  # Name component
        texture_path = BOUNTY_POSTER_NAME_TEXTURE_PATH
        font_path = BOUNTY_POSTER_NAME_FONT_PATH
        font_size = BOUNTY_POSTER_NAME_FONT_SIZE
        max_w = BOUNTY_POSTER_NAME_MAX_W
        max_kern = BOUNTY_POSTER_NAME_MAX_KERN
        x_pos = BOUNTY_POSTER_NAME_START_X
        box_h = BOUNTY_POSTER_NAME_H

    elif c_type == BOUNTY_POSTER_COMPONENT_BELLY:  # Belly component
        texture_path = BOUNTY_POSTER_BELLY_TEXTURE_PATH
        font_path = BOUNTY_POSTER_BELLY_FONT_PATH
        font_size = BOUNTY_POSTER_BELLY_FONT_SIZE
        max_w = BOUNTY_POSTER_BELLY_MAX_W
        max_kern = BOUNTY_POSTER_BELLY_MAX_KERN
        x_pos = BOUNTY_POSTER_BELLY_START_X
        box_h = BOUNTY_POSTER_BELLY_H
    else:
        raise Exception('Invalid component type')

    texture_background: Image = Image.open(texture_path)
    texture_background_w, texture_background_h = texture_background.size
    font: ImageFont = ImageFont.truetype(font_path, font_size)

    # Create new alpha channel - solid black
    # Alpha with more height to account for characters that are cut off under
    alpha: Image = Image.new('L', (texture_background_w, texture_background_h))
    draw: ImageDraw = ImageDraw.Draw(alpha)

    # Get text size
    should_scale: bool = False
    text_w, text_h = draw.textsize(text, font=font)

    if text_w < max_w:
        width_difference = max_w - text_w
        try:
            kern = int(width_difference / (len(text) - 1))
        except ZeroDivisionError:
            kern = int(width_difference / (len(text)))

        # Avoid too much kerning
        if kern > max_kern:
            kern = max_kern
            x_pos += int((max_w / 2) - ((text_w + (kern * (len(text) - 1))) / 2))

        # Draw char by char considering kerning
        for char in text:
            draw.text((x_pos, box_h), char, font=font, fill='white', anchor='ls')
            char_width, letter_height = draw.textsize(char, font=font)
            x_pos += char_width + kern
    else:
        # If width is too big, increase alpha channel width
        if text_w > max_w:
            # Calculate new width
            new_w = int((text_w * texture_background_w) / max_w)
            alpha = Image.new('L', (new_w, texture_background_h))
            draw = ImageDraw.Draw(alpha)
            should_scale = True

        # Draw text on baseline in the image
        draw.text((int(alpha.size[0] / 2), box_h), text, font=font, fill='white', anchor='ms')

        # Scale texture image if needed
        if should_scale:
            alpha = alpha.resize((texture_background_w, texture_background_h))

    # Use text cutout as alpha channel for texture image
    texture_background.putalpha(alpha)

    return texture_background


def get_full_name(first_name: str, last_name: str) -> str:
    """
    Preprocesses the name to be up to a maximum length
    :param first_name: The first name
    :param last_name: The last name
    :return: The full name
    """

    full_name = first_name + " " + last_name

    if len(full_name) <= BOUNTY_POSTER_NAME_MAX_LENGTH:
        return full_name

    # Use first name only
    full_name = first_name
    if len(full_name) <= BOUNTY_POSTER_NAME_MAX_LENGTH:
        return full_name

    # Still too long, split by 'space' and concatenate till it's not too long
    parts = full_name.split(' ')
    result = ''
    for part in parts:
        if len(result + ' ' + part) > BOUNTY_POSTER_NAME_MAX_LENGTH:
            return full_name
        result += ' ' + part

    # Use result or only the first part
    full_name = parts[0] if len(result) == 0 else result
    if len(full_name) <= BOUNTY_POSTER_NAME_MAX_LENGTH:
        return full_name

    # Still too long, remove extra characters
    full_name = full_name[:(BOUNTY_POSTER_NAME_MAX_LENGTH - 2)] + '.'
    return full_name
