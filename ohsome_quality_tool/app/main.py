import json

from fastapi import FastAPI

from ohsome_quality_tool import oqt
from ohsome_quality_tool.utils import geodatabase

app = FastAPI()


@app.get("/test/{indicator_name}")
async def get_test(indicator_name: str):
    return {"indicator_name": indicator_name}


@app.get("/static_indicator/{indicator_name}")
async def get_static_indicator(indicator_name: str, dataset: str, feature_id: int):
    results = oqt.get_static_indicator(
        indicator_name=indicator_name, dataset=dataset, feature_id=feature_id
    )
    return results


@app.get("/static_report/{report_name}")
async def get_static_report(report_name: str, dataset: str, feature_id: int):
    results = oqt.get_static_report(
        report_name=report_name, dataset=dataset, feature_id=feature_id
    )
    return results


@app.get("/dynamic_report/{report_name}")
async def get_dynamic_report(report_name: str, bpolys: str):
    bpolys = json.loads(bpolys)
    result, indicators, metadata = oqt.get_dynamic_report(
        report_name=report_name, bpolys=bpolys
    )

    print(result, indicators, metadata)

    response = {
        "attribution": {
            "url": "https://ohsome.org/copyrights",
            "text": "© OpenStreetMap contributors",
        },
        "apiVersion": "0.1",
        "metadata": metadata._asdict(),
        "result": result._asdict(),
        "indicators": indicators,
    }

    return response


@app.get("/geometries/{dataset}")
async def get_bpolys_from_db(dataset: str, feature_id: int):
    bpolys = geodatabase.get_bpolys_from_db(dataset=dataset, feature_id=feature_id)
    return bpolys
