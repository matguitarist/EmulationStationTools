import os
from PIL import Image, ImageDraw, ImageOps

def process_image(image_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the image
    image = Image.open(image_path)

    # Get only the label region (you may need to adjust the coordinates based on your images)
    label_region = image.crop((68, 215, 400, 548))  # Replace x1, y1, x2, y2 with the actual coordinates

    # Create the output image with only the label and rounded corners
    label_image = Image.new("RGBA", label_region.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(label_image)

    # Create a rounded rectangle mask
    corner_radius = 20  # Adjust the corner radius as needed
    mask = Image.new("L", label_region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), label_region.size], corner_radius, fill=255)

    # Paste the label region onto the rounded rectangle
    label_image.paste(label_region, (0, 0), mask)

    # Get the file name without extension
    file_name = os.path.splitext(os.path.basename(image_path))[0]

    # Save the new image in the Labels folder with the same name as the original
    output_path = os.path.join(output_folder, f"{file_name}.png")
    label_image.save(output_path)

if __name__ == "__main__":
    # Specify the folder where the script is launched
    current_folder = os.path.dirname(os.path.abspath(__file__))

    # Specify the output folder for labeled images
    labels_folder = os.path.join(current_folder, "Labels")

    # Iterate through all files in the current folder
    for file_name in os.listdir(current_folder):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(current_folder, file_name)
            process_image(file_path, labels_folder)

    print("Labeling process with rounded corners completed.")
