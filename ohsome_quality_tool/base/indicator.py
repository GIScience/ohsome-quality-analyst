from abc import ABCMeta, abstractmethod
from typing import Dict, Tuple

from geojson import FeatureCollection

from ohsome_quality_tool.utils.config import logger
from ohsome_quality_tool.utils.definitions import (
    IndicatorMetadata,
    IndicatorResult,
    TrafficLightQualityLevels,
)
from ohsome_quality_tool.utils.geodatabase import (
    get_bpolys_from_db,
    get_indicator_results_from_db,
)


class BaseIndicator(metaclass=ABCMeta):
    """The base class for all indicators."""

    def __init__(
        self,
        dynamic: bool,
        layers: Dict,
        bpolys: FeatureCollection = None,
        dataset: str = None,
        feature_id: int = None,
    ) -> None:
        """Initialize an indicator"""
        # here we can put the default parameters for indicators
        self.dynamic = dynamic
        self.layers = layers

        if self.dynamic:
            if bpolys is None:
                raise ValueError
            # for dynamic calculation you need to provide geojson geometries
            self.bpolys = bpolys
        else:
            if dataset is None or feature_id is None:
                raise ValueError
            # for static calculation you need to provide the dataset name and
            # optionally an feature_id string, e.g. which geometry ids to use
            self.dataset = dataset
            self.feature_id = feature_id
            self.bpolys = get_bpolys_from_db(self.dataset, self.feature_id)

        self.metadata = IndicatorMetadata(self.name, self.description)

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
        label, value, test, data = self.calculate(preprocessing_results)
        svg = self.create_figure(data)
        print(len(svg))
        logger.info(f"finished run for indicator {self.name}")

        result = IndicatorResult(
            label=TrafficLightQualityLevels.YELLOW.name,
            value=0.5,
            text="a textual description of the results",
            svg="test",
        )

        return result

    def save_to_database(self) -> None:
        """Save the results to the geo database."""
        pass

    def get_from_database(self) -> IndicatorResult:
        """Get pre-processed indicator results from geo database."""
        result = get_indicator_results_from_db(
            dataset=self.dataset, feature_id=self.feature_id, indicator=self.name
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
