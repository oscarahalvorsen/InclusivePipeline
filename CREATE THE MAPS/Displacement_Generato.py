import pygame
import openpyxl
import os

# Initialize Pygame with a dummy video driver
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
pygame.display.set_mode((1, 1))  # Set up a minimal display to satisfy Pygame's requirements

# Step 1: Get data from Excel file
def read_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    matrix = []
    for row in ws.iter_rows(values_only=True):
        matrix.append(list(row))
    return matrix

# Load images with specified width and height
def load_images(image_size):
    images = {}
    for i in range(3):  # Assuming you have images 0.png, 1.png, 2.png
        img_path = rf"C:\Users\oscar\oscar\myProjects\polimi\inclusive\3dconverter\CREATE THE MAPS\{i}.png"
        try:
            image = pygame.image.load(img_path)
            image = pygame.transform.scale(image, (int(image_size), int(image_size)))
            images[i] = image
        except pygame.error as e:
            print(f"Error loading image {img_path}: {e}")
    return images

# Show images based on numbers using Pygame without a display window
def show_images_pygame(matrix, save_image=False, file_name="Displacement_finaltest.png"):
    # Calculate screen size based on matrix size and image size
    image_size = 100  # Default image size
    rows, cols = len(matrix), len(matrix[0])
    screen_width = cols * image_size
    screen_height = rows * image_size

    # Create a new surface to blit images onto
    surface = pygame.Surface((cols * image_size, rows * image_size))
    images = load_images(image_size)  # Load images once

    for i, row in enumerate(matrix):
        for j, num in enumerate(row):
            if num == 0:
                surface.blit(images[2], (j * image_size, i * image_size))
            elif num == 1:
                surface.blit(images[0], (j * image_size, i * image_size))
            else:
                surface.blit(images[1], (j * image_size, i * image_size))

    if save_image:
        save_directory = r"C:\Users\oscar\oscar\myProjects\polimi\inclusive\InclusivePipeline\3D GENERARTOR\dis-project\public"
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        pygame.image.save(surface, os.path.join(save_directory, file_name))  # Save the rendered surface

    pygame.quit()

# Export the displayed image
def export_image(matrix):
    show_images_pygame(matrix, save_image=True)  # Set save_image=True to save the image

# Main function
def main():
    file_path = r'C:\Users\oscar\oscar\myProjects\polimi\inclusive\InclusivePipeline\CREATE THE MAPS\Excel_test.xlsx'
    matrix = read_excel(file_path)
    export_image(matrix)

if __name__ == "__main__":
    main()
