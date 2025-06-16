# Cradle Custom Predictor

This Repository contains a template for creating a Cradle custom predictor
and tooling to import it into a Cradle workspace.

## REST interface

TODO(armin): document the REST interface here

## Getting Started

TODO(armin): populate

- Install uv
- `uv sync`
- `uv run pre-commit install`
- Install docker
- Edit name, description, authors in pyproject.toml
- Edit other metadata in metadata.py
- Build the actual logic in XXX.py
- Docker build

## Metadata

The `metadata.py` file should describe the metadata for the predictor. It is
used by the unit test that makes sure the predictor's output value matches
the expectation and by the import tool that imports it into a Cradle workspace.

## Unit test

Run `uv run pytest` to run the unit test. It calls the custom predictor with
some example sequences and checks that its output conforms to the interface
as defined above.

## Import tool

Run `uv run tools/import.py` to import stuff the predictor into a workspace.
Arguments are:

- `--workspace_name=`: Provides the name of the workspace to import it into.

If the predictor has been imported previously, then a new version will be
imported.
