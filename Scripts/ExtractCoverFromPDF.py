import os
import shutil
import fitz  # PyMuPDF
from PyPDF2 import PdfReader

def convert_pdf_to_png(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Get the first page
    pdf_page = pdf_document.load_page(0)

    # Convert the page to an image
    image = pdf_page.get_pixmap()

    # Save the image as a PNG file
    image_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}-thumb.png")
    image.save(image_path)

    # Close the PDF document
    pdf_document.close()

    return image_path

def process_pdfs(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through PDF files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            png_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}-thumb.png")

            # Skip if the PNG file already exists
            if os.path.exists(png_path):
                print(f"Skipping {filename} (PNG file already exists)")
                continue

            # Convert the first page of the PDF to PNG
            image_path = convert_pdf_to_png(pdf_path, output_folder)
            print(f"Converted {filename} to {image_path}")

if __name__ == "__main__":
    input_folder = "."  # Change this to the path of your PDF files
    output_folder = "images"

    process_pdfs(input_folder, output_folder)
