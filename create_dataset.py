import pandas as pd
import numpy as np
import random
import argparse

from concurrent.futures import ThreadPoolExecutor, as_completed
from faker import Faker
from pathlib import Path
from threading import Lock

def generate_names(fake, min_count, max_count, size, progress_interval=10000):
    names = []
    counts = []
    for _ in range(size):
        name = fake.last_name()
        name = ''.join(filter(str.isalpha, name))

        names.append(name)
        count = random.randint(min_count, max_count)
        counts.append(count)

        if len(names) % progress_interval == 0:
            print(f"Generated {len(names)} ({(len(names) / size) * 100:.2f}%) names from a total of {size} so far...")

    return names, counts

def generate_complex_dataset(input_file, output_file, size=100000):
    fake = Faker()
    try:
        census_data = pd.read_csv(input_file, header=None, names=['Name', 'Count', 'Rank'],
                                  dtype={'Name': str, 'Count': str, 'Rank': str}, low_memory=False)
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    for column in ['Count', 'Rank']:
        census_data[column] = pd.to_numeric(census_data[column], errors='coerce')
        census_data = census_data.dropna(subset=[column])
        census_data[column] = census_data[column].astype(int)

    min_count = census_data['Count'].min()
    max_count = census_data['Count'].max()

    num_workers = 4
    chunk_size = size // num_workers
    lock = Lock()

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(generate_names, fake, min_count, max_count, chunk_size) for _ in range(num_workers)]
        names = []
        counts = []

        for future in as_completed(futures):
            chunk_names, chunk_counts = future.result()
            with lock:
                names.extend(chunk_names)
                counts.extend(chunk_counts)

    # Ensure the final dataset has the exact size
    if len(names) > size:
        names = names[:size]
        counts = counts[:size]
    elif len(names) < size:
        additional_names, additional_counts = generate_names(fake, min_count, max_count, size - len(names))
        names.extend(additional_names)
        counts.extend(additional_counts)

    # Ensure the lengths are the same
    if len(names) != len(counts):
        raise ValueError("The lengths of names and counts do not match.")

    df = pd.DataFrame({
        'Name': names,
        'Count': counts
    })

    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    df.to_csv(output_file, index=False)
    print(f"Generated complex dataset with {size} records saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate a complex dataset for sorting benchmarking using local census data.")
    parser.add_argument("input_file", help="Path to the local US Census data file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    parser.add_argument("-s", "--size", type=int, default=100000,
                        help="Number of records to generate (default: 100000)")

    args = parser.parse_args()
    generate_complex_dataset(args.input_file, args.output_file, args.size)

if __name__ == "__main__":
    main()