import matplotlib.pyplot as plt

# Data from the previous analysis
categories = [
    'Natural & Supernatural',
    'Physical Violence',
    'Indirect/Psychological'
]
counts = [22, 24, 6]

# Create the bar chart in the style of visualize_data.py
plt.figure(figsize=(12, 8))
bars = plt.bar(categories, counts, color='#008080') # Teal color

# Add titles and labels
plt.title('Number of Modes of Demise per Upper Category', fontsize=16)
plt.ylabel('Number of Occurrences', fontsize=12)
plt.xlabel('Categories', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add the count labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center', fontsize=12)

# Ensure everything fits
plt.tight_layout()

# Save the figure
plt.savefig('../images/demise_category_histogram_styled.png')

print("Successfully generated demise_category_histogram_styled.png")
