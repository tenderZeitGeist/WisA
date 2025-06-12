import pandas as pd
import matplotlib.pyplot as plt
import argparse
import seaborn as sns

sns.set_theme(style="whitegrid")

def plot_execution_times(csv_file):
    """
    Creates bar charts comparing the execution speed of different algorithms
    between Python and C++ implementations, and additional charts showing the
    execution speed by data type for each algorithm.

    Parameters:
    csv_file (str): Path to the CSV file containing the data.
    """
    try:
        # Load the CSV file
        data = pd.read_csv(csv_file)

        # Check if required columns are present
        required_columns = ['implementation', 'algorithm', 'time_in_milliseconds', 'file_name']
        if not all(col in data.columns for col in required_columns):
            raise ValueError("CSV file is missing one or more required columns.")

        # Extract data type from file_name
        data['data_type'] = data['file_name'].str.replace('.csv', '', regex=False).str.split('_').str[-1]

        # First plot: Execution time by algorithm
        # Group by algorithm and implementation, then calculate the mean time in milliseconds
        grouped_data_algorithm = data.groupby(['algorithm', 'implementation'])['time_in_milliseconds'].mean().reset_index()

        # Convert the grouped mean times from milliseconds to seconds
        grouped_data_algorithm['time_in_seconds'] = grouped_data_algorithm['time_in_milliseconds'] / 1000

        # Create the first figure with the algorithm comparison
        fig1, ax1 = plt.subplots(figsize=(12, 6))

        # Set the color palette to match your preferences
        palette = {'Python': 'orange', 'C++': 'blue'}
        sns.set_palette([palette['C++'], palette['Python']])

        # Use seaborn's barplot
        sns.barplot(data=grouped_data_algorithm, x='algorithm', y='time_in_seconds', hue='implementation', ax=ax1,
                    width=.5)

        ax1.set_xlabel('', fontsize=12)
        ax1.set_ylabel('Execution Time (seconds)', fontsize=12)
        ax1.set_title('Execution Speed by Algorithm', fontsize=14)
        ax1.tick_params(axis='x')
        ax1.legend(title='Implementation', fontsize=10)

        plt.tight_layout()
        plt.savefig(f'execution_speed.png', format="png", dpi=300)
        plt.close()

        # Now create separate plots for each algorithm, showing execution time by data type
        algorithms = data['algorithm'].unique()

        for algorithm in algorithms:
            # Filter data for the current algorithm
            alg_data = data[data['algorithm'] == algorithm]

            # Group by data_type and implementation, then calculate the mean time in milliseconds
            grouped_data = alg_data.groupby(['data_type', 'implementation'])['time_in_milliseconds'].mean().reset_index()

            # Convert the grouped mean times from milliseconds to seconds
            grouped_data['time_in_seconds'] = grouped_data['time_in_milliseconds'] / 1000

            # Only create a plot if there's data for this algorithm
            if not grouped_data.empty:
                # Create a new figure for this algorithm
                fig, ax = plt.subplots(figsize=(12, 6))

                # Set the color palette again
                sns.set_palette([palette['C++'], palette['Python']])

                # Use seaborn's barplot
                sns.barplot(data=grouped_data, x='data_type', y='time_in_seconds', hue='implementation', ax=ax,
                            width=.5)

                ax.set_xlabel('', fontsize=12)
                ax.set_ylabel('Execution Time (seconds)', fontsize=12)
                ax.set_title(f'Execution Speed by Data Type for {algorithm}', fontsize=14)
                ax.tick_params(axis='x')
                ax.legend(title='Implementation', fontsize=10)

                plt.tight_layout()
                plt.savefig(f'{algorithm}_speed_by_data_types.png', format="png", dpi=300)
                plt.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot execution times of algorithms.')
    parser.add_argument('--csv', type=str, default='data.csv', help='Path to the CSV file containing the data.')
    args = parser.parse_args()

    plot_execution_times(args.csv)

