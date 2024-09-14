import pytesseract as tess
from PIL import Image
import os


def rename(path):
    top_path = path
    bottom_path = path.replace('top', 'bottom')
    img = Image.open(top_path)
    text = tess.image_to_string(img)

    extracted_text = text.strip().lower().split('\n')[0].replace(' ', '_')
    new_top_path = extracted_text + '_top.png'
    new_bottom_path = extracted_text + '_bottom.png'

    # Save extracted text to a file
    with open(top_path[:-4] + '.txt', 'w') as file:
        file.write(text)

    # os.rename(top_path, os.path.join(os.path.dirname(top_path), new_top_path))
    # os.rename(bottom_path, os.path.join(os.path.dirname(bottom_path), new_bottom_path))


for card in os.listdir('assets/skorne'):
    if 'top' in card:
        rename(f'assets/skorne/{card}')