#!/usr/bin/env python3
"""
cdx2html.py - Convert CDXML files to PNG images and generate HTML index

This script converts ChemDraw XML (.cdxml) molecular structure files to PNG images
and generates an HTML index page displaying the structures in a table.

Uses OpenBabel/pybel for molecular structure processing and rendering.

Usage: python cdx2html.py <cdxml_files...>
Examples: 
    python cdx2html.py *.cdxml
    python cdx2html.py rx00005.cdxml rx00153.cdxml
    python cdx2html.py rx002*.cdxml
"""

import sys
import glob
import os
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from openbabel import pybel
except ImportError:
    print("Error: OpenBabel/pybel not available. Install with: pip install openbabel-wheel", file=sys.stderr)
    sys.exit(1)

# Try importing Indigo for high-quality rendering
try:
    from indigo import Indigo
    from indigo.renderer import IndigoRenderer
    INDIGO_AVAILABLE = True
except ImportError:
    INDIGO_AVAILABLE = False
    print("Warning: Indigo not available. Rendering will use PIL fallback. Install with: pip install epam.indigo", file=sys.stderr)

def cdxml_to_mol2(cdxml_file):
    """
    Convert CDXML to MOL2 format by parsing the XML structure
    
    Args:
        cdxml_file: Path to CDXML file
    
    Returns:
        str: Path to MOL2 file or None if conversion fails
    """
    try:
        tree = ET.parse(cdxml_file)
        root = tree.getroot()
        
        # Build a simple MOL file format
        mol_lines = []
        mol_lines.append(os.path.basename(cdxml_file))
        mol_lines.append("  Converted from CDXML")
        mol_lines.append("")
        
        # Collect nodes (atoms) and bonds
        nodes = {}
        bonds = []
        
        for node in root.iter():
            if node.tag.endswith('n'):
                node_id = node.get('id')
                pos_str = node.get('p', '0 0')
                pos = pos_str.split()
                if len(pos) >= 2:
                    element = node.get('Element', '6')
                    element_map = {
                        '1': 'H', '6': 'C', '7': 'N', '8': 'O', '9': 'F',
                        '13': 'Al', '14': 'Si', '15': 'P', '16': 'S', '17': 'Cl', '35': 'Br', '53': 'I'
                    }
                    element_symbol = element_map.get(element, 'C')
                    nodes[node_id] = {
                        'id': len(nodes) + 1,
                        'symbol': element_symbol,
                        'x': float(pos[0]),
                        'y': float(pos[1]),
                        'z': 0.0
                    }
        
        for bond in root.iter():
            if bond.tag.endswith('b'):
                begin_id = bond.get('B')
                end_id = bond.get('E')
                order = bond.get('Order', '1').split('.')[0]
                if begin_id in nodes and end_id in nodes:
                    bonds.append((nodes[begin_id]['id'], nodes[end_id]['id'], order))
        
        # Write counts line
        mol_lines.append(f"{len(nodes):3d}{len(bonds):3d}  0  0  0  0  0  0  0  0999 V2000")
        
        # Write atom block
        for node_id in sorted(nodes.keys(), key=lambda x: nodes[x]['id']):
            node = nodes[node_id]
            mol_lines.append(f"{node['x']:10.4f}{node['y']:10.4f}{node['z']:10.4f} {node['symbol']:<3s} 0  0  0  0  0  0  0  0  0  0  0  0")
        
        # Write bond block
        for begin, end, order in bonds:
            mol_lines.append(f"{begin:3d}{end:3d}{order:3s}  0  0  0  0")
        
        mol_lines.append("M  END")
        
        # Write to file
        mol_file = cdxml_file.replace('.cdxml', '.mol')
        with open(mol_file, 'w') as f:
            f.write('\n'.join(mol_lines))
        
        return mol_file
    except Exception as e:
        print(f"Error converting {cdxml_file} to MOL: {e}", file=sys.stderr)
        return None

