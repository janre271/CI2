# Assignment A11 - ChEMBL 3D Explorer with Django

A Django web application with three pages for exploring molecular structures using SMILES notation, querying the ChEMBL database, and generating 3D visualizations with POV-Ray.

## Prerequisites

- **Ubuntu/Debian or WSL** (recommended environment)
- Python 3.10 or newer
- `obabel` (Open Babel 3.x) installed and on PATH
- `povray` 3.7+ installed and on PATH
- Internet connectivity (the app contacts https://www.ebi.ac.uk/chembl/ws)

## Running from Windows PowerShell with WSL

If you're on Windows, you can run the application through WSL directly from PowerShell:

### Step 1: Open WSL from PowerShell

```powershell
wsl
```

### Step 2: Navigate to the project (adjust path as needed)

```bash
cd /mnt/c/Users/YourUsername/path/to/CI2/A11
```

Then follow the Ubuntu/WSL instructions below.

---

## Running in Ubuntu/WSL

All commands below should be executed inside Ubuntu or WSL (not Windows PowerShell).

### Step 1: Clone the repository

```bash
git clone https://github.com/janre271/CI2.git
cd CI2/A11
```

### Step 2: Install system dependencies

```bash
sudo apt update
sudo apt install -y openbabel povray
```

### Step 3: Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 4: Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Apply database migrations

```bash
python manage.py migrate
```

### Step 6: Run the Django server

```bash
python manage.py runserver
```

### Step 7: Open in browser

Visit `http://127.0.0.1:8000/` in your browser.

## Application Features

### Page A: Home Page (/)

- Welcome text and overview of the application
- Navigation links to ChEMBL Search and 3D Visualization pages
- Example SMILES strings for testing

### Page B: ChEMBL Search (/chembl/)

- Enter a SMILES string to query the ChEMBL database
- View molecular information (formula, weight, synonyms, identifiers)
- Each SMILES query is saved to the database with timestamp
- View recent search history (last 10 queries)

### Page C: POV-Ray 3D Visualization (/povray/)

- Enter a SMILES string to generate 3D molecular structure
- Uses Open Babel to convert SMILES to 3D coordinates
- Uses POV-Ray to render ball-and-stick models
- Generated images displayed directly in browser

