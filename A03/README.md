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

The expected output is a list of compound names found in the HTML file.

