# Assignment A10 - ChEMBL 3D Explorer with Playwright Tests

This assignment extends A09 with comprehensive end-to-end tests using Playwright and pytest.

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
cd /mnt/c/Users/YourUsername/path/to/CI2/A10
```

Then follow the Ubuntu/WSL instructions below.

**Note:** For running tests, you'll need two WSL terminals:
- Terminal 1: Run the Flask server
- Terminal 2: Run pytest

Open a second PowerShell window and run `wsl` to get a second WSL terminal.

---

## Running in Ubuntu/WSL

All commands below should be executed inside Ubuntu or WSL (not Windows PowerShell).

### Step 1: Clone the repository

```bash
git clone https://github.com/janre271/CI2.git
cd CI2/A10
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

### Step 5: Install Playwright browsers

```bash
playwright install chromium --with-deps
```

If you encounter errors about missing dependencies (e.g., `libasound2`), install them manually:

```bash
sudo apt-get install -y libnss3 libnspr4 libasound2t64
playwright install chromium
```

### Step 6: Run the Flask server (Terminal 1)

```bash
python app.py 5000
```

### Step 7: Run tests (Terminal 2)

Open another terminal, activate the venv, and run:

```bash
source .venv/bin/activate
pytest tests/test_web.py -v
```

## Test Coverage

The tests verify:
1. Page loads correctly
2. Form data is read correctly (SMILES input processing)
3. Correct data obtained from ChEMBL server
4. Picture of the molecule is created and displayed
