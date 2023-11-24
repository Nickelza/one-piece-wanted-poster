import os
import uuid
from enum import Enum
from io import BytesIO
from typing import Union, Tuple

from PIL import Image, ImageFont, ImageDraw
from unidecode import unidecode

ROOT_DIR = os.path.dirname(__file__)
BOUNTY_POSTER_EXTENSION = 'jpg'
BOUNTY_POSTER_ASSETS_PATH = os.path.join(ROOT_DIR, 'assets')
BOUNTY_POSTER_TEMPLATE_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components', 'template.png')
BOUNTY_POSTER_NO_PHOTO_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components', 'no_portrait.jpg')
BOUNTY_POSTER_PORTRAIT_BOX_START_Y = 238
BOUNTY_POSTER_PORTRAIT_BOX_H = 464
BOUNTY_POSTER_PORTRAIT_BOX_START_X = 73
BOUNTY_POSTER_PORTRAIT_BOX_W = 640
BOUNTY_POSTER_PORTRAIT_TEXTURE_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components',
                                                   'texture_portrait.jpg')
BOUNTY_POSTER_CAPTURE_CONDITION_DEAD_OR_ALIVE_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components',
                                                                  'dead_or_alive.jpg')
BOUNTY_POSTER_CAPTURE_CONDITION_ONLY_DEAD_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components',
                                                              'only_dead.jpg')
BOUNTY_POSTER_CAPTURE_CONDITION_ONLY_ALIVE_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components',
                                                               'only_alive.jpg')
BOUNTY_POSTER_EFFECT_FROST_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components', 'effect_frost.png')
BOUNTY_POSTER_LIGHTNING_EFFECT_PATH = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components',
                                                   'effect_lightning.png')
BOUNTY_POSTER_STAMP_WARLORD = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components', 'stamp_warlord.png')
BOUNTY_POSTER_STAMP_DO_NOT_ENGAGE = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components',
                                                 'stamp_do_not_engage.png')
BOUNTY_POSTER_STAMP_FLEE_ON_SIGHT = os.path.join(BOUNTY_POSTER_ASSETS_PATH, 'image_components',
                                                 'stamp_flee_on_sight.png')
BOUNTY_POSTER_NAME_FONT_SIZE = 150
BOUNTY_POSTER_NAME_MAX_W = 595
BOUNTY_POSTER_NAME_H = 109
BOUNTY_POSTER_NAME_START_X = 95
BOUNTY_POSTER_NAME_START_Y = 802
BOUNTY_POSTER_NAME_END_Y = 911
BOUNTY_POSTER_NAME_MAX_KERN = 65
BOUNTY_POSTER_NAME_OPTIMAL_MAX_LENGTH = 16
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
BOUNTY_POSTER_CAPTURE_CONDITION_START_X = 0
BOUNTY_POSTER_CAPTURE_CONDITION_START_Y = 724
BOUNTY_POSTER_STAMP_START_X = 0
BOUNTY_POSTER_STAMP_START_Y = 100


class HorizontalAlignment(Enum):
    LEFT = 'LEFT'
    CENTER = 'CENTER'
    RIGHT = 'RIGHT'


class VerticalAlignment(Enum):
    TOP = 'TOP'
    CENTER = 'CENTER'
    BOTTOM = 'BOTTOM'


class CaptureCondition(Enum):
    DEAD_OR_ALIVE = 'DEAD_OR_ALIVE'
    ONLY_DEAD = 'ONLY_DEAD'
    ONLY_ALIVE = 'ONLY_ALIVE'


class Effect(Enum):
    FROST = 'FROST'
    LIGHTNING = 'LIGHTNING'


class Stamp(Enum):
    WARLORD = 'WARLORD'
    DO_NOT_ENGAGE = 'DO_NOT_ENGAGE'
    FLEE_ON_SIGHT = 'FLEE_ON_SIGHT'


EFFECT_IMAGE_PATHS = {
    Effect.FROST: BOUNTY_POSTER_EFFECT_FROST_PATH,
    Effect.LIGHTNING: BOUNTY_POSTER_LIGHTNING_EFFECT_PATH
}

STAMP_IMAGE_PATHS = {
    Stamp.WARLORD: BOUNTY_POSTER_STAMP_WARLORD,
    Stamp.DO_NOT_ENGAGE: BOUNTY_POSTER_STAMP_DO_NOT_ENGAGE,
    Stamp.FLEE_ON_SIGHT: BOUNTY_POSTER_STAMP_FLEE_ON_SIGHT
}


