# Land Survey Calculator

A professional, self-contained Jupyter notebook for calculating land survey areas using dual verification methods (Shoelace Formula and Double Meridian Distance). Produces publication-quality visualizations and comprehensive analysis reports.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

![Survey Visualization Example](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## 🎯 Features

### Core Capabilities
- ✅ **Dual Calculation Methods** - Independent verification using Shoelace and DMD
- ✅ **Self-Contained** - All formulas embedded (no external dependencies)
- ✅ **Multiple Input Options** - CSV, Excel, or paste data directly
- ✅ **Professional Visualizations** - Publication-quality polygon plots and comparison charts
- ✅ **Comprehensive Analysis** - Closure error, precision metrics, quality assessment
- ✅ **Unit Conversion** - Automatic conversion to m², hectares, acres, and sq ft

### Advanced Features
- 🎨 **Professional polygon visualization** with smart label positioning
- 📊 **Comparison charts** showing area, units, and closure errors
- 🧭 **North arrow indicator** with circular styling
- 📈 **Quality metrics** with precision grading (Engineering/Property/General)
- ⚠️ **Closure error analysis** with visual indicators
- 📋 **Detailed summary reports** with method comparison

---

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Data Format](#data-format)
- [Usage](#usage)
- [Output Examples](#output-examples)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab

### Setup

1. **Clone or download** this repository:
   ```bash
   git clone https://github.com/argeoalecha/land-survey.git
   cd "surveyor formulas"
   ```

2. **Install Jupyter** (if not already installed):
   ```bash
   pip install jupyter
   ```

3. **Open the notebook**:
   ```bash
   jupyter notebook Land_survey_Calculator.ipynb
   ```

4. **Dependencies** - The notebook automatically installs required packages:
   - pandas
   - matplotlib
   - openpyxl
   - numpy

---

## ⚡ Quick Start

### Option 1: Using Sample Data (Fastest)

1. Open `Land_survey_Calculator.ipynb`
2. Click **Cell → Run All**
3. Enter a lot name when prompted (or press Enter for default)
4. Review results and visualizations

The notebook includes sample survey data for immediate testing.

### Option 2: Using Your Own CSV File

1. Prepare your CSV file with columns: `Lines`, `Bearings`, `Distances`
2. In **Cell 8**, uncomment and modify:
   ```python
   csv_file = 'your_survey.csv'
   df = pd.read_csv(csv_file)
   ```
3. Comment out the default data in **Cell 10**
4. Run all cells

### Option 3: Using Excel File

1. In **Cell 9**, uncomment and modify:
   ```python
   excel_file = 'your_survey.xlsx'
   df = pd.read_excel(excel_file, sheet_name=0)
   ```
2. Comment out the default data in **Cell 10**
3. Run all cells

---

## 📝 Data Format

### Required Columns

Your data must include three columns:

| Lines | Bearings    | Distances |
|-------|-------------|-----------|
| 1-2   | S 45°05' E  | 33.28     |
| 2-3   | S 46°29' W  | 36.60     |
| 3-4   | S 48°53' E  | 28.47     |
| ...   | ...         | ...       |

### Bearing Format

Bearings must follow the format: `[N/S] [Degrees]°[Minutes]' [E/W]`

**Valid Examples:**
```
S 45°05' E  → Southeast, 45 degrees 5 minutes
N 46°29' W  → Northwest, 46 degrees 29 minutes
S 48°53' E  → Southeast, 48 degrees 53 minutes
N 54°11' W  → Northwest, 54 degrees 11 minutes
```

**Valid Quadrants:**
- `N xxx° E` → Northeast (0° to 90°)
- `S xxx° E` → Southeast (0° to 90°)
- `S xxx° W` → Southwest (0° to 90°)
- `N xxx° W` → Northwest (0° to 90°)

### Distance Format
- Must be numeric (decimal values allowed)
- Unit: meters
- Must be positive values

---

## 💻 Usage

### Step-by-Step Workflow

1. **Install Dependencies** (Cell 1)
   - Automatic installation of required packages
   - One-time setup

2. **Import Libraries** (Cell 2)
   - Loads Python libraries

3. **Load Utilities** (Cells 3-6)
   - Embedded calculation formulas
   - No external files required

4. **Input Data** (Cells 7-10)
   - Choose your input method
   - Validate data format

5. **Run Calculations** (Cells 11-12)
   - Enter lot name
   - Execute both methods

6. **Review Results** (Cells 13-17)
   - Summary reports
   - Comparison tables
   - Visualizations

### Calculation Methods

#### 1. Shoelace Formula (Surveyor's Formula)
```
Area = |∑(xᵢ × yᵢ₊₁ - xᵢ₊₁ × yᵢ)| / 2
```

#### 2. DMD Method (Double Meridian Distance)
```
Area = |∑(DMD × Latitude)| / 2
Where: DMD = previous_DMD + previous_departure + current_departure
```

Both methods calculate independently for verification and quality assurance.

---

## 📊 Output Examples

### 1. Summary Report
```
====================================================================================================
SURVEY ANALYSIS SUMMARY - Sample Lot
====================================================================================================

SHOELACE METHOD
  AREA CALCULATIONS:
    •     4,091.61 m²
    •     0.409161 hectares
    •     1.011058 acres
    •    44,041.71 ft²

  CLOSURE ANALYSIS:
    • Linear Error: 0.0088 m
    • Precision: 1:35082
    • Grade: Engineering Grade (Excellent)
    • Status: Closed (Excellent)
```

### 2. Comparison Table
| Metric              | Shoelace Method | DMD Method  |
|---------------------|-----------------|-------------|
| Area (m²)           | 4091.61         | 4091.77     |
| Area (hectares)     | 0.409161        | 0.409177    |
| Closure Error (m)   | 0.0088          | 0.0088      |
| Precision           | 1:35082         | 1:35082     |
| Status              | Closed          | Closed      |

### 3. Visualizations

#### A. Comparison Charts (Cell 15)
- Area comparison bar chart
- Unit conversion comparison
- Closure error analysis
- Survey statistics summary

#### B. Professional Polygon Plot (Cell 16)
- Survey polygon with vertices and coordinates
- Bearing and distance labels on each line
- North arrow with circular indicator
- Area/Perimeter info box
- Closure error indicator
- Smart label positioning
- Publication-quality graphics

---

## 🔧 Technical Details

### Notebook Structure (35 Cells)

#### Setup Section (Cells 1-2)
- Dependency installation
- Library imports

#### Embedded Code (Cells 3-6)
- **Cell 3**: Shared utilities (exceptions, data classes, converters)
- **Cell 4**: Shoelace Calculator
- **Cell 5**: DMD Calculator
- **Cell 6**: Survey Runner (orchestrator)

#### Input Section (Cells 7-10)
- **Cell 7**: Instructions (markdown)
- **Cell 8**: CSV file input (commented)
- **Cell 9**: Excel file input (commented)
- **Cell 10**: Paste data directly (active by default)

#### Execution Section (Cells 11-17)
- **Cell 11**: Data validation
- **Cell 12**: Run calculations
- **Cell 13**: Print summary
- **Cell 14**: Comparison table
- **Cell 15**: Comparison charts (2×2 grid)
- **Cell 16**: Professional polygon visualization
- **Cell 17**: Input data reference

### Quality Metrics

| Precision Grade | Relative Precision | Suitability |
|----------------|-------------------|-------------|
| Engineering    | ≥ 1:5000         | Excellent   |
| Property       | ≥ 1:3000         | Good        |
| General        | ≥ 1:1000         | Acceptable  |
| Rough          | ≥ 1:500          | Poor        |

### Closure Error Standards

| Linear Error | Status          |
|--------------|-----------------|
| < 0.01 m     | Closed (Excellent) |
| < 0.1 m      | Well Closed     |
| < 1.0 m      | Closed          |
| < 5.0 m      | Poorly Closed   |
| ≥ 5.0 m      | Open/Not Closed |

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "Module not found" error
**Solution:**
```python
# Run Cell 1 to install dependencies
# Then restart kernel: Kernel → Restart
```

#### 2. "File not found" error (CSV/Excel input)
**Solutions:**
- Verify file is in the same directory as notebook
- Use absolute path: `/full/path/to/your_survey.csv`
- Check file name spelling

#### 3. Data validation errors
**Check:**
- CSV has columns: `Lines`, `Bearings`, `Distances`
- Bearing format: `S 45°05' E` (with ° and ')
- Distances are numeric values
- No negative distances

#### 4. Bearing format errors
**Common mistakes:**
- Missing degree symbol (°) → Use Alt+0 (Windows) or Option+0 (Mac)
- Using apostrophe (') instead of minute symbol (')
- Incorrect quadrant combination (e.g., N xxx° S)

#### 5. Visualization not displaying
**Solutions:**
```python
# Add this at the top of visualization cells:
%matplotlib inline

# Or try:
%matplotlib notebook
```

### Getting Help

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review error messages carefully
3. Verify data format matches examples
4. Try with sample data first
5. Refer to [STANDALONE_NOTEBOOK_GUIDE.md](STANDALONE_NOTEBOOK_GUIDE.md)

---

## 📈 Examples

### Example 1: 8-Sided Polygon (LOT_7156-C2)

**Input Data:**
```csv
Lines,Bearings,Distances
1-2,S 45°05' E,33.28
2-3,S 46°29' W,36.60
3-4,S 48°53' E,28.47
4-5,S 58°17' E,17.51
5-6,S 38°41' W,36.79
6-7,N 54°11' W,20.00
7-8,N 46°20' W,63.99
8-1,N 46°30' E,71.86
```

**Results:**
- **Area:** 4,091.61 m² (0.409 hectares / 1.011 acres)
- **Perimeter:** 308.50 m
- **Closure Error:** 0.0088 m
- **Precision:** 1:35,082 (Engineering Grade)

### Example 2: 5-Sided Polygon

**Results:**
- **Area:** Calculated using both methods
- **Verification:** < 0.1 m² difference
- **Quality:** Suitable for property surveys

---

## 🧮 Formulas & Algorithms

### Coordinate Calculation
```python
# From bearing and distance to (x, y) coordinates
azimuth = bearing_to_azimuth(bearing)
delta_x = distance * sin(azimuth)  # Easting
delta_y = distance * cos(azimuth)  # Northing
```

### Shoelace Area Formula
```python
area = 0
for i in range(n):
    j = (i + 1) % n
    area += points[i].x * points[j].y
    area -= points[j].x * points[i].y
area = abs(area) / 2
```

### DMD Area Formula
```python
for i in range(n):
    DMD[i] = DMD[i-1] + departure[i-1] + departure[i]
    area_product[i] = DMD[i] * latitude[i]
area = abs(sum(area_products)) / 2
```

### Closure Analysis
```python
closure_x = final_x - start_x
closure_y = final_y - start_y
linear_error = sqrt(closure_x² + closure_y²)
relative_precision = perimeter / linear_error
```

---

## 🎨 Visualization Features

### Polygon Plot Enhancements
- **Smart Label Positioning**: Automatically positions labels to avoid overlap
- **North Arrow**: Red arrow with circular 'N' indicator
- **Info Boxes**: Area, perimeter, and precision metrics
- **Color Scheme**: Professional blue/yellow/gray palette
- **Grid Styling**: Dashed gray lines on subtle background
- **Equal Aspect Ratio**: Accurate spatial representation
- **Publication Quality**: Suitable for reports and presentations

### Chart Enhancements
- **2×2 Comparison Grid**: Area, units, errors, statistics
- **Color-Coded Bars**: Visual distinction between methods
- **Data Labels**: Values displayed on charts
- **Professional Styling**: Clean, modern appearance

---

## 🔄 Comparison with Other Tools

### Advantages
- ✅ **Self-Contained**: No external dependencies
- ✅ **Dual Verification**: Two independent calculation methods
- ✅ **Visual Feedback**: Professional polygon plots
- ✅ **Quality Metrics**: Automatic precision grading
- ✅ **Multiple Input Options**: CSV, Excel, or paste
- ✅ **Free & Open Source**: No licensing costs

### Limitations
- ❌ No batch processing (single lot at a time)
- ❌ No export to CAD formats
- ❌ No GPS coordinate import
- ❌ No topographic adjustments

---

## 📚 References

### Surveying Formulas
- Shoelace Formula (Gauss's Area Formula)
- Double Meridian Distance Method
- Traverse Closure Analysis
- Coordinate Geometry in Surveying

### Standards
- Engineering Survey Standards (1:5000)
- Property Survey Standards (1:3000)
- General Survey Standards (1:1000)

### Unit Conversions
- 1 m² = 10.7639 ft²
- 1 m² = 0.000247105 acres
- 1 m² = 0.0001 hectares

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Areas for Contribution
- Additional visualization options
- Support for more input formats
- Export functionality (PDF, PNG, CSV)
- Batch processing multiple surveys
- Additional calculation methods
- Unit tests
- Documentation improvements

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Argeo Alecha**
- GitHub: [@argeoalecha](https://github.com/argeoalecha)
- Project: Land Survey Calculator

---

## 🙏 Acknowledgments

- Based on classical surveying formulas and methods
- Inspired by professional surveying software (AutoCAD Civil 3D, Carlson Survey)
- Built with Python, Jupyter, and open-source libraries
- Enhanced visualizations based on `survey_visualization.py`

---

## 📞 Support

If you encounter issues or have questions:
- Review the [STANDALONE_NOTEBOOK_GUIDE.md](STANDALONE_NOTEBOOK_GUIDE.md)
- Check the [Troubleshooting](#troubleshooting) section
- Open an issue on GitHub with error details

---

## 🗺️ Roadmap

### Future Enhancements
- [ ] PDF report generation
- [ ] Batch processing multiple lots
- [ ] Interactive web interface
- [ ] GPS coordinate support
- [ ] Topographic adjustments
- [ ] Additional coordinate systems
- [ ] Export to CAD formats
- [ ] Mobile-friendly version

---

## 📊 Project Stats

- **Language**: Python 3.8+
- **Notebook Cells**: 35
- **Lines of Code**: ~1,500
- **Dependencies**: 4 (pandas, matplotlib, numpy, openpyxl)
- **Calculation Methods**: 2 (Shoelace, DMD)
- **Visualization Types**: 6 (polygon plot, comparison charts)

---

## 🔖 Version History

### v1.2.0 (Current - December 2024)
- ✨ Enhanced polygon visualization with professional styling
- 🎨 Smart label positioning
- 🧭 Circular north arrow indicator
- 📊 Info boxes for metrics
- ⚠️ Closure error visualization
- 📈 Publication-quality graphics

### v1.1.0 (November 2024)
- Added polygon visualization
- Improved comparison charts
- Better error handling

### v1.0.0 (Initial Release)
- Basic Shoelace and DMD calculations
- Three input options
- Summary reports

---

## 📁 Project Files

### Main Files
- **Land_survey_Calculator.ipynb** - Main calculator notebook (self-contained)
- **README.md** - This file (project documentation)
- **STANDALONE_NOTEBOOK_GUIDE.md** - Detailed usage guide
- **LOT_7156-C2.csv** - Sample survey data for testing

### Reference Files
- **survey_visualization.py** - Reference visualization code
- **test_standalone_calculation.py** - Test script demonstrating calculations

### Legacy Files
- **Surveyors_Calculator_*.ipynb** - Original notebooks (require external modules)
- **surveyors-calculator/** - Original calculator modules (deprecated)

---

<div align="center">

**Made with ❤️ for surveyors and engineers**

⭐ **If you find this useful, please star this repository!**

---

[Report Bug](https://github.com/argeoalecha/land-survey/issues) · [Request Feature](https://github.com/argeoalecha/land-survey/issues) · [Documentation](STANDALONE_NOTEBOOK_GUIDE.md)

</div>
