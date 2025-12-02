# Assignment 06


This Python script creates a visualization of the reciprocal function (y = 1/x) from CSV data and saves it as a PNG image. The script reads x and y values from a CSV file and generates a professionally formatted graph with proper labels, grid, and high resolution output.



Prerequisites
-------------

- Python 3.7 or newer installed

- Git installed (to clone the repository)



How to clone from GitHub
-----------------

Clone the repository and navigate to the assignment folder:

```bash
git clone https://github.com/janre271/CI2.git
cd CI2/A06
```


Quick steps to run the script 
------------------

**Step 1:** Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

On Linux/macOS:
```bash
source venv/bin/activate
```


**Step 2:** Install required dependencies

```bash
pip install -r requirements.txt
```


**Step 3:** Run the script to generate the graph

```bash
python graph.py
```

This will read data from `graph.csv` and create `graph.png` in the current directory.



How it works

------------

1. **pandas** reads the CSV file containing x and y columns

2. **matplotlib.pyplot** creates a professional graph visualization with grid, labels, and markers

3. **numpy** provides array/matrix functionality for numerical operations

4. Generates a high-resolution PNG image (300 DPI) saved as output file



Usage Options

--------------

The script accepts optional command-line arguments for custom input and output files:

```bash
# Default: reads graph.csv, outputs graph.png
python graph.py

# Custom input CSV file
python graph.py mydata.csv

# Custom input and output files
python graph.py mydata.csv output.png
```



Troubleshooting

---------------

**"No module named 'pandas'"?**
- Make sure you ran `pip install -r requirements.txt` in the activated virtual environment

**"FileNotFoundError: graph.csv"?**
- Ensure your CSV file is in the same directory as `graph.py`
- Or provide the full path: `python graph.py /path/to/data.csv`

**Need custom input/output files?**
- Run `python graph.py input.csv output.png`

**Need to regenerate?**
- Simply run `python graph.py` again to overwrite the existing image



Expected output

---------------

You should see console output confirming success:

```
Graph saved successfully to graph.png
```

Open the PNG file in any image viewer to see the reciprocal function visualization with:
- Line plot connecting all data points
- Circular markers at each point
- Grid lines for easier reading
- Axis labels and title
- High-resolution output (300 DPI)
