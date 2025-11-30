import pandas as pd

try:
    df = pd.read_csv('../MoD_Triples.csv')

    # Filter for Orpheus as victim (case-insensitive and partial match for robustness)
    # The original CSV has 'Orpheus' with different casing or leading/trailing spaces sometimes.
    # Also, some entries might have additional text. Let's make it robust.
    eurydice_df = df[df['Victim'].astype(str).str.strip().str.contains('Orpheus', case=False, na=False)]

    death_events_df = eurydice_df

    # Count occurrences of unique triples
    # Ensure all columns are treated as strings before grouping
    result_table = death_events_df.groupby(['Victim', 'Mode of Demise', 'Perpetrator']).size().reset_index(name='Count')

    # Display the total count and the table
    total_count = result_table['Count'].sum()

    print(f"Orpheus is the victim in {total_count} death event(s).")
    print("\nCounts for each unique triple (Orpheus, Mode of Demise, Perpetrator):")
    if not result_table.empty:
        print(result_table.to_markdown(index=False))
    else:
        print("No death events found for Orpheus meeting the criteria.")

except FileNotFoundError:
    print("Error: MoD_Triples.csv not found.")
    
except Exception as e:
    print(f"An error occurred: {e}")
