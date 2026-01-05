# Assignment A08 - ChEMBL SMILES Explorer

This assignment builds a Flask web application that accepts a SMILES string, queries the public ChEMBL web services (via `chembl_webresource_client`), and reports the first matching compound in a structured, browser-based report. All functionality is implemented inside functions, and the script exposes a CLI entry point through `if __name__ == '__main__': main(sys.argv)` as required.

Prerequisites
-------------

- Git installed (to clone the repository)
- Python 3.10 or newer available on PATH
- Internet connectivity (the app contacts https://www.ebi.ac.uk/chembl/ws at runtime)

How to clone from GitHub
------------------------

Clone the repository and navigate to the assignment folder:

```bash
git clone https://github.com/janre271/CI2.git
cd CI2/A08
```

Quick steps to run the app
--------------------------

**Step 1:** Create and activate a virtual environment (recommended)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Step 2:** Install Python dependencies

```bash
pip install -r requirements.txt
```

This pulls in Flask 3.0.0, chembl-webresource-client 0.10.9, and Werkzeug 3.0.1.

**Step 3:** Launch the Flask server

```bash
python app.py          # default port 5000
python app.py 8080     # run on a custom port
```

**Step 4:** Open the web UI

Visit `http://localhost:PORT`, enter any SMILES string (for example, `OC(=O)CCCCCCCC(=O)O`), and submit the form. The response shows the compound overview, physicochemical properties, synonyms, and structure identifiers. The form remains visible for repeated searches without reloading the page.

How it works
------------

1. The Flask route (`/`) renders `templates/index.html`, which contains the SMILES input form and the result sections.
2. On POST, the server calls `search_chembl(smiles)` which uses `chembl_webresource_client.new_client.molecule.filter` to request the first compound that flex-matches the given SMILES.
3. `_prepare_compound_payload()` extracts the subset of ChEMBL fields used in the UI (IDs, synonyms, molecular properties, structure identifiers).
4. The template displays the resulting dictionary in four stacked sections so the compound dossier is immediately readable.

Files included
--------------

```
A08/
├── app.py           # Flask application and helper functions
├── requirements.txt # Python dependencies for pip install -r
├── templates/
│   └── index.html   # Form + compound report UI
└── README.md        # Assignment description and run instructions
```

Example page content (Azelaic Acid)
-----------------------------------

Use the following text snapshot—obtained by searching for azelaic acid (`OC(=O)CCCCCCCC(=O)O`)—to validate that your deployment renders the same content:

```
Compound Overview
ChEMBL ID: CHEMBL1238
Preferred Name: AZELAIC ACID
Molecule Type: Small molecule
Max Phase: 4.0

Key Properties
Formula: C9H16O4
Molecular Weight: 188.22
ALogP: 1.89
H-Bond Acceptors: 2
H-Bond Donors: 2
Polar Surface Area: 74.60
Rotatable Bonds: 8
Ro5 Violations: 0

Synonyms
Acide azelaique, Acido azelaico, Anchoic acid, Azelaic acid, Azelaic acid

Structure Identifiers
SMILES: O=C(O)CCCCCCCC(=O)O
InChI: InChI=1S/C9H16O4/c10-8(11)6-4-2-1-3-5-7-9(12)13/h1-7H2,(H,10,11)(H,12,13)
InChI Key: BDJRBEYXGGNYIS-UHFFFAOYSA-N
```
