import textwrap
from typing import Any, List

import pytest
import rich
from typer.testing import CliRunner, Result

import prefect.cli
from prefect.cli import app


def invoke_and_assert(
    command: List[str],
    expected_output: str = None,
    expected_code: int = 0,
    echo: bool = True,
    user_input=None,
) -> Result:
    """
    Test utility for the Prefect CLI application.
    """
    runner = CliRunner()
    result = runner.invoke(app, command, catch_exceptions=False, input=user_input)

    if echo:
        print(result.stdout)

    if expected_code is not None:
        assert (
            result.exit_code == expected_code
        ), f"Actual exit code: {result.exit_code!r}"

    if expected_output is not None:
        output = result.stdout.strip()
        expected_output = textwrap.dedent(expected_output).strip()

        print("------ expected ------")
        print(expected_output)
        print()

        assert output == expected_output

    return result


@pytest.fixture
def disable_terminal_wrapping(monkeypatch):
    """
    Sometimes, line wrapping makes it hard to make deterministic assertions about the
    output of a CLI command. Wrapping can be disabled by using this fixture.
    """
    monkeypatch.setattr(
        "prefect.cli.base.app.console", rich.console.Console(soft_wrap=True)
    )
