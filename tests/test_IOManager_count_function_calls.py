import abjad
import platform
import pytest
import sys


@pytest.mark.skipif(
    platform.python_implementation() != "CPython",
    reason="Benchmarking is only for CPython.",
)
def test_IOManager_count_function_calls_01():
    result = abjad.IOManager.count_function_calls(
        "abjad.Note('c4')", global_context=globals()
    )
    assert result < 4000


@pytest.mark.skipif(
    platform.python_implementation() != "CPython",
    reason="Benchmarking is only for CPython.",
)
def test_IOManager_count_function_calls_02():
    result = abjad.IOManager.count_function_calls(
        "abjad.Note(-12, (1, 4))", global_context=globals()
    )
    assert result < 400
