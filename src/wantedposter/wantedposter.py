import os
import uuid
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw
from unidecode import unidecode

ROOT_DIR = os.path.dirname(__file__)
BOUNTY_POSTER_EXTENSION = 'jpg'
BOUNTY_POSTER_ASSETS_PATH = os.path.join(ROOT_DIR, 'assets')
BOUNTY_POSTER_TEMPLATE_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components', 'template.png')
BOUNTY_POSTER_NO_PHOTO_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components', 'no_portrait.jpg')
BOUNTY_POSTER_PORTRAIT_BOX_START_Y = 238
BOUNTY_POSTER_PORTRAIT_BOX_H = 463
BOUNTY_POSTER_PORTRAIT_BOX_START_X = 73
BOUNTY_POSTER_PORTRAIT_BOX_W = 640
BOUNTY_POSTER_PORTRAIT_TEXTURE_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components',
                                                   'texture_portrait.jpg')
BOUNTY_POSTER_NAME_FONT_SIZE = 150
BOUNTY_POSTER_NAME_MAX_W = 595
BOUNTY_POSTER_NAME_H = 109
BOUNTY_POSTER_NAME_START_X = 95
BOUNTY_POSTER_NAME_START_Y = 802
BOUNTY_POSTER_NAME_END_Y = 911
BOUNTY_POSTER_NAME_MAX_KERN = 65
BOUNTY_POSTER_NAME_MAX_LENGTH = 16
BOUNTY_POSTER_NAME_SPACE_SUB_MIN_LENGTH = 14
BOUNTY_POSTER_NAME_SPACE_SUB_CHAR = '•'
BOUNTY_POSTER_NAME_TEXTURE_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components', 'texture_name.jpg')
BOUNTY_POSTER_NAME_FONT_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'fonts', 'PlayfairDisplay-Bold.ttf')
BOUNTY_POSTER_BELLY_FONT_SIZE = 37
BOUNTY_POSTER_BELLY_MAX_W = 522
BOUNTY_POSTER_BELLY_H = 35
BOUNTY_POSTER_BELLY_START_X = 150
BOUNTY_POSTER_BELLY_START_Y = 952
BOUNTY_POSTER_BELLY_END_Y = 987
BOUNTY_POSTER_BELLY_MAX_KERN = 30
BOUNTY_POSTER_BELLY_TEXTURE_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components', 'texture_belly.jpg')
BOUNTY_POSTER_BELLY_FONT_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'fonts', 'Lilly__.ttf')
BOUNTY_POSTER_COMPONENT_NAME = 1
BOUNTY_POSTER_COMPONENT_BELLY = 2


