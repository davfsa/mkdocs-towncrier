# Copyright (c) 2024-present davfsa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Nox pipelines."""

from __future__ import annotations

import nox

nox.options.default_venv_backend = "uv|virtualenv"


@nox.session(reuse_venv=True, default=True)
def format_code(session: nox.Session) -> None:
    """Reformat code with ruff."""
    session.install("ruff")

    session.run("ruff", "format")
    session.run("ruff", "check", "--fix")


@nox.session(reuse_venv=True, default=False)
def check_code(session: nox.Session) -> None:
    """Check code for abnormalities with ruff."""
    session.install("ruff")

    session.run("ruff", "format", "--check")
    session.run("ruff", "check", "--output-format", "github")


@nox.session(reuse_venv=True, default=True)
def typecheck(session: nox.Session) -> None:
    """Typecheck code with pyright."""
    session.install("pyright", "-e", ".")

    session.run("pyright", "src")
