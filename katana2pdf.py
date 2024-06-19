import argparse
import os
import zipfile
from PIL import Image

parser = argparse.ArgumentParser(prog="python katana2pdf.py", description="Transforms zip files downloaded from MangaKatana into PDFs")
parser.add_argument("--path", help="The path to a zip file, or directory full of zip files, downloaded from MangaKatana", required=True)
parser.add_argument("--dont-zoom", help="By default, if there are large panels that take up 2 pages, additional zoomed-in views will be inserted so you can read the text better. Set this flag to prevent this.", action="store_true")
args = parser.parse_args()

files = []

if os.path.isdir(args.path):
    for filename in os.listdir(args.path):
        file_path = os.path.join(args.path, filename)
        if os.path.isfile(file_path) and file_path.endswith(".zip"):
            files.append(file_path)
else:
    if os.path.isfile(args.path) and args.path.endswith(".zip"):
        files.append(args.path)

if len(files) == 0:
    print("No zip files found at the specified path")
    exit(1)

def sort_key(filename):
    parts = filename.split('/')
    chapter_number = int(parts[0][1:])
    image_number = int(parts[1].split('.')[0])
    return chapter_number, image_number

for file in files:
    archive = zipfile.ZipFile(file, 'r')
    image_names = []
    for image_name in archive.namelist():
        info = archive.getinfo(image_name)
        if not info.is_dir():
            image_names.append(image_name)
    image_names = sorted(image_names, key=sort_key)
    images = []
    for image_name in image_names:
        with archive.open(image_name) as f:
            try:
                image = Image.open(f)
                image.load()
                images.append(image)
                if not args.dont_zoom:
                    width, height = image.size
                    if width > height:
                        midpoint = width // 2
                        left_half = image.crop((0, 0, midpoint, height))
                        right_half = image.crop((midpoint, 0, width, height))
                        images.append(right_half)
                        images.append(left_half)
            except:
                pass
    if len(images) > 0:
        new_name = file.split(".zip")[0] + ".pdf"
        images[0].save(new_name, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
        print(f"Created {new_name}")
        for image in images:
            image.close()
    else:
        print(f"No images found in zip file {file}")

print("Done")