import pandas as pd
import matplotlib.pyplot as plt

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

# Clean and standardize data in the 'Murder' column
df['Murder'] = df['Murder'].astype(str).str.strip().str.lower()
df['Murder'].replace(['---', '', 'unnamed', 'nan'], 'unspecified', inplace=True)

# --- Visualization ---

def create_murder_distribution_chart(data_frame):
    """Creates a bar chart for the distribution of values in the 'Murder' column."""
    plt.figure(figsize=(10, 6))
    
    counts = data_frame['Murder'].value_counts()
    
    # Use a color palette
    colors = ['#4682B4', '#191970', '#008080']
    
    ax = counts.plot(kind='bar', color=colors)
    
    # Add counts on top of the bars
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=10)
    
    plt.title('Distribution of Murder (Yes/No/Unspecified)')
    plt.ylabel('Number of Occurrences')
    plt.xlabel('Murder')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    filename = '../images/murder_distribution.png'
    plt.savefig(filename)
    plt.close()
    print(f"Saved {filename}")

# --- Generate Plot ---
create_murder_distribution_chart(df)

print("Murder distribution visualization has been generated.")
