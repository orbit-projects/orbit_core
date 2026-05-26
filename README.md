# Orbit Core

Core runtime primitives for the Orbit framework.

Orbit Core provides the foundational building
blocks required to create Orbit applications.

Features:

* Application management
* Route registration
* Dynamic route matching
* Dependency injection
* Middleware registration
* Request dispatch foundations
* Framework contracts

## Installation

```bash
pip install orbit-framework-core
```

## Example

```python
from orbit_core import App

app = App()


@app.get("/")
def home():
    return {
        "message": "Hello Orbit",
    }
```

## Components

### App

Primary application abstraction.

```python
app = App()
```

### RouteRegistry

Stores and manages application routes.

### Container

Provides dependency registration and
resolution functionality.

### RouteDefinition

Structured route metadata representation.

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run coverage:

```bash
pytest --cov=orbit_core
```

## License

MIT License.
