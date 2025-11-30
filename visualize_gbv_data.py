import pandas as pd
import matplotlib.pyplot as plt
import os

def create_histogram(data_frame, column_name, output_filename):
    """
    Creates and saves a histogram for a given column in a DataFrame.

    Args:
        data_frame (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to create a histogram for.
        output_filename (str): The filename to save the histogram to.
    """
    if column_name not in data_frame.columns:
        print(f"Error: '{column_name}' column not found.")
        return

    clean_column = data_frame[column_name].str.strip().str.lower()
    counts = clean_column.value_counts()

    if counts.empty:
        print(f"No data to plot for {column_name} histogram.")
        return

    total_count = counts.sum()

    plt.figure(figsize=(10, 6))
    ax = counts.plot(kind='bar', color='#191970')
    plt.title(f'Histogram of {column_name}')
    plt.xlabel(column_name)
    plt.ylabel('Number of Occurrences')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for i, count in enumerate(counts):
        percentage = (count / total_count) * 100
        plt.text(i, count / 2, f'{percentage:.1f}%', ha='center', va='center', color='white', fontweight='bold', fontsize=12)

    plt.savefig(output_filename)
    plt.close()
    print(f"Saved {output_filename}")

def create_stacked_barchart(data_frame, index_col, stack_col, output_filename):
    """
    Creates and saves a stacked bar chart.

    Args:
        data_frame (pd.DataFrame): The input DataFrame.
        index_col (str): The column for the bar index (e.g., 'Level of Explicity').
        stack_col (str): The column for the stacks (e.g., 'Rape/Non-Con Tag').
        output_filename (str): The filename to save the chart to.
    """
    if index_col not in data_frame.columns or stack_col not in data_frame.columns:
        print(f"Error: One or more columns not found.")
        return

    df_copy = data_frame.copy()
    df_copy[index_col] = df_copy[index_col].str.strip().str.lower()
    df_copy[stack_col] = df_copy[stack_col].str.strip().str.lower()

    grouped_data = df_copy.groupby([index_col, stack_col]).size().unstack(fill_value=0)
    
    colors = ['#4682B4', '#191970'] 
    
    if 'yes' in grouped_data.columns and 'no' in grouped_data.columns:
        grouped_data = grouped_data[['no', 'yes']]

    ax = grouped_data.plot(kind='bar', stacked=True, figsize=(10, 7), color=colors)

    plt.title(f'Stacked Bar Chart of {stack_col} by {index_col}')
    plt.xlabel(index_col)
    plt.ylabel('Number of Occurrences')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    for container in ax.containers:
        ax.bar_label(container, label_type='center', color='white', fontweight='bold')

    plt.savefig(output_filename)
    plt.close()
    print(f"Saved {output_filename}")

def main():
    """
    Main function to generate histograms for GBV data.
    """
    file_path = 'Instances_of_GBV_anonym.csv'

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        exit()

    df.columns = df.columns.str.strip()

    create_histogram(df, 'Focalization', 'histogram_focalization.png')
    create_histogram(df, 'Level of Explicity', 'histogram_level_of_explicity.png')
    create_stacked_barchart(df, 'Level of Explicity', 'Rape/Non-Con Tag', 'stacked_barchart_explicity_tag.png')

if __name__ == '__main__':
    main()
