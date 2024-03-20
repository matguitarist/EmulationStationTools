# The Python script extracts the first page of each PDF or Ebook files in a specified folder,
# converts it to a PNG image, and saves the image with the same name as the original PDF file and add -image suffix to it in an "images" folder.
# The script skips conversion if the corresponding PNG file already exists.

import os
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from ebooklib import epub
import ebooklib

def convert_pdf_to_png(pdf_path, output_folder):
    try:
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
    except fitz.FileDataError as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def convert_epub_to_png(epub_path, output_folder):
    # Read the EPUB file
    ebook = epub.read_epub(epub_path)

    # Get the first document (item) in the EPUB file
    first_item = next(iter(ebook.get_items_of_type(ebooklib.ITEM_DOCUMENT)))

    # Get the content of the document
    content = first_item.get_content()

    # Create a temporary PDF file for the EPUB content
    temp_pdf_path = os.path.join(output_folder, "temp.pdf")
    with open(temp_pdf_path, "wb") as temp_pdf:
        temp_pdf.write(content)

    # Convert the temporary PDF to PNG
    image_path = convert_pdf_to_png(temp_pdf_path, output_folder)

    # Remove the temporary PDF file
    os.remove(temp_pdf_path)

    return image_path

def process_documents(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through files in the input folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        png_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}-thumb.png")

        # Skip if it's not a file or not a PDF or EPUB
        if not os.path.isfile(file_path) or not (filename.lower().endswith(".pdf") or filename.lower().endswith(".epub")):
            print(f"Skipping {filename} (Unsupported file format)")
            continue

        # Skip if the PNG file already exists
        if os.path.exists(png_path):
            print(f"Skipping {filename} (PNG file already exists)")
            continue

        # Convert the document to PNG based on the file type
        if filename.lower().endswith(".pdf"):
            image_path = convert_pdf_to_png(file_path, output_folder)
            if image_path:
                print(f"Converted {filename} to {image_path}")
        elif filename.lower().endswith(".epub"):
            image_path = convert_epub_to_png(file_path, output_folder)
            if image_path:
                print(f"Converted {filename} to {image_path}")

if __name__ == "__main__":
    input_folder = "."  # Change this to the path of your PDF and EPUB files
    output_folder = "images"

    process_documents(input_folder, output_folder)
