# Assignment A10 - ChEMBL 3D Explorer with Playwright Tests

This assignment extends the ChEMBL 3D Explorer from A09 by implementing comprehensive end-to-end tests using Playwright and pytest. The test suite validates form input processing, ChEMBL API integration, and 3D molecule image generation through automated browser interactions.

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
cd CI2/A10
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

This pulls in Flask 3.0.0, chembl-webresource-client 0.10.9, Werkzeug 3.0.1, pytest 7.4.3, pytest-playwright 0.4.3, and playwright 1.40.0.

**Step 3:** Install Playwright browser binaries

```bash
playwright install chromium
```

For WSL/Linux users, install with system dependencies:

```bash
playwright install chromium --with-deps
```

**Step 4:** Launch the Flask server

```bash
python app.py 5000     # run on port 5000 (required for tests)
python app.py 8080     # run on a custom port
```

**Step 5:** Open the web UI

Visit `http://localhost:5000`, enter any SMILES string (for example, `CC(=O)Oc1ccccc1C(=O)O`), and click "Generate dossier". The page performs a JavaScript `fetch` to `/api/compound`. The backend will:

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

**Note on rendering**: Open Babel's POV-Ray export generates 3D ball-and-stick models but does not visually distinguish double bonds from single bonds in the final image. The structural geometry is correct, but C=O carbonyl groups and other multiple bonds appear as standard cylinders.

Running the tests
-----------------

The test suite uses Playwright for automated browser testing. **Important**: The Flask server must be running on port 5000 before executing tests.

**Terminal 1:** Start the server

```bash
python app.py 5000
```

**Terminal 2:** Run all tests

```bash
pytest tests/test_web.py -v
```

**Expected output:** All 10 tests should pass.

### Test coverage

The test suite (`tests/test_web.py`) verifies:

1. **test_page_loads** - Page loads correctly with proper title and elements
2. **test_search_with_molecule_name_aspirin** - Searching by molecule name
3. **test_search_with_smiles_aspirin** - Searching for aspirin using SMILES notation
4. **test_search_with_smiles_caffeine** - Caffeine search and image generation verification
5. **test_search_with_benzene** - Benzene search and result component verification
6. **test_empty_search** - Error handling for empty searches
7. **test_invalid_smiles** - Error handling for invalid SMILES strings
8. **test_ui_elements_present** - All main UI elements are present
9. **test_multiple_searches_sequentially** - Multiple searches in sequence
10. **test_page_responsiveness** - Page remains responsive during and after search

Each test verifies the three key requirements:
- Form data is read correctly (SMILES input processing)
- Correct data obtained from ChEMBL server (API integration)
- Picture of the molecule is created and displayed (image generation)

### Additional test options

Run specific test:
```bash
pytest tests/test_web.py::test_search_with_smiles_aspirin -v
```

Run tests matching a pattern:
```bash
pytest tests/test_web.py -k "search" -v
```

Run tests in headed mode (see the browser):
```bash
pytest tests/test_web.py --headed
```

Files included
--------------

```
A10/
├── .gitignore                  # Git ignore patterns
├── app.py                      # Flask application, JSON API, and helper functions
├── pytest.ini                  # Pytest configuration (sets base URL to localhost:5000)
├── requirements.txt            # Python dependencies for pip install -r
├── README.md                   # Assignment description and run instructions
├── static/
│   └── generated/
│       └── .gitkeep            # Ensures the image directory exists in git
├── templates/
│   └── index.html              # Single-page UI with JavaScript fetch workflow
└── tests/
    ├── conftest.py             # Pytest fixtures and configuration
    └── test_web.py             # Playwright test suite (10 tests)
```

Troubleshooting
---------------

- **`obabel`/`povray` not found**: Install the tools and restart the terminal so PATH updates. The API will respond with `Required command 'obabel' is not available on PATH. Install it first.` until resolved.
- **babel_povray3.inc missing**: Run `sudo cp /usr/share/openbabel/3.1.1/babel_povray3.inc /usr/share/povray-3.7/include/` to copy the include file into POV-Ray's search path.
- **Tests fail with "Connection Refused"**: Make sure the Flask server is running on `http://localhost:5000` before running tests.
- **Playwright browser not installed**: Run `playwright install chromium` (or `playwright install chromium --with-deps` for WSL/Linux).
- **Tests timeout**: Some tests may take longer if the ChEMBL API is slow. The tests include appropriate timeouts and wait conditions.
- **WSL file paths**: When running inside WSL, keep the repo in the Linux filesystem (`~/CI2/A10`) so POSIX paths work for POV-Ray.

