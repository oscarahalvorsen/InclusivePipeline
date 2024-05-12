import pygame
import openpyxl
import os
import pandas as pd

# Read the Excel file and modify it based on conditions
def process_excel(input_file_path, output_file_path):
    df = pd.read_excel(input_file_path, header=None)

    # Define a function to update the values
    def update_value(value, current_max):
        if value == 0 or value == 2:  # Keep 2 unchanged
            return value
        elif value == 1:
            return current_max

    # Iterate through each cell and update the values
    current_max = 2
    for i in range(len(df)):
        for j in range(len(df.columns)):
            df.at[i, j] = update_value(df.at[i, j], current_max)
        if all(value == 2 for value in df.iloc[i]): # Check if all values in a row are 2
            current_max += 1
            if current_max == 2:  # To start from 3 instead of 4
                current_max += 1

    # Write the modified data to a new Excel file
    df.to_excel(output_file_path, header=False, index=False)

# Step 1: Get data from Excel file
def read_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    matrix = []
    for row in ws.iter_rows(values_only=True):
        matrix.append(list(row))
    return matrix

# Step 2: Show images based on numbers using Pygame
def show_images_pygame(matrix, save_image=False, file_name="diffuse_finaltest.png"):
    pygame.init()

    # Calculate total number of rows and columns
    rows, cols = len(matrix), len(matrix[0])

    # Calculate the maximum dimension among rows and columns
    max_dimension = max(rows, cols)

    # Calculate the image size based on the maximum dimension
    image_size = 800 // max_dimension

    # Calculate screen size based on matrix size and image size
    screen_width = cols * image_size
    screen_height = rows * image_size

    # Ensure that the screen dimensions are square
    if screen_width != screen_height:
        max_size = max(screen_width, screen_height)
        screen_width = max_size
        screen_height = max_size

    screen = pygame.display.set_mode((int(screen_width), int(screen_height)))
    pygame.display.set_caption("Images from Excel")

    # Fill the screen with white color
    screen.fill((255, 255, 255))

    images = load_images(image_size, image_size)  # Load images once

    for i, row in enumerate(matrix):
        for j, num in enumerate(row):
            if num in images:
                screen.blit(images[num], (j * image_size, i * image_size))

    pygame.display.update()

    if save_image:
        save_directory = r"C:\POLIMI\2023-2024\SEM02-2023-2024\Digital Inclusive Design\React\3D_Saloon\dis-project\public"
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        pygame.image.save(screen, os.path.join(save_directory, file_name))  # Save the displayed image with specified file name

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

# Step 3: Load images with specified width and height
def load_images(image_width, image_height):
    images = {}
    image_folder = r'C:\POLIMI\2023-2024\SEM02-2023-2024\Digital Inclusive Design\Code\COLOR'
    for i in range(12):  # Assuming you have images 0.png, 1.png, 2.png
        img_path = os.path.join(image_folder, f"{i}.png")
        image = pygame.image.load(img_path).convert()
        image = pygame.transform.scale(image, (int(image_width), int(image_height)))
        images[i] = image
    return images

# Step 4: Main function
def main():
    input_file_path = r'C:\POLIMI\2023-2024\SEM02-2023-2024\Digital Inclusive Design\Code\Chair.xlsx'
    output_file_path = r'C:\POLIMI\2023-2024\SEM02-2023-2024\Digital Inclusive Design\Code\Chair_Color.xlsx'
    
    # Process the Excel file to modify based on conditions
    process_excel(input_file_path, output_file_path)

    # Read the modified Excel file
    matrix = read_excel(output_file_path)

    # Show images based on numbers using Pygame
    show_images_pygame(matrix, save_image=True)  # Set save_image=True to save the image

if __name__ == "__main__":
    main()
