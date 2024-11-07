import PyPDF2

def pdf_to_string(path):
    # Open the PDF file
    pdf_file_obj = open(path, 'rb')

    # Create a PDF file reader object
    reader = PyPDF2.PdfReader(pdf_file_obj)

    # Get the number of pages in the PDF file
    num_pages = len(reader.pages)

    # Initialize a string to store the text
    text = ''

    # Loop through all the pages in the PDF file
    for i in range(num_pages):
        # Get the page object
        page_obj = reader.pages[i]

        # Extract the text from the page
        text += page_obj.extract_text()

    # Close the PDF file
    pdf_file_obj.close()

    # Return the extracted text
    return text 