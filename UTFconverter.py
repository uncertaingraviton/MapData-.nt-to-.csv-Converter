# this converts files with undesirable UTF formats to UTF-8 encoding



input_file = "" # your input file which has the undesirable UTF format
output_file = "" # the output file which will be created with UTF-8 encoding
# make sure they are in the same folder and they have the same extension

with open(input_file, "rb") as f:
    raw = f.read()

# Try decoding using likely encodings
for enc in ["utf-16", "utf-8-sig", "iso-8859-1", "cp1252"]:
    try:
        text = raw.decode(enc)
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(text)
        print(f"Successfully converted from {enc} to UTF-8.")
        break
    except UnicodeDecodeError:
        continue
else:
    print("❌ Failed to decode file using all common encodings.")
