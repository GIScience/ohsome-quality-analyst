import asyncio
import os
from datetime import datetime

import pytest

from ohsome_quality_analyst.indicators.ghs_pop_comparison_buildings.indicator import (
    GhsPopComparisonBuildings,
)

from .utils import get_fixture_dir, get_geojson_fixture, get_layer_fixture, oqt_vcr


@pytest.fixture
def mock_env_oqt_data_dir(monkeypatch):
    directory = os.path.join(get_fixture_dir(), "rasters")
    monkeypatch.setenv("OQT_DATA_DIR", directory)


@oqt_vcr.use_cassette()
def test(mock_env_oqt_data_dir):
    feature = get_geojson_fixture("algeria-touggourt-feature.geojson")
    layer = get_layer_fixture("building_count")
    indicator = GhsPopComparisonBuildings(feature=feature, layer=layer)

    asyncio.run(indicator.preprocess())
    for attribute in (
        indicator.pop_count,
        indicator.area,
        indicator.feature_count,
        indicator.feature_count_per_sqkm,
        indicator.pop_count_per_sqkm,
        indicator.attribution(),
    ):
        assert attribute is not None
    assert isinstance(indicator.result.timestamp_osm, datetime)
    assert isinstance(indicator.result.timestamp_oqt, datetime)

    indicator.calculate()
    for attribute in (
        indicator.result.label,
        indicator.result.value,
        indicator.result.description,
    ):
        assert attribute is not None

    indicator.create_figure()
    assert indicator.result.svg is not None
