# Data Processing Pipeline

This repository contains a set of Python scripts for processing and cleaning vehicle location data. The scripts are designed to work together in a pipeline to convert, clean, and validate data.

## Scripts Overview

### 1. UTFconverter.py
Converts files with various UTF encodings to UTF-8 format. This is typically the first step in the pipeline to ensure consistent encoding.

**Usage:**
1. Open `UTFconverter.py`
2. Set the `input_file` variable to your source file path
3. Set the `output_file` variable to your desired output file path
4. Run the script

The script will attempt to decode the file using common encodings (UTF-16, UTF-8-SIG, ISO-8859-1, CP1252) and convert it to UTF-8.

### 2. NTtoCSVconverter.py
Converts RDF-N triples (.nt files) to CSV format. This is useful for converting semantic web data into a tabular format.

**Usage:**
1. Open `NTtoCSVconverter.py`
2. Set the input file path in the `g.parse()` function
3. Run the script
4. The output will be saved as "output.csv" with columns: Subject, Predicate, Object

### 3. deduplicate_vehicle_locations.py
Removes duplicate vehicle location entries based on vehicle type, coordinates, and timestamp (minute-level granularity).

**Usage:**
1. Open `deduplicate_vehicle_locations.py`
2. Set the `input_file` variable to your CSV file path
3. Set the `output_file` variable to your desired output file path
4. Run the script

The script will:
- Automatically detect timestamp columns
- Extract minute-level timestamps
- Remove duplicates based on vehicle type, longitude, latitude, and minute
- Save the deduplicated data to the output file

### 4. check_coordinates_in_bounds.py
Validates if coordinates fall within a specified bounding box (default set to an area near Brussels, Belgium).

**Usage:**
1. Open `check_coordinates_in_bounds.py`
2. Set the `input_file` variable to your CSV file path
3. Optionally modify the bounding box coordinates:
   - LEFT = 3.68
   - RIGHT = 3.70
   - BOTTOM = 51.02
   - TOP = 51.04
4. Run the script

The script will:
- Calculate the bounding box of your data
- Count points within the specified bounds
- Display a sample of points within bounds

## Recommended Processing Order

1. Start with `UTFconverter.py` to ensure proper encoding
2. If your data is in RDF-N triples format, use `NTtoCSVconverter.py`
3. Use `deduplicate_vehicle_locations.py` to remove duplicate entries
4. Finally, use `check_coordinates_in_bounds.py` to validate coordinate ranges

## Requirements

- Python 3.x
- pandas
- rdflib (for NTtoCSVconverter.py)

Install required packages using:
```bash
pip install pandas rdflib
```

## Notes

- Make sure to backup your data before processing
- All scripts expect CSV files unless specified otherwise
- The coordinate checker is currently set to a specific area in Brussels, Belgium
- Adjust the bounding box coordinates in `check_coordinates_in_bounds.py` according to your needs 