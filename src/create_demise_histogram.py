import matplotlib.pyplot as plt

# Data from the previous analysis
categories = [
    'Natural & Supernatural',
    'Physical Violence',
    'Indirect/Psychological'
]
counts = [22, 24, 6]

# Create the bar chart
plt.figure(figsize=(10, 6))
bars = plt.bar(categories, counts, color=['#1f77b4', '#ff7f0e', '#2ca02c'])

# Add titles and labels
plt.title('Number of Modes of Demise per Upper Category', fontsize=16)
plt.ylabel('Number of Modes', fontsize=12)
plt.xlabel('Categories', fontsize=12)
plt.xticks(rotation=10) # Rotate labels slightly for better readability

# Add the count labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center', fontsize=12)

# Ensure everything fits
plt.tight_layout()

# Save the figure
plt.savefig('../images/demise_category_histogram.png')

print("Successfully generated demise_category_histogram.png")
