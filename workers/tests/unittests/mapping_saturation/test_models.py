import unittest

import fixtures
import numpy as np

from ohsome_quality_analyst.indicators.mapping_saturation import models


class TestModels(unittest.TestCase):
    def setUp(self):
        self.ydata = fixtures.VALUES
        self.xdata = np.asarray(range(len(fixtures.VALUES)))

    def test_sigmoid(self):
        model = models.Sigmoid()

        guess = model.initial_guess(self.xdata, self.ydata)
        self.assertIsNotNone(guess)

        bounds = model.bounds(self.xdata, self.ydata)
        self.assertIsNotNone(bounds)

        coef = model.fit(self.xdata, self.ydata)
        self.assertIsNotNone(coef)

        ydata = model.function(self.xdata, **coef)
        self.assertIsNotNone(ydata)

    def test_sslogis(self):
        model = models.SSlogis()
        coef = model.fit(self.xdata, self.ydata)
        self.assertIsNotNone(coef)
        ydata = model.function(self.xdata, **coef)
        self.assertIsNotNone(ydata)

    def test_ssdoubles(self):
        model = models.SSdoubleS()
        guess = model.initial_guess(self.xdata, self.ydata)
        self.assertIsNotNone(guess)

        coef = model.fit(self.xdata, self.ydata)
        self.assertIsNotNone(coef)

        ydata = model.function(self.xdata, **coef)
        self.assertIsNotNone(ydata)

    def test_ssfpl(self):
        model = models.SSfpl()
        coef = model.fit(self.xdata, self.ydata)
        self.assertIsNotNone(coef)
        ydata = model.function(self.xdata, **coef)
        self.assertIsNotNone(ydata)

    def test_ssasymp(self):
        model = models.SSasymp()
        coef = model.fit(self.xdata, self.ydata)
        self.assertIsNotNone(coef)
        ydata = model.function(self.xdata, **coef)
        self.assertIsNotNone(ydata)

    def test_ssmicmen_inlcude_zero(self):
        """Test model with zero in input data."""
        model = models.SSmicmen()
        # xdata starts with first element = 0
        coef = model.fit(self.xdata, self.ydata)
        self.assertIsNotNone(coef)
        ydata = model.function(self.xdata, **coef)
        self.assertIsNotNone(ydata)

    def test_ssmicmen_without_zero(self):
        model = models.SSmicmen()
        # To avoid zero in input data add 1 to each element
        coef = model.fit(self.xdata + 1, self.ydata)
        self.assertIsNotNone(coef)
        ydata = model.function(self.xdata, **coef)
        self.assertIsNotNone(ydata)


if __name__ == "__main__":
    unittest.main()
