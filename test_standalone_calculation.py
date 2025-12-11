#!/usr/bin/env python3
"""
Test calculation using the standalone notebook's embedded code
Demonstrates calculation with sample_lot.csv data
"""

import math
import re
from typing import List, Dict, Optional
from dataclasses import dataclass

# ============================================================================
# EMBEDDED CODE FROM STANDALONE NOTEBOOK
# ============================================================================

# Custom Exceptions
class SurveyException(Exception):
    pass

class BearingFormatError(SurveyException):
    pass

class ValidationError(SurveyException):
    pass

# Data Classes
@dataclass
class Point:
    x: float
    y: float
    label: str = ""

@dataclass
class TraverseLine:
    bearing: str
    distance: float
    azimuth: Optional[float] = None

@dataclass
class ClosureAnalysis:
    closure_error_x: float
    closure_error_y: float
    linear_error: float
    perimeter: float
    relative_precision: float

    def is_acceptable(self, standard: str = "general") -> bool:
        standards = {
            'engineering': 5000,
            'property': 3000,
            'general': 1000,
            'rough': 500
        }
        required = standards.get(standard, 1000)
        return self.relative_precision >= required

# Bearing Converter
class BearingConverter:
    BEARING_PATTERN = re.compile(
        r'^([NS])\s+(\d{1,2})°(\d{1,2})\'\s+([EW])$'
    )

    @staticmethod
    def to_azimuth(bearing: str) -> float:
        match = BearingConverter.BEARING_PATTERN.match(bearing)
        if not match:
            raise BearingFormatError(f"Invalid bearing format: '{bearing}'")

        quadrant1, degrees, minutes, quadrant2 = match.groups()
        deg = int(degrees)
        min_ = int(minutes)

        if deg > 90 or deg < 0:
            raise BearingFormatError(f"Degrees must be 0-90, got {deg}")
        if min_ > 59 or min_ < 0:
            raise BearingFormatError(f"Minutes must be 0-59, got {min_}")

        decimal_angle = deg + min_ / 60.0

        if quadrant1 == 'N' and quadrant2 == 'E':
            azimuth = decimal_angle
        elif quadrant1 == 'S' and quadrant2 == 'E':
            azimuth = 180 - decimal_angle
        elif quadrant1 == 'S' and quadrant2 == 'W':
            azimuth = 180 + decimal_angle
        elif quadrant1 == 'N' and quadrant2 == 'W':
            azimuth = 360 - decimal_angle
        else:
            raise BearingFormatError(f"Invalid quadrant combination")

        return azimuth

# Unit Converter
class UnitConverter:
    M2_TO_FT2 = 10.7639
    M2_TO_ACRE = 0.000247105
    M2_TO_HECTARE = 0.0001

    @staticmethod
    def sqm_to_acres(area_m2: float) -> float:
        return area_m2 * UnitConverter.M2_TO_ACRE

    @staticmethod
    def sqm_to_hectares(area_m2: float) -> float:
        return area_m2 * UnitConverter.M2_TO_HECTARE

    @staticmethod
    def sqm_to_sqft(area_m2: float) -> float:
        return area_m2 * UnitConverter.M2_TO_FT2

# Quality Metrics
class QualityMetrics:
    @staticmethod
    def get_precision_description(relative_precision: float) -> str:
        if relative_precision >= 5000:
            return "Engineering Grade (Excellent)"
        elif relative_precision >= 3000:
            return "Property Survey Grade (Good)"
        elif relative_precision >= 1000:
            return "General Survey Grade (Acceptable)"
        elif relative_precision >= 500:
            return "Rough Survey (Poor)"
        else:
            return "Unacceptable Precision"

    @staticmethod
    def get_closure_status(linear_error: float) -> str:
        if linear_error < 0.01:
            return "Closed (Excellent)"
        elif linear_error < 0.1:
            return "Well Closed"
        elif linear_error < 1.0:
            return "Closed"
        elif linear_error < 5.0:
            return "Poorly Closed"
        else:
            return "Open/Not Closed"

