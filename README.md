# Cradle Custom Predictor

This Repository contains a template for creating a Cradle custom predictor
in Python, and tooling to import it into a Cradle workspace.

## Custom predictor contract

In order for Cradle to use a custom predictor, it must adhere to this contract.

### Metadata

A custom predictor must expose the following metadata:

- `name`: The name of the descriptor
- `description`: A description of what the descriptor does
- `inputs`: A list of input parameters, types and default values
- `outputs`: A list of output names that the predictor generates for each sequence
   (there must be at least one output)
- `batch_size`: How many sequences the predictor can be invoked with at a time
- `cpu_mcores`: How much CPU compute the predictor consumes per invocation, in
   millicores
- `main_memory_mib`: How much RAM the predictor consumes per invocation, in MiB
- `gpu_memory_mib`: How much GPU memory the predictor consumes per invocation, in MiB

The metadata are registered with the Cradle platform when importing the predictor
into a Cradle workspace.

### Input parameters

The input parameters of the custom predictors are assigned values when launching a task
using the predictor and then provided as command line arguments to the predictor in the
form `--name=value`. Input parameter values must be of type `bool`, `int`, `float` or
`string`.

### REST interface

A custom predictor is expected to provide a simple REST interface via HTTP on
port 8080. It should expose an endpoint at /predict where it accepts POST request
with a JSON body containing the following fields:

- `sequences`: A list of strings representing the sequences for which to create
   predictions. Strings can contain the 20 standard amino acids and `|` as a separator
   token in case of multimers.
- `random-seed`: An integer that can be used as a random seed.

The response to this request should have HTTP status code 200 and provide one
scalar floating point value per sequence and per predictor output (as defined
in the metadata). The response contains a JSON body with the folowing fields:

- `scores`: A list-of-list representing a 2-dimensional array of shape
   `num_sequences × num_outputs`, each scalar being of floating point type.
   `num_outputs` in the inner dimension and `num_sequences` the outer dimension.

In case the request could not be processed, the response should contain a HTTP status
code in the 4xx or 5xx range and a JSON-formatted body according to
[RFC9457](https://www.rfc-editor.org/rfc/rfc9457.html).

## Getting Started

This repository implements an example custom predictor with two input parameters and two
outputs.

The first input parameter (named "factor") is a floating point parameter which
all outputs are multiplied with. The second input parameter (named "subseq") is an amino
acid sequence which is searched for in the sequences to be predicted.

The first output of the predictor, named "As" is the number of "A" amino acids in the
provided sequence. The second output, named "Subseqs" is the number of
subsequences as specified by the "subseq" parameter that occur in the provided sequence.
Both outputs are multiplied by the "factor" value before the final output.

To start working with this predictor, perform the following steps:

1. Create a fork of this repository

2. Install the [uv](https://docs.astral.sh/uv/getting-started/installation/) tool
   if you don't have it yet.

3. Run `uv sync` to install the correct Python version and dependencies. The
   predictor itself does not use any dependencies other than the Python standard
   libraries, but dependencies can easily be added in the `pyproject.toml`
   configuration file. It does use some dev-dependencies that are only used
   during development (e.g. ruff, pyright, pre-commit, pytest).

4. Run `uv run pre-commit install` to install the pre-commit hooks that
   provide linting and typechecking of the Python code.

5. Run `uv run metadata` to dump the predictor's metadata.

6. Run `uv run custom-predictor --subseq=E` to run the predictor with the "subseq"
   input parameter set to the string "E".

   1. At this point you can use a HTTP client to query the predictor, e.g. with `curl`:

      ```sh
      curl -H 'Content-Type: application/json' \
           -d '{"sequences": ["CR", "CRAD", "CRADLE"], "random-seed": 2}' \
           -X POST \
           http://localhost:8080/predict
      ```

7. Run `uv run pytest` to run unit tests for the predictor. The unit tests
   make sure that the metadata for the predictor contains valid values and
   it also invokes it with some example sequences and checks that the
   predictor output conforms to the contract specified above.

8. Run `uv run build-docker-image` to build a docker image of the predictor. This needs
   [Docker Engine](https://docs.docker.com/engine/) (Docker CE) or
   [Docker Desktop](https://docs.docker.com/desktop/) to be installed.

   1. The created image will have the same name as the predictor, in this
      case "custom-predictor-template". It can then be run as follows:

      ```sh
      docker run --rm -it -p 8080:8080 custom-predictor-template:latest --subseq=E
      ```

### Modifying the predictor

The easiest way to build your own custom predictor for Cradle is by
modifying this template, through the following steps:

1. Edit the predictor name and author(s) in the `pyproject.toml` file.

2. Edit other metadata in the `predictor/metadata.py` file.

3. Build the actual logic in the `predictor/processor.py` file. If you need
   to add additional python dependencies, add them to the `pyproject.toml`
   file and install them through `uv sync`.

4. In `tests/conftest.py`, specify the input parameters to be used for the
   unit test. Make sure running the unit test (with `uv run pytest`) passes.

5. Add additional unit tests for your business logic if desired.

### Importing the custom predictor to Cradle

When the business logic of the predictor is ready, it can be imported into a Cradle
workspace. Make sure that [Docker Engine](https://docs.docker.com/engine/) or
[Docker Desktop](https://docs.docker.com/desktop/) are installed.

To import it, simply run `uv run import-to-cradle --workspace=<workspace-name>`.
If the predictor has been imported previously, a new version of it will be
created.
