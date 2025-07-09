# Cradle Custom Predictor

This directory contains a slightly more advanced custom predictor that uses
the `uv` build system which can be employed to use additional Python packages. It
also demonstrates robust error handling, multiple inputs and outputs of the
predictor and unit tests.

## Getting Started

The example custom predictor has two input parameters and two outputs.

The first input parameter (named "factor") is a floating point parameter which
all outputs are multiplied with. The second input parameter (named "subseq") is an amino
acid sequence which is searched for in the sequences to be predicted.

The first output of the custom predictor, named "alanine_count" is the number of Alanine
amino acids in the provided sequence. The second output, named "subseq_count" is the number of
subsequences as specified by the "subseq" parameter that occur in the provided sequence.
Both outputs are multiplied by the "factor" value before the final output.

To start working with this custom predictor, perform the following steps:

1. Create a fork of this repository

2. Install the [uv](https://docs.astral.sh/uv/getting-started/installation/) tool
   if you don't have it yet.

3. Run `uv sync` to install the correct Python version and dependencies.

4. Run `uv run pre-commit install` to install the pre-commit hooks that
   provide linting and typechecking of the Python code.

5. Run `uv run python -m custom_predictor build <output dir>` to build the
   container image containing the custom predictor and the `metadata.json`
   file. This needs [Docker Engine](https://docs.docker.com/engine/) (Docker CE) or
   [Docker Desktop](https://docs.docker.com/desktop/) to be installed.

   1. The created image will have the same name as the custom predictor, in this
      case "custom-predictor-template". If you are running on a linux/amd64 platform,
      it can then be run locally as follows (with the "subseq" input parameter set to
      the string "E"):

      ```sh
      docker run --rm -it -p 8080:8080 custom-predictor-template:latest --subseq=E
      ```

   2. At this point you can use a HTTP client to query the custom predictor, e.g. with `curl`:

      ```sh
      curl -H 'Content-Type: application/json' \
           -d '{"sequences": ["CR", "CRAD", "CRADLE"], "random-seed": 2}' \
           -X POST \
           http://localhost:8080/predict
      ```

### Modifying the custom predictor

You can modify this template to build your own custom predictor for Cradle,
by following these steps:

1. Edit the custom predictor name and author(s) in the `pyproject.toml` file.

2. Edit other metadata and build the actual logic in the
   `custom_predictor/_processor.py` file. If you need to add additional python
   dependencies, add them to the `pyproject.toml` file and install them
   through `uv sync`.

   1. During development of the custom predictor logic, you can run it
      outside of a docker container with `uv run python -m custom_predictor serve --subseq=E`
      for faster iteration.

3. In `tests/conftest.py`, specify the input parameters to be used for the
   unit test. Make sure running the unit test (with `uv run pytest`) passes.
   The unit tests make sure that the metadata for the custom predictor contains valid
   values and it also invokes it with some example sequences and checks that the
   custom predictor output conforms to the contract specified above.

4. Add additional unit tests for your business logic if desired.

### Importing the custom predictor to Cradle

1. Run `uv run python -m custom_predictor build <output dir>` and upload the generated
   tarball and `metadata.json` file to Cradle.
