<div align="center">
<h1>mkdocs-towncrier</h1>
<h4>An insanely small plugin to add towncrier changelog draft into mkdocs</h4>
<a href="https://pypi.org/project/mkdocs-towncrier"><img height="20" alt="Supported python versions" src="https://img.shields.io/pypi/pyversions/mkdocs-towncrier"></a>
<a href="https://pypi.org/project/mkdocs-towncrier"><img height="20" alt="PyPI version" src="https://img.shields.io/pypi/v/mkdocs-towncrier"></a>
<br>
<a href="https://microsoft.github.io/pyright/"><img height="20" alt="Pyright badge" src="https://microsoft.github.io/pyright/img/pyright_badge.svg"></a>
<a href="https://pypi.org/project/ruff"><img height="20" alt="Ruff badge" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json"></a>
<br>
</div>

## Installation

You can install the package from PyPI using:

```bash
pip install -U mkdocs-towncier
```

and then enabling it in your `mkdocs.yml` file:

```yaml
plugins:
  - towncrier
```

## Usage

Using mkdocs-towncrier is as easy as adding a directive to wherever you want the draft changelog
to be added:

```md
# Changelog

<!--- You can even specify the header value! (defaults to "Unreleased") -->
:: towncrier-draft Unreleased changes

--8<-- "CHANGELOG.md"
```

And that's it! Any draft fragment files will be picked up and automatically added to your pages.

## Acknowledgements

This project is heavily inspired in the wonderful
[sphinx-contrib/sphinxcontrib-towncrier](https://github.com/sphinx-contrib/sphinxcontrib-towncrier)!
