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
  print(f'🔃 Rendering file {file}...')
  page_list = []
  poppler_path = r'C:/Program Files/poppler-24.08.0/Library/bin'
  pages = convert_from_path(prefix + file, 100, poppler_path=poppler_path)
  
  # Crop the pages to remove the borders
  for i, page in enumerate(pages):
    print(f'🔃 Rendering page {i}...')
    borders = [85, 1, 86, 2] # left, top, right, bottom
    page = page.crop((borders[0], borders[1], page.width - borders[2], page.height - borders[3]))
    page.save(f'renders/png/{file[:-4]}_{i}.png', 'PNG')
    page_list.append(f'renders/png/{file[:-4]}_{i}.png')
    print(f'✅ Page {i} rendered successfully!')
  
  print(f'✅ File {file} rendered successfully!')
  return page_list

def ocr_image(file:str):
  
  # Open the image
  image = Image.open(file)
  
  # Set the tesseract path
  pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
  
  # Detect the text in the image
  text = pytesseract.image_to_string(image)
  
  # Find date in text using regex
  if re.search(r'Menu du self', text): doctype = 'm'
  elif re.search(r'Menu du soir', text): doctype = 's'
  else: doctype = 'u'
  date_pattern = r'- [A-Z][a-z]{2} \d{2}/\d{2} -'
  date_match = re.search(date_pattern, text)
  if date_match:
    date = date_match.group()
    date = date[6:-2].replace('/', '-')
    print(f'📅 Date found: {date}')
    # Create the final directory if it doesn't exist
    final_dir = 'renders/final'
    if not os.path.exists(final_dir):
      os.makedirs(final_dir)
    
    # Construct the new file name with the date
    new_file_name = f'{final_dir}/{doctype}-{date}.png'
    
    # Move and rename the file
    os.rename(file, new_file_name)
    print(f'📁 File moved to {new_file_name}')
    return date
  return None

file = selector()
prefix = 'renders/pdf/'

page_list = render_file(file, prefix)

for page in page_list:
  date = ocr_image(page)