# Minimal example for a Cradle Custom Predictor

This directory contains a minimal custom predictor written in Python.
The predictor counts the number of Alanine amino acids in the input
sequence(s). The logic is contained in `custom_prodictor.py`. Metadata
is supplied in the `metadata.json` file.

## Building

To start building the custom predictor, perform the following steps:

1. Create a fork of this repository

2. Make sure [Docker Engine](https://docs.docker.com/engine/) (Docker CE) or
   [Docker Desktop](https://docs.docker.com/desktop/) are installed.

3. Build the docker image by running `docker build . --platform linux/amd64 -t custom-predictor-template`

   1. If you are running a linux/amd64 system, the image can then be run locally as follows:

      ```sh
      docker run --rm -it -p 8080:8080 custom-predictor-template
      ```

   2. At this point you can use a HTTP client to query the custom predictor, e.g. with `curl`:

      ```sh
      curl -H 'Content-Type: application/json' \
           -d '{"sequences": ["CR", "CRAD", "CRADLE"], "random-seed": 2}' \
           -X POST \
           http://localhost:8080/predict
      ```

4. Create the image tarball with `docker save custom-predictor-template --platform linux/amd64 -o custom-predictor.tar`

5. Upload both the `custom-predictor.tar` and the `metadata.json` file to
   Cradle.
