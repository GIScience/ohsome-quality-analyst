"""
Standalone helper functions.
"""

import datetime
import importlib
import json
import logging
import os
import pathlib
import pkgutil
import re
from typing import Generator, Union

import geojson
from geojson import Feature, FeatureCollection, MultiPolygon, Polygon


def name_to_class(class_type: str, name: str):
    """Convert class name of class type (indicator or report) to the class.

    Assumptions:
    - Class is named in Camel Case (E.g. GhsPopComparison).
    - Path to the module is in Snake Case (E.g. indicators.ghs_pop_comparison.indicator)
    """
    # Alternatives:
    # - Hard code import of classes
    # - Dynamically import all classes in package
    #     - https://julienharbulot.com/python-dynamical-import.html
    class_path = "ohsome_quality_analyst.{0}s.{1}.{2}".format(
        class_type,
        camel_to_snake(name),
        class_type,
    )
    return getattr(importlib.import_module(class_path), name)


def camel_to_snake(camel: str) -> str:
    """Converts Camel Case to Snake Case"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel).lower()


def snake_to_lower_camel(snake: str) -> str:
    """Convertes Snake Case to Lower Camel Case"""
    parts = snake.split("_")
    return parts[0] + "".join(part.title() for part in parts[1:])


def name_to_lower_camel(name: str) -> str:
    """Convert name to Lower Camel Case"""
    name = name.replace(" ", "_")
    name = name.replace("-", "_")
    return snake_to_lower_camel(name)


def get_module_dir(module_name: str) -> str:
    """Get directory of module name."""
    module = pkgutil.get_loader(module_name)
    return os.path.dirname(module.get_filename())


def datetime_to_isostring_timestamp(time: datetime) -> str:
    """
    Checks for datetime objects and converts them to ISO 8601 format.

    Serves as function that gets called for objects that can’t otherwise be
    serialized by the `json` module.
    It should return a JSON encodable version of the object or raise a TypeError.
    https://docs.python.org/3/library/json.html#basic-usage
    """
    try:
        return time.isoformat()
    except AttributeError:
        raise TypeError


def write_geojson(
    outfile: str, geojson_object: Union[Feature, FeatureCollection]
) -> None:
    """Writes a GeoJSON object to disk.

    If path does not exists it will be created.
    """
    outfile = pathlib.Path(outfile)
    outfile.parent.mkdir(parents=True, exist_ok=True)
    with open(outfile, "w") as file:
        geojson.dump(
            geojson_object,
            file,
            default=datetime_to_isostring_timestamp,
            allow_nan=True,
        )
        logging.info("Output file written:\t" + str(outfile))


def loads_geojson(bpolys: str) -> Generator[Feature, None, None]:
    """Load and validate GeoJSON object."""
    bpolys = geojson.loads(bpolys)
    if bpolys.is_valid is False:
        raise ValueError("Input geometry is not valid")
    elif isinstance(bpolys, FeatureCollection):
        for feature in bpolys["features"]:
            yield feature
    elif isinstance(bpolys, Feature):
        yield bpolys
    elif isinstance(bpolys, (Polygon, MultiPolygon)):
        yield Feature(geometry=bpolys)
    else:
        raise ValueError(
            "Input GeoJSON Objects have to be of type Feature, Polygon or MultiPolygon"
        )


def flatten_dict(input_dict: dict, *, separator: str = ".", prefix: str = "") -> dict:
    """Returns the given dict as flattened one-level dict."""
    if isinstance(input_dict, dict):
        output = {}
        if prefix != "":
            prefix += separator
        for key, value in input_dict.items():
            output.update(
                flatten_dict(input_dict[key], separator=separator, prefix=prefix + key)
            )
        return output
    else:
        return {prefix: input_dict}


def check_serializability(input_dict: dict, default_serializer: type = str) -> dict:
    """
    Returns the given json, checks if it's serializable (using dumps), but uses a
    default serializer if the object can not be serialized.
    """
    return json.loads(json.dumps(input_dict, default=default_serializer))
