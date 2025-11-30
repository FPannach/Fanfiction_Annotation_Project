import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os # Import os module to handle file paths

# Load the dataset
csv_file_path = '../MoD_Triples.csv'
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"Error: {csv_file_path} not found.")
    exit()

# --- Data Cleaning ---

# Strip leading/trailing whitespace from column names
df.columns = df.columns.str.strip()

# Columns to analyze
columns_to_analyze = ['Mode of Demise', 'Victim', 'Perpetrator']

# Clean and standardize data in the relevant columns
for col in columns_to_analyze:
    # Ensure column is string type before using .str accessor
    df[col] = df[col].astype(str)
    # Strip whitespace from data and convert to lowercase
    df[col] = df[col].str.strip().str.lower()
    # Replace various forms of 'missing' with a standard 'unspecified'
    # Also handles 'nan' strings that can result from astype(str)
    df[col] = df[col].replace(['---', '', 'unnamed', 'nan'], 'unspecified')


# Merge different spellings and references to Clytemnestra
df['Victim'] = df['Victim'].replace(["klytemnestra", "clytaemnestra", "agamemnon's wife"], "clytemnestra")
df['Perpetrator'] = df['Perpetrator'].replace(["klytemnestra", "clytaemnestra", "agamemnon's wife"], "clytemnestra")


# --- Visualization Functions ---

