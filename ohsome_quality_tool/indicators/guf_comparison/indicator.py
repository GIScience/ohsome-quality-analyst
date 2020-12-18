import json
import os
import uuid
from math import ceil
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import yaml
from geojson import FeatureCollection

from ohsome_quality_tool.base.indicator import BaseIndicator
from ohsome_quality_tool.utils import geodatabase, ohsome_api
from ohsome_quality_tool.utils.auth import PostgresDB
from ohsome_quality_tool.utils.definitions import (
    DATA_PATH,
    TrafficLightQualityLevels,
    logger,
)


class Indicator(BaseIndicator):
    """Set number of features and population into perspective."""

    name = "guf-comparison"
    description = (
        "Compare OSM features against built up area defined by "
        "Global Urban Footprint dataset."
    )

    def __init__(
        self,
        dynamic: bool,
        layer_name: str,
        bpolys: FeatureCollection = None,
        dataset: str = None,
        feature_id: str = None,
    ) -> None:
        super().__init__(
            dynamic=dynamic,
            layer_name=layer_name,
            bpolys=bpolys,
            dataset=dataset,
            feature_id=feature_id,
        )
        # TODO: Change arbitrary thresholds
        self.threshold_high: float = 0.6
        self.threshold_low: float = 0.2
        self.area: float = None
        self.guf_built_up_area: float = None
        self.osm_built_up_area: float = None
        self.ratio: float = None
        self.name: str = ""
        self.description: str = ""

        # TODO: Run during init instead by oqt.py
        #   Benni: Not sure if it needs to be done during init
        #   for instance we do not need to run this for
        #   pre-processed results, so maybe okay outside init?
        # self.preprocess()
        # self.calculate()
        # self.create_figure()

    def read_metadata(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(directory, "metadata.yaml")
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def preprocess(self) -> None:
        logger.info(f"run preprocessing for {self.name} indicator")
        db = PostgresDB()

        # Get data from geodatabase
        if self.dynamic:
            directory = os.path.dirname(os.path.abspath(__file__))
            aoi_geom = json.dumps(self.bpolys["features"][0]["geometry"])
            # Get total area and built-up area (GUF) in km^2 for AOI
            sql_file = os.path.join(directory, "query.sql")
            with open(sql_file) as reader:
                query = reader.read()
            result = db.retr_query(query=query, data=(aoi_geom, aoi_geom, aoi_geom))
            self.area = result[0][0] / 1000000  # m^2 to km^2
            self.guf_built_up_area = result[0][1] / 1000000
        else:
            # TODO: check if this works here
            self.guf_built_up_area = geodatabase.get_value_from_db(
                dataset=self.dataset,
                feature_id=self.feature_id,
                field_name="population",
            )

        # Get data from ohsome API
        # TODO: Difficult to read and understand.
        query_results = ohsome_api.process_ohsome_api(
            endpoint="elements/{unit}/",
            layers=self.layers,
            bpolys=json.dumps(self.bpolys),
        )
        self.osm_built_up_area = (
            query_results["buildings"]["result"][0]["value"] / 1000000
        )

    def calculate(
        self, preprocessing_results: Dict
    ) -> Tuple[TrafficLightQualityLevels, float, str, Dict]:

        self.ratio = self.guf_built_up_area / self.osm_built_up_area

        if self.ratio <= self.threshold_low:
            value = TrafficLightQualityLevels.RED.value
        elif self.ratio <= self.threshold_high:
            value = TrafficLightQualityLevels.YELLOW.value
        else:
            value = TrafficLightQualityLevels.GREEN.value

        label = TrafficLightQualityLevels(ceil(value))
        text = "test test test"

        return label, value, text, preprocessing_results

    def create_figure(self, data: Dict) -> str:
        """Create a plot and return as SVG string."""
        px = 1 / plt.rcParams["figure.dpi"]  # Pixel in inches
        figsize = (400 * px, 400 * px)
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()

        ax.set_title("Built-Up Area")
        ax.set_xlabel("Global Urban Footprint [%]")
        ax.set_ylabel("OpenStreetMap [%]")
        ax.set_xlim((0, 100))
        ax.set_ylim((0, 100))

        # Plot thresholds as line.
        x = [0, 100]
        y1 = [0, 100 * self.threshold_high]
        y2 = [0, 100 * self.threshold_low]
        line = line = ax.plot(
            x,
            y1,
            color="black",
            label="Threshold A",
        )
        plt.setp(line, linestyle="--")

        line = ax.plot(
            x,
            y2,
            color="black",
            label="Threshold B",
        )
        plt.setp(line, linestyle=":")

        # Fill in space between thresholds
        ax.fill_between(x, y2, 0, alpha=0.5, color="red")
        ax.fill_between(x, y1, y2, alpha=0.5, color="yellow")
        ax.fill_between(x, y1, 100, alpha=0.5, color="green")

        # Plot point as circle ("o").
        ax.plot(
            self.guf_built_up_area * 100 / self.area,
            self.osm_built_up_area * 100 / self.area,
            "o",
            color="black",
            label=(
                f"Indicator value: {round(self.ratio)}"
                # f"{round(self.guf_built_up_area)}/"
                # f"{round(self.osm_built_up_area)} "
                # f"[$km^2$]"
            ),
        )

        ax.legend()

        random_id = uuid.uuid1()
        filename = f"{self.name}_{random_id}.svg"
        outfile = os.path.join(DATA_PATH, filename)

        plt.savefig(outfile, format="svg")
        plt.close("all")
        logger.info(f"export figures for {self.name} indicator")
        return filename