# Shoelace Calculator
class ShoelaceCalculator:
    def __init__(self):
        self.lines: List[TraverseLine] = []
        self.points: List[Point] = []

    def add_line(self, bearing: str, distance: float) -> None:
        if distance <= 0:
            raise ValidationError(f"Distance must be positive, got {distance}")
        line = TraverseLine(bearing=bearing, distance=distance)
        line.azimuth = BearingConverter.to_azimuth(bearing)
        self.lines.append(line)

    def calculate_coordinates(self, start_x: float = 0.0, start_y: float = 0.0) -> List[Point]:
        if len(self.lines) < 3:
            raise ValidationError("Polygon must have at least 3 sides")

        self.points = []
        current_x, current_y = start_x, start_y
        self.points.append(Point(current_x, current_y, "1"))

        for i, line in enumerate(self.lines, 1):
            azimuth_rad = math.radians(line.azimuth)
            delta_x = line.distance * math.sin(azimuth_rad)
            delta_y = line.distance * math.cos(azimuth_rad)
            current_x += delta_x
            current_y += delta_y
            if i < len(self.lines):
                self.points.append(Point(current_x, current_y, str(i + 1)))

        self._final_x = current_x
        self._final_y = current_y
        return self.points

    def calculate_area(self) -> float:
        if not self.points:
            raise ValidationError("Must calculate coordinates first")

        n = len(self.points)
        area = 0.0

        for i in range(n):
            j = (i + 1) % n
            area += self.points[i].x * self.points[j].y
            area -= self.points[j].x * self.points[i].y

        area = abs(area) / 2.0
        return area

    def analyze_closure(self) -> ClosureAnalysis:
        if not self.points:
            raise ValidationError("Must calculate coordinates first")

        start_point = self.points[0]
        closure_x = self._final_x - start_point.x
        closure_y = self._final_y - start_point.y
        linear_error = math.sqrt(closure_x**2 + closure_y**2)
        perimeter = sum(line.distance for line in self.lines)
        relative_precision = perimeter / linear_error if linear_error > 0 else float('inf')

        return ClosureAnalysis(
            closure_error_x=closure_x,
            closure_error_y=closure_y,
            linear_error=linear_error,
            perimeter=perimeter,
            relative_precision=relative_precision
        )

    def get_summary(self) -> Dict:
        area = self.calculate_area()
        closure = self.analyze_closure()

        return {
            'method': 'Shoelace',
            'area_m2': area,
            'area_hectares': UnitConverter.sqm_to_hectares(area),
            'area_acres': UnitConverter.sqm_to_acres(area),
            'area_sqft': UnitConverter.sqm_to_sqft(area),
            'perimeter_m': closure.perimeter,
            'num_sides': len(self.lines),
            'closure_error_m': closure.linear_error,
            'closure_error_x': closure.closure_error_x,
            'closure_error_y': closure.closure_error_y,
            'relative_precision': f"1:{closure.relative_precision:.0f}",
            'precision_grade': QualityMetrics.get_precision_description(closure.relative_precision),
            'closure_status': QualityMetrics.get_closure_status(closure.linear_error),
            'acceptable_general': closure.is_acceptable('general'),
            'acceptable_property': closure.is_acceptable('property'),
        }