class WantedPoster:
    def __init__(self, portrait: str | BytesIO = None, first_name: str = '', last_name: str = '', bounty: int = 0
                 ) -> None:
        """
        Creates a Wanted Poster object
        :param portrait: The portrait image, either a path to the image or a BytesIO object
        :param first_name: The first name of the user
        :param last_name: The last name of the user
        :param bounty: The bounty of the user
        :return: None
        """

        self.portrait: str = portrait
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.bounty: int = bounty

    def generate(self, output_poster_path: str = None, portrait_vertical_align: str = 'center',
                 portrait_horizontal_align: str = 'center', should_make_portrait_transparent: bool = False,
                 portrait_transparency_value: int = 200) -> str:
        """
        Generates a wanted poster and saves it to the specified path
        :param output_poster_path: The path to the output poster. If None, a temporary file will be created
        :param portrait_vertical_align: The vertical alignment of the portrait image (top, center, bottom)
        :param portrait_horizontal_align: The horizontal alignment of the portrait image (left, center, right)
        :param should_make_portrait_transparent: Whether to make the portrait semi-transparent
        :param portrait_transparency_value: The transparency value of the portrait (0-255). Higher = less transparent
        :return: The path to the generated poster
        """

        # If output path is not specified, use a temporary file
        if output_poster_path is None:
            output_poster_path = uuid.uuid4().hex + '.jpg'

        if portrait_vertical_align not in ["top", "center", "bottom"]:
            raise ValueError("Invalid vertical_align value")

        if portrait_horizontal_align not in ["left", "center", "right"]:
            raise ValueError("Invalid horizontal_align value")

        # Set portrait image
        if self.portrait is None:
            portrait = BOUNTY_POSTER_NO_PHOTO_PATH
            portrait_vertical_align = "center"
            portrait_horizontal_align = "center"
        else:
            portrait = self.portrait

        # Open poster template
        poster_template = Image.open(BOUNTY_POSTER_TEMPLATE_PATH).convert("RGBA")

        # Create a new image with the same size as the template
        new_image = Image.new("RGB", poster_template.size)

        # Paste portrait texture into new image
        texture_portrait = Image.open(BOUNTY_POSTER_PORTRAIT_TEXTURE_PATH)
        new_image.paste(texture_portrait, (BOUNTY_POSTER_PORTRAIT_BOX_START_X, BOUNTY_POSTER_PORTRAIT_BOX_START_Y))

        # Open portrait image
        portrait = Image.open(portrait)
        # Resize portrait
        portrait = self.resize_portrait(portrait)

        # Align portrait image
        portrait_coordinate_x, portrait_coordinate_y = self.align_image(portrait, portrait_vertical_align,
                                                                        portrait_horizontal_align)

        # Paste portrait into new image
        if should_make_portrait_transparent:
            portrait.putalpha(portrait_transparency_value)
            mask = portrait
        else:
            mask = None
        new_image.paste(portrait, (portrait_coordinate_x, portrait_coordinate_y), mask)

        # Paste poster template into the new image
        new_image.paste(poster_template, (0, 0), mask=poster_template)

        # Add name component
        full_name = self.get_bounty_poster_name()
        name_component: Image = self.get_bounty_poster_component(full_name, BOUNTY_POSTER_COMPONENT_NAME)
        new_image.paste(name_component, (0, BOUNTY_POSTER_NAME_START_Y), name_component)

        # Add belly component
        belly = '{0:,}'.format(self.bounty) + '-'
        belly_component: Image = self.get_bounty_poster_component(belly, BOUNTY_POSTER_COMPONENT_BELLY)
        new_image.paste(belly_component, (0, BOUNTY_POSTER_BELLY_START_Y), belly_component)

        # Save image
        save_path = output_poster_path
        new_image.save(save_path)

        return save_path

    @staticmethod
    def align_image(portrait: Image, vertical_align: str, horizontal_align: str) -> tuple[int, int]:
        """
        Calculate the portrait's coordinate based on the desired alignment
        :param portrait: Image to align
        :param vertical_align: The vertical alignment of the portrait image (top, center, bottom)
        :param horizontal_align: The horizontal alignment of the portrait image (left, center, right)
        :return: The portrait's start coordinate
        """

        # Get portrait size
        portrait_width, portrait_height = portrait.size

        # Calculate the portrait's x coordinate based on the desired alignment
        if horizontal_align == "left":
            portrait_x = BOUNTY_POSTER_PORTRAIT_BOX_START_X
        elif horizontal_align == "center":
            portrait_x = int((BOUNTY_POSTER_PORTRAIT_BOX_W - portrait_width) / 2) + BOUNTY_POSTER_PORTRAIT_BOX_START_X
        else:  # right
            portrait_x = BOUNTY_POSTER_PORTRAIT_BOX_W - portrait_width + BOUNTY_POSTER_PORTRAIT_BOX_START_X

        # Adjust the portrait's y coordinate based on the desired alignment
        if vertical_align == "top":
            portrait_y = BOUNTY_POSTER_PORTRAIT_BOX_START_Y
        elif vertical_align == "center":
            portrait_y = int((BOUNTY_POSTER_PORTRAIT_BOX_H - portrait_height) / 2) + BOUNTY_POSTER_PORTRAIT_BOX_START_Y
        else:  # bottom
            portrait_y = BOUNTY_POSTER_PORTRAIT_BOX_H - portrait_height + BOUNTY_POSTER_PORTRAIT_BOX_START_Y

        return portrait_x, portrait_y

    @staticmethod
    def resize_portrait(portrait: Image) -> Image:
        """
        Resizes a portrait image to fit the wanted poster
        :param portrait: The portrait image
        :return: The resized portrait image
        """

        # Get portrait size
        portrait_width, portrait_height = portrait.size

        # Calculate wanted poster image box aspect ratio
        image_box_aspect_ratio = BOUNTY_POSTER_PORTRAIT_BOX_W / BOUNTY_POSTER_PORTRAIT_BOX_H

        # Calculate portrait aspect ratio
        portrait_aspect_ratio = portrait_width / portrait_height

        if portrait_aspect_ratio < image_box_aspect_ratio:
            # Portrait is wider than the wanted poster image box
            # Resize portrait to fit the width of the wanted poster image box
            new_width = BOUNTY_POSTER_PORTRAIT_BOX_W
            new_height = int(new_width / portrait_aspect_ratio)
        elif portrait_aspect_ratio > image_box_aspect_ratio:
            # Portrait is taller than the wanted poster image box
            # Resize portrait to fit the height of the wanted poster image box
            new_height = BOUNTY_POSTER_PORTRAIT_BOX_H
            new_width = int(new_height * portrait_aspect_ratio)
        else:
            # Portrait has the same aspect ratio as the wanted poster image box
            # Resize portrait to fit the wanted poster image box
            new_width = BOUNTY_POSTER_PORTRAIT_BOX_W
            new_height = BOUNTY_POSTER_PORTRAIT_BOX_H

        # Resize portrait
        portrait = portrait.resize((new_width, new_height), Image.ANTIALIAS)

        return portrait

    def get_bounty_poster_name(self) -> str:
        """
        Gets the bounty poster's name of a user
        """

        # Get full name
        full_name = self.get_full_name()

        # Add space sub if too long or D. in name
        if len(full_name) >= BOUNTY_POSTER_NAME_SPACE_SUB_MIN_LENGTH or 'D.' in full_name:
            full_name = full_name.replace(' ', BOUNTY_POSTER_NAME_SPACE_SUB_CHAR)

        # Replace 'D.' with 'D'
        full_name = full_name.replace('D.', 'D')

        return full_name

    @staticmethod
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

    def get_full_name(self) -> str:
        """
        Preprocesses the name to be up to a maximum length
        :return: The full name
        """

        # Normalize to ascii
        first_name = unidecode(self.first_name).upper().strip()
        last_name = unidecode(self.last_name).upper().strip()

        full_name = f'{last_name} {first_name}'

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
