"""Flask API + UI for querying ChEMBL and rendering molecule images."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from uuid import uuid4

from chembl_webresource_client.new_client import new_client
from flask import Flask, jsonify, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
GENERATED_DIR = STATIC_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


class MoleculeImageError(RuntimeError):
    """Raised when obabel or povray fail to render."""


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


def search_chembl(smiles: str) -> Optional[Dict[str, Any]]:
    """Return the first compound matching the provided SMILES string."""
    results = new_client.molecule.filter(
        molecule_structures__canonical_smiles__flexmatch=smiles
    )
    return _prepare_compound_payload(results[0]) if results else None


def _ensure_binary(name: str) -> None:
    """Raise an informative error if the command is unavailable."""
    if shutil.which(name) is None:
        raise MoleculeImageError(
            f"Required command '{name}' is not available on PATH. Install it first."
        )


def _run_command(command: List[str], error_hint: str) -> None:
    """Execute a CLI tool and raise MoleculeImageError on failure."""
    try:
        subprocess.run(
            command,
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
    """Use obabel + povray to render a 3D PNG into static/generated."""
    _ensure_binary("obabel")
    _ensure_binary("povray")

    suffix = uuid4().hex
    pov_path = GENERATED_DIR / f"mol_{suffix}.pov"
    png_path = GENERATED_DIR / f"mol_{suffix}.png"

    obabel_cmd = ["obabel", f"-:{smiles}", "--gen3d", "-O", str(pov_path), "-xc"]
    povray_cmd = [
        "povray",
        f"+I{pov_path}",
        f"+O{png_path}",
        f"+L{BASE_DIR}",
        "+W800",
        "+H600",
        "+D",
        "+A",
        "+FN",
    ]

    _run_command(obabel_cmd, "Open Babel failed to convert the SMILES")

    # Don't modify the POV-Ray file - use obabel's defaults
    # The camera and molecule positioning are already correct from obabel

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

    return png_path.relative_to(STATIC_DIR).as_posix()


def create_app() -> Flask:
    """Create and configure the Flask application instance."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.get("/")
    def index() -> str:
        return render_template("index.html")

    @app.post("/api/compound")
    def api_compound():
        payload = request.get_json(silent=True) or {}
        smiles_value = str(payload.get("smiles", "")).strip()

        if not smiles_value:
            return jsonify({"error": "SMILES string is required."}), 400

        try:
            compound_info = search_chembl(smiles_value)
        except Exception as exc:  # pragma: no cover - external service guard
            return jsonify({"error": f"Unable to contact ChEMBL services: {exc}"}), 502

        if not compound_info:
            return jsonify({"error": "No compound was found for the provided SMILES."}), 404

        try:
            image_rel_path = generate_molecule_image(smiles_value)
        except MoleculeImageError as exc:
            return jsonify({"error": str(exc)}), 500

        image_url = url_for("static", filename=image_rel_path)
        return jsonify(
            {
                "compound": compound_info,
                "imageUrl": image_url,
                "smiles": smiles_value,
            }
        )

    return app


def main(argv: List[str]) -> None:
    """CLI entry point."""
    try:
        port = int(argv[1])
    except (IndexError, ValueError):
        port = 5000

    create_app().run(debug=True, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main(sys.argv)
