# pipeline.py

import cvs_converter
import diffuse_generator
import displacement_generator

def run_pipeline():
    # Define the path to the image you want to process
    image_path = r'C:\Users\oscar\oscar\myProjects\polimi\inclusive\InclusivePipeline\python\saloon5.png'
    
    # Generate the seat map using the cvs_converter
    seat_map = cvs_converter.generate_seat_map(image_path) 
    print(seat_map)
    
    # Use the generated seat map as input for the diffuse_generator and displacement_generator
    diffuse_generator.display_image(seat_map, file_name="diffuse_image.png")
    displacement_generator.display_image(seat_map, file_name="displacement_image.png")

if __name__ == "__main__":
    run_pipeline()
