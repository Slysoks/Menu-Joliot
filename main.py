import os
from pick import pick
from pdf2image import convert_from_path

def init():
  title = "Please choose a file:"
  warn = "Note: The files will end up with the id of product in the name."
  dirList = os.listdir("./renders/pdf")
  outputPath = "./renders/final/"
  if dirList == []:
    print("There are no files to render. Please add some files to the renders/pdf folder.")
    exit()
  return title, outputPath, warn, dirList

def get_files(dirList, fileExtention):
  files = []
  for file in dirList:
      if file.endswith(fileExtention) and not file.startswith('~$'):
          files.append(file)
  return files

def pick_file(files, title, warn):
  option, index = pick(files, title, indicator='=>', min_selection_count=1)
  renderFileName = str(input(f'{warn}\nEnter the name of the file you want to render: '))
  return option, index, renderFileName

def render_pdf(file, outputPath, renderFileName):
  print(f"🔄️ Rendering {file}")
  pages = convert_from_path(f"./renders/pdf/{file}", 500)
  for i, page in enumerate(pages):
    print(f"🔄️ Rendering page {i}")
    page.save(f"{outputPath}{renderFileName}_{i}.jpg", 'JPEG')
  print(f"🔄️ {file} has been rendered successfully!")


if __name__ == '__main__':
  title, outputPath, warn, dirList = init()
  files = get_files(dirList, '.pdf')
  option, index, renderFileName = pick_file(files, title, warn)
  render_pdf(option, outputPath, renderFileName)
  
  
  
