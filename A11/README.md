# Assignment A11 - ChEMBL 3D Explorer with Django

This assignment implements a Django web application with three main pages for exploring molecular structures using SMILES notation, querying the ChEMBL database, and generating 3D visualizations with POV-Ray.

Prerequisites
-------------

- Git installed (to clone the repository)
- Python 3.10 or newer available on PATH
- `obabel` (Open Babel 3.x) CLI installed and on PATH
- `povray` 3.7+ CLI installed and on PATH
- Internet connectivity (the app contacts https://www.ebi.ac.uk/chembl/ws at runtime)

Installing CLI dependencies
---------------------------

> **Why CLI tools?** The 3D visualization feature requires Open Babel and POV-Ray. The Django server shells out to those commands to generate molecule images.

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

Validate the installation with `obabel -V` and `povray -V` before running the Django server.

> **Important for WSL users**: Copy the `babel_povray3.inc` include file into POV-Ray's search path:
> ```bash
> sudo cp /usr/share/openbabel/3.1.1/babel_povray3.inc /usr/share/povray-3.7/include/
> ```

How to clone from GitHub
------------------------

Clone the repository and navigate to the assignment folder:

```bash
git clone https://github.com/janre271/CI2.git
cd CI2/A11
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

This pulls in Django 5.0.1 and chembl-webresource-client 0.10.9.

**Step 3:** Apply database migrations

```bash
python manage.py migrate
```

This creates the SQLite database and tables for storing SMILES query history.

**Step 4:** (Optional) Create a superuser for admin access

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. This allows you to access the Django admin panel at `/admin/`.

**Step 5:** Run the development server

```bash
python manage.py runserver
```

The server will start on `http://127.0.0.1:8000/` by default.

**Step 6:** Open the web application

Visit `http://127.0.0.1:8000/` in your browser.

Application features
-------------------

### Page A: Home Page

The home page (`/`) provides:
- Welcome message and overview of the application
- Navigation links to ChEMBL Search and 3D Visualization pages
- Example SMILES strings for testing
- Description of each feature

### Page B: ChEMBL Database Search

The ChEMBL page (`/chembl/`) allows users to:
- Enter a SMILES string to query the ChEMBL database
- View comprehensive molecular information including:
  - Chemical identifiers (ChEMBL ID, preferred name)
  - Molecular properties (formula, weight, ALogP, etc.)
  - Pharmacological data (max phase, molecule type)
  - Structure identifiers (SMILES, InChI, InChI Key)
  - Synonyms
- **Database logging**: Every SMILES query is automatically saved to the database with a timestamp
- View recent search history (last 10 queries)

### Page C: 3D Molecular Visualization

The POV-Ray page (`/povray/`) enables users to:
- Enter a SMILES string to generate a 3D molecular structure
- Uses Open Babel to convert SMILES to 3D coordinates
- Uses POV-Ray to render high-quality ball-and-stick models
- Generated images are saved to the `media/` directory
- Images are displayed directly in the browser

How it works
------------

1. **Django Templates**: The application uses template inheritance. `base.html` provides the layout with header and navigation menu. The `home.html`, `chembl.html`, and `povray.html` templates extend the base template and define only their main content.

2. **ChEMBL Integration**: The `chembl()` view uses the `chembl_webresource_client` to query the ChEMBL API. Results are processed and displayed in a structured format.

3. **Database**: The `SmilesQuery` model stores each SMILES search with a timestamp. This is automatically saved when a user submits a query on the ChEMBL page.

4. **3D Visualization**: The `povray()` view:
   - Validates the SMILES input
   - Uses `obabel` to convert SMILES to a POV-Ray scene file
   - Adjusts camera positioning and molecule rotation
   - Renders the scene with `povray` to generate a PNG image
   - Stores the image in the `media/` directory
   - Returns the image URL to be displayed in the template

5. **URL Routing**: The project uses Django's URL configuration to route requests:
   - `/` → Home page
   - `/chembl/` → ChEMBL search page
   - `/povray/` → 3D visualization page
   - `/admin/` → Django admin panel


Example usage
-------------

**ChEMBL Search Examples:**
- Aspirin: `CC(=O)Oc1ccccc1C(=O)O`
- Caffeine: `CN1C=NC2=C1C(=O)N(C(=O)N2C)C`
- Glucose: `C(C1C(C(C(C(O1)O)O)O)O)O`

**3D Visualization Examples:**
- Benzene: `c1ccccc1`
- Methane: `C`
- Ethanol: `CCO`

Troubleshooting
---------------

- **`obabel`/`povray` not found**: Install the tools and restart the terminal so PATH updates. The 3D visualization will show an error message until resolved.
- **babel_povray3.inc missing**: Run `sudo cp /usr/share/openbabel/3.1.1/babel_povray3.inc /usr/share/povray-3.7/include/` to copy the include file into POV-Ray's search path.
- **ChEMBL API timeout**: The ChEMBL web service may be slow or unavailable. Try again after a few moments.
- **Database errors**: Delete `db.sqlite3` and run `python manage.py migrate` again to recreate the database.
- **Static files warning**: This is normal in development. Django will still serve static files correctly.

Admin panel
-----------

After creating a superuser (Step 4), you can access the admin panel at `http://127.0.0.1:8000/admin/` to:
- View all SMILES queries stored in the database
- Filter queries by timestamp
- Search for specific SMILES strings
- Manually add or delete query records
