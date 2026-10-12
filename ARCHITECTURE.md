# Architecture

Feedlane is a batch job, not a web service. `python -m feedlane` parses arguments and calls `runner.run`.

The runner reads every JSON object, asks `transform.normalize` for a clean product or a rejection, then drops duplicate SKUs. Nothing is written until the whole file has been classified, so a crash mid-run does not leave a half-updated catalog from this process. The three output files are replaced together at the end.

The Docker image copies the package and sets `PYTHONPATH=/app/src`. Compose mounts the input read-only and the output directory from the host, so the result stays after the container exits.
