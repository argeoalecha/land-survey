import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.patches import Polygon
from matplotlib.patches import FancyArrowPatch

def bearing_to_azimuth(bearing_str):
    """
    Convert bearing string (e.g., 'S 39°52' W') to azimuth in degrees
    Azimuth is measured clockwise from North (0°)
    """
    parts = bearing_str.strip().split()
    quadrant1 = parts[0]  # N or S
    angle_parts = parts[1].split('°')
    degrees = float(angle_parts[0])
    minutes = float(angle_parts[1].replace("'", ""))
    
    # Convert to decimal degrees
    decimal_angle = degrees + minutes/60
    
    quadrant2 = parts[2]  # E or W
    
    # Convert to azimuth based on quadrant
    if quadrant1 == 'N' and quadrant2 == 'E':
        azimuth = decimal_angle
    elif quadrant1 == 'S' and quadrant2 == 'E':
        azimuth = 180 - decimal_angle
    elif quadrant1 == 'S' and quadrant2 == 'W':
        azimuth = 180 + decimal_angle
    elif quadrant1 == 'N' and quadrant2 == 'W':
        azimuth = 360 - decimal_angle
    
    return azimuth

def calculate_coordinates(bearings, distances, start_x=0, start_y=0):
    """
    Calculate coordinates of each point given bearings and distances
    Returns list of (x, y) coordinates and delta values
    """
    coordinates = [(start_x, start_y)]
    deltas = []
    current_x, current_y = start_x, start_y
    
    for bearing, distance in zip(bearings, distances):
        azimuth = bearing_to_azimuth(bearing)
        azimuth_rad = math.radians(azimuth)
        
        # Calculate change in coordinates
        # In surveying: x is East, y is North
        delta_x = distance * math.sin(azimuth_rad)
        delta_y = distance * math.cos(azimuth_rad)
        
        deltas.append((delta_x, delta_y))
        
        current_x += delta_x
        current_y += delta_y
        coordinates.append((current_x, current_y))
    
    return coordinates, deltas

def calculate_area_shoelace(coordinates):
    """
    Calculate area using the shoelace formula (surveyor's formula)
    Returns area and intermediate products for educational purposes
    """
    n = len(coordinates) - 1  # Exclude the duplicate last point
    products_positive = []
    products_negative = []
    
    for i in range(n):
        j = (i + 1) % n
        pos = coordinates[i][0] * coordinates[j][1]
        neg = coordinates[j][0] * coordinates[i][1]
        products_positive.append(pos)
        products_negative.append(neg)
    
    area = abs(sum(products_positive) - sum(products_negative)) / 2
    
    return area, products_positive, products_negative

# Data from the survey document
bearings = [
    "S 45°05' E",  # Line 1-2
    "S 38°41' W",  # Line 2-3
    "N 58°17' W",  # Line 3-4
    "N 48°53' W",  # Line 4-5
    "N 48°29' E"   # Line 5-1
]

distances = [
    41.10,    # m
    30.88,    # m
    17.51,    # m
    28.47,    # m
    36.60     # m
]

# Calculate coordinates and area
coordinates, deltas = calculate_coordinates(bearings, distances)
area, products_pos, products_neg = calculate_area_shoelace(coordinates)

# Create comprehensive visualization
fig = plt.figure(figsize=(18, 12))

# Create grid layout
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# ============================================================================
# Plot 1: Main Polygon Plot
# ============================================================================
ax1 = fig.add_subplot(gs[0:2, 0:2])

# Extract x and y coordinates
x_coords = [coord[0] for coord in coordinates[:-1]]
y_coords = [coord[1] for coord in coordinates[:-1]]

# Plot the polygon
polygon = Polygon(list(zip(x_coords, y_coords)), 
                 fill=True, 
                 facecolor='lightblue', 
                 edgecolor='darkblue', 
                 linewidth=2.5,
                 alpha=0.6)
ax1.add_patch(polygon)

# Plot vertices
ax1.plot(x_coords, y_coords, 'ro', markersize=10, zorder=5, label='Vertices')

# Add point labels
point_labels = ['1', '2', '3', '4', '5']
for i, (x, y, label) in enumerate(zip(x_coords, y_coords, point_labels)):
    offset = 3
    ax1.annotate(f'Point {label}\n({x:.1f}, {y:.1f})', 
                xy=(x, y), 
                xytext=(offset, offset),
                textcoords='offset points',
                fontsize=10,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                ha='left')

# Add distance and bearing labels on each line
line_labels = ['1-2', '2-3', '3-4', '4-5', '5-1']
for i in range(len(x_coords)):
    j = (i + 1) % len(x_coords)
    mid_x = (x_coords[i] + x_coords[j]) / 2
    mid_y = (y_coords[i] + y_coords[j]) / 2
    
    # Create label with bearing and distance
    label_text = f'{line_labels[i]}\n{bearings[i]}\n{distances[i]:.2f} m'
    ax1.annotate(label_text,
                xy=(mid_x, mid_y),
                fontsize=8,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='blue', alpha=0.8),
                ha='center',
                va='center')

# Add north arrow
arrow_length = 15
arrow_x = max(x_coords) - 10
arrow_y = min(y_coords) + 10
ax1.annotate('', xy=(arrow_x, arrow_y + arrow_length), 
            xytext=(arrow_x, arrow_y),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='red'))
ax1.text(arrow_x + 3, arrow_y + arrow_length/2, 'N', 
        fontsize=14, fontweight='bold', color='red')