def parse_cdxml_formula(cdxml_file):
    """
    Parse molecular formula from CDXML XML file using pybel
    
    Args:
        cdxml_file: Path to CDXML file
    
    Returns:
        str: Molecular formula or "N/A" if extraction fails
    """
    try:
        # Convert CDXML to MOL format first
        mol_file = cdxml_to_mol2(cdxml_file)
        if not mol_file or not os.path.exists(mol_file):
            return "N/A"
        
        # Read with pybel and get formula
        mol = next(pybel.readfile("mol", mol_file))
        formula = mol.formula
        
        # Clean up
        if os.path.exists(mol_file):
            os.remove(mol_file)
        
        return formula if formula else "N/A"
    except Exception as e:
        print(f"Error extracting formula from {cdxml_file}: {e}", file=sys.stderr)
        
        # Fallback: Parse from XML
        tree = ET.parse(cdxml_file)
        root = tree.getroot()
        
        # Look for ChemPropFormula attribute
        formula_attr = root.get('ChemPropFormula', '')
        if 'Formula:' in formula_attr:
            formula = formula_attr.split('Formula:')[-1].strip()
            if formula:
                return formula
        
        # Alternative: Count atoms from the structure including implicit hydrogens
        atoms = {}
        bonds_per_atom = {}
        
        # First pass: count explicit atoms and bonds
        for node in root.iter():
            if node.tag.endswith('n'):  # Node element
                node_id = node.get('id')
                element = node.get('Element', '6')  # Default to carbon (atomic number 6)
                if element.isdigit():
                    # Element is specified as atomic number
                    element_map = {
                        '1': 'H', '6': 'C', '7': 'N', '8': 'O', '9': 'F',
                        '13': 'Al', '14': 'Si', '15': 'P', '16': 'S', '17': 'Cl', '35': 'Br', '53': 'I'
                    }
                    element = element_map.get(element, 'C')
                atoms[element] = atoms.get(element, 0) + 1
                bonds_per_atom[node_id] = 0
                
                # Add explicit hydrogens
                num_h = int(node.get('NumHydrogens', '0'))
                if num_h > 0:
                    atoms['H'] = atoms.get('H', 0) + num_h
        
        # Count bonds for each atom to calculate implicit hydrogens
        for bond in root.iter():
            if bond.tag.endswith('b'):
                begin_id = bond.get('B')
                end_id = bond.get('E')
                order = int(bond.get('Order', '1').split('.')[0])  # Handle Order="1.5" etc
                
                if begin_id in bonds_per_atom:
                    bonds_per_atom[begin_id] += order
                if end_id in bonds_per_atom:
                    bonds_per_atom[end_id] += order
        
        # Calculate implicit hydrogens for carbon atoms
        for node in root.iter():
            if node.tag.endswith('n'):
                node_id = node.get('id')
                element = node.get('Element', '6')
                if element == '6' and node_id in bonds_per_atom:  # Carbon
                    # Carbon typically has 4 bonds
                    explicit_h = int(node.get('NumHydrogens', '0'))
                    if explicit_h == 0:  # Only add implicit H if not explicitly specified
                        bond_count = bonds_per_atom[node_id]
                        implicit_h = max(0, 4 - bond_count)
                        if implicit_h > 0:
                            atoms['H'] = atoms.get('H', 0) + implicit_h
        
        if atoms:
            # Build formula string (C, H, then alphabetically)
            formula_parts = []
            for elem in ['C', 'H']:
                if elem in atoms:
                    count = atoms[elem]
                    formula_parts.append(f"{elem}{count if count > 1 else ''}")
            for elem in sorted(atoms.keys()):
                if elem not in ['C', 'H']:
                    count = atoms[elem]
                    formula_parts.append(f"{elem}{count if count > 1 else ''}")
            return ''.join(formula_parts) if formula_parts else "N/A"
        
        return "N/A"
    except Exception as e:
        print(f"Error parsing formula from {cdxml_file}: {e}", file=sys.stderr)
        return "N/A"

