# Assignment A08 - ChEMBL Compound Search Web Application

## Description

This Flask web application allows users to search for chemical compound information from the ChEMBL database using SMILES (Simplified Molecular Input Line Entry System) notation. The application provides a user-friendly web interface where users can enter SMILES strings and retrieve detailed compound information.

## Features

- Simple web form for entering SMILES notation
- Integration with ChEMBL Web API via the chembl_webresource_client Python package
- Display of comprehensive compound information including:
  - ChEMBL ID
  - Preferred name and synonyms
  - Molecular formula and weight
  - Chemical structure identifiers (SMILES, InChI, InChI Key)
  - Physicochemical properties (ALogP, H-bond acceptors/donors, polar surface area)
  - Drug-likeness metrics (Lipinski's Rule of Five violations)
  - Development phase information
- Responsive and visually appealing web interface

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/janre271/CI2.git
cd CI2/A08
```

### 2. Create a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0 - Web framework
- chembl-webresource-client 0.10.9 - ChEMBL API client
- Werkzeug 3.0.1 - WSGI utility library

## Running the Application

### Start the Flask Server

**Default port (5000):**
```bash
python app.py
```

**Custom port:**
```bash
python app.py 8080
```

The server will start and display:
```
 * Running on http://0.0.0.0:5000
```

### Access the Web Interface

Open your web browser and navigate to:
```
http://localhost:5000
```

## Using the Application

1. **Enter SMILES notation** in the input field on the main page
   - Example for aspirin: `CC(=O)Oc1ccccc1C(=O)O`
   - Example for azelaic acid: `OC(=O)CCCCCCCC(=O)O`

2. **Click "Search ChEMBL Database"** button

3. **View the results** displayed on the page, including:
   - Compound identification (ChEMBL ID, name)
   - Molecular properties
   - Chemical structure representations
   - Drug development information

4. **Perform a new search** by entering another SMILES string in the form at the top

## Example Output

### Search Query: Azelaic Acid
**SMILES:** `OC(=O)CCCCCCCC(=O)O`

**Compound Information Retrieved:**

- **ChEMBL ID:** CHEMBL1238
- **Preferred Name:** AZELAIC ACID
- **Molecule Type:** Small molecule
- **Max Phase:** 4.0
- **Molecular Formula:** C9H16O4
- **Molecular Weight:** 188.22
- **ALogP:** 1.89
- **H-Bond Acceptors:** 2
- **H-Bond Donors:** 2
- **Polar Surface Area:** 74.60
- **Rotatable Bonds:** 8
- **Ro5 Violations:** 0
- **Synonyms:** Acide azelaique, Acido azelaico, Anchoic acid, Azelaic acid, Azelaic acid
- **Canonical SMILES:** O=C(O)CCCCCCCC(=O)O
- **InChI Key:** BDJRBEYXGGNYIS-UHFFFAOYSA-N
- **Standard InChI:** InChI=1S/C9H16O4/c10-8(11)6-4-2-1-3-5-7-9(12)13/h1-7H2,(H,10,11)(H,12,13)

## Project Structure

```
A08/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Web interface template
└── .venv/                # Virtual environment (created during setup)
```

## Technical Details

- **Framework:** Flask 3.0.0
- **API:** ChEMBL Web Services (https://www.ebi.ac.uk/chembl/ws)
- **Python Version:** Python 3.7+
- **Architecture:** Function-based Flask application with modular design

## Troubleshooting

- **Port already in use:** Change the port number when starting the application: `python app.py 8080`
- **Module not found:** Ensure all dependencies are installed: `pip install -r requirements.txt`
- **No compound found:** Verify the SMILES notation is correct
- **API timeout:** Check internet connection and ChEMBL service availability

## Author

Created for CI2 Course - Assignment A08
Date: December 15, 2025
