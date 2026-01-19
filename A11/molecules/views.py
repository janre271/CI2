"""Views for the molecules application."""
from __future__ import annotations

import re
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, Iterable, Optional
from uuid import uuid4

from chembl_webresource_client.new_client import new_client
from django.conf import settings
from django.shortcuts import render

from .models import SmilesQuery


class MoleculeImageError(RuntimeError):
    """Raised when obabel or povray fail to render."""


def home(request):
    """Render the home page with navigation."""
    return render(request, 'molecules/home.html')


def _extract_synonyms(raw_synonyms: Optional[Iterable[Any]]) -> str:
    """Return a readable, comma-separated string of up to five synonyms."""
    names = []
    for entry in list(raw_synonyms or [])[:5]:
        if isinstance(entry, dict):
            entry = entry.get("molecule_synonym")
        if entry:
            names.append(str(entry))
    return ", ".join(names) if names else "N/A"


def _prepare_compound_payload(compound: Dict[str, Any]) -> Dict[str, Any]:
    """Extract only the fields we show on the page."""
    properties = compound.get("molecule_properties") or {}
    structures = compound.get("molecule_structures") or {}
    grab = properties.get

    return {
        "chembl_id": compound.get("molecule_chembl_id", "N/A"),
        "pref_name": compound.get("pref_name", "N/A"),
        "synonyms": _extract_synonyms(compound.get("molecule_synonyms")),
        "molecular_formula": grab("full_molformula", "N/A"),
        "molecular_weight": grab("full_mwt", "N/A"),
        "alogp": grab("alogp", "N/A"),
        "hba": grab("hba", "N/A"),
        "hbd": grab("hbd", "N/A"),
        "psa": grab("psa", "N/A"),
        "rtb": grab("rtb", "N/A"),
        "num_ro5_violations": grab("num_ro5_violations", "N/A"),
        "ro3_pass": grab("ro3_pass", "N/A"),
        "molecule_type": compound.get("molecule_type", "N/A"),
        "max_phase": compound.get("max_phase", "N/A"),
        "smiles": structures.get("canonical_smiles", "N/A"),
        "inchi": structures.get("standard_inchi", "N/A"),
        "inchi_key": structures.get("standard_inchi_key", "N/A"),
    }


def search_chembl_api(smiles: str) -> Optional[Dict[str, Any]]:
    """Return the first compound matching the provided SMILES string."""
    results = new_client.molecule.filter(
        molecule_structures__canonical_smiles__flexmatch=smiles
    )
    return _prepare_compound_payload(results[0]) if results else None


def chembl(request):
    """Handle ChEMBL SMILES search and save to database."""
    compound = None
    error = None
    smiles_input = ''
    
    if request.method == 'POST':
        smiles_input = request.POST.get('smiles', '').strip()
        
        if smiles_input:
            # Save to database
            SmilesQuery.objects.create(smiles=smiles_input)
            
            try:
                compound = search_chembl_api(smiles_input)
                if not compound:
                    error = f"No compound found for SMILES: {smiles_input}"
            except Exception as e:
                error = f"Error querying ChEMBL: {str(e)}"
        else:
            error = "Please enter a SMILES string"
    
    # Get recent queries
    recent_queries = SmilesQuery.objects.all()[:10]
    
    context = {
        'compound': compound,
        'error': error,
        'smiles_input': smiles_input,
        'recent_queries': recent_queries,
    }
    
    return render(request, 'molecules/chembl.html', context)


def _ensure_binary(name: str) -> None:
    """Raise an informative error if the command is unavailable in WSL."""
    try:
        result = subprocess.run(
            ["wsl", "-d", "Ubuntu", "bash", "-c", f"which {name}"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise MoleculeImageError(
                f"Required command '{name}' is not available in WSL. Install it first with: sudo apt install {name}"
            )
    except FileNotFoundError:
        raise MoleculeImageError(
            "WSL is not available. Please ensure WSL is installed and Ubuntu distribution is set up."
        )


def _run_command(command: list, error_hint: str) -> None:
    """Execute a CLI tool and raise MoleculeImageError on failure."""
    # Run commands through WSL - use shlex.quote to properly escape all arguments
    escaped_args = " ".join(shlex.quote(str(arg)) for arg in command)
    wsl_command = ["wsl", "-d", "Ubuntu", "bash", "-c", escaped_args]
    
    try:
        subprocess.run(
            wsl_command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except FileNotFoundError as exc:
        raise MoleculeImageError(
            f"Command '{command[0]}' is missing. Install the dependency and retry."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise MoleculeImageError(f"{error_hint}: {exc.stdout.strip()}") from exc


def generate_molecule_image(smiles: str) -> str:
    """Use obabel + povray to render a 3D PNG into media directory."""
    _ensure_binary("obabel")
    _ensure_binary("povray")

    media_root = Path(settings.MEDIA_ROOT)
    media_root.mkdir(parents=True, exist_ok=True)

    suffix = uuid4().hex
    pov_path = media_root / f"mol_{suffix}.pov"
    png_path = media_root / f"mol_{suffix}.png"

    # Convert Windows paths to WSL paths
    def to_wsl_path(path: Path) -> str:
        """Convert Windows path to WSL path format."""
        path_str = str(path.resolve())
        # C:\Users\... -> /mnt/c/Users/...
        if len(path_str) > 1 and path_str[1] == ':':
            drive = path_str[0].lower()
            rest = path_str[2:].replace('\\', '/')
            return f"/mnt/{drive}{rest}"
        return path_str

    wsl_pov_path = to_wsl_path(pov_path)
    wsl_png_path = to_wsl_path(png_path)

    obabel_cmd = ["obabel", f"-:{smiles}", "--gen3d", "-O", wsl_pov_path, "-xc"]
    povray_cmd = [
        "povray",
        f"+I{wsl_pov_path}",
        f"+O{wsl_png_path}",
        "+W800",
        "+H600",
        "+D",
        "+A",
        "+FN",
    ]

    _run_command(obabel_cmd, "Open Babel failed to convert the SMILES")

    # Adjust POV-Ray scene for better framing
    pov_content = pov_path.read_text()
    pov_content = pov_content.replace("union {", "union {\n  rotate <0, 90, 0>", 1)
    
    # Replace the entire camera block
    camera_block = 'camera {\n  location <0, 0, 18>\n  look_at <0, 0, 0>\n  right x*image_width/image_height\n}'
    pov_content = re.sub(
        r'camera\s*\{[^}]*\}',
        camera_block,
        pov_content,
        count=1
    )
    pov_path.write_text(pov_content)

    try:
        _run_command(povray_cmd, "POV-Ray failed to render the molecule")
    finally:
        if pov_path.exists():
            try:
                pov_path.unlink()
            except OSError:
                pass

    if not png_path.exists():
        raise MoleculeImageError("POV-Ray did not produce an image file.")

    return f"mol_{suffix}.png"


def povray(request):
    """Handle POV-Ray 3D molecule image generation."""
    image_url = None
    error = None
    smiles_input = ''
    
    if request.method == 'POST':
        smiles_input = request.POST.get('smiles', '').strip()
        
        if smiles_input:
            try:
                image_filename = generate_molecule_image(smiles_input)
                image_url = f"{settings.MEDIA_URL}{image_filename}"
            except MoleculeImageError as e:
                error = str(e)
            except Exception as e:
                error = f"Error generating image: {str(e)}"
        else:
            error = "Please enter a SMILES string"
    
    context = {
        'image_url': image_url,
        'error': error,
        'smiles_input': smiles_input,
    }
    
    return render(request, 'molecules/povray.html', context)
