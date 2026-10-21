"""
Functions to persist LilyPond files to disk.
"""

import os
import pathlib
import re
import shutil
import tempfile

from . import contextmanagers as _contextmanagers
from . import illustrators as _illustrators
from . import io as _io
from . import lilypondfile as _lilypondfile
from . import tag as _tag


def as_ly(
    argument,
    ly_file_path,
    *,
    illustrate_function=None,
    keep_tags=False,
    **illustrate_keywords,
):
    """
    Persists ``argument`` as LilyPond file.

    Returns Abjad formatting time in seconds.
    """
    if isinstance(argument, _lilypondfile.LilyPondFile):
        lilypond_file = argument
    elif illustrate_function is not None:
        lilypond_file = illustrate_function(**illustrate_keywords)
    else:
        lilypond_file = _illustrators.illustrate(argument, **illustrate_keywords)
    assert ly_file_path is not None, repr(ly_file_path)
    ly_file_path = str(ly_file_path)
    ly_file_path = os.path.expanduser(ly_file_path)
    timer = _contextmanagers.Timer()
    with timer:
        string = lilypond_file._get_lilypond_format()
    if not keep_tags:
        string = _tag.remove_tags(string)
    abjad_formatting_time = timer.elapsed_time()
    directory = os.path.dirname(ly_file_path)
    _io._ensure_directory_existence(directory)
    with open(ly_file_path, "w") as file_pointer:
        print(string, file=file_pointer)
    return abjad_formatting_time


def as_midi(
    argument,
    midi_file_path,
    *,
    lilypond_flags: str = "",
    **illustrate_keywords,
):
    """
    Persists ``argument`` as MIDI file.

    Returns a 3-tuple of Abjad formatting time, LilyPond rendering time and exit code.
    """
    if isinstance(argument, _lilypondfile.LilyPondFile) and "score" in argument:
        lilypond_file = argument
    else:
        lilypond_file = _illustrators.illustrate(argument, **illustrate_keywords)
    assert "score" in lilypond_file, repr(lilypond_file)
    assert midi_file_path is not None, repr(midi_file_path)
    midi_file_path = os.path.expanduser(midi_file_path)
    midi_file_path = pathlib.Path(midi_file_path)
    ly_file_path = str(midi_file_path.with_suffix(".ly"))
    abjad_formatting_time = as_ly(argument, ly_file_path, **illustrate_keywords)
    timer = _contextmanagers.Timer()
    with timer:
        exit_code = _io.run_lilypond(ly_file_path, flags=lilypond_flags)
    lilypond_rendering_time = timer.elapsed_time()
    return abjad_formatting_time, lilypond_rendering_time, exit_code


def as_pdf(
    argument,
    pdf_file_path,
    *,
    lilypond_flags: str = "",
    illustrate_function=None,
    keep_tags=False,
    **illustrate_keywords,
):
    """
    Persists ``argument`` as PDF.

    Returns a 3-tuple of Abjad formatting time, LilyPond rendering time and exit code.
    """
    if pdf_file_path is None:
        raise ValueError("pdf_file_path must have a '.pdf' extension.")
    pdf_file_path = os.path.expanduser(str(pdf_file_path))
    if pathlib.Path(pdf_file_path).suffix != ".pdf":
        raise ValueError(
            f"pdf_file_path must have a '.pdf' extension: {pdf_file_path!r}"
        )
    ly_file_path = str(pathlib.Path(pdf_file_path).with_suffix(".ly"))
    abjad_formatting_time = as_ly(
        argument,
        ly_file_path,
        illustrate_function=illustrate_function,
        keep_tags=keep_tags,
        **illustrate_keywords,
    )
    timer = _contextmanagers.Timer()
    with timer:
        exit_code = _io.run_lilypond(ly_file_path, flags=lilypond_flags)
    lilypond_rendering_time = timer.elapsed_time()
    return abjad_formatting_time, lilypond_rendering_time, exit_code


def as_png(
    argument,
    png_file_path,
    *,
    lilypond_flags: str = "--png",
    illustrate_function=None,
    preview: bool = False,
    resolution=False,
    keep_tags: bool = False,
    **illustrate_keywords,
):
    """
    Persists ``argument`` as PNG.

    Autogenerates file path when ``png_file_path`` is none.

    Returns output path(s), elapsed formatting time and elapsed rendering time.
    """
    assert isinstance(lilypond_flags, str), repr(lilypond_flags)
    if png_file_path is not None:
        png_file_path = os.path.expanduser(png_file_path)
        without_extension = os.path.splitext(png_file_path)[0]
        ly_file_path = f"{without_extension}.ly"
    else:
        ly_file_path = None
    abjad_formatting_time = as_ly(
        argument,
        ly_file_path,
        illustrate_function=illustrate_function,
        keep_tags=keep_tags,
        **illustrate_keywords,
    )
    assert isinstance(ly_file_path, str)
    original_directory = os.path.split(ly_file_path)[0]
    original_ly_file_path = ly_file_path
    temporary_directory = tempfile.mkdtemp()
    assert isinstance(temporary_directory, str)
    temporary_ly_file_path = os.path.join(
        temporary_directory, os.path.split(ly_file_path)[1]
    )
    shutil.copy(original_ly_file_path, temporary_ly_file_path)
    if preview:
        lilypond_flags += " -dpreview"
    if resolution and isinstance(resolution, int):
        lilypond_flags += f" -dresolution={resolution}"
    timer = _contextmanagers.Timer()
    with timer:
        exit_code = _io.run_lilypond(temporary_ly_file_path, flags=lilypond_flags)
    lilypond_rendering_time = timer.elapsed_time()
    png_file_paths = []
    for file_name in os.listdir(temporary_directory):
        if not file_name.endswith(".png"):
            continue
        source_png_file_path = os.path.join(temporary_directory, file_name)
        target_png_file_path = os.path.join(original_directory, file_name)
        shutil.move(source_png_file_path, target_png_file_path)
        png_file_paths.append(target_png_file_path)
    shutil.rmtree(temporary_directory)
    if 1 < len(png_file_paths) and preview is False:
        _png_page_pattern = re.compile(r".+page(\d+)\.png")

        def _key(path):
            match = _png_page_pattern.match(path)
            assert match is not None
            group = match.groups()[0]
            return group

        png_file_paths.sort(key=_key)
    return (
        tuple(png_file_paths),
        abjad_formatting_time,
        lilypond_rendering_time,
        exit_code,
    )
