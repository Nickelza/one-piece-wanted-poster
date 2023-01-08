from PIL import Image, ImageFont, ImageDraw
from unidecode import unidecode
from constants import *


def main(first_name: str, last_name: str, photo_path: str, bounty: int) -> str:
    """
    Gets the bounty poster of a user
    :param update: Telegram update
    :param user: The user to get the poster of
    :return: The poster of the bounty
    """

    # Open poster template
    poster_template = Image.open(BOUNTY_POSTER_TEMPLATE_PATH).convert("RGBA")
    # Get poster template size
    poster_template_width, poster_template_height = poster_template.size

    # Create a new image with the same size as the template
    new_image = Image.new("RGB", poster_template.size)

    # Get profile photo of user
    if photo_path is None:
        photo_path = BOUNTY_POSTER_NO_PHOTO_PATH

    # Add profile photo
    photo = Image.open(photo_path)
    # Get profile photo size
    photo_width, photo_height = photo.size

    # Get where profile image should be placed
    if photo_path == BOUNTY_POSTER_NO_PHOTO_PATH:
        # Excess photo parts should be evenly cropped from top and bottom
        delta = photo_height - BOUNTY_POSTER_IMAGE_BOX_H
        photo_y = BOUNTY_POSTER_IMAGE_BOX_START_Y - int(delta / 2)
    else:
        # Excess photo parts should be cropped from bottom
        photo_y = BOUNTY_POSTER_IMAGE_BOX_START_Y

    # Profile photo should be placed in the center of the poster template
    photo_x = int((poster_template_width - photo_width) / 2)
    # Paste profile image into the new image
    new_image.paste(photo, (photo_x, photo_y))

    # Paste poster template into the new image
    new_image.paste(poster_template, (0, 0), mask=poster_template)

    # Add name component
    full_name = get_bounty_poster_name(user)
    name_component: Image = get_bounty_poster_component(full_name, BOUNTY_POSTER_COMPONENT_NAME)
    new_image.paste(name_component, (0, BOUNTY_POSTER_NAME_START_Y), name_component)

    # Add belly component
    belly = user.get_bounty_formatted() + '-'
    belly_component: Image = get_bounty_poster_component(belly, BOUNTY_POSTER_COMPONENT_BELLY)
    new_image.paste(belly_component, (0, BOUNTY_POSTER_BELLY_START_Y), belly_component)

    # Save image
    save_path = generate_temp_file_path(BOUNTY_POSTER_EXTENSION)
    new_image.save(save_path)

    return save_path


def get_bounty_poster_name(user: User) -> str:
    """
    Gets the bounty poster's name of a user
    :param user: The user to get the poster's name of
    :return: The name to display on the bounty poster
    """

    # Set values
    first_name = user.tg_first_name if user.tg_first_name is not None else ''
    last_name = user.tg_last_name if user.tg_last_name is not None else ''

    # Normalize to ascii
    first_name = unidecode(first_name).upper().strip()
    last_name = unidecode(last_name).upper().strip()

    # Get full name
    full_name = (first_name + ' ' + last_name).strip()

    while True:  # Should run only once
        if len(full_name) <= BOUNTY_POSTER_NAME_MAX_LENGTH:
            break

        # Use first name only
        full_name = first_name
        if len(full_name) <= BOUNTY_POSTER_NAME_MAX_LENGTH:
            break

        # Still too long, split by 'space' and concatenate till it's not too long
        parts = full_name.split(' ')
        result = ''
        for part in parts:
            if len(result + ' ' + part) > BOUNTY_POSTER_NAME_MAX_LENGTH:
                break
            result += ' ' + part

        # Use result or only the first part
        full_name = parts[0] if len(result) == 0 else result
        if len(full_name) <= BOUNTY_POSTER_NAME_MAX_LENGTH:
            break

        # Still too long, remove extra characters
        full_name = full_name[:(BOUNTY_POSTER_NAME_MAX_LENGTH - 2)] + '.'
        break

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

