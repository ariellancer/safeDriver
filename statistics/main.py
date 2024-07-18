import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')  # Use the Agg backend, which is non-interactive and suitable for saving figures
import matplotlib.pyplot as plt


def create_clock_pie_chart(data, output_filename):
    if len(data) != 12:
        raise ValueError("The input array must have 12 cells.")

    # Set equal-sized values for each slice
    equal_values = [1 / 12 for _ in range(12)]

    # Define colors based on percentage ranges
    colors = []
    percentiles = data.copy()
    percentiles.sort()
    percentiles = [percentiles[i] for i in [2,5,8]]

    for value in data:
        if value <= percentiles[0]:
            colors.append('#d9d2e9')  # Light Purple
        elif value <= percentiles[1]:
            colors.append('#b3a2c7')  # Medium Purple
        elif value <= percentiles[2]:
            colors.append('#7a5299')  # Dark Purple
        else:
            colors.append('#3f007d')  # Very Dark Purple

    # Create pie chart
    plt.figure(figsize=(5, 5))  # Adjusted for a 5.5-inch phone display
    plt.pie(equal_values, startangle=90, colors=colors)

    # Add text annotations
    plt.text(0, 1.1, '00:00', horizontalalignment='center', verticalalignment='center',
             fontsize=8)  # Adjusted font size
    plt.text(0, -1.1, '12:00', horizontalalignment='center', verticalalignment='center',
             fontsize=8)  # Adjusted font size
    plt.text(1.3, 0, '06:00', horizontalalignment='center', verticalalignment='center',
             fontsize=8)  # Adjusted font size
    plt.text(-1.3, 0, '18:00', horizontalalignment='center', verticalalignment='center',
             fontsize=8)  # Adjusted font size

    # Create legend
    legend_labels = ['You are very focused', 'Slightly tired, suggested to bring a snack',
                     'You are somewhat tired suggested driving with a friend',
                     'You are exhausted, do not get on the road']
    plt.legend(legend_labels, loc='upper right', bbox_to_anchor=(0.92, 0.05), fontsize=8)  # Adjusted legend font size

    # Save the plot as a PNG file
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')


# Example usage:
data_array = [50, 30, 45, 60, 20, 35, 50, 10, 80, 90, 10, 5]
output_filename = "your_statistics.png"
create_clock_pie_chart(data_array, output_filename)
