import pygame
import openpyxl
import os

# Step 1: Get data from Excel file
def read_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    matrix = []
    for row in ws.iter_rows(values_only=True):
        matrix.append(list(row))
    return matrix

# Step 2: Show images based on numbers using Pygame
def show_images_pygame(matrix, save_image=False, file_name="Displacement_finaltest.png"):
    pygame.init()

    # Calculate screen size based on matrix size and image size
    image_size = 100  # Default image size
    rows, cols = len(matrix), len(matrix[0])
    screen_width = cols * image_size
    screen_height = rows * image_size

    # Adjust screen size to be square if necessary
    if screen_width > screen_height:
        screen_height = screen_width
    elif screen_height > screen_width:
        screen_width = screen_height

    screen = pygame.display.set_mode((int(screen_width), int(screen_height)))
    pygame.display.set_caption("Images from Excel")

    images = load_images(image_size)  # Load images once

    # Create a new surface to blit images onto
    surface = pygame.Surface((cols * image_size, rows * image_size))

    for i, row in enumerate(matrix):
        for j, num in enumerate(row):
            if num in images:
                surface.blit(images[num], (j * image_size, i * image_size))

    screen.blit(surface, (0, 0))  # Blit the surface onto the screen

    pygame.display.flip()  # Update the entire screen

    if save_image:
        save_directory = r"C:\POLIMI\2023-2024\SEM02-2023-2024\Digital Inclusive Design\React\3D_Saloon\dis-project\public"
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        pygame.image.save(surface, os.path.join(save_directory, file_name))  # Save the displayed image with specified file name

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

# Step 3: Load images with specified width and height
def load_images(image_size):
    images = {}
    for i in range(3):  # Assuming you have images 0.png, 1.png, 2.png
        img_path = rf"C:\POLIMI\2023-2024\SEM02-2023-2024\Digital Inclusive Design\Code\{i}.png"
        try:
            image = pygame.image.load(img_path).convert()
            image = pygame.transform.scale(image, (int(image_size), int(image_size)))
            images[i] = image
        except pygame.error as e:
            print(f"Error loading image {img_path}: {e}")
    return images

# Step 4: Export the displayed image
def export_image(matrix):
    show_images_pygame(matrix, save_image=True)  # Set save_image=True to save the image

# Step 5: Main function
def main():
    file_path = r'C:\POLIMI\2023-2024\SEM02-2023-2024\Digital Inclusive Design\Code\Chair.xlsx'
    matrix = read_excel(file_path)
    export_image(matrix)

if __name__ == "__main__":
    main()
