import logging
from typing import Optional

import geojson
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ohsome_quality_analyst import __version__ as oqt_version
from ohsome_quality_analyst import oqt
from ohsome_quality_analyst.geodatabase import client as db_client
from ohsome_quality_analyst.utils.definitions import GEOM_SIZE_LIMIT, configure_logging
from ohsome_quality_analyst.utils.helper import name_to_lower_camel

configure_logging()
logging.info("Logging enabled")
logging.debug("Debugging output enabled")


def empty_api_response() -> dict:
    RESPONSE_TEMPLATE = {
        "attribution": {
            "url": "https://ohsome.org/copyrights",
            "text": "© OpenStreetMap contributors",
        },
        "apiVersion": oqt_version,
    }
    return RESPONSE_TEMPLATE


async def load_bpolys(bpolys: str) -> None:
    """Load and check validity and size of bpolys"""
    # TODO: Return API response with error message
    bpolys = geojson.loads(bpolys)
    if bpolys.is_valid is False:
        raise ValueError("Input geometry is not valid")
    elif await db_client.get_area_of_bpolys(bpolys) > GEOM_SIZE_LIMIT:
        raise ValueError(
            "Input geometry is too big. It should be less than {0}.".format(
                GEOM_SIZE_LIMIT
            )
        )
    else:
        return bpolys


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IndicatorParameters(BaseModel):
    bpolys: Optional[str] = None
    dataset: Optional[str] = None
    featureId: Optional[int] = None
    layerName: Optional[str] = None


class ReportParameters(BaseModel):
    bpolys: Optional[str] = None
    dataset: Optional[str] = None
    featureId: Optional[int] = None


@app.get("/indicator/{name}")
async def get_indicator(
    name: str,
    request: Request,
    layerName: str,
    bpolys: Optional[str] = None,
    dataset: Optional[str] = None,
    featureId: Optional[int] = None,
):
    url = request.url._url
    return await _fetch_indicator(name, layerName, url, bpolys, dataset, featureId)


@app.post("/indicator/{name}")
async def post_indicator(name: str, request: Request, item: IndicatorParameters):
    layer_name = item.dict().get("layerName", None)
    bpolys = item.dict().get("bpolys", None)
    dataset = item.dict().get("dataset", None)
    feature_id = item.dict().get("featureId", None)
    url = request.url._url
    return await _fetch_indicator(name, layer_name, url, bpolys, dataset, feature_id)


async def _fetch_indicator(
    name: str,
    layer_name: str,
    url: str,
    bpolys: Optional[str] = None,
    dataset: Optional[str] = None,
    feature_id: Optional[int] = None,
):
    if bpolys is not None:
        bpolys = await load_bpolys(bpolys)

    indicator = await oqt.create_indicator(
        name, layer_name, bpolys, dataset, feature_id
    )

    response = empty_api_response()
    response["metadata"] = vars(indicator.metadata)
    response["metadata"]["requestUrl"] = url
    response["metadata"].pop("result_description", None)
    response["metadata"].pop("label_description", None)
    response["layer"] = vars(indicator.layer)
    response["result"] = vars(indicator.result)
    return response


@app.get("/report/{name}")
async def get_report(
    name: str,
    request: Request,
    bpolys: Optional[str] = None,
    dataset: Optional[str] = None,
    featureId: Optional[int] = None,
):
    url = request.url._url
    return await _fetch_report(name, url, bpolys, dataset, featureId)


@app.post("/report/{name}")
async def post_report(name: str, request: Request, item: ReportParameters):
    bpolys = item.dict().get("bpolys", None)
    dataset = item.dict().get("dataset", None)
    feature_id = item.dict().get("featureId", None)
    url = request.url._url
    return await _fetch_report(name, url, bpolys, dataset, feature_id)


async def _fetch_report(
    name: str,
    url: str,
    bpolys: Optional[str] = None,
    dataset: Optional[str] = None,
    feature_id: Optional[int] = None,
):
    if bpolys is not None:
        bpolys = await load_bpolys(bpolys)

    report = await oqt.create_report(
        name, bpolys=bpolys, dataset=dataset, feature_id=feature_id
    )

    response = empty_api_response()
    response["metadata"] = vars(report.metadata)
    response["metadata"]["requestUrl"] = url
    response["metadata"].pop("label_description", None)
    response["result"] = vars(report.result)
    response["result"]["label"] = report.result.label
    response["indicators"] = {}
    for indicator in report.indicators:
        metadata = vars(indicator.metadata)
        metadata.pop("result_description", None)
        metadata.pop("label_description", None)
        layer = vars(indicator.layer)
        result = vars(indicator.result)
        indicator_name = name_to_lower_camel(metadata["name"])
        layer_name = name_to_lower_camel(layer["name"])
        response["indicators"][indicator_name + layer_name] = {
            "metadata": metadata,
            "layer": layer,
            "result": result,
        }
    return response


@app.get("/geometries/{dataset}")
async def get_bpolys_from_db(dataset: str, featureId: int):
    bpolys = await db_client.get_bpolys_from_db(dataset=dataset, feature_id=featureId)
    return bpolys


@app.get("/regions")
async def get_available_regions():
    return await db_client.get_available_regions()
