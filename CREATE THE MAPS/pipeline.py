# pipeline.py

import cvs_converter
import diffuse_generator

def run_pipeline():
    # Define the path to the image you want to process
    image_path = r'C:\Users\oscar\oscar\myProjects\polimi\inclusive\InclusivePipeline\CREATE THE MAPS\saloon5.png'
    
    # Generate the seat map using the cvs_converter
    seat_map = cvs_converter.generate_seat_map(image_path)
    
    # Use the generated seat map as input for the diffuse_generator
    diffuse_generator.display_image(seat_map, save_image=True)

if __name__ == "__main__":
    run_pipeline()
