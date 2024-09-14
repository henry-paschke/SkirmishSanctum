from pdf2image import convert_from_path
from PIL import Image

def convert_to_image(pdf_path):
    # Specify the path to the PDF and the desired DPI (e.g., 300 for high resolution)
    dpi = 300

    # Convert PDF to image(s)
    images = convert_from_path(pdf_path, dpi=dpi)

    DOTTED_LINE_HEIGHT = 4
    GREY_BAR_WIDTH = 6

    CARD_WIDTH = 747
    CARD_HEIGHT = 1050

    STARTING_X = 142
    STARTING_Y = 228

    for i, image in enumerate(images):
        for x in range(4):
            for y in range(2):
                x_pos = STARTING_X + (CARD_WIDTH + GREY_BAR_WIDTH) * x
                y_pos = STARTING_Y + (CARD_HEIGHT + DOTTED_LINE_HEIGHT) * y
                cropped_image = image.crop((x_pos, y_pos, x_pos + CARD_WIDTH, y_pos + CARD_HEIGHT))
                image_path = f'{pdf_path[:-4]}_page_{i+1}_card_{x+1}_{"bottom" if y else "top"}.png'
                if y == 1:
                    cropped_image = cropped_image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
                cropped_image.save(image_path, 'PNG')
                print(f"Page {i+1} card {x+1} converted to image and saved as {image_path}")
        

convert_to_image("assets/trollbloods/Trollbloods.pdf")  # Replace with your PDF path


# 142, 228, 889, 1278