def cdxml_to_png(cdxml_file, png_file, img_size=300):
    """
    Convert a CDXML file to PNG image using Indigo for rendering
    (OpenBabel/pybel is used for formula extraction in parse_cdxml_formula)
    
    Args:
        cdxml_file: Path to input CDXML file
        png_file: Path to output PNG file
        img_size: Size of the output image in pixels
    
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    # Try using Indigo for high-quality ChemDraw-style rendering
    if INDIGO_AVAILABLE:
        try:
            indigo = Indigo()
            renderer = IndigoRenderer(indigo)
            
            # Read CDXML file
            with open(cdxml_file, 'r', encoding='utf-8') as f:
                cdxml_content = f.read()
            
            mol = indigo.loadMolecule(cdxml_content)
            
            # Configure rendering options for ChemDraw-style output
            indigo.setOption("render-output-format", "png")
            indigo.setOption("render-background-color", "1.0, 1.0, 1.0")
            indigo.setOption("render-image-width", img_size)
            indigo.setOption("render-image-height", img_size)
            indigo.setOption("render-bond-line-width", 1.2)
            indigo.setOption("render-margins", 10, 10)
            indigo.setOption("render-relative-thickness", 1.0)
            indigo.setOption("render-label-mode", "hetero")  # Only show heteroatoms (standard notation)
            
            # Render to PNG
            renderer.renderToFile(mol, png_file)
            return True
        except Exception as e:
            print(f"Indigo rendering failed: {e}", file=sys.stderr)
            pass  # Fall through to PIL fallback
    
    # Fallback: Use PIL rendering with CDXML parsing
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a white background image with higher resolution
        img = Image.new('RGB', (img_size, img_size), color='white')
        d = ImageDraw.Draw(img)
        
        # Parse CDXML to get structure info
        tree = ET.parse(cdxml_file)
        root = tree.getroot()
        
        # Extract ChemDraw rendering parameters for 1:1 appearance
        cdxml_bond_length = float(root.get('BondLength', '30'))
        cdxml_line_width = float(root.get('LineWidth', '1'))
        
        # Extract bounding box for accurate scaling
        bbox = root.get('BoundingBox', '0 0 100 100')
        bbox_vals = [float(x) for x in bbox.split()]
        x_min, y_min, x_max, y_max = bbox_vals
        
        # Calculate scaling to fit molecule in image with padding
        padding = 30
        cdxml_width = x_max - x_min
        cdxml_height = y_max - y_min
        
        # Calculate scale to fit within image bounds
        available_width = img_size - 2 * padding
        available_height = img_size - 2 * padding
        
        if cdxml_width > 0 and cdxml_height > 0:
            scale_x = available_width / cdxml_width
            scale_y = available_height / cdxml_height
            scale = min(scale_x, scale_y)  # Use the smaller scale to ensure molecule fits
        else:
            scale = 1.0
        
        # Calculate scaled dimensions
        scaled_width = cdxml_width * scale
        scaled_height = cdxml_height * scale
        
        # Center the molecule in the image
        offset_x = (img_size - scaled_width) / 2 - x_min * scale
        offset_y = (img_size - scaled_height) / 2 - y_min * scale
        
        # Build node position map
        nodes = {}
        for node in root.iter():
            if node.tag.endswith('n'):
                node_id = node.get('id')
                if node_id:
                    pos_str = node.get('p', '0 0')
                    pos = pos_str.split()
                    if len(pos) >= 2:
                        nodes[node_id] = {
                            'x': float(pos[0]),
                            'y': float(pos[1]),
                            'element': node.get('Element', '6'),
                            'num_hydrogens': int(node.get('NumHydrogens', '0'))
                        }
        
        # Calculate line width using ChemDraw's LineWidth parameter
        base_line_width = max(1, int(cdxml_line_width * scale * 1.5))  # Scale ChemDraw line width
        
        # Helper function to shorten bond line if it connects to a heteroatom
        import math
        def adjust_bond_endpoint(x1, y1, x2, y2, element, shorten_distance):
            """Shorten bond line near heteroatom labels"""
            if element != '6' and element != '1':  # If heteroatom (not C or H)
                dx = x2 - x1
                dy = y2 - y1
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    # Shorten by moving point toward the other end
                    ratio = shorten_distance / length
                    x2 = x2 - dx * ratio
                    y2 = y2 - dy * ratio
            return x2, y2
        
        # Draw bonds with better styling
        for bond in root.iter():
            if bond.tag.endswith('b'):
                try:
                    begin_id = bond.get('B')
                    end_id = bond.get('E')
                    order = bond.get('Order', '1')
                    
                    if begin_id in nodes and end_id in nodes:
                        x1 = nodes[begin_id]['x'] * scale + offset_x
                        y1 = nodes[begin_id]['y'] * scale + offset_y
                        x2 = nodes[end_id]['x'] * scale + offset_x
                        y2 = nodes[end_id]['y'] * scale + offset_y
                        
                        # Shorten bonds at heteroatom ends for better alignment
                        # Use a fraction of the ChemDraw bond length
                        shorten = cdxml_bond_length * scale * 0.25
                        x1_adj, y1_adj = adjust_bond_endpoint(x2, y2, x1, y1, nodes[begin_id]['element'], shorten)
                        x2_adj, y2_adj = adjust_bond_endpoint(x1, y1, x2, y2, nodes[end_id]['element'], shorten)
                        
                        # Draw single bond
                        if order == '1' or order == '1.5':
                            d.line([(x1_adj, y1_adj), (x2_adj, y2_adj)], fill='black', width=base_line_width)
                        # Draw double bond
                        elif order == '2':
                            # Calculate perpendicular offset
                            dx = x2_adj - x1_adj
                            dy = y2_adj - y1_adj
                            length = math.sqrt(dx*dx + dy*dy)
                            if length > 0:
                                # Use ChemDraw's BondSpacing if available, or a fraction of bond length
                                bond_spacing = float(root.get('BondSpacing', str(cdxml_bond_length * 0.2)))
                                offset = bond_spacing * scale * 0.5
                                px = -dy / length * offset
                                py = dx / length * offset
                                d.line([(x1_adj+px, y1_adj+py), (x2_adj+px, y2_adj+py)], fill='black', width=base_line_width)
                                d.line([(x1_adj-px, y1_adj-py), (x2_adj-px, y2_adj-py)], fill='black', width=base_line_width)
                        # Draw triple bond
                        elif order == '3':
                            d.line([(x1_adj, y1_adj), (x2_adj, y2_adj)], fill='black', width=base_line_width)
                            dx = x2_adj - x1_adj
                            dy = y2_adj - y1_adj
                            length = math.sqrt(dx*dx + dy*dy)
                            if length > 0:
                                bond_spacing = float(root.get('BondSpacing', str(cdxml_bond_length * 0.2)))
                                offset = bond_spacing * scale * 0.6
                                px = -dy / length * offset
                                py = dx / length * offset
                                d.line([(x1_adj+px, y1_adj+py), (x2_adj+px, y2_adj+py)], fill='black', width=max(1, base_line_width-1))
                                d.line([(x1_adj-px, y1_adj-py), (x2_adj-px, y2_adj-py)], fill='black', width=max(1, base_line_width-1))
                except:
                    pass
        
        # Draw atom labels with better font (using ChemDraw's LabelSize)
        cdxml_label_size = float(root.get('LabelSize', '10'))
        font_size = max(8, min(20, int(cdxml_label_size * scale * 1.2)))
        font_size_small = max(6, int(font_size * 0.7))
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
            font_small = ImageFont.truetype("arial.ttf", font_size_small)
        except:
            font = ImageFont.load_default()
            font_small = font
        
        element_map = {
            '1': 'H', '6': 'C', '7': 'N', '8': 'O', '9': 'F',
            '13': 'Al', '14': 'Si', '15': 'P', '16': 'S', '17': 'Cl', '35': 'Br', '53': 'I'
        }
        
        for node_id, node_data in nodes.items():
            x = node_data['x'] * scale + offset_x
            y = node_data['y'] * scale + offset_y
            element = node_data['element']
            num_h = node_data.get('num_hydrogens', 0)
            
            # Determine if we need to show the atom label
            # Only show non-carbon heteroatoms (never show carbon or hydrogen atoms)
            show_h = num_h > 0 and element != '6' and element != '1'
            show_label = element != '6' and element != '1' and (element != '6' or show_h)
            
            if show_label:
                symbol = element_map.get(element, element)
                
                # Build full label with hydrogens (but not for carbon)
                label = symbol
                if show_h:
                    if num_h == 1:
                        label += 'H'
                    else:
                        label += f'H{num_h}'
                
                # Get text bounding box for centering
                bbox = d.textbbox((0, 0), label, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Draw white background for text
                d.rectangle([x - text_width/2 - 2, y - text_height/2 - 2, 
                           x + text_width/2 + 2, y + text_height/2 + 2], 
                          fill='white', outline=None)
                
                # For labels with hydrogens, draw element and subscript separately for better formatting
                if show_h:
                    # Draw main element symbol
                    elem_bbox = d.textbbox((0, 0), symbol, font=font)
                    elem_width = elem_bbox[2] - elem_bbox[0]
                    d.text((x - text_width/2, y - text_height/2), symbol, fill='black', font=font)
                    
                    # Draw H
                    h_x = x - text_width/2 + elem_width
                    d.text((h_x, y - text_height/2), 'H', fill='black', font=font)
                    
                    # Draw subscript number if > 1
                    if num_h > 1:
                        h_bbox = d.textbbox((0, 0), 'H', font=font)
                        h_width = h_bbox[2] - h_bbox[0]
                        sub_x = h_x + h_width
                        sub_y = y - text_height/2 + 4  # Slightly lower for subscript
                        d.text((sub_x, sub_y), str(num_h), fill='black', font=font_small)
                else:
                    # Draw simple label
                    d.text((x - text_width/2, y - text_height/2), label, fill='black', font=font)
        
        img.save(png_file)
        return True
    except Exception as e:
        print(f"Error converting {cdxml_file}: {e}", file=sys.stderr)
        return False

def generate_html(data):
    """
    Generate HTML index page with molecule structures
    
    Args:
        data: List of tuples (filename, formula, png_file)
    
    Returns:
        str: HTML content
    """
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Molecular Structures Index</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        img {
            display: block;
            max-width: 300px;
            height: auto;
        }
        .filename {
            font-family: monospace;
            color: #0066cc;
        }
        .formula {
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Molecular Structures</h1>
    <table>
        <tr>
            <th>Filename</th>
            <th>Formula</th>
            <th>2D Structure</th>
        </tr>
"""
    
    for filename, formula, png_file in data:
        # Format formula with subscripts (convert "C8 H16" to "C<sub>8</sub>H<sub>16</sub>")
        formatted_formula = ""
        i = 0
        while i < len(formula):
            if formula[i].isalpha():
                # Add the element symbol
                elem = formula[i]
                i += 1
                # Collect multi-character element symbols (e.g., Cl, Br, Si)
                while i < len(formula) and formula[i].islower():
                    elem += formula[i]
                    i += 1
                formatted_formula += elem
                
                # Skip spaces
                while i < len(formula) and formula[i] == ' ':
                    i += 1
                
                # Collect numbers and add as subscript
                num = ""
                while i < len(formula) and formula[i].isdigit():
                    num += formula[i]
                    i += 1
                if num:
                    formatted_formula += f"<sub>{num}</sub>"
                
                # Skip spaces after number
                while i < len(formula) and formula[i] == ' ':
                    i += 1
            else:
                i += 1
        
        html += f"""        <tr>
            <td class="filename">{filename}</td>
            <td class="formula">{formatted_formula}</td>
            <td><img src="{png_file}" alt="{filename}"></td>
        </tr>
"""
    
    html += """    </table>
</body>
</html>
"""
    return html

