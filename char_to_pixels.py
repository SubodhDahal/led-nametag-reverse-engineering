from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np

def char_to_pixels(text, path='./advanced_led_board-7.ttf', fontsize=14):
    font = ImageFont.truetype(path, fontsize)
    w, h = font.getsize(text)
    h *= 2
    image = Image.new('L', (w, h), 1)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    arr = arr[(arr != 0).any(axis=1)]
    return arr

def get_block_values(text):
    retval = []
    for character in text:
        arr = char_to_pixels(character)

        retval.append(0x00)
        for row1 in arr:
            value = ''
            for row2 in row1:
                value += str(row2)

            value = int(value, 2)
            retval.append(value)

        if (len(retval) % 11 != 0):
            remaining_lines = 11 - len(retval) % 11

            for i in range(0, remaining_lines):
                retval.append(0x00)

        print(retval)
    return retval

if __name__ == '__main__':
    pixel_values = get_block_values('Subodh')

    print(pixel_values)
