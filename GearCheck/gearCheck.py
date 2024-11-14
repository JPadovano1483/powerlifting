import pdfParser as parser

def main():
  pdf_string = parser.pdf_to_string(r"GearCheck\PDFs\USAPL-Rulebook.pdf")
  table_of_contents = parser.extract_table_of_contents(pdf_string)
  page_range = parser.extract_equipment_pages(table_of_contents)
  equipment_rules = parser.get_page(pdf_string, page_range)
  print(parser.parse_sections(equipment_rules)['3']['subsections'])

if __name__ == "__main__":
  main()