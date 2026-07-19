# Examples

Custom predictors are an advanced feature that is only available via the
Cradle SDK. The scripts in this directory contain examples on how to use the
SDK to achieve certain tasks with custom predictors.

- [engineer](example-engineer.py) A code snippet that starts an "engineer" task
  to optimize a template sequence, using a custom predictor as a filterer (i.e.
  only sequences passing the filter criteria are generated).

  Make sure you have `uv` installed, go through the file and review the lines
  marked with "!!!" and then run the example with `uv run example-engineer.py`.
