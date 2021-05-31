import asyncio
import logging
import pathlib

import click
import geojson
import yaml

from ohsome_quality_analyst import oqt
from ohsome_quality_analyst.cli_opts import (
    dataset_name_opt,
    feature_id_opt,
    force_opt,
    indicator_name_opt,
    infile_opt,
    layer_name_opt,
    outfile_opt,
    report_name_opt,
)
from ohsome_quality_analyst.geodatabase import client as db_client
from ohsome_quality_analyst.utils.definitions import (
    DATASETS,
    configure_logging,
    load_layer_definitions,
    load_metadata,
)


def add_opts(options):
    """Adds options to cli."""

    def _add_opts(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_opts


@click.group()
@click.version_option()
@click.option("--quiet", "-q", is_flag=True, help="Disable logging.")
def cli(quiet: bool):
    if not quiet:
        configure_logging()
        logging.info("Logging enabled")


@cli.command("list-indicators")
def list_indicators():
    """List available indicators and their metadata."""
    metadata = load_metadata("indicators")
    metadata = yaml.dump(metadata, default_style="|")
    click.echo(metadata)


@cli.command("list-reports")
def list_reports():
    """List available reports and their metadata."""
    metadata = load_metadata("reports")
    metadata = yaml.dump(metadata, default_style="|")
    click.echo(metadata)


@cli.command("list-layers")
def list_layers():
    """List available layers and how they are definied (ohsome API parameters)."""
    layers = load_layer_definitions()
    layers = yaml.dump(layers, default_style="|")
    click.echo(layers)


@cli.command("list-datasets")
def list_datasets():
    """List available datasets."""
    click.echo(DATASETS.keys())


@cli.command("list-regions")
def get_available_regions():
    """List available regions."""
    regions = asyncio.run(db_client.get_available_regions())
    click.echo(regions)


@cli.command("create-indicator")
@add_opts(indicator_name_opt)
@add_opts(layer_name_opt)
@add_opts(infile_opt)
@add_opts(outfile_opt)
@add_opts(dataset_name_opt)
@add_opts(feature_id_opt)
@add_opts(force_opt)
def create_indicator(
    indicator_name: str,
    infile: str,
    outfile: str,
    layer_name: str,
    feature_id: int,
    dataset_name: str,
    force: bool,
):
    """Create an Indicator and print results to stdout."""
    # TODO: replace this with a function that loads the file AND
    #    checks the validity of the geometries, e.g. enforce polygons etc.
    if force:
        click.echo(
            "The argument 'force' will update the indicator result in the database."
        )
        click.confirm("Do you want to continue?", abort=True)
    if infile is not None:
        infile = pathlib.Path(infile)
        with open(infile, "r") as file:
            feature_collection = geojson.load(file)
        if feature_collection.is_valid is False:
            raise ValueError("Input geometry is not valid")
        for feature in feature_collection.features:
            sub_collection = geojson.FeatureCollection([feature])
            indicator = asyncio.run(
                oqt.create_indicator(
                    indicator_name,
                    layer_name,
                    bpolys=sub_collection,
                    feature_id=feature_id,
                    dataset=dataset_name,
                    force=force,
                )
            )
            if indicator.data is not None:
                feature["properties"].update(vars(indicator.data))
            feature["properties"].update(vars(indicator.metadata))
            feature["properties"].update(vars(indicator.result))
        if outfile is None:
            outfile = infile.stem + "_" + indicator_name + infile.suffix
        else:
            outfile = pathlib.Path(outfile)
            outfile.parent.mkdir(parents=True, exist_ok=True)
        with open(outfile, "w") as f:
            geojson.dump(feature_collection, f)
    else:
        bpolys = None
        indicator = asyncio.run(
            oqt.create_indicator(
                indicator_name,
                layer_name,
                bpolys=bpolys,
                feature_id=feature_id,
                dataset=dataset_name,
                force=force,
            )
        )
        # TODO: Save as GeoJSON instead of printing to Stdout
        click.echo(indicator.metadata)
        click.echo(indicator.result)


@cli.command("create-report")
@add_opts(report_name_opt)
@add_opts(infile_opt)
@add_opts(outfile_opt)
@add_opts(dataset_name_opt)
@add_opts(feature_id_opt)
@add_opts(force_opt)
def create_report(
    report_name: str,
    infile: str,
    outfile: str,
    dataset_name: str,
    feature_id: int,
    force: bool,
):
    """Create a Report and print results to stdout."""
    if infile is not None:
        infile = pathlib.Path(infile)
        with open(infile, "r") as file:
            feature_collection = geojson.load(file)
        if feature_collection.is_valid is False:
            raise ValueError("Input geometry is not valid")
        for feature in feature_collection.features:
            sub_collection = geojson.FeatureCollection([feature])
            report = asyncio.run(
                oqt.create_report(
                    report_name,
                    bpolys=sub_collection,
                    dataset=dataset_name,
                    feature_id=feature_id,
                    force=force,
                )
            )
            feature["properties"].update(vars(report.metadata))
            feature["properties"].update(vars(report.result))
        if outfile is None:
            outfile = infile.stem + "_" + report_name + infile.suffix
        else:
            outfile = pathlib.Path(outfile)
            outfile.parent.mkdir(parents=True, exist_ok=True)
        with open(outfile, "w") as f:
            geojson.dump(feature_collection, f)
    else:
        bpolys = None
        report = asyncio.run(
            oqt.create_report(
                report_name,
                bpolys=bpolys,
                dataset=dataset_name,
                feature_id=feature_id,
                force=force,
            )
        )
        # TODO: Save as GeoJSON instead of printing to Stdout
        click.echo(report.metadata)
        click.echo(report.result)


@cli.command("create-all-indicators")
@add_opts(force_opt)
def create_all_indicators(force: bool):
    """Create all indicators for OQT regions."""
    click.echo(
        "This command will calculate all indicators for OQT regions "
        + "and may take a while to complete."
    )
    if force:
        click.echo(
            "The argument 'force' will update the indicator results in the database."
        )
    click.confirm("Do you want to continue?", abort=True)
    asyncio.run(oqt.create_all_indicators(force=force))


if __name__ == "__main__":
    cli()
