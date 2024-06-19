# katana2pdf
Transforms zip files downloaded from MangaKatana into PDFs

Installation:
```
git clone https://github.com/emilypeto/katana2pdf
pip install Pillow
```

```
usage: python katana2pdf.py [-h] --path PATH [--dont-zoom]

Transforms zip files downloaded from MangaKatana into PDFs

options:
  -h, --help   show this help message and exit
  --path PATH  The path to a zip file, or directory full of zip files, downloaded from
               MangaKatana
  --dont-zoom  By default, if there are large panels that take up 2 pages, additional
               zoomed-in views will be inserted so you can read the text better. Set
               this flag to prevent this.
```