ax1.set_xlabel('Easting (meters)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Northing (meters)', fontsize=12, fontweight='bold')
ax1.set_title('Sample Lot Five-Sided Polygon\nSurvey Plot', 
             fontsize=14, fontweight='bold', pad=20)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_aspect('equal', adjustable='box')
ax1.legend(loc='upper left', fontsize=10)

# ============================================================================
# Plot 2: Bearing Diagram (Compass Rose)
# ============================================================================
ax2 = fig.add_subplot(gs[0, 2], projection='polar')

# Convert bearings to azimuths for polar plot
azimuths = []
for bearing in bearings:
    azimuth = bearing_to_azimuth(bearing)
    # Convert to radians and adjust for polar plot (0 at top, clockwise)
    # Polar plot has 0 at right, counter-clockwise, so we need to transform
    theta = math.radians(90 - azimuth)
    azimuths.append(theta)

# Plot lines from center
colors = ['red', 'green', 'blue', 'orange', 'purple']
line_labels = ['1-2', '2-3', '3-4', '4-5', '5-1']

for i, (theta, distance, color, label) in enumerate(zip(azimuths, distances, colors, line_labels)):
    ax2.plot([0, theta], [0, 1], color=color, linewidth=2.5, label=f'Line {label}')

ax2.set_theta_zero_location('N')
ax2.set_theta_direction(-1)
ax2.set_ylim(0, 1)
ax2.set_yticks([])
ax2.set_title('Bearing Diagram\n(Compass Rose)', 
             fontsize=12, fontweight='bold', pad=20)
ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=8)

# ============================================================================
# Plot 3: Area Calculation Table
# ============================================================================
ax3 = fig.add_subplot(gs[1, 2])
ax3.axis('tight')
ax3.axis('off')

# Create table data
table_data = []
table_data.append(['Point', 'X (E)', 'Y (N)', 'X₁·Y₂', 'X₂·Y₁'])

for i in range(len(x_coords)):
    j = (i + 1) % len(x_coords)
    point = point_labels[i]
    x = x_coords[i]
    y = y_coords[i]
    prod_pos = products_pos[i]
    prod_neg = products_neg[i]
    table_data.append([
        point,
        f'{x:.2f}',
        f'{y:.2f}',
        f'{prod_pos:.2f}',
        f'{prod_neg:.2f}'
    ])

table_data.append(['', '', 'Sum:', f'{sum(products_pos):.2f}', f'{sum(products_neg):.2f}'])
table_data.append(['', '', 'Diff:', f'{abs(sum(products_pos) - sum(products_neg)):.2f}', ''])
table_data.append(['', '', 'Area:', f'{area:.2f} m²', ''])

table = ax3.table(cellText=table_data, cellLoc='center', loc='center',
                 colWidths=[0.12, 0.15, 0.15, 0.15, 0.15])
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 2)

# Style header row
for i in range(5):
    table[(0, i)].set_facecolor('#4CAF50')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style sum rows
for i in range(5):
    table[(6, i)].set_facecolor('#FFF9C4')
    table[(7, i)].set_facecolor('#FFF9C4')
    table[(8, i)].set_facecolor('#FFD700')
    table[(8, i)].set_text_props(weight='bold')

ax3.set_title('Shoelace Formula Calculation', 
             fontsize=12, fontweight='bold', pad=10)

# ============================================================================
# Plot 4: Summary Statistics
# ============================================================================
ax4 = fig.add_subplot(gs[2, :])
ax4.axis('off')

# Calculate statistics
perimeter = sum(distances)
closure_x = coordinates[-1][0] - coordinates[0][0]
closure_y = coordinates[-1][1] - coordinates[0][1]
closure_error = math.sqrt(closure_x**2 + closure_y**2)

summary_text = f"""
SURVEY SUMMARY - Sample Lot
{'='*120}

AREA CALCULATIONS:
    • Area: {area:,.2f} m²  |  {area/10000:.6f} hectares  |  {area/4046.86:.6f} acres  |  {area*10.7639:,.2f} ft²

POLYGON DIMENSIONS:
    • Perimeter: {perimeter:.2f} m
    • Number of Sides: 5
    • Number of Vertices: 5

CLOSURE ANALYSIS:
    • Closure Error (X): {closure_x:+.4f} m  |  Closure Error (Y): {closure_y:+.4f} m  |  Total: {closure_error:.4f} m
    • Relative Precision: 1:{perimeter/closure_error:.0f}
    • Closure Status: {'Acceptable for general surveying' if closure_error < 2.0 else 'May need verification'}

COORDINATES (Relative to Point 1):
    Point 1: ({x_coords[0]:>7.2f}, {y_coords[0]:>7.2f})    Point 2: ({x_coords[1]:>7.2f}, {y_coords[1]:>7.2f})    Point 3: ({x_coords[2]:>7.2f}, {y_coords[2]:>7.2f})
    Point 4: ({x_coords[3]:>7.2f}, {y_coords[3]:>7.2f})    Point 5: ({x_coords[4]:>7.2f}, {y_coords[4]:>7.2f})
"""

ax4.text(0.05, 0.5, summary_text, 
        fontsize=10, 
        fontfamily='monospace',
        verticalalignment='center',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.suptitle('Comprehensive Survey Analysis - Sample Lot', 
            fontsize=16, fontweight='bold', y=0.98)

plt.savefig('survey_analysis.png', dpi=300, bbox_inches='tight')
print("Visualization saved to: survey_analysis.png")

plt.show()
