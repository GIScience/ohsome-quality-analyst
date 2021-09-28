import logging
from io import StringIO
from string import Template

import matplotlib.pyplot as plt
import numpy as np
from dateutil.parser import isoparse
from geojson import Feature

from ohsome_quality_analyst.base.indicator import BaseIndicator
from ohsome_quality_analyst.indicators.mapping_saturation.fit import get_best_fit
from ohsome_quality_analyst.ohsome import client as ohsome_client

# threshold values defining the color of the traffic light
# derived directly from MA Katha p24 (mixture of Gröchenig et al. +  Barrington-Leigh)
# saturation: 0 < f‘(x) <= 0.03 and years with saturation > 2
THRESHOLD_YELLOW = 0.03
# TODO define THRESHOLD_RED (where start stadium ends) with function from MA


class MappingSaturation(BaseIndicator):
    """The Mapping Saturation Indicator.

    Time period is one month since 2008.
    """

    def __init__(
        self,
        layer_name: str,
        feature: Feature,
        time_range: str = "2008-01-01//P1M",
    ) -> None:
        super().__init__(
            layer_name=layer_name,
            feature=feature,
        )
        self.time_range = time_range
        # The following attributes will be set during the life-cycle of the object.
        # Attributes needed for calculation
        self.values: list = []
        self.timestamps: list = []
        self.no_data: bool = False
        self.deleted_data: bool = False

        # Attributes needed for result determination
        self.saturation = None
        self.growth = None

    async def preprocess(self) -> None:
        query_results = await ohsome_client.query(
            layer=self.layer, bpolys=self.feature.geometry, time=self.time_range
        )
        self.values = [item["value"] for item in query_results["result"]]
        self.timestamps = [
            isoparse(item["timestamp"]) for item in query_results["result"]
        ]
        # Latest timestamp of ohsome API results
        self.result.timestamp_osm = self.timestamps[-1]
        max_value = max(self.values)
        if max_value == 0:
            self.no_data = True
        elif self.values[-1] == 0:
            self.deleted_data = True

    def calculate(self) -> None:
        """Calculate the growth rate and saturation level within the last 3 years."""
        if self.no_data:
            self.result.description = "No features were mapped in this region."
            return
        if self.deleted_data:
            self.result.description = (
                "All mapped features in this region have been since deleted."
            )
            return
        xdata = list(range(len(self.timestamps)))
        best_fit = get_best_fit(xdata=xdata, ydata=self.values)
        if max(self.values) <= 2:
            # start stadium, some data are there, but not much
            self.saturation = 0
        else:
            # calculate slope of last 3 years (saturation)
            self.saturation = (np.interp(xdata[-36], xdata, best_fit.ydata)) / (
                np.interp(xdata[-1], xdata, best_fit.ydata)
            )
        self.growth = 1 - self.saturation
        description = Template(self.metadata.result_description).substitute(
            saturation=self.saturation,
            growth=self.growth,
        )
        if self.saturation == 0:
            self.result.label = "red"
            self.result.value = 0.0
            self.result.description = (
                description + self.metadata.label_description["red"]
            )
        # growth is larger than 3% within last 3 years
        elif self.growth <= THRESHOLD_YELLOW:
            self.result.label = "green"
            self.result.value = 1.0
            self.result.description = (
                description + self.metadata.label_description["green"]
            )
        else:
            self.result.label = "yellow"
            self.result.value = 0.5
            self.result.description = (
                description + self.metadata.label_description["yellow"]
            )

    def create_figure(self) -> None:
        """Create svg with data line in blue and sigmoid curve in red."""
        if self.result.label == "undefined":
            logging.info("Result is undefined. Skipping figure creation.")
            return
        xdata = list(range(len(self.timestamps)))
        best_fit = get_best_fit(xdata=xdata, ydata=self.values)
        # color the lines with different colors
        linecol = ["b-", "g-", "r-", "y-", "black", "gray", "m-", "c-"]
        px = 1 / plt.rcParams["figure.dpi"]  # Pixel in inches
        figsize = (400 * px, 400 * px)
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()
        ax.set_title("Saturation level of the data")
        # plot the data
        ax.plot(
            self.timestamps,
            self.values,
            linecol[0],
            label="OSM data",
        )
        # plot sigmoid curve
        ax.plot(
            self.timestamps,
            best_fit.ydata,
            linecol[2],
            label="Sigmoid curve: " + best_fit.name,
        )
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.45))
        fig.subplots_adjust(bottom=0.3)
        fig.tight_layout()
        img_data = StringIO()
        plt.savefig(img_data, format="svg", bbox_inches="tight")
        self.result.svg = img_data.getvalue()  # this is svg data
        logging.debug("Successful SVG figure creation")
        plt.close("all")
