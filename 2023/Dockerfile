FROM 690616407375.dkr.ecr.us-east-1.amazonaws.com/py-marvel/devcontainers/images/python:latest AS builder

# Allow poetry install access to our internal packages.
COPY ./.devcontainer/pypi-token.txt /tmp/pypi-token.txt
RUN poetry config http-basic.hudl aws $(cat /tmp/pypi-token.txt)

# Install dependencies first to reuse the layer when nothing here changes.
WORKDIR /app
ARG DEV="--only main"
COPY poetry.* pyproject.toml ./
RUN poetry install ${DEV} && rm -rf ~/.cache

# Install the project on top of the dependencies.
COPY . .
RUN poetry install ${DEV} && rm -rf ~/.cache

# Package the final venv into a prod image.
FROM python:3.9.16-bullseye AS prod

# Inject a commit ID for debugging support and logging.
ARG LOG_VAR_COMMIT
ENV LOG_VAR_COMMIT ${LOG_VAR_COMMIT}

# Copy the application and virtualenv into the production image.
COPY --from=builder /app /app
RUN python3 -m venv /app/.venv
ENV PATH=/app/.venv/bin:$PATH

# Configure the production image defaults.
WORKDIR /app
ENTRYPOINT ["/app/.venv/bin/python", "main.py"]
CMD [ "--", "--help" ]
