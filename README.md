# N-triples to CSV converter for RDF map data

This contains a set of Python scripts for processing and cleaning RDF-file-type vehicle location data. The scripts are designed to work together in a pipeline to convert, clean, and validate data.
GO THROUGH ALL THE STEPS TO AVOID ERRORS

# Prerequisite steps-(for coding noobs)
1. Download this folder as zip.
2. unzip
3. drag and drop your .nt file (which has your raw map data) into this folder
4. Open this folder in your preferred IDE (like, VScode)
5. Run- 
```bash
pip install pandas rdflib python 
```
in the terminal. Ideally this terminal should be opened in the same folder (meaning, navigate to the downloaded and unzipped folder in your terminal and then run this command. If youre using VScode, this is done automatically so you dont have to worry) {these are packages that the python codefiles use to process the converting and what not and is absolutely essential}.
6. Make sure when youre following the steps, you type in the correct input files into the pyhton code files.
7. To run a python codefile, simply type in,
```bash
python NAMEOFTHEFILE.py
```
into the terminal and this runs the specific python file and gives the output file you desire into the same folder. (if you get any errors related to python/pandas/rdflib, make sure you've done step 5 properly. You can repeat it if you want).
8. Make sure the names of the files wherever you are typing them in, like in the terminal for the .py files or your input/output files in the codefiles are matching correctly or else it will lead to errors. To be safe, you can copy paste them, this will rule out any possibilities for errors.



# Steps Overview - More details in next steps
1. Run `UTFconverter.py` to your base raw file. This makes sure that the N-triples file (.nt) is in the compatible utf format. Additionaly this can be used to convert any type of files.
2. Input the correct file into the `NTtoCSVconverter.py`. IMPORTANT- specify the header columns that you will need in your output CSV. some relevant headers that I used- Vehicle type, Location, Timestamp. 
Then run this file.
3. For deduplication, input the new CSV file into the `deduplicate_vehicle_locations.py` and run it, you will get a de-duplicated csv file.
4. This is an ADDITIONAL/OPTIONAL step. The `check_coordinates_in_bounds.py` file calculates the bounds of your CSV results range and also counts points within specified bounds.
>>>>>>> 21e2a86 (README CHANGES)

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