"""Flask web UI for querying ChEMBL compounds by SMILES."""

from __future__ import annotations

import sys
from typing import Any, Dict, Iterable, List, Optional

from flask import Flask, render_template, request
from chembl_webresource_client.new_client import new_client


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


def create_app() -> Flask:
    """Create and configure the Flask application instance."""
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        smiles_value = ""
        compound_info = None
        error_message = None

        if request.method == "POST":
            smiles_value = request.form.get("smiles", "").strip()

            if not smiles_value:
                error_message = "Please enter a SMILES string before submitting."
            else:
                try:
                    compound_info = search_chembl(smiles_value)
                    if not compound_info:
                        error_message = "No compound was found for the provided SMILES string."
                except Exception as exc:  # pragma: no cover - defensive guard
                    error_message = f"Unable to contact ChEMBL services: {exc}"

        return render_template(
            "index.html",
            compound_info=compound_info,
            error_message=error_message,
            smiles_input=smiles_value,
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
