# Assignment A09 - ChEMBL 3D Explorer

Prerequisites
-------------

- Git installed (to clone the repository)
- Python 3.10 or newer available on PATH
- `obabel` (Open Babel 3.x) CLI installed and on PATH
- `povray` 3.7+ CLI installed and on PATH
- Internet connectivity (the app contacts https://www.ebi.ac.uk/chembl/ws at runtime)

Installing CLI dependencies
---------------------------

> **Why CLI tools?** The assignment requires generating a 3D molecule image with Open Babel and POV-Ray. The Flask server shells out to those commands, stores the PNG in `static/generated/`, and returns its URL in the JSON payload.

Choose any method that keeps the binaries on PATH (native Linux, WSL, or Windows package managers):

- **Ubuntu / Debian / WSL**
  ```bash
  sudo apt update
  sudo apt install openbabel povray
  ```
- **macOS (Homebrew)**
  ```bash
  brew install open-babel povray
  ```
- **Windows (native PowerShell, Chocolatey)**
  ```powershell
  choco install openbabel povray
  ```
- **Windows (winget)**
  ```powershell
  winget install --id OpenBabel.OpenBabel
  winget install --id PersistenceOfVision.POVRay
  ```

Validate the installation with `obabel -V` and `povray -V` before running the Flask server. If either command is missing, the API will respond with an error message.

> **Important for WSL users**: Copy the `babel_povray3.inc` include file into POV-Ray's search path:
> ```bash
> sudo cp /usr/share/openbabel/3.1.1/babel_povray3.inc /usr/share/povray-3.7/include/
> ```

How to clone from GitHub
------------------------

Clone the repository and navigate to the assignment folder:

```bash
git clone https://github.com/janre271/CI2.git
cd CI2/A09
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

Visit `http://localhost:PORT`, enter any SMILES string (for example, `OC(=O)CCCCCCCC(=O)O`), and submit. The page performs a JavaScript `fetch` to `/api/compound`. The backend will:

1. Query ChEMBL via `chembl_webresource_client`.
2. Render a POV-Ray PNG using Open Babel + POV-Ray and store it in `static/generated/`.
3. Return JSON containing the curated compound fields plus the static image URL.

The browser overlays the results on the same page — no navigation, no reload.

How it works
------------

1. The Flask route (`GET /`) renders `templates/index.html`, which hosts the single-page UI with the SMILES input form.
2. On form submission, JavaScript calls `POST /api/compound` with the SMILES string in the request body.
3. The server calls `search_chembl(smiles)` which uses `chembl_webresource_client.new_client.molecule.filter` to request the first compound that flex-matches the given SMILES.
4. `_prepare_compound_payload()` extracts the subset of ChEMBL fields used in the UI (IDs, synonyms, molecular properties, structure identifiers).
5. `generate_molecule_image()` shells out to `obabel` (SMILES ➜ POV-Ray scene) and then to `povray` (scene ➜ PNG). The camera is adjusted to ensure the entire molecule fits in frame with proper rotation.
6. The API returns JSON containing the compound data and the image URL.
7. JavaScript updates the DOM with the new data and displays the rendered 3D image without reloading the page.

**Note on rendering**: Open Babel's POV-Ray export generates 3D ball-and-stick models but does not visually distinguish double bonds from single bonds in the final image. The structural geometry is correct, but C=O carbonyl groups and other multiple bonds appear as standard cylinders. For publication-quality visualization with clear double bond notation, specialized tools like PyMOL or ChimeraX would be required.

Files included
--------------

```
A09/
├── app.py                 # Flask application, JSON API, and helper functions
├── requirements.txt       # Python dependencies for pip install -r
├── README.md              # Assignment description and run instructions
├── static/
│   └── generated/
│       └── .gitkeep       # Ensures the image directory exists in git
└── templates/
    └── index.html         # Single-page UI with JavaScript fetch workflow
```

Troubleshooting
---------------

- **`obabel`/`povray` not found**: Install the tools and restart the terminal so PATH updates. The API will respond with `Required command 'obabel' is not available on PATH. Install it first.` until resolved.
- **babel_povray3.inc missing**: Run `sudo cp /usr/share/openbabel/3.1.1/babel_povray3.inc /usr/share/povray-3.7/include/` to copy the include file into POV-Ray's search path.
- **Slow rendering**: Large molecules can take a few seconds to render. The UI keeps the loading indicator visible until both ChEMBL and POV-Ray finish.
- **WSL file paths**: When running inside WSL, keep the repo in the Linux filesystem (`~/CI2/A09`) so POSIX paths work for POV-Ray.

