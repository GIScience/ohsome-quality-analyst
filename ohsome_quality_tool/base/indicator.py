import os
import uuid
from abc import ABCMeta, abstractmethod
from typing import Dict, Tuple

from geojson import FeatureCollection

from ohsome_quality_tool.utils.definitions import (
    DATA_PATH,
    IndicatorMetadata,
    IndicatorResult,
    TrafficLightQualityLevels,
    logger,
)
from ohsome_quality_tool.utils.geodatabase import (
    get_bpolys_from_db,
    get_indicator_results_from_db,
    save_indicator_results_to_db,
)
from ohsome_quality_tool.utils.layers import get_all_layer_definitions


class BaseIndicator(metaclass=ABCMeta):
    """The base class for all indicators."""

    def __init__(
        self,
        dynamic: bool,
        layer_name: str,
        bpolys: FeatureCollection = None,
        dataset: str = None,
        feature_id: int = None,
    ) -> None:
        """Initialize an indicator"""
        # here we can put the default parameters for indicators
        self.dynamic = dynamic
        self.layer = get_all_layer_definitions()[layer_name]
        self.metadata = IndicatorMetadata(
            indicator_name=self.name,
            indicator_description=self.description,
            layer_name=self.layer.name,
            layer_description=self.layer.description,
        )

        # generate random id for filename to avoid overwriting existing files
        random_id = uuid.uuid1()
        self.filename = f"{self.name}_{self.layer.name}_{random_id}.svg"
        self.outfile = os.path.join(DATA_PATH, self.filename)

        if self.dynamic:
            if bpolys is None:
                raise ValueError("Dynamic calculation requires a GeoJSON as input.")
            self.bpolys = bpolys
        else:
            if dataset is None or feature_id is None:
                raise ValueError(
                    "Static calculation requires the dataset name "
                    "and the feature id as string."
                )
            self.dataset = dataset
            self.feature_id = feature_id
            self.bpolys = get_bpolys_from_db(self.dataset, self.feature_id)

    def get(self) -> Tuple[IndicatorResult, IndicatorMetadata]:
        """Pass the indicator results to the user.

        For dynamic indicators this will trigger the processing.
        For non-dynamic (pre-processed) indicators this will
        extract the results from the geo database.
        """
        if self.dynamic:
            logger.info(f"Run processing for dynamic indicator {self.name}.")
            result = self.run_processing()
        else:
            logger.info(
                f"Get pre-processed results from geo db for indicator {self.name}."
            )
            result = self.get_from_database()

        return result, self.metadata

    def run_processing(self) -> IndicatorResult:
        """Run all steps needed to actually compute the indicator"""
        preprocessing_results = self.preprocess()
        label, value, text, data = self.calculate(preprocessing_results)
        svg = self.create_figure(data)
        logger.info(f"finished run for indicator {self.name}")

        result = IndicatorResult(
            label=label.name,
            value=value,
            text=text,
            svg=svg,
        )

        return result

    def save_to_database(self, result: IndicatorResult) -> None:
        """Save the results to the geo database."""
        save_indicator_results_to_db(
            dataset=self.dataset,
            feature_id=self.feature_id,
            layer_name=self.layer.name,
            indicator=self.name,
            results=result,
        )

    def get_from_database(self) -> IndicatorResult:
        """Get pre-processed indicator results from geo database."""
        result = get_indicator_results_from_db(
            dataset=self.dataset,
            feature_id=self.feature_id,
            layer_name=self.layer.name,
            indicator=self.name,
        )
        return result

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    # the abstract method defines that this function
    # needs to be implemented by all children
    @abstractmethod
    def preprocess(self) -> Dict:
        pass

    @abstractmethod
    def calculate(
        self, preprocessing_results: Dict
    ) -> Tuple[TrafficLightQualityLevels, float, str, Dict]:
        pass

    @abstractmethod
    def create_figure(self, data: Dict):
        pass
