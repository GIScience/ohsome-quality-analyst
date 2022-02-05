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
import warnings
from typing import Generator, Union

import geojson
import joblib
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
    """Converts Snake Case to Lower Camel Case"""
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

    If path does not exist it will be created.
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


def loads_geojson(bpolys: dict) -> Generator[Feature, None, None]:
    """Load and validate GeoJSON object."""
    bpolys = geojson.loads(json.dumps(bpolys))
    if bpolys.is_valid is False:
        raise ValueError(
            "The provided parameter `bpolys` is not a valid GeoJSON: " + bpolys.errors()
        )
    elif isinstance(bpolys, FeatureCollection):
        for feature in bpolys["features"]:
            yield feature
    elif isinstance(bpolys, Feature):
        yield bpolys
    elif isinstance(bpolys, (Polygon, MultiPolygon)):
        yield Feature(geometry=bpolys)
    else:
        raise ValueError(
            "Input GeoJSON Objects have to be of type "
            + " Feature, FeatureCollection, Polygon or MultiPolygon"
        )


def flatten_dict(input_: dict, *, separator: str = ".", prefix: str = "") -> dict:
    """Return the given dictionary as flattened one-level dict.

    If the given dictionary contains a list it will be flattened as well.
    For each element of the list the index of this element will be part of the key.
    """
    output = {}
    if isinstance(input_, dict):
        if prefix != "":
            prefix += separator
        for key, _ in input_.items():
            output.update(
                flatten_dict(
                    input_[key],
                    separator=separator,
                    prefix=prefix + key,
                ),
            )
        return output
    elif isinstance(input_, list):
        for i, item in enumerate(input_):
            output.update(
                flatten_dict({str(i): item}, separator=separator, prefix=prefix),
            )
        return output
    else:
        return {prefix: input_}


def unflatten_dict(input_dict: dict, *, separator: str = "."):
    """Returns the given one-level dict as unflatten dict."""
    output_dict = {}
    for k, v in input_dict.items():
        keys = k.split(separator)
        temp_dict = {}
        for i, key in enumerate(reversed(keys)):
            if i == 0:
                temp_dict = {key: v}
            else:
                temp_dict = {key: temp_dict}
        output_dict = merge_dicts(output_dict, temp_dict)
    return output_dict


def merge_dicts(dict1, dict2):
    """Merges two nested dictionaries."""
    for key in dict2:
        if key in dict1:
            merge_dicts(dict1[key], dict2[key])
        else:
            dict1[key] = dict2[key]
    return dict1


def flatten_sequence(input_seq: Union[dict, list, tuple, set]) -> list:
    """Returns the given input sequence as a list.

    If the input is a dict, it returns all values.
    """
    output = []
    if isinstance(input_seq, dict):
        input_seq = input_seq.values()
    for val in input_seq:
        if isinstance(val, (dict, list, tuple, set)):
            output += flatten_sequence(val)
        else:
            output.append(val)
    return output


def load_sklearn_model(path: str):
    """Load sklearn model from disk

    Raise an error if a `UserWarning` is thrown during loading of a model from disk.
    The `UserWarning` is most likely due to use of different versions of `scikit-learn`
    for dumping and for loading the model with `joblib`.
    https://scikit-learn.org/stable/modules/model_persistence.html#security-maintainability-limitations
    """
    warnings.simplefilter("error", UserWarning)  # Raise exception if warning occurs
    model = joblib.load(path)
    warnings.resetwarnings()
    return model