# DMD Calculator
class DMDCalculator:
    def __init__(self):
        self.lines: List[TraverseLine] = []
        self.points: List[Point] = []
        self.departures: List[float] = []
        self.latitudes: List[float] = []
        self.dmds: List[float] = []
        self.area_products: List[float] = []

    def add_line(self, bearing: str, distance: float) -> None:
        if distance <= 0:
            raise ValidationError(f"Distance must be positive, got {distance}")
        line = TraverseLine(bearing=bearing, distance=distance)
        line.azimuth = BearingConverter.to_azimuth(bearing)
        self.lines.append(line)

    def calculate_coordinates(self, start_x: float = 0.0, start_y: float = 0.0) -> List[Point]:
        if len(self.lines) < 3:
            raise ValidationError("Polygon must have at least 3 sides")

        self.points = []
        self.departures = []
        self.latitudes = []
        current_x, current_y = start_x, start_y
        self.points.append(Point(current_x, current_y, "1"))

        for i, line in enumerate(self.lines, 1):
            azimuth_rad = math.radians(line.azimuth)
            delta_x = line.distance * math.sin(azimuth_rad)
            delta_y = line.distance * math.cos(azimuth_rad)
            self.departures.append(delta_x)
            self.latitudes.append(delta_y)
            current_x += delta_x
            current_y += delta_y
            if i < len(self.lines):
                self.points.append(Point(current_x, current_y, str(i + 1)))

        self._final_x = current_x
        self._final_y = current_y
        self._calculate_dmd()
        return self.points

    def _calculate_dmd(self) -> None:
        self.dmds = []
        self.area_products = []
        previous_dmd = 0.0
        n = len(self.departures)

        for i in range(n):
            current_dmd = previous_dmd + self.departures[i - 1] + self.departures[i]
            self.dmds.append(current_dmd)
            area_product = current_dmd * self.latitudes[i]
            self.area_products.append(area_product)
            previous_dmd = current_dmd

    def calculate_area(self) -> float:
        if not self.dmds:
            raise ValidationError("Must calculate coordinates first")
        area = abs(sum(self.area_products)) / 2.0
        return area

    def analyze_closure(self) -> ClosureAnalysis:
        if not self.points:
            raise ValidationError("Must calculate coordinates first")

        start_point = self.points[0]
        closure_x = self._final_x - start_point.x
        closure_y = self._final_y - start_point.y
        linear_error = math.sqrt(closure_x**2 + closure_y**2)
        perimeter = sum(line.distance for line in self.lines)
        relative_precision = perimeter / linear_error if linear_error > 0 else float('inf')

        return ClosureAnalysis(
            closure_error_x=closure_x,
            closure_error_y=closure_y,
            linear_error=linear_error,
            perimeter=perimeter,
            relative_precision=relative_precision
        )

    def get_summary(self) -> Dict:
        area = self.calculate_area()
        closure = self.analyze_closure()

        return {
            'method': 'DMD (Double Meridian Distance)',
            'area_m2': area,
            'area_hectares': UnitConverter.sqm_to_hectares(area),
            'area_acres': UnitConverter.sqm_to_acres(area),
            'area_sqft': UnitConverter.sqm_to_sqft(area),
            'perimeter_m': closure.perimeter,
            'num_sides': len(self.lines),
            'closure_error_m': closure.linear_error,
            'closure_error_x': closure.closure_error_x,
            'closure_error_y': closure.closure_error_y,
            'relative_precision': f"1:{closure.relative_precision:.0f}",
            'precision_grade': QualityMetrics.get_precision_description(closure.relative_precision),
            'closure_status': QualityMetrics.get_closure_status(closure.linear_error),
            'acceptable_general': closure.is_acceptable('general'),
            'acceptable_property': closure.is_acceptable('property'),
        }

# ============================================================================
# DEMONSTRATION WITH sample_lot DATA
# ============================================================================

