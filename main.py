import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd
from rdflib import Graph
import csv
import re
from urllib.parse import urlparse  # ← this might be missing

# -------------------- UTFconverter.py --------------------
def utf_convert(input_file, output_file):
    with open(input_file, "rb") as f:
        raw = f.read()

    # Detect ASCII
    try:
        raw.decode("ascii")
        print("✅ Detected ASCII. Skipping conversion.")
        with open(output_file, "wb") as out:
            out.write(raw)
        return
    except UnicodeDecodeError:
        pass

    # Try other encodings
    for enc in ["utf-8", "utf-16", "utf-8-sig", "iso-8859-1", "cp1252"]:
        try:
            text = raw.decode(enc)
            with open(output_file, "w", encoding="utf-8") as out:
                out.write(text)
            print(f"✅ Successfully converted from {enc} to UTF-8.")
            return
        except UnicodeDecodeError:
            continue

    raise Exception("❌ Failed to decode file using all common encodings.")
#--------------------- validation step------------------------

def validate_nt_file(nt_file):
    g = Graph()
    try:
        g.parse(nt_file, format="nt")
    except Exception as e:
        raise Exception(f"❌ Failed to parse .nt file: {e}")

    required_predicates = {
        "vehicle_type": False,
        "location": False,
        "timestamp": False
    }

    for _, p, _ in g:
        pred = urlparse(str(p)).path.split('/')[-1].lower()
        if pred in required_predicates:
            required_predicates[pred] = True
        if pred == "observation_time":  # Accept this as timestamp too
            required_predicates["timestamp"] = True

    missing = [k for k, v in required_predicates.items() if not v]
    if missing:
        raise Exception(f"❌ Missing required predicate(s) in .nt file: {', '.join(missing)}")

    print("✅ NT file passed pre-check validation.")

# -------------------- NTtoCSVconverter.py --------------------
# -------------------- Improved NT to CSV converter --------------------
def nt_to_csv(input_file, output_file):
    g = Graph()
    g.parse(input_file, format="nt")

    data = {}
    for s, p, o in g:
        subject = str(s)
        predicate = str(p).split("/")[-1]  # Take the last part of the URI
        obj = str(o)

        if subject not in data:
            data[subject] = {}
        data[subject][predicate] = obj

    # Convert dict to DataFrame
    df = pd.DataFrame.from_dict(data, orient="index").reset_index(drop=True)
    df.to_csv(output_file, index=False, encoding="utf-8")
    print("✅ RDF N-Triples converted to CSV (tabular format).")

# -------------------- deduplicate_vehicle_locations.py --------------------
def extract_minute(ts):
    if pd.isnull(ts):
        return None
    match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})', str(ts))
    if match:
        return match.group(1)
    return ts

def deduplicate_csv(input_file, output_file):
    df = pd.read_csv(input_file)

    print(f"📄 Columns in CSV: {list(df.columns)}")

    # Step 1: Find timestamp column
    timestamp_col = None
    for col in df.columns:
        if any(key in col.lower() for key in ['timestamp', 'observation', 'time', 'date']):
            timestamp_col = col
            print(f"✅ Timestamp column detected: {timestamp_col}")
            break

    if not timestamp_col:
        print('⚠️ No timestamp or observation column found. Cannot deduplicate by time.')
        return

    # Step 2: Extract minute from timestamp
    def extract_minute(ts):
        if pd.isnull(ts):
            return None
        match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})', str(ts))
        if match:
            return match.group(1)
        return ts

    df['minute'] = df[timestamp_col].apply(extract_minute)

    # Step 3: Extract longitude and latitude from 'location'
    if 'location' in df.columns:
        coords = df['location'].str.extract(r'POINT\s*\(\s*([-\d.]+)\s+([-\d.]+)\s*\)')
        df['longitude'] = coords[0].astype(float)
        df['latitude'] = coords[1].astype(float)
        print("✅ Extracted longitude and latitude from location column.")
    else:
        print("❌ 'location' column not found.")
        return

    # Step 4: Deduplicate
    dedup_cols = ['vehicle_type', 'longitude', 'latitude', 'minute']
    for col in dedup_cols:
        if col not in df.columns:
            print(f"⚠️ Missing required column: {col}")
            return

    df_dedup = df.drop_duplicates(subset=dedup_cols)
    df_dedup = df_dedup.drop(columns=['minute'])
    df_dedup.to_csv(output_file, index=False)
    print(f"✅ Deduplicated CSV saved as {output_file} ({len(df_dedup)} rows).")
    return True  # <-- add this line

# -------------------- check_coordinates_in_bounds.py --------------------
def check_bounds(input_file):
    LEFT, RIGHT, BOTTOM, TOP = 3.68, 3.70, 51.02, 51.04
    df = pd.read_csv(input_file)

    if 'location' not in df.columns:
        raise Exception("Missing 'location' column for bounds checking.")

    coords = df['location'].str.extract(r'POINT\(([^ ]+) ([^)]+)\)')
    if coords.isnull().values.any():
        raise Exception("Failed to parse coordinates from 'location' column.")

    df['longitude'] = coords[0].astype(float)
    df['latitude'] = coords[1].astype(float)

    in_bounds = df[
        (df['longitude'] >= LEFT) & (df['longitude'] <= RIGHT) &
        (df['latitude'] >= BOTTOM) & (df['latitude'] <= TOP)
    ]

    print(f"✅ Number of points within bounds: {len(in_bounds)}")
    print(in_bounds.head())
# -------------------- Main GUI Application --------------------
def convert_pipeline(nt_file_path):
    folder = os.path.dirname(nt_file_path)
    utf_output = os.path.join(folder, "utf_converted.nt")
    csv_output = os.path.join(folder, "output.csv")
    dedup_output = os.path.join(folder, "deduplicated_output.csv")

    try:
        utf_convert(nt_file_path, utf_output)
        print("✅ UTF conversion step complete.")

        #Validation step
        validate_nt_file(utf_output)

        nt_to_csv(utf_output, csv_output)
        print("✅ RDF N-Triples converted to CSV.")

        dedup_success = deduplicate_csv(csv_output, dedup_output)
        if dedup_success is None:
            messagebox.showinfo("⚠️ Partial Success", f"Conversion complete, but no timestamp/observation column found.\nCheck: {csv_output}")
            return

        check_bounds(dedup_output)
        messagebox.showinfo("✅ Done", f"Conversion successful!\nFinal output: {dedup_output}")

    except Exception as e:
        messagebox.showerror("❌ Error", str(e))

def select_file():
    path = filedialog.askopenfilename(filetypes=[("N-Triples", "*.nt")])
    if path:
        convert_pipeline(path)

root = tk.Tk()
root.title("NT to CSV Converter")
root.geometry("400x200")

label = tk.Label(root, text="Select an .nt file to start conversion:", font=("Arial", 12))
label.pack(pady=20)

btn = tk.Button(root, text="Upload .nt File", command=select_file, width=25, height=2)
btn.pack()

root.mainloop()
