import math
import cv2
import numpy as np

def generate_seat_map(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for different colors in HSV
    colors_hsv = {
        "gray": (np.array([0, 0, 50]), np.array([180, 50, 220])),
        "light_pink": (np.array([150, 50, 50]), np.array([180, 255, 255])),
        "yellow": (np.array([20, 100, 100]), np.array([40, 255, 255])),
        "light_blue": (np.array([90, 50, 50]), np.array([130, 255, 255])),
        "dark_pink": (np.array([168, 100, 100]), np.array([175, 255, 255])),
        "medium_blue": (np.array([110, 50, 50]), np.array([130, 255, 255])),
        "orange": (np.array([10, 100, 100]), np.array([25, 255, 255])),
        "light_purple": (np.array([125, 50, 50]), np.array([155, 255, 255])),
        "purplish_pink": (np.array([160, 50, 50]), np.array([167, 255, 255])),
        "brown1": (np.array([0, 50, 50]), np.array([15, 255, 255])),
        "brown2": (np.array([175, 50, 50]), np.array([180, 255, 255]))
    }

    # Determine scaling for image analysis
    height = math.ceil(image.shape[0] / 17)
    width = math.ceil(image.shape[1] / 17)

    # Create masks for each color and find the seats
    seat_map = np.zeros((height, width), dtype=int)
    for i, (color, (lower, upper)) in enumerate(colors_hsv.items()):
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 50:
                x, y, w, h = cv2.boundingRect(contour)
                row = int(y // (image.shape[0] / height))
                col = int(x // (image.shape[1] / width))
                seat_map[row, col] = i + 1

    return seat_map

def main(image_path):
    seat_map = generate_seat_map(image_path)
    print(seat_map)  # Print or further process seat_map as needed
    return seat_map

if __name__ == "__main__":
    main()
