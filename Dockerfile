FROM condaforge/miniforge3:24.7.1-2 AS build
LABEL authors="markjackson"


COPY environment-from-history.yml .
RUN mamba env create -f environment-from-history.yml

# Install conda-pack:
RUN mamba install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n alloy-debugger -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar


# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack

FROM python:3.12.7-slim-bookworm AS runtime

# Copy /venv from the previous stage:
COPY --from=build /venv /venv

RUN mkdir -p /usr/local/app/
COPY src /usr/local/app/src

WORKDIR /usr/local/app

# When image is run, run the code with the environment
# activated:
SHELL ["/bin/bash", "-c"]
ENTRYPOINT source /venv/bin/activate && \
           python -m streamlit run src/app.py