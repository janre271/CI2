# Assignment 07

This assignment creates a POV-Ray visualization of four glycine molecules arranged at the vertices of a square. The glycine molecular structure is defined using SMILES notation, converted to POV-Ray format using OpenBabel.

Prerequisites
-------------

- Python 3.7 or newer installed
- Git installed (to clone the repository)
- OpenBabel (command-line tool for molecular structure conversion)


How to clone from GitHub
-----------------

Clone the repository and navigate to the assignment folder:

```bash
git clone https://github.com/janre271/CI2.git
cd CI2/A07
```

Quick steps to run the script 
------------------

**Step 1:** Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

On Linux/macOS:
```bash
source venv/bin/activate
```

**Step 2:** Install required Python dependencies

```bash
pip install -r requirements.txt
```

**Step 3:** Install OpenBabel (for molecular structure conversion)

```bash
# Windows (conda):
conda install -c conda-forge openbabel

# Linux/Ubuntu:
sudo apt-get install openbabel

# macOS:
brew install open-babel
```

**Step 4:** Install POV-Ray (for rendering)

- **Windows:** Download and install from http://www.povray.org/download/
- **Linux:** `sudo apt-get install povray`
- **macOS:** `brew install povray`

**Step 5:** Convert SMILES to POV-Ray format

```bash
obabel glycine.smi -O glycine.pov --gen3D
```

This converts the glycine SMILES structure to POV-Ray format with 3D coordinates.

How it works
------------

1. **glycine.smi** contains the SMILES notation for glycine: `C(C(=O)O)N`
2. **OpenBabel** converts SMILES to POV-Ray format with 3D coordinates
3. **glycine.pov** defines the molecular structure with atoms and bonds
4. **gly4.pov** includes glycine.pov and places four molecules at square vertices
5. **babel_povray3.inc** provides POV-Ray definitions for atoms and bonds
---------------

After rendering, you should see:

```
POV-Ray rendering output...
Render complete
```