import pandas as pd
import re

def extract_minute(ts):
    # Try to extract the minute from a timestamp string
    # Accepts formats like '2023-05-17T18:15:00.000Z' or '2023-05-17T18:15:00Z'
    if pd.isnull(ts):
        return None
    match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})', str(ts))
    if match:
        return match.group(1)
    return ts  # fallback to original if not matched

def main():
    input_file = '' # Specify the path to your CSV file here
    output_file = '' # The output file name which wil be created, add the name here in the same extension as the input file
    df = pd.read_csv(input_file)

    # Try to find a timestamp column
    timestamp_col = None
    for col in df.columns:
        if 'time' in col.lower() or 'date' in col.lower():
            timestamp_col = col
            break
    if not timestamp_col:
        # Try to extract from observation_uri if present
        for col in df.columns:
            if 'observation' in col.lower():
                timestamp_col = col
                break
    if not timestamp_col:
        print('No timestamp or observation column found. Cannot deduplicate by time.')
        return

    # Extract minute from timestamp
    df['minute'] = df[timestamp_col].apply(extract_minute)

    # Deduplicate by vehicle_type, longitude, latitude, and minute
    dedup_cols = ['vehicle_type', 'longitude', 'latitude', 'minute']
    df_dedup = df.drop_duplicates(subset=dedup_cols)
    df_dedup = df_dedup.drop(columns=['minute'])
    df_dedup.to_csv(output_file, index=False)
    print(f'Deduplicated file saved as {output_file} with {len(df_dedup)} rows (removed {len(df) - len(df_dedup)} duplicates).')

if __name__ == '__main__':
    main() 