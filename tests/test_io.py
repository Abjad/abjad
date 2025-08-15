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
    pitch = abjad.NamedPitch(-12)
    duration = abjad.Duration(1, 4)
    result = abjad.io.count_function_calls(
        "abjad.Note.from_pitch_and_duration(pitch, duration)",
        global_context=globals(),
        local_context=locals(),
    )
    assert result < 400


def test_io_spawn_subprocess_01():
    assert abjad.io.spawn_subprocess('echo "hello world"') == 0
