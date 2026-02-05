# Assignment A09 - ChEMBL 3D Explorer

This Flask web application accepts a SMILES string via JavaScript API, queries ChEMBL, and generates a 3D molecule image using Open Babel and POV-Ray.

## Prerequisites

- **Ubuntu/Debian or WSL**
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
cd /mnt/c/Users/YourUsername/path/to/CI2/A09
```

Then follow the Ubuntu/WSL instructions below.

---

## Running in Ubuntu/WSL

All commands below should be executed inside Ubuntu or WSL.

### Step 1: Clone the repository

```bash
git clone https://github.com/janre271/CI2.git
cd CI2/A09
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

### Step 5: Run the Flask server

```bash
python app.py
```

Or specify a custom port:

```bash
python app.py 8080
```

### Step 6: Open in browser

Visit `http://localhost:5000` (or your custom port), enter a SMILES string (e.g., `CC(=O)Oc1ccccc1C(=O)O` for Aspirin), and click submit.

The page sends a JavaScript API request to `/api/compound`. The backend:
1. Queries ChEMBL for compound information
2. Generates a 3D image using `obabel` and `povray`
3. Returns JSON with compound data and image URL
4. JavaScript updates the page without reloading

