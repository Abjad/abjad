import platform

import pytest

import abjad


@pytest.mark.skipif(
    platform.python_implementation() != "CPython",
    reason="Benchmarking is only for CPython.",
)
def test_io_count_function_calls_01():
    result = abjad.io.count_function_calls("abjad.Note('c4')", global_context=globals())
    assert result < 4000


@pytest.mark.skipif(
    platform.python_implementation() != "CPython",
    reason="Benchmarking is only for CPython.",
)
def test_io_count_function_calls_02():
    result = abjad.io.count_function_calls(
        "abjad.Note(-12, (1, 4))", global_context=globals()
    )
    assert result < 400


def test_io_spawn_subprocess_01():
    assert abjad.io.spawn_subprocess('echo "hello world"') == 0
