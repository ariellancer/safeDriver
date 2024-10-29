import matplotlib.pyplot as plt
import matplotlib
import io
import base64

from matplotlib.patches import Patch

matplotlib.use(
    'Agg')  # Use the Agg backend, which is non-interactive and suitable for saving figuresimport matplotlib.pyplot as plt


def create_clock_pie_chart(data):
    if len(data) != 12:
        raise ValueError("The input array must have 12 cells.")

    # Set equal-sized values for each slice
    equal_values = [1 / 12 for _ in range(12)]

    # Define colors based on percentage ranges
    colors = []
    percentiles = data.copy()
    percentiles = sorted(percentiles)
    thresholds = [percentiles[2], percentiles[5], percentiles[8]]
    data.reverse()  ##to make with clockwise
    for value in data:
        if value <= thresholds[0]:
            colors.append('#d9d2e9')  # Light Purple
        elif value <= thresholds[1]:
            colors.append('#b3a2c7')  # Medium Purple
        elif value <= thresholds[2]:
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
    legend_colors = ['#d9d2e9', '#b3a2c7', '#7a5299', '#3f007d']
    patches = [Patch(color=color, label=label) for color, label in zip(legend_colors, legend_labels)]
    plt.legend(handles=patches, loc='upper right', bbox_to_anchor=(0.92, 0.05), fontsize=8)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return img_base64
