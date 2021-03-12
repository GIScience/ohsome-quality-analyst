"""Run uvicorn with custom options to start API server for development purposes"""

import click
import uvicorn

from ohsome_quality_analyst.utils.definitions import load_logging_config


@click.command()
@click.option("--host", default="127.0.0.1", type=str)
@click.option("--port", default=8080, type=int)
def run(host: str, port: int):
    uvicorn.run(
        "ohsome_quality_analyst.api:app",
        host=host,
        port=port,
        reload=True,
        reload_dirs=["."],
        log_config=load_logging_config(),
    )


if __name__ == "__main__":
    run()