# A04

Create a local SQLite database (`db.sqlite`) from three semicolon-delimited CSV files and answer:

"In what countries is used the Spanish language? Provide their full names, sorted alphabetically." 

Prerequisites
-------------
- Python 3.8 or newer installed
	- Check with: `python --version`
- Git installed (to clone the repository)
- CSV files: `country.csv`, `countrylanguage.csv`, `city.csv` (semicolon `;` as delimiter; first line = headers)
- Place all three CSV files in the same folder as the script `db.py` (the `A04` directory)

Clone from GitHub
-----------------
```powershell
# Clone the repository via HTTPS
git clone https://github.com/janre271/CI2.git
cd CI2

Quick steps to run
------------------
```powershell
# 1. Create and activate a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate   # Windows
## On Linux/macOS: source venv/bin/activate

# 2. Go to the assignment folder
cd A04

# 3. Ensure the CSV files are in this folder (same directory as db.py):
#    country.csv, countrylanguage.csv, city.csv

# 4. Run the importer by passing the filenames (no folders needed)
python db.py country.csv countrylanguage.csv city.csv

# 5. Re-run later (idempotent)
#    If the database already exists, you can simply run without arguments to print the answer again
python db.py
```

Expected output (example)
-------------------------
You should see the question followed by an alphabetically sorted list of country names where Spanish is used. Example snippet:
```
In what countries is used the Spanish language? Provide their full names, sorted alphabetically.
Answer:
Argentina
Chile
Colombia
... (more countries) ...
Spain
Uruguay
```

How it works
------------
1. Reads each CSV and creates a table named after the file (without extension) if it doesn't exist yet.
2. Stores all columns as TEXT (simplifies import; acceptable for the query).
3. Inserts rows in bulk within a transaction.
4. Executes a JOIN query to list country names where `Language = 'Spanish'` in `countrylanguage`.


Troubleshooting
---------------
- "File not found"? Make sure you are in the `A04` folder and that the three CSV files are in the same folder as `db.py`.
- Empty output? Confirm `countrylanguage.csv` was imported and actually contains Spanish entries.
- Re-running doesn't duplicate rows – tables are skipped if they already exist.
- Need to reset? Delete `db.sqlite` and run the command again.

