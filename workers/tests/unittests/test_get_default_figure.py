import os
import unittest

import geojson

from ohsome_quality_analyst.indicators.ghs_pop_comparison.indicator import (
    GhsPopComparison,
)


class TestGetDefaultFigure(unittest.TestCase):
    def test_get_default_figure(self):
        infile = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "fixtures",
            "heidelberg_altstadt.geojson",
        )
        with open(infile, "r") as f:
            bpolys = geojson.load(f)
        indicator = GhsPopComparison(bpolys=bpolys, layer_name="building_count")
        self.assertIsInstance(indicator.result.svg, str)
        # TODO: Validate SVG