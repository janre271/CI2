"""
Flask web application for searching chemical compounds in ChEMBL database using SMILES.
"""

import sys
from flask import Flask, render_template, request
from chembl_webresource_client.new_client import new_client


def extract_synonyms(synonyms_list):
    """
    Extract synonym strings from the synonyms list.
    
    Args:
        synonyms_list (list): List of synonym objects or strings
        
    Returns:
        str: Comma-separated list of synonyms or 'N/A'
    """
    if not synonyms_list:
        return 'N/A'
    
    syn_list = []
    for s in synonyms_list[:5]:
        if isinstance(s, dict):
            syn_list.append(s.get('molecule_synonym', ''))
        else:
            syn_list.append(str(s))
    
    return ', '.join(filter(None, syn_list)) if syn_list else 'N/A'


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        """Main page with SMILES input form and results display."""
        compound_info = None
        error_message = None
        smiles_input = None
        
        if request.method == 'POST':
            smiles_input = request.form.get('smiles', '').strip()
            
            if smiles_input:
                try:
                    compound_info = search_chembl(smiles_input)
                    if not compound_info:
                        error_message = "No compound found for the given SMILES."
                except Exception as e:
                    error_message = f"Error searching ChEMBL database: {str(e)}"
            else:
                error_message = "Please enter a SMILES string."
        
        return render_template('index.html', 
                             compound_info=compound_info, 
                             error_message=error_message,
                             smiles_input=smiles_input)
    
    return app


def search_chembl(smiles):
    """
    Search ChEMBL database for compound information using SMILES.
    
    Args:
        smiles (str): SMILES notation of the chemical compound
        
    Returns:
        dict: Dictionary containing compound information or None if not found
    """
    try:
        # Create a molecule client
        molecule = new_client.molecule
        
        # Search for compounds with similar structure
        results = molecule.filter(molecule_structures__canonical_smiles__flexmatch=smiles)
        
        # Get the first result
        if results:
            compound = results[0]
            
            # Extract relevant information
            compound_info = {
                'chembl_id': compound.get('molecule_chembl_id', 'N/A'),
                'pref_name': compound.get('pref_name', 'N/A'),
                'synonyms': extract_synonyms(compound.get('molecule_synonyms', [])),
                'molecular_formula': compound.get('molecule_properties', {}).get('full_molformula', 'N/A') if compound.get('molecule_properties') else 'N/A',
                'molecular_weight': compound.get('molecule_properties', {}).get('full_mwt', 'N/A') if compound.get('molecule_properties') else 'N/A',
                'smiles': compound.get('molecule_structures', {}).get('canonical_smiles', 'N/A') if compound.get('molecule_structures') else 'N/A',
                'inchi': compound.get('molecule_structures', {}).get('standard_inchi', 'N/A') if compound.get('molecule_structures') else 'N/A',
                'inchi_key': compound.get('molecule_structures', {}).get('standard_inchi_key', 'N/A') if compound.get('molecule_structures') else 'N/A',
                'alogp': compound.get('molecule_properties', {}).get('alogp', 'N/A') if compound.get('molecule_properties') else 'N/A',
                'hba': compound.get('molecule_properties', {}).get('hba', 'N/A') if compound.get('molecule_properties') else 'N/A',
                'hbd': compound.get('molecule_properties', {}).get('hbd', 'N/A') if compound.get('molecule_properties') else 'N/A',
                'psa': compound.get('molecule_properties', {}).get('psa', 'N/A') if compound.get('molecule_properties') else 'N/A',
                'rtb': compound.get('molecule_properties', {}).get('rtb', 'N/A') if compound.get('molecule_properties') else 'N/A',
                'ro3_pass': compound.get('molecule_properties', {}).get('ro3_pass', 'N/A') if compound.get('molecule_properties') else 'N/A',
                'num_ro5_violations': compound.get('molecule_properties', {}).get('num_ro5_violations', 'N/A') if compound.get('molecule_properties') else 'N/A',
                'molecule_type': compound.get('molecule_type', 'N/A'),
                'max_phase': compound.get('max_phase', 'N/A'),
            }
            
            return compound_info
        
        return None
        
    except Exception as e:
        raise Exception(f"ChEMBL search failed: {str(e)}")


def main(port=5000):
    """
    Main function to run the Flask application.
    
    Args:
        port (int): Port number for the Flask server (default: 5000)
    """
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=port)


if __name__ == '__main__':
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}. Using default port 5000.")
            port = 5000
    
    main(port)
