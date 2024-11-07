import re
import pdfToString as converter

def main():
  # Your main code goes here
  pdf_string = converter.pdf_to_string(r"C:\Users\Jamie Padovano\VSCode\personal\powerlifting\GearCheck\PDFs\USAPL-Rulebook.pdf")
  # print(pdf_string)
  table_of_contents = extract_table_of_contents(pdf_string)
  print(extract_equipment_pages(table_of_contents))

def extract_table_of_contents(text):
  # Find the table of contents
  # probably should store the pdf page number here so we can determine which pages to start and stop at instead of guessing the offset
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

if __name__ == "__main__":
  main()