def create_combined_stacked_barchart(data_frame, column_names):
    """Creates a combined stacked barchart of 'unspecified' vs. 'other' for multiple columns."""
    plt.figure(figsize=(9, 8)) # Adjusted for multiple bars

    # Use two slightly different shades of dark blue to distinguish the 'unspecified' vs 'other'
    dark_blue_unspecified = '#4682B4' # SteelBlue
    dark_blue_other = '#191970'       # MidnightBlue

    x_positions = np.arange(len(column_names))
    width = 0.5

    all_unspecified_percentages = []
    all_other_percentages = []
    
    for i, col_name in enumerate(column_names):
        unspecified_count = data_frame[col_name].value_counts().get('unspecified', 0)
        total_count = len(data_frame[col_name])
        
        if total_count > 0:
            unspecified_percentage = (unspecified_count / total_count) * 100
            other_percentage = 100 - unspecified_percentage
        else:
            unspecified_percentage = 0
            other_percentage = 0
        
        all_unspecified_percentages.append(unspecified_percentage)
        all_other_percentages.append(other_percentage)

        # Plot bars with percentages
        p1 = plt.bar(x_positions[i], unspecified_percentage, width, color=dark_blue_unspecified, label='Unspecified' if i == 0 else "")
        p2 = plt.bar(x_positions[i], other_percentage, width, bottom=unspecified_percentage, color=dark_blue_other, label='All Others' if i == 0 else "")

        # Add text labels as percentages
        if unspecified_percentage > 0:
            plt.text(x_positions[i], unspecified_percentage / 2,
                     f"{unspecified_percentage:.1f}%", ha='center', va='center', color='white', fontsize=12, fontweight='bold')
        if other_percentage > 0:
            plt.text(x_positions[i], unspecified_percentage + other_percentage / 2,
                     f"{other_percentage:.1f}%", ha='center', va='center', color='white', fontsize=12, fontweight='bold')

    plt.ylabel('Percentage of Occurrences (%)')
    plt.title('Combined Categories: Unspecified vs. Other')
    plt.xticks(x_positions, column_names, rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    filename = f'../images/stacked_barchart_combined.png'
    plt.savefig(filename)
    plt.close()
    print(f"Saved {filename}")


def create_histogram(data_frame, column_name, top_n=None, title_suffix="", filename_prefix=""):
    """
    Creates a histogram of value counts for a column, ordered by frequency.
    Can optionally show only the top N occurrences and excludes 'unspecified' instances.
    Accepts title_suffix and filename_prefix for custom naming.
    """
    plt.figure(figsize=(12, 8))

    # Filter out 'unspecified' instances
    filtered_df = data_frame[data_frame[column_name] != 'unspecified']
    counts = filtered_df[column_name].value_counts().sort_values(ascending=False)

    if counts.empty:
        print(f"No non-unspecified data to plot for {filename_prefix}{column_name} histogram.")
        plt.close()
        return

    title_main = f'Histogram of "{column_name}"'
    filename_main = f'histogram_{column_name.replace(" ", "_").lower()}'
    
    if top_n:
        counts = counts.head(top_n)
        title_main += f' (Top {top_n})'
        filename_main += f'_top_{top_n}'

    title_main += ' (Excluding Unspecified)'
    filename_main += '_no_unspecified'

    # Use teal color for all bars in the histogram
    teal_color = '#008080' # Teal
    counts.plot(kind='bar', color=teal_color)

    plt.title(f"{title_main} {title_suffix}")
    plt.ylabel('Number of Occurrences')
    plt.xlabel(column_name)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    filename = f"{filename_prefix}{filename_main}.png"
    plt.savefig(filename)
    plt.close()
    print(f"Saved {filename}")


def create_zeus_histograms(data_frame):
    """
    Creates histograms for victims and modes of demise specifically when the perpetrator is 'zeus'.
    """
    zeus_df = data_frame[data_frame['Perpetrator'] == 'zeus'].copy()

    if zeus_df.empty:
        print("No data found for 'zeus' as a perpetrator. Skipping Zeus-specific histograms.")
        return

    # Histogram for victims when perpetrator is Zeus
    create_histogram(zeus_df.copy(), 'Victim', top_n=10, 
                     title_suffix="when Perpetrator is Zeus", 
                     filename_prefix="histogram_victims_perpetrator_zeus_")

    # Histogram for mode of demise when perpetrator is Zeus
    create_histogram(zeus_df.copy(), 'Mode of Demise', top_n=10, 
                     title_suffix="when Perpetrator is Zeus", 
                     filename_prefix="histogram_mode_of_demise_perpetrator_zeus_")

def create_victim_perpetrator_stacked_chart(data_frame, top_n=20):
    """
    Creates a stacked bar chart for the top N characters, showing their occurrences as 'Victim' vs. 'Perpetrator'.
    """
    # Combine 'Victim' and 'Perpetrator' columns to find top characters
    all_chars = pd.concat([data_frame['Victim'], data_frame['Perpetrator']])
    
    # Filter out 'unspecified'
    all_chars = all_chars[all_chars != 'unspecified']
    
    # Get top N characters
    top_chars = all_chars.value_counts().nlargest(top_n).index

    victim_counts = []
    perpetrator_counts = []

    for char in top_chars:
        victim_count = data_frame[data_frame['Victim'] == char].shape[0]
        perpetrator_count = data_frame[data_frame['Perpetrator'] == char].shape[0]
        victim_counts.append(victim_count)
        perpetrator_counts.append(perpetrator_count)

    plt.figure(figsize=(15, 10))
    
    # Colors for the stacked bars
    victim_color = '#4682B4'  # SteelBlue
    perpetrator_color = '#191970' # MidnightBlue

    # Create stacked bar chart
    plt.bar(top_chars, victim_counts, color=victim_color, label='Victim')
    plt.bar(top_chars, perpetrator_counts, bottom=victim_counts, color=perpetrator_color, label='Perpetrator')

    plt.ylabel('Number of Occurrences')
    plt.xlabel('Character')
    plt.title(f'Top {top_n} Characters: Occurrences as Victim vs. Perpetrator')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    filename = 'victim_perpetrator_stacked_chart.png'
    plt.savefig(filename)
    plt.close()
    print(f"Saved {filename}")

# --- Generate Plots ---
create_combined_stacked_barchart(df.copy(), columns_to_analyze)
# Generate histograms for top 10 (excluding unspecified)
for col in columns_to_analyze:
    create_histogram(df.copy(), col, top_n=10)

create_zeus_histograms(df.copy())
create_victim_perpetrator_stacked_chart(df.copy())

print("All visualizations have been generated.")