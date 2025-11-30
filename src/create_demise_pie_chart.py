import matplotlib.pyplot as plt

# Data from the previous analysis
categories = [
    'Natural & Supernatural',
    'Physical Violence',
    'Indirect/Psychological'
]
counts = [22, 24, 6]
# Using shades of blue as requested
colors = ['#4682B4', '#191970', '#A0C4FF']

# Create the pie chart
plt.figure(figsize=(10, 8))
wedges, texts, autotexts = plt.pie(counts, labels=categories, colors=colors, autopct='%1.1f%%', startangle=140, pctdistance=0.85)

# Make the percentages bigger and bold
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_fontweight('bold')
    autotext.set_color('white')

# Add a title
plt.title('Distribution of Modes of Demise per Upper Category', fontsize=16)

# Equal aspect ratio ensures that pie is drawn as a circle.
plt.axis('equal')  

# Save the figure
plt.savefig('../images/demise_category_pie_chart.png')

print("Successfully generated demise_category_pie_chart.png")
