import pygame
import os
import openpyxl

# Function to read data from an Excel file
def read_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    matrix = []
    for row in ws.iter_rows(values_only=True):
        matrix.append(list(row))
    return matrix

# Function to load images into a dictionary
def load_images(image_width, image_height):
    images = {}
    image_folder = r'C:\Users\oscar\oscar\myProjects\polimi\inclusive\InclusivePipeline\CREATE THE MAPS\COLOR'
    pygame.display.init()  # Initialize display
    pygame.display.set_mode((1, 1))  # Create the smallest window possible
    for i in range(12):  # Assuming you have images 0.png to 11.png
        img_path = os.path.join(image_folder, f"{i}.png")
        image = pygame.image.load(img_path)
        image = pygame.transform.scale(image, (int(image_width), int(image_height)))
        images[i] = image.convert()  # Use convert after window is initialized
    pygame.display.quit()  # Close the display if not needed anymore
    return images


# Function to render images based on the matrix and save them
def show_images_pygame(matrix, save_image=False, file_name="diffuse_finaltest.png"):
    pygame.init()

    # Calculate total number of rows and columns
    rows, cols = len(matrix), len(matrix[0])

    # Calculate the maximum dimension among rows and columns
    max_dimension = max(rows, cols)

    # Calculate the image size based on the maximum dimension
    image_size = 800 // max_dimension

    # Set up off-screen rendering surface
    surface = pygame.Surface((cols * image_size, rows * image_size))
    surface.fill((255, 255, 255))  # Fill the surface with white color

    images = load_images(image_size, image_size)  # Load images once

    for i, row in enumerate(matrix):
        for j, num in enumerate(row):
            if num in images:
                surface.blit(images[num], (j * image_size, i * image_size))

    if save_image:
        save_directory = r"C:\Users\oscar\oscar\myProjects\polimi\inclusive\InclusivePipeline\3D GENERARTOR\dis-project\public"
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        pygame.image.save(surface, os.path.join(save_directory, file_name))  # Save the rendered surface

    pygame.quit()

# Main function to execute the workflow
def main():
    input_file_path = r'C:\Users\oscar\oscar\myProjects\polimi\inclusive\InclusivePipeline\CREATE THE MAPS\Excel_test.xlsx'
    matrix = read_excel(input_file_path)
    show_images_pygame(matrix, save_image=True, file_name="diffuse_finaltest.png")

if __name__ == "__main__":
    main()
