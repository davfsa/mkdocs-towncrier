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
"""A small Mkdocs plugin to add towncrier fragments to your documentation."""

from __future__ import annotations

import functools
import logging
import re
import subprocess
import textwrap

import mkdocs
import mkdocs.config.config_options as c
import mkdocs.config.defaults
import mkdocs.exceptions
import mkdocs.plugins
import mkdocs.structure.files
import mkdocs.structure.pages

__all__ = ("TowncrierPlugin",)


LOGGER = logging.getLogger("mkdocs.plugin.towncrier")


@functools.cache
def _generate_changelog_draft(version_string: str) -> str:
    command = ["towncrier", "build", "--draft", "--version", version_string]
    response = subprocess.run(command, capture_output=True, text=True, check=False)  # noqa: S603

    if response.returncode != 0:
        stdout = response.stdout or "[None]"
        stderr = response.stderr or "[None]"

        msg = (
            f"Command `{" ".join(command)}` exited unexpectedly\n"
            f"Return code: {response.returncode}\n"
            f"stdout:\n{textwrap.indent(stdout, " " * 4)}\n"
            f"stderr:\n{textwrap.indent(stderr, " " * 4)}\n"
        )
        raise mkdocs.exceptions.BuildError(msg)

    return response.stdout


class TowncrierPluginConfig(mkdocs.config.Config):
    hide_if_empty = c.Type(bool, default=True)


class TowncrierPlugin(mkdocs.plugins.BasePlugin[TowncrierPluginConfig]):
    """Towncrier plugin."""

    directive_regex = re.compile(r"^:: towncrier-draft ?(?P<header>.+?)? *$", flags=re.MULTILINE)

    def on_page_markdown(
        self,
        markdown: str,
        /,
        *,
        page: mkdocs.structure.pages.Page,  # noqa: ARG002 - Unused argument
        config: mkdocs.config.defaults.MkDocsConfig,  # noqa: ARG002 - Unused argument
        files: mkdocs.structure.files.Files,  # noqa: ARG002 - Unused argument
    ) -> str | None:
        """See https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown for more info."""
        while directive_match := self.directive_regex.search(markdown):
            version_name = directive_match.group(1) or "Unreleased"
            draft = _generate_changelog_draft(version_name)

            if self.config.hide_if_empty and "No significant changes" in draft:
                # Just replace the directive
                draft = ""

            # Replace the directive with the draft changelog
            match_beginning, match_end = directive_match.span(0)
            markdown = markdown[:match_beginning] + draft + markdown[match_end:]

        return markdown
