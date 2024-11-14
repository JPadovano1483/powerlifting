import re
import PyPDF2

# might want to make this a class and instantiate a parser object in the main file

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

def extract_table_of_contents(text):
    # Find the table of contents
    toc_start = text.lower().find('table of contents')
    if toc_start == -1:
        return None

    # Extract the table of contents section
    toc_end = text.lower().find("appendix", toc_start)
    toc_text = text[toc_start:toc_end]

    # Remove lines that start with 'Revised'
    toc_lines = toc_text.split('\n')
    toc_lines = [line for line in toc_lines if not line.strip().lower().startswith('revised')]
    toc_text = '\n'.join(toc_lines)

    return toc_text

# Find out what pages are related to personal apparel and equipment
def extract_equipment_pages(toc_text):
  equipment_pages = []

  # TODO: Can merge the following two functions into one by starting search for next index aftert we find the first one - saves on processing time

  # find the index number of the equpiment section and start page number
  for line in toc_text.split('\n'):
    if 'personal apparel and equipment' in line.lower():
      start_index_num = re.match(r'(\d+(\.\d+)*\.)\s', line)
      start_page_number = re.search(r'(\d+)\s*$', line)
      if start_page_number:
        equipment_pages.append(int(start_page_number.group(1)))
  
  # find the page we want to end at
  end_index_num = str(int(start_index_num[0].rstrip('. ')) + 1) + '. '
  for line in toc_text.split('\n'):
    if line.lower().startswith(end_index_num):
      end_page_number = re.search(r'(\d+)\s*$', line)
      if end_page_number:
        equipment_pages.append(int(end_page_number.group(1)))
    
  return equipment_pages

def get_page(text, page_range):
  # Get the text from the specified page range
  start_page = page_range[0]
  end_page = page_range[1]

  # Find the start and end index of the page range
  start_index = text.lower().find(f'page {start_page}')
  end_index = text.lower().find(f'page {end_page}')

  # Extract the text from the page range
  page_text = text[start_index:end_index]

  return page_text

def parse_sections(page_text):
  sections = {}
  current_section = None
  current_subsection = None

  for line in page_text.split('\n'):
    # Match main sections (e.g., "1. Section Title")
    main_section_match = re.match(r'^(\d+)\.\s+(.*)', line)
    if main_section_match:
      current_section = main_section_match.group(1)
      sections[current_section] = {'title': main_section_match.group(2), 'subsections': {}}
      current_subsection = None
      continue

    # Match subsections (e.g., "1.1. Subsection Title")
    subsection_match = re.match(r'^(\d+\.\d+)\.\s+(.*)', line)
    if subsection_match:
      current_subsection = subsection_match.group(1)
      sections[current_section]['subsections'][current_subsection] = {'title': subsection_match.group(2), 'subsections': {}}
      continue

    # Match sub-subsections (e.g., "1.1.1. Sub-subsection Title")
    sub_subsection_match = re.match(r'^(\d+\.\d+\.\d+)\.\s+(.*)', line)
    if sub_subsection_match:
      sub_subsection = sub_subsection_match.group(1)
      sections[current_section]['subsections'][current_subsection]['subsections'][sub_subsection] = sub_subsection_match.group(2)
      continue

    # # Match sub-sub-subsections (e.g., "1.1.1.1. Sub-sub-subsection Title")
    # sub_sub_subsection_match = re.match(r'^(\d+\.\d+\.\d+\.\d+)\.\s+(.*)', line)
    # if sub_sub_subsection_match:
    #   sub_sub_subsection = sub_sub_subsection_match.group(1)
    #   sections[current_section]['subsections'][current_subsection]['subsections'][sub_subsection]['subsections'] = sections[current_section]['subsections'][current_subsection]['subsections'].get(sub_subsection, {})
    #   sections[current_section]['subsections'][current_subsection]['subsections'][sub_subsection]['subsections'][sub_sub_subsection] = sub_sub_subsection_match.group(2)
    #   continue

  return sections