def main():
    if len(sys.argv) < 2:
        print("Usage: python cdx2html.py <cdxml_files...>")
        print("Example: python cdx2html.py *.cdxml")
        print("Example: python cdx2html.py rx*.cdxml")
        sys.exit(1)
    
    # Collect all CDXML files from command line arguments (expand wildcards)
    cdxml_files = []
    for arg in sys.argv[1:]:
        matched_files = glob.glob(arg)
        if matched_files:
            cdxml_files.extend(matched_files)
        else:
            # If no wildcard match, try the argument as-is
            if os.path.exists(arg) and arg.endswith('.cdxml'):
                cdxml_files.append(arg)
    
    if not cdxml_files:
        print("Error: No CDXML files found matching the specified patterns.")
        sys.exit(1)
    
    print(f"Processing {len(cdxml_files)} CDXML file(s)...")
    
    # Process each CDXML file
    data = []
    for cdxml_file in sorted(cdxml_files):
        filename = os.path.basename(cdxml_file)
        png_file = os.path.splitext(filename)[0] + ".png"
        
        print(f"Processing {filename}...", end=" ")
        
        # Get molecular formula
        formula = parse_cdxml_formula(cdxml_file)
        
        # Convert to PNG
        if cdxml_to_png(cdxml_file, png_file):
            data.append((filename, formula, png_file))
            print("OK")
        else:
            print("FAILED")
    
    if not data:
        print("Error: No files were successfully processed.")
        sys.exit(1)
    
    # Generate HTML
    html_content = generate_html(data)
    
    # Write HTML file
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"\nSuccess! Generated index.html with {len(data)} molecule(s).")
    print("Open index.html in a web browser to view the results.")

if __name__ == "__main__":
    main()
