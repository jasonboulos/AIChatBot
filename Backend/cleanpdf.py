from PyPDF2 import PdfReader, PdfWriter

def remove_first_n_pages(input_pdf_path, output_pdf_path, n_pages):
    """
    Removes the first `n_pages` from the input PDF and saves the result to a new file.

    :param input_pdf_path: Path to the original PDF file.
    :param output_pdf_path: Path to save the modified PDF file.
    :param n_pages: Number of pages to remove from the beginning.
    """
    try:
        # Read the input PDF
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        # Iterate over remaining pages and add to writer
        for page_num in range(n_pages, len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        # Write the output PDF
        with open(output_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

        print(f"First {n_pages} pages removed. New file saved as '{output_pdf_path}'.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
input_pdf = "./docs/pdfData/HAS/Insuffisance_Cardiaque_Has.pdf"
output_pdf = "./docs/pdfData/HAS/Insuffisance_Cardiaque_Has.pdf"
remove_first_n_pages(input_pdf, output_pdf, n_pages=5)
