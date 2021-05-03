import unittest
from unittest.mock import Mock

from ohsome_quality_analyst.reports.remote_mapping_level_one.report import (
    RemoteMappingLevelOne,
)


class TestReportRemoteMappingLevelOne(unittest.TestCase):
    def test_combine_indicators_mean(self):
        report = RemoteMappingLevelOne()
        report.set_indicator_layer()

        # Mock indicator objects with a fixed result value
        for _ in report.indicator_layer:
            indicator = Mock()
            indicator.result = Mock()
            indicator.result.value = 0.5
            report.indicators.append(indicator)

        report.combine_indicators()

        self.assertIsNotNone(report.result.label)
        self.assertIsNotNone(report.result.description)
        # Should be the mean of all indicator result values
        self.assertEqual(report.result.value, 0.5)


if __name__ == "__main__":
    unittest.main()