# Assignment 05


Write a Python script `cdx2html.py` that creates an `index.html` page showing molecular structures from `.cdxml` files. Convert each `.cdxml` file to a corresponding `.png` file, included in the HTML in an `img` element, organized in `table/tr/td` elements with column headings: 'filename', 'formula', and '2D structure'.



Prerequisites
-------------

- Python 3.8 or newer installed

- Git installed (to clone the repository)

- CDXML files: ChemDraw XML molecular structure files 

- Place CDXML files in the same folder as the script `cdx2html.py`



How to clone from GitHub

-----------------

# Clone the repository via HTTPS

git clone https://github.com/janre271/CI2.git

cd CI2


Quick steps to run the script 
------------------

# 1. Create and activate a virtual environment (optional but recommended)

python -m venv venv

venv\Scripts\activate   # Windows

## On Linux/macOS: source venv/bin/activate


# 2. Go to the assignment folder

cd A05

# Clone the repository via HTTPS


# 3. Install required dependencies

pip install -r requirements.txt


# 4. Ensure CDXML files are in the same directory as cdx2html.py


# 5. Run the converter to process all CDXML files

python cdx2html.py *.cdxml



How it works

------------

1. **OpenBabel/pybel** extracts molecular formulas by converting CDXML to MOL format and calculating formulas with correct implicit hydrogen counts 

2. **Indigo** renders quality PNG images with native CDXML support and ChemDraw-style rendering.

3. **PIL (Pillow)** provides fallback rendering if Indigo is unavailable.

4. Generates an HTML table with filenames, formulas (formatted with subscripts), and embedded PNG images.



Troubleshooting

- Ensure CDXML files are in the same directory as cdx2html.py

- "No module named 'openbabel'"? Make sure you ran `pip install -r requirements.txt` in the activated virtual environment.

- "Indigo warning"? Install with `pip install epam.indigo` for best quality (script will use PIL fallback otherwise).

- Need to regenerate? Simply run `python cdx2html.py *.cdxml` again to overwrite existing files.



Expected output (example)

-------------------------

You should see console output showing progress:


Processing 9 CDXML file(s)...

Success! Generated index.html with 9 molecule(s)

Open index.html in a web browser to view the results.








