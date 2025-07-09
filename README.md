# Cradle Custom Predictor

This Repository contains templates for creating a Cradle custom predictor.
It provides the following templates:

- [minimal](minimal): This is a minimal custom predictor written in Python.
- [uv](uv): A more elaborate example that uses the `uv` package manager
   and demonstrates additional features.

## Custom predictor contract

In order for Cradle to use a custom predictor, it must adhere to this contract,
which is implemented by all templates in this repository.

A custom predictor is a Docker container which, when run, responds to HTTP
requests asking for predictions to be made for one or more sequences. When importing
the custom predictor into the Cradle platform (in order to make it available to tasks
launched on it), the Docker image must be provided together with metadata describing
certain aspects of it.

### Metadata

A custom predictor must provide metadata at the time the custom predictor is
imported into a Cradle workspace. The metadata consist of the following fields:

- `name`: A machine-readable name of the custom predictor which is used to
  reference this custom predictor from tasks.
- `display_name`: A human-readable name of the custom predictor which is displayed
  in user interfaces such as reports.
- `description`: A description of what the descriptor does
- `inputs`: A list of input parameters, types and default values
- `outputs`: A list of output names that the custom predictor generates for each sequence
   (there must be at least one output)
- `batch_size`: How many sequences the custom predictor can be invoked with at a time
- `cpu_mcores`: How much CPU compute the custom predictor consumes per invocation, in
   millicores
- `main_memory_mib`: How much RAM the custom predictor consumes per invocation, in MiB
- `gpu_memory_mib`: How much GPU memory the custom predictor consumes per invocation, in MiB

These metadata serve three purposes:

- They provide the name and a description of the custom predictor with which
  it appears on the Cradle UI.
- They allow Cradle to validate that data passed into a custom predictor and data
  coming out of a custom predictor conforms to the required types and shapes.
- They provide information about hardware resources that Cradle should provision
  when running the custom predictor.

### Input parameters

The input parameters of the custom predictors are assigned values when launching a task
using the custom predictor and then provided as command line arguments to the custom
predictor in the form `--name=value`. Input parameter values must be of type `bool`,
`int`, `float` or `str`.

### REST interface

A custom predictor is expected to provide a simple REST interface via HTTP on
port 8080. It should expose an endpoint at /predict where it accepts POST request
with a JSON body containing the following fields:

- `sequences`: A list of strings representing the sequences for which to create
   predictions. Strings can contain the 20 standard amino acids and `:` as a separator
   token in case of multimers.
- `random-seed`: An integer that can be used as a random seed.

The response to this request should have HTTP status code 200 and provide one
scalar floating point value per sequence and per predictor output (as defined
in the metadata). The response contains a JSON body with the folowing fields:

- `scores`: An array-of-arrays representing a 2-dimensional array of shape
   `num_sequences × num_outputs`, each scalar being of floating point type.
   `num_outputs` in the inner dimension and `num_sequences` the outer dimension.

In case the request could not be processed, the response should contain a HTTP status
code in the 4xx or 5xx range and a JSON-formatted body according to
[RFC9457](https://www.rfc-editor.org/rfc/rfc9457.html).
