from pdf2image import convert_from_path
from pick import pick
from PIL import Image
import os, pytesseract, re

def selector():
  title = 'First, select a PDF file'
  options = os.listdir('renders/pdf')
  option, index = pick(options, title, indicator='=>', default_index=0)
  return option

def render_file(file:str, prefix:str):
  page_list = []
  poppler_path = r'C:/Program Files/poppler-24.08.0/Library/bin'
  pages = convert_from_path(prefix + file, 100, poppler_path=poppler_path)
  for i, page in enumerate(pages):
    borders = [85, 1, 86, 2] # left, top, right, bottom
    page = page.crop((borders[0], borders[1], page.width - borders[2], page.height - borders[3]))
    page.save(f'renders/png/{file[:-4]}_{i}.png', 'PNG')
    page_list.append(f'renders/png/{file[:-4]}_{i}.png')
  return page_list

def ocr_image(file:str):
  image = Image.open(file)
  pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
  
  # Detect the text in the image
  text = pytesseract.image_to_string(image)
  
  # Find date in text using regex
  date_pattern = r'- [A-Z][a-z]{2} \d{2}/\d{2} -'
  date_match = re.search(date_pattern, text)
  if date_match:
    date = date_match.group()
    date = date[6:-2].replace('/', '-')
    return date
  return None

file = selector()
prefix = 'renders/pdf/'

page_list = render_file(file, prefix)

for page in page_list:
  print(page)
  date = ocr_image(page)
  print(date)

# Ne marche pas sur les PDF contenant plusieurs pages...