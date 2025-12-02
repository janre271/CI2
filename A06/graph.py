"""
Graph generator for reciprocal function (y = 1/x)
Reads data from graph.csv and creates a visualization in graph.png
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def generate_graph(csv_file='graph.csv', output_file='graph.png'):
    """
    Generate a graph from CSV data and save it as PNG.
    
    Parameters:
    -----------
    csv_file : str
        Path to the input CSV file (default: 'graph.csv')
    output_file : str
        Path to the output PNG file (default: 'graph.png')
    """
    # Read the CSV file
    data = pd.read_csv(csv_file)
    
    # Extract x and y columns
    x = data['x']
    y = data['y']
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2, marker='o', markersize=5, label='y = 1/x')
    
    # Add labels and title
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Reciprocal Function: y = 1/x', fontsize=14, fontweight='bold')
    
    # Add grid
    plt.grid(True, alpha=0.3)
    
    # Add legend
    plt.legend()
    
    # Save the figure
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Graph saved successfully to {output_file}")
    
    # Close the plot to free memory
    plt.close()


if __name__ == '__main__':
    # Default values
    csv_file = 'graph.csv'
    output_file = 'graph.png'
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    # Generate the graph
    generate_graph(csv_file, output_file)
