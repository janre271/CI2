A03, assignment number 4
# MOLBASE Benzidine Compound Parser
This project provides a script to parse compound names from the results page of a MOLBASE search for "benzidine".  
1. Go to [https://www.molbase.com/](https://www.molbase.com/) and search for "benzidine".
2. Save the first page of the search results as `molbase_benzidine.html`, the search results page must be saved as a complete HTML file with UTF-8 encoding for proper parsing.
3. Place `molbase_benzidine.html` in the project directory.

Prerequisites
-------------
- Python 3.7+ installed
  - Verify with `python --version` or `py --version` in PowerShell.
- Git installed if you want to clone from GitHub.
 
Clone from GitHub 
----------------------------
# Clone the repository via HTTPS 
git clone https://github.com/janre271/CI2.git
cd CI2
# Place `molbase_benzidine.html` in the project directory. 

Quick steps to run
------------------------------
# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt

# Run the parser
python molbase_parser.py

# The expected output is a list of compound names found in the HTML file:

4-(4-aminophenyl)aniline

2,6,2',6'-tetrachloro-benzidine

3,3'-diethoxy-benzidine

N,N'-Diphenylbenzidine

acetic acid,4-(4-aminophenyl)aniline

Benzidine sulphate

Benzidine dihydrochloride

2-[[4-[4-[(1-anilino-1,3-dioxobutan-2-yl)diazenyl]-3-chlorophenyl]-2-chlorophenyl]diazenyl]-3-oxo-N-phenylbutanamide

2-[[2-chloro-4-[3-chloro-4-[[1-(2-methylanilino)-1,3-dioxobutan-2-yl]diazenyl]phenyl]phenyl]diazenyl]-N-(2-methylphenyl)-3-oxobutanamide

PSB 1115 potassium salt hydrate

N,N'-bis(4-isopropylphenyl)benzidine

N,N'-bis-(furan-2-carbonyl)-benzidine

4-(4-amino-3-bromophenyl)-2-bromoaniline

4-[4-amino-2-(trifluoromethyl)phenyl]-3-(trifluoromethyl)aniline

N-[4-[4-(naphthalen-1-ylamino)phenyl]phenyl]naphthalen-1-amine

4-[4-amino-3-(trifluoromethyl)phenyl]-2-(trifluoromethyl)aniline

4-(4-amino-3-methoxy-phenyl)-2-methoxy-aniline dihydrochloride

5-amino-2-(4-amino-2-sulfophenyl)benzenesulfonic acid

Tetramethylbenzidine

2,2'-difluoro-benzidine

