# Contributing

## Development setup

With [uv](https://docs.astral.sh/uv/) (recommended):

```bash
uv sync
uv run pre-commit install
```

Without uv:

```bash
pip install -e ".[dev]"
pre-commit install
```

## Tests

Python (pytest + pytest-django):

```bash
uv run pytest
```

Coverage (configured in `pyproject.toml`):

```bash
uv run coverage run -m pytest
uv run coverage report
```

## Lint / format / type-check

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
# or, everything at once:
uv run pre-commit run --all-files
```

## Before opening a PR

- [ ] `uv run pytest`
- [ ] `uv run pre-commit run --all-files`
