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
    tags=False,
    **keywords,
):
    """
    Persists ``argument`` as LilyPond file.

    Returns output path and elapsed formatting time when LilyPond output is written.
    """
    if isinstance(argument, _lilypondfile.LilyPondFile):
        lilypond_file = argument
    elif illustrate_function is not None:
        lilypond_file = illustrate_function(**keywords)
    else:
        lilypond_file = _illustrators.illustrate(argument, **keywords)
    assert ly_file_path is not None, repr(ly_file_path)
    ly_file_path = str(ly_file_path)
    ly_file_path = os.path.expanduser(ly_file_path)
    timer = _contextmanagers.Timer()
    with timer:
        string = lilypond_file._get_lilypond_format()
    if not tags:
        string = _tag.remove_tags(string)
    abjad_formatting_time = timer.elapsed_time
    directory = os.path.dirname(ly_file_path)
    _io._ensure_directory_existence(directory)
    with open(ly_file_path, "w") as file_pointer:
        print(string, file=file_pointer)
    return ly_file_path, abjad_formatting_time


def as_midi(argument, midi_file_path, *, flags: str = "", **keywords):
    """
    Persists ``argument`` as MIDI file.

    Returns 4-tuple of output MIDI path, Abjad formatting time, LilyPond rendering time
    and success boolean.
    """
    if isinstance(argument, _lilypondfile.LilyPondFile) and "score" in argument:
        lilypond_file = argument
    else:
        lilypond_file = _illustrators.illustrate(argument, **keywords)
    assert "score" in lilypond_file, repr(lilypond_file)
    assert midi_file_path is not None, repr(midi_file_path)
    midi_file_path = os.path.expanduser(midi_file_path)
    midi_file_path = pathlib.Path(midi_file_path)
    ly_file_path = midi_file_path.with_suffix(".ly")
    ly_file_path, abjad_formatting_time = as_ly(argument, ly_file_path, **keywords)
    timer = _contextmanagers.Timer()
    with timer:
        success = _io.run_lilypond(ly_file_path, flags=flags)
    lilypond_rendering_time = timer.elapsed_time
    if os.name == "nt":
        extension = "mid"
    else:
        extension = "midi"
    path = os.path.splitext(ly_file_path)[0]
    midi_file_path = f"{path}.{extension}"
    return (
        midi_file_path,
        abjad_formatting_time,
        lilypond_rendering_time,
        success,
    )


def as_pdf(
    argument,
    pdf_file_path,
    *,
    flags: str = "",
    illustrate_function=None,
    tags=False,
    **keywords,
):
    """
    Persists ``argument`` as PDF.

    Returns output path, elapsed formatting time and elapsed rendering time when PDF
    output is written.
    """
    if pdf_file_path is not None:
        pdf_file_path = str(pdf_file_path)
        pdf_file_path = os.path.expanduser(pdf_file_path)
        without_extension = os.path.splitext(pdf_file_path)[0]
        ly_file_path = f"{without_extension}.ly"
    else:
        ly_file_path = None
    result = as_ly(
        argument,
        ly_file_path,
        illustrate_function=illustrate_function,
        tags=tags,
        **keywords,
    )
    ly_file_path, abjad_formatting_time = result
    assert isinstance(ly_file_path, str)
    without_extension = os.path.splitext(ly_file_path)[0]
    pdf_file_path = f"{without_extension}.pdf"
    timer = _contextmanagers.Timer()
    with timer:
        success = _io.run_lilypond(ly_file_path, flags=flags)
    lilypond_rendering_time = timer.elapsed_time
    return (
        pdf_file_path,
        abjad_formatting_time,
        lilypond_rendering_time,
        success,
    )


def as_png(
    argument,
    png_file_path,
    *,
    flags: str = "--png",
    illustrate_function=None,
    preview: bool = False,
    resolution=False,
    tags: bool = False,
    **keywords,
):
    """
    Persists ``argument`` as PNG.

    Autogenerates file path when ``png_file_path`` is none.

    Returns output path(s), elapsed formatting time and elapsed rendering time.
    """
    assert isinstance(flags, str), repr(flags)
    if png_file_path is not None:
        png_file_path = os.path.expanduser(png_file_path)
        without_extension = os.path.splitext(png_file_path)[0]
        ly_file_path = f"{without_extension}.ly"
    else:
        ly_file_path = None
    result = as_ly(
        argument,
        ly_file_path,
        illustrate_function=illustrate_function,
        tags=tags,
        **keywords,
    )
    ly_file_path, abjad_formatting_time = result
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
        flags += " -dpreview"
    if resolution and isinstance(resolution, int):
        flags += f" -dresolution={resolution}"
    timer = _contextmanagers.Timer()
    with timer:
        success = _io.run_lilypond(temporary_ly_file_path, flags=flags)
    lilypond_rendering_time = timer.elapsed_time
    png_file_paths = []
    for file_name in os.listdir(temporary_directory):
        if not file_name.endswith(".png"):
            continue
        source_png_file_path = os.path.join(temporary_directory, file_name)
        target_png_file_path = os.path.join(original_directory, file_name)
        shutil.move(source_png_file_path, target_png_file_path)
        png_file_paths.append(target_png_file_path)
    shutil.rmtree(temporary_directory)
    if 1 < len(png_file_paths):
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
        success,
    )
