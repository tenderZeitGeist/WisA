import argparse
import csv
import random
import string

def generate_random_integers(n):
    return[random.randint(0, n) for _ in range(n)]

def generate_random_floats(n):
    return[random.uniform(0, n) for _ in range(n)]

def generate_random_strings(n):
    return [''.join(random.choices(string.ascii_letters, k=random.randint(1, 32))) for _ in range(n)]

def save_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for value in data:
            writer.writerow([value])

def main() -> None:
    parser = argparse.ArgumentParser(description='Generate a CSV file with random data.')
    parser.add_argument('n', type=int, help='Number of entries to generate.')
    parser.add_argument('data_type', type=str, choices=['int', 'float', 'string'], help='Type of data to generate.')
    parser.add_argument('filename', type=str, help='Name of the CSV file to save.')

    args = parser.parse_args()

    if args.data_type == 'int':
        data = generate_random_integers(args.n)
    elif args.data_type == 'float':
        data = generate_random_floats(args.n)
    elif args.data_type == 'string':
        data = generate_random_strings(args.n)

    save_to_csv(args.filename, data)
    print(f"CSV file '{args.filename}' with {args.n} {args.data_type} entries has been created.")

if __name__ == '__main__':
    main()
