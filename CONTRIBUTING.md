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

## Compatibility matrix (tox)

`uv run pytest` above only runs against whatever Django version `uv.lock`
resolved (the newest one satisfying `dependencies`). To check the full
supported range — every Django series in `classifiers`, against the
oldest and newest Python it supports (within this package's own
`requires-python` floor) — run the tox matrix instead:

```bash
uv run tox run-parallel   # every env, in parallel
uv run tox -e py312-dj60  # a single env, e.g. to debug one failure
```

`tox.ini` lists the exact envs. Each one gets its own ephemeral venv (via
[tox-uv](https://github.com/tox-dev/tox-uv), using uv's own Python
builds — `uv python install <version>` once for any you don't have yet)
with only `pytest`/`pytest-django`/`pytest-cov` and that env's pinned
Django, not the full `dev` group. This only tests boundaries (oldest +
newest Python per Django series), not every valid combination — that
catches most real breakage while staying fast. `requires-python` says
`>=3.7`, but uv's managed Python builds start at 3.8, so 3.7 itself isn't
covered here — everything 3.8 and up is. Runs in CI as a separate
`compat-matrix.yml` workflow, alongside the regular `pytest.yml`.

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
