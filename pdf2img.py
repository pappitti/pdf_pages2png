import fitz  # PyMuPDF
from PIL import Image, PngImagePlugin
import os
from datetime import datetime
import argparse

def convert_pdf_to_images(pdf_path, output_folder, metadata=None):
    """
    Convert PDF to images and save them with metadata.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_folder (str): Path to save the images
        metadata (dict): Optional metadata to add to images
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    try:
        pdf_document = fitz.open(pdf_path)
        
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            
            # Get the page as an image
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
            
            # Create image filename
            image_path = os.path.join(
                output_folder,
                f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{page_number + 1}.png"
            )
            
            # Convert pix to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  

            meta = PngImagePlugin.PngInfo()
            # Add basic metadata
            meta.add_text('Source_PDF', os.path.basename(pdf_path))
            meta.add_text('Conversion_Date', datetime.now().isoformat())
            meta.add_text('Page_Number', str(page_number + 1))
            meta.add_text('Total_Pages', str(pdf_document.page_count))
    
            # Add metadata using ExifTool if available (optional)
            if metadata:
                # Add custom metadata
                for key, value in metadata.items():
                    meta.add_text(key, str(value))
                    
            # Save with metadata
            img.save(image_path, "PNG", pnginfo=meta)

        print(f"Successfully converted: {os.path.basename(pdf_path)}")
        return True
        
    except Exception as e:
        print(f"Error converting {os.path.basename(pdf_path)}: {str(e)}")
        return False
    
    finally:
        if 'pdf_document' in locals():
            pdf_document.close()

def batch_convert_pdfs(input_folder, output_folder, metadata=None):
    """
    Convert all PDFs in a folder to images.
    
    Args:
        input_folder (str): Path to folder containing PDFs
        output_folder (str): Path to save the images
        metadata (dict): Optional metadata to add to images
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get all PDF files in the input folder
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the input folder")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF
    successful = 0
    failed = 0
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        
        # Create a subfolder for this PDF's images
        pdf_output_folder = os.path.join(output_folder, os.path.splitext(pdf_file)[0])
        
        if convert_pdf_to_images(pdf_path, pdf_output_folder, metadata):
            successful += 1
        else:
            failed += 1
    
    # Print summary
    print("\nConversion Summary:")
    print(f"Successfully converted: {successful} PDFs")
    print(f"Failed conversions: {failed} PDFs")

def main():
    parser = argparse.ArgumentParser(description='Convert PDFs to images with metadata')
    parser.add_argument('input_folder', help='Folder containing PDF files')
    parser.add_argument('output_folder', help='Folder to save image files')
    parser.add_argument('--author', help='Author metadata for the images')
    parser.add_argument('--project', help='Project metadata for the images')
    parser.add_argument('--department', help='Department metadata for the images')
    
    args = parser.parse_args()
    
    # Create metadata dictionary from command line arguments
    metadata = {}
    if args.author:
        metadata['Author'] = args.author
    if args.project:
        metadata['Project'] = args.project
    if args.department:
        metadata['Department'] = args.department
    
    batch_convert_pdfs(args.input_folder, args.output_folder, metadata)

# Example usage
if __name__ == "__main__":
    main()