class WantedPoster:
    def __init__(self, portrait: Union[str, BytesIO] = None, first_name: str = '', last_name: str = '', bounty: int = 0
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
        self.first_name: str = first_name if first_name is not None else ''
        self.last_name: str = last_name if last_name is not None else ''
        self.bounty: int = bounty

    def generate(self, output_poster_path: str = None,
                 portrait_horizontal_align: HorizontalAlignment = HorizontalAlignment.CENTER,
                 portrait_vertical_align: VerticalAlignment = VerticalAlignment.CENTER,
                 should_make_portrait_transparent: bool = False,
                 portrait_transparency_value: int = 200,
                 full_name_max_length: Union[int, None] = BOUNTY_POSTER_NAME_OPTIMAL_MAX_LENGTH,
                 use_space_sub: bool = True,
                 capture_condition: CaptureCondition = CaptureCondition.DEAD_OR_ALIVE,
                 effects: list[Effect] = None, stamp: Stamp = None) -> str:
        """
        Generates a wanted poster and saves it to the specified path
        :param output_poster_path: The path to the output poster. If None, a temporary file will be created
        :param portrait_vertical_align: The vertical alignment of the portrait image
        :param portrait_horizontal_align: The horizontal alignment of the portrait image
        :param should_make_portrait_transparent: Whether to make the portrait semi-transparent
        :param portrait_transparency_value: The transparency value of the portrait (0-255). Higher = less transparent
        :param full_name_max_length: The maximum length of the full name. If None, no limit
        :param use_space_sub: Whether to use the space substitution character (•) if the name is too long or D. in name
        :param capture_condition: The capture condition to display on the poster
        :param effects: The effects to apply to the poster
        :param stamp: The stamp to apply to the poster
        :return: The path to the generated poster
        """

        # If output path is not specified, use a temporary file
        if output_poster_path is None:
            output_poster_path = uuid.uuid4().hex + '.jpg'

        if effects is None:
            effects = []

        # Get portrait image
        if self.portrait is None:
            portrait = BOUNTY_POSTER_NO_PHOTO_PATH
            portrait_vertical_align = VerticalAlignment.CENTER
            portrait_horizontal_align = HorizontalAlignment.CENTER
            should_make_portrait_transparent = False
        else:
            portrait = self.portrait

        # Get capture condition image
        if capture_condition is CaptureCondition.ONLY_DEAD:
            capture_condition_image_path = BOUNTY_POSTER_CAPTURE_CONDITION_ONLY_DEAD_PATH
        elif capture_condition is CaptureCondition.ONLY_ALIVE:
            capture_condition_image_path = BOUNTY_POSTER_CAPTURE_CONDITION_ONLY_ALIVE_PATH
        else:
            capture_condition_image_path = BOUNTY_POSTER_CAPTURE_CONDITION_DEAD_OR_ALIVE_PATH

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
        portrait = self.__resize_portrait(portrait)

        # Align portrait image
        portrait_coordinate_x, portrait_coordinate_y = self.__align_image(portrait, portrait_vertical_align,
                                                                          portrait_horizontal_align)

        # Paste portrait into new image
        if should_make_portrait_transparent:
            portrait.putalpha(portrait_transparency_value)
            mask = portrait
        else:
            mask = None
        new_image.paste(portrait, (portrait_coordinate_x, portrait_coordinate_y), mask)

        # Paste poster template onto the new image
        new_image.paste(poster_template, (0, 0), mask=poster_template)

        # Add capture condition component
        capture_condition_image = Image.open(capture_condition_image_path)
        new_image.paste(capture_condition_image, (BOUNTY_POSTER_CAPTURE_CONDITION_START_X,
                                                  BOUNTY_POSTER_CAPTURE_CONDITION_START_Y))

        # Add name component
        full_name = self.__get_bounty_poster_name(full_name_max_length, use_space_sub)
        name_component: Image = self.__get_bounty_poster_component(full_name, BOUNTY_POSTER_COMPONENT_NAME)
        new_image.paste(name_component, (0, BOUNTY_POSTER_NAME_START_Y), name_component)

        # Add belly component
        belly = '{0:,}'.format(self.bounty) + '-'
        belly_component: Image = self.__get_bounty_poster_component(belly, BOUNTY_POSTER_COMPONENT_BELLY)
        new_image.paste(belly_component, (0, BOUNTY_POSTER_BELLY_START_Y), belly_component)

        # Add stamp
        if stamp is not None:
            stamp_image = Image.open(STAMP_IMAGE_PATHS[stamp])
            new_image.paste(stamp_image, (BOUNTY_POSTER_STAMP_START_X, BOUNTY_POSTER_STAMP_START_Y), mask=stamp_image)

        # Add effects
        for effect in effects:
            effect_image = Image.open(EFFECT_IMAGE_PATHS[effect]).convert("RGBA")
            new_image.paste(effect_image, (0, 0), mask=effect_image)

        # Save image
        save_path = output_poster_path
        new_image.save(save_path)

        return save_path

    @staticmethod
    def __align_image(portrait: Image, vertical_align: VerticalAlignment, horizontal_align: HorizontalAlignment
                      ) -> Tuple[int, int]:
        """
        Calculate the portrait's coordinate based on the desired alignment
        :param portrait: Image to align
        :param vertical_align: The vertical alignment of the portrait image
        :param horizontal_align: The horizontal alignment of the portrait image
        :return: The portrait's start coordinate
        """

        # Get portrait size
        portrait_width, portrait_height = portrait.size

        # Calculate the portrait's x coordinate based on the desired alignment
        if horizontal_align is HorizontalAlignment.LEFT:
            portrait_x = BOUNTY_POSTER_PORTRAIT_BOX_START_X
        elif horizontal_align is HorizontalAlignment.CENTER:
            portrait_x = int((BOUNTY_POSTER_PORTRAIT_BOX_W - portrait_width) / 2) + BOUNTY_POSTER_PORTRAIT_BOX_START_X
        else:  # Right
            portrait_x = BOUNTY_POSTER_PORTRAIT_BOX_W - portrait_width + BOUNTY_POSTER_PORTRAIT_BOX_START_X

        # Adjust the portrait's y coordinate based on the desired alignment
        if vertical_align is VerticalAlignment.TOP:
            portrait_y = BOUNTY_POSTER_PORTRAIT_BOX_START_Y
        elif vertical_align is VerticalAlignment.CENTER:
            portrait_y = int((BOUNTY_POSTER_PORTRAIT_BOX_H - portrait_height) / 2) + BOUNTY_POSTER_PORTRAIT_BOX_START_Y
        else:  # Bottom
            portrait_y = BOUNTY_POSTER_PORTRAIT_BOX_H - portrait_height + BOUNTY_POSTER_PORTRAIT_BOX_START_Y

        return portrait_x, portrait_y

    @staticmethod
    def __resize_portrait(portrait: Image) -> Image:
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

    def __get_bounty_poster_name(self, max_length: Union[int, None], use_space_sub) -> str:
        """
        Gets the bounty poster's name of a user
        :param max_length: The maximum length of the name
        :param use_space_sub: Whether to use the space substitution character (•) if the name is too long or D. in name
        :return: The bounty poster's name of a user
        """

        # Get full name
        full_name = self.__get_full_name(max_length)

        # Add space sub if too long or D. in name
        if use_space_sub:
            if len(full_name) >= BOUNTY_POSTER_NAME_SPACE_SUB_MIN_LENGTH or 'D.' in full_name:
                full_name = full_name.replace(' ', BOUNTY_POSTER_NAME_SPACE_SUB_CHAR)

            # Replace 'D.' with 'D'
            full_name = full_name.replace('D.', 'D')

        return full_name

    @staticmethod
    def __get_bounty_poster_component(text: str, c_type: int) -> Image:
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

    def __get_full_name(self, max_length: Union[int, None]) -> str:
        """
        Preprocesses the name to be up to a maximum length
        :param max_length: The maximum length of the name
        :return: The full name
        """

        # Normalize to ascii, for non latin characters
        first_name = unidecode(self.first_name).upper().strip()
        last_name = unidecode(self.last_name).upper().strip()

        full_name = f'{last_name} {first_name}'.strip()

        if max_length is None or len(full_name) <= max_length:
            return full_name

        # Use first name only
        full_name = first_name
        if len(full_name) <= max_length:
            return full_name

        # Still too long, split by 'space' and concatenate till it's not too long
        parts = full_name.split(' ')
        result = ''
        for part in parts:
            if len(result + ' ' + part) > max_length:
                return full_name
            result += ' ' + part

        # Use result or only the first part
        full_name = parts[0] if len(result) == 0 else result
        if len(full_name) <= max_length:
            return full_name

        # Still too long, remove extra characters
        full_name = full_name[:(max_length - 2)] + '.'
        return full_name
