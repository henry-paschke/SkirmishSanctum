from pdf2image import convert_from_path
from PIL import Image
import os
import shutil
import time

def convert_to_images(pdf_path, output_directory):
    # Specify the path to the PDF and the desired DPI (e.g., 300 for high resolution)
    dpi = 300

    # Convert PDF to image(s)
    images = convert_from_path(pdf_path, dpi=dpi)

    DOTTED_LINE_HEIGHT = 4
    GREY_BAR_WIDTH = 6

    CARD_WIDTH = 747
    CARD_HEIGHT = 1050

    STARTING_X = 142
    STARTING_Y = 228;

    for i, image in enumerate(images):
        for x in range(4):
            for y in range(2):
                x_pos = STARTING_X + (CARD_WIDTH + GREY_BAR_WIDTH) * x
                y_pos = STARTING_Y + (CARD_HEIGHT + DOTTED_LINE_HEIGHT) * y
                cropped_image = image.crop((x_pos, y_pos, x_pos + CARD_WIDTH, y_pos + CARD_HEIGHT))
                image_path = f'{output_directory}{pdf_path[:-4].split("/")[-1]}_page_{i+1}_card_{x+1}_{"bottom" if y else "top"}.png'
                if y == 1:
                    cropped_image = cropped_image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
                cropped_image.save(image_path, 'PNG')
                print(f"Page {i+1} card {x+1} converted to image and saved as {image_path}")


def create_output_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory {directory_path} created.")
    else:
        print(f"Directory {directory_path} already exists.")

def convert_and_populate_images(output_directory):
    create_output_directory(output_directory)

    for pdf_file in os.listdir("data"):
        if pdf_file.endswith(".pdf"):
            pdf_path = f"data/{pdf_file}"
            create_output_directory(output_directory + "/" + pdf_file[:-4])
            convert_to_images(pdf_path, output_directory + "/" + pdf_file[:-4] + "/")


def rename_files(directory):
    for faction in os.listdir(directory):
        pdf = f"{directory}/{faction}"
        filename = pdf.split(" ")[0]
        if filename.endswith(".pdf"):
            filename = filename[:-4]
        if os.path.isfile(pdf):
            if pdf.endswith(".pdf"):
                try:
                    os.rename(pdf, f"{filename}.pdf")
                except FileExistsError:
                    os.rename(pdf, f"{filename}_2.pdf")

def copy_raw_data_folder(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"Copied {src} to {dst}")


start_time = time.time()

copy_raw_data_folder("raw_data", "data")
rename_files("data")
convert_and_populate_images("new_images")

shutil.rmtree("data")
print("Deleted 'data' folder.")

end_time = time.time()
print(f"Total execution time: {end_time - start_time} seconds")

    