import pdfToString as converter

def main():
  # Your main code goes here
  pdf_string = converter.pdf_to_string(r"C:\Users\Jamie Padovano\VSCode\personal\powerlifting\GearCheck\PDFs\USAPL-Rulebook.pdf")
  print(pdf_string)

if __name__ == "__main__":
  main()