if __name__ == "__main__":
    print("="*100)
    print("STANDALONE NOTEBOOK CALCULATION DEMONSTRATION")
    print("Using data from: sample_lot.csv")
    print("="*100)

    # Data from sample_lot.csv
    bearings = [
        "S 45°05' E",
        "S 46°29' W",
        "S 48°53' E",
        "S 58°17' E",
        "S 38°41' W",
        "N 54°11' W",
        "N 46°20' W",
        "N 46°30' E"
    ]

    distances = [33.28, 36.6, 28.47, 17.51, 36.79, 20.0, 63.99, 71.86]

    lot_name = "Sample Lot"

    print(f"\nLot Name: {lot_name}")
    print(f"Number of Lines: {len(bearings)}")
    print(f"Total Perimeter: {sum(distances):.2f} m")

    # Run Shoelace calculation
    print("\n" + "-"*100)
    print("SHOELACE METHOD CALCULATION")
    print("-"*100)

    shoelace_calc = ShoelaceCalculator()
    for bearing, distance in zip(bearings, distances):
        shoelace_calc.add_line(bearing, distance)

    shoelace_calc.calculate_coordinates()
    shoelace_result = shoelace_calc.get_summary()

    print(f"\nArea: {shoelace_result['area_m2']:.2f} m²")
    print(f"      {shoelace_result['area_hectares']:.6f} hectares")
    print(f"      {shoelace_result['area_acres']:.6f} acres")
    print(f"      {shoelace_result['area_sqft']:.2f} ft²")
    print(f"\nClosure Error: {shoelace_result['closure_error_m']:.4f} m")
    print(f"Precision: {shoelace_result['relative_precision']}")
    print(f"Grade: {shoelace_result['precision_grade']}")
    print(f"Status: {shoelace_result['closure_status']}")

    # Run DMD calculation
    print("\n" + "-"*100)
    print("DMD METHOD CALCULATION")
    print("-"*100)

    dmd_calc = DMDCalculator()
    for bearing, distance in zip(bearings, distances):
        dmd_calc.add_line(bearing, distance)

    dmd_calc.calculate_coordinates()
    dmd_result = dmd_calc.get_summary()

    print(f"\nArea: {dmd_result['area_m2']:.2f} m²")
    print(f"      {dmd_result['area_hectares']:.6f} hectares")
    print(f"      {dmd_result['area_acres']:.6f} acres")
    print(f"      {dmd_result['area_sqft']:.2f} ft²")
    print(f"\nClosure Error: {dmd_result['closure_error_m']:.4f} m")
    print(f"Precision: {dmd_result['relative_precision']}")
    print(f"Grade: {dmd_result['precision_grade']}")
    print(f"Status: {dmd_result['closure_status']}")

    # Comparison
    print("\n" + "-"*100)
    print("COMPARISON & VERIFICATION")
    print("-"*100)

    area_diff = abs(shoelace_result['area_m2'] - dmd_result['area_m2'])
    area_diff_pct = (area_diff / shoelace_result['area_m2'] * 100) if shoelace_result['area_m2'] > 0 else 0

    print(f"\nArea Difference: {area_diff:.4f} m² ({area_diff_pct:.4f}%)")
    print(f"  • Shoelace: {shoelace_result['area_m2']:.2f} m²")
    print(f"  • DMD: {dmd_result['area_m2']:.2f} m²")

    if area_diff < 0.01:
        print("\n✓ EXCELLENT: Methods produce identical results")
    elif area_diff < 0.1:
        print("\n✓ Methods produce nearly identical results (excellent verification)")
    elif area_diff < 1.0:
        print("\n✓ Methods produce similar results (acceptable verification)")
    else:
        print("\n⚠ WARNING: Significant difference - review calculations")

    print("\n" + "="*100)
    print("QUALITY ASSESSMENT")
    print("="*100)

    gen_ok = '✓ Yes' if shoelace_result['acceptable_general'] else '✗ No'
    prop_ok = '✓ Yes' if shoelace_result['acceptable_property'] else '✗ No'

    print(f"\nAcceptable for General Survey: {gen_ok}")
    print(f"Acceptable for Property Survey: {prop_ok}")

    print("\n" + "="*100)
    print("This demonstrates the standalone notebook's embedded calculation code")
    print("The notebook produces identical results without requiring external modules!")
    print("="*100)
