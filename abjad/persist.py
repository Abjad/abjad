import os
import pathlib
import re
import shutil
import tempfile
import typing

from . import contextmanagers as _contextmanagers
from . import format as _format
from . import illustrators as _illustrators
from . import io as _io
from . import lilypondfile as _lilypondfile
from . import tag as _tag


def as_ly(
    argument,
    ly_file_path: str | pathlib.Path,
    *,
    illustrate_function: typing.Callable | None = None,
    keep_site_comments: bool = False,
    keep_tags: bool = False,
    **illustrate_keywords,
) -> float:
    """
    Persists ``argument`` as LilyPond file.

    Changes ``argument`` to Abjad LilyPond file object:

      * Leaves ``argument`` unchanged if ``argument`` already is a LilyPond file;
      * Otherwise, tries ``illustrate_function(argument, **illustrate_keywords)``;
      * Otherwise, tries ``abjad.illustrate(argument, **illustrate_keywords)``

    Gets Abjad format string of LilyPond file object.

    Calls ``abjad.tag.remove_tages()`` on format string when ``keep_tags`` is false.

    Calls ``abjad.format.remove_site_comments()`` on format when string when
    ``keep_site_comments`` is false.

    Writes format string to disk at ``ly_file_path``.

    ``ly_file_path`` should initialize a ``pathlib.Path`` object.

    ``ly_file_path`` should carry ``.ly`` suffix.

    ``ly_file_path`` parent directory should already exist.

    Returns Abjad format time in seconds.
    """
    ly_file_path = pathlib.Path(ly_file_path)
    assert ly_file_path.suffix == ".ly", repr(ly_file_path)
    assert ly_file_path.parent.is_dir(), repr(ly_file_path)
    if illustrate_function is not None:
        assert callable(illustrate_function), repr(illustrate_function)
    assert isinstance(keep_site_comments, bool), repr(keep_site_comments)
    assert isinstance(keep_tags, bool), repr(keep_tags)
    if "tags" in illustrate_keywords:
        raise Exception("change tags=False to keep_tags=False")
    if isinstance(argument, _lilypondfile.LilyPondFile):
        assert illustrate_function is None, repr(illustrate_function)
        assert illustrate_keywords == {}, repr(illustrate_keywords)
        lilypond_file = argument
    elif illustrate_function is not None:
        lilypond_file = illustrate_function(**illustrate_keywords)
    else:
        lilypond_file = _illustrators.illustrate(argument, **illustrate_keywords)
    with _contextmanagers.Timer() as timer:
        string = lilypond_file._get_lilypond_format()
    if keep_site_comments is False:
        _format.remove_site_comments(string)
    if keep_tags is False:
        string = _tag.remove_tags(string)
    abjad_format_time = timer.elapsed_time
    assert isinstance(abjad_format_time, float), repr(abjad_format_time)
    with open(ly_file_path, "w") as file_pointer:
        print(string, file=file_pointer)
    return abjad_format_time


def as_midi(
    argument,
    midi_file_path: str | pathlib.Path,
    *,
    illustrate_function: typing.Callable | None = None,
    keep_site_comments: bool = False,
    keep_tags: bool = False,
    lilypond_flags: str = "",
    **illustrate_keywords,
) -> tuple[float, float, int]:
    """
    Persists ``argument`` as MIDI file.

    Writes ``midi_file_path`` to disk.

    Writes corresponding ``.ly`` file in parent directory of ``midi_file_path``.

    ``midi_file_path`` should initialize a ``pathlib.Path`` object.

    ``midi_file_path`` should carry ``.mid`` (Windows NT) or ``.midi`` (all others)
    suffix.

    Passes ``illustrate_function`` to ``abjad.persist.as_ly()``

    Passes ``keep_tags`` to ``abjad.persist.as_ly()``.

    Passes ``lilypond_flags`` to ``abjad.io.run_lilypond()``.

    Passes ``**illustrate_keywords`` to ``abjad.persist.as_ly()``.

    Returns triple:

      * Abjad format time in seconds (from ``abjad.persist.as_ly()``)
      * LilyPond render time in seconds (from ``abjad.io.run_lilypond()``)
      * exit code (from ``abjad.io.run_lilypond()``)

    """
    if isinstance(argument, _lilypondfile.LilyPondFile) and "score" in argument:
        lilypond_file = argument
    else:
        lilypond_file = _illustrators.illustrate(argument, **illustrate_keywords)
    assert "score" in lilypond_file, repr(lilypond_file)
    midi_file_path = pathlib.Path(midi_file_path)
    if os.name == "nt":
        assert midi_file_path.suffix == ".mid", repr(midi_file_path)
    else:
        assert midi_file_path.suffix == ".midi", repr(midi_file_path)
    assert midi_file_path.parent.is_dir(), repr(midi_file_path)
    assert isinstance(lilypond_flags, str), repr(lilypond_flags)
    if illustrate_function is not None:
        assert callable(illustrate_function), repr(illustrate_function)
    assert isinstance(keep_site_comments, bool), repr(keep_site_comments)
    assert isinstance(keep_tags, bool), repr(keep_tags)
    if "tags" in illustrate_keywords:
        raise Exception("change tags=False to keep_tags=False")
    ly_file_path = midi_file_path.with_suffix(".ly")
    abjad_format_time = as_ly(
        argument,
        ly_file_path,
        illustrate_function=illustrate_function,
        keep_site_comments=keep_site_comments,
        keep_tags=keep_tags,
        **illustrate_keywords,
    )
    with _contextmanagers.Timer() as timer:
        exit_code = _io.run_lilypond(ly_file_path, flags=lilypond_flags)
    lilypond_render_time = timer.elapsed_time
    assert isinstance(lilypond_render_time, float), repr(lilypond_render_time)
    return (
        abjad_format_time,
        lilypond_render_time,
        exit_code,
    )


def as_pdf(
    argument,
    pdf_file_path: str | pathlib.Path,
    *,
    illustrate_function: typing.Callable | None = None,
    keep_site_comments: bool = False,
    keep_tags: bool = False,
    lilypond_flags: str = "",
    **illustrate_keywords,
) -> tuple[float, float, int]:
    """
    Persists ``argument`` as PDF.

    Writes ``pdf_file_path`` to disk.

    Writes corresponding ``.ly`` file in parent directory of ``pdf_file_path``.

    ``pdf_file_path`` should initialize a ``pathlib.Path`` object.

    ``pdf_file_path`` should carry ``.pdf`` suffix.

    Passes ``lilypond_flags`` to ``abjad.io.run_lilypond()``.

    Passes ``illustrate_function`` to ``abjad.persist.as_ly()``

    Passes ``keep_tags`` to ``abjad.persist.as_ly()``.

    Passes ``**illustrate_keywords`` to ``abjad.persist.as_ly()``.

    Returns triple:

      * Abjad format time in seconds (from ``abjad.persist.as_ly()``)
      * LilyPond render time in seconds (from ``abjad.io.run_lilypond()``)
      * exit code (from ``abjad.io.run_lilypond()``)

    """
    pdf_file_path = pathlib.Path(pdf_file_path)
    # TODO: remove .pdf constraint
    # assert pdf_file_path.suffix == ".pdf", repr(pdf_file_path)
    assert pdf_file_path.parent.is_dir(), repr(pdf_file_path)
    if illustrate_function is not None:
        assert callable(illustrate_function), repr(illustrate_function)
    assert isinstance(keep_site_comments, bool), repr(keep_site_comments)
    assert isinstance(keep_tags, bool), repr(keep_tags)
    assert isinstance(lilypond_flags, str), repr(lilypond_flags)
    if "tags" in illustrate_keywords:
        raise Exception("change tags=False to keep_tags=False")
    ly_file_path = pdf_file_path.with_suffix(".ly")
    abjad_format_time = as_ly(
        argument,
        ly_file_path,
        illustrate_function=illustrate_function,
        keep_site_comments=keep_site_comments,
        keep_tags=keep_tags,
        **illustrate_keywords,
    )
    with _contextmanagers.Timer() as timer:
        exit_code = _io.run_lilypond(ly_file_path, flags=lilypond_flags)
    lilypond_render_time = timer.elapsed_time
    assert isinstance(lilypond_render_time, float), repr(lilypond_render_time)
    return (
        abjad_format_time,
        lilypond_render_time,
        exit_code,
    )


def as_png(
    argument,
    png_file_path: str | pathlib.Path,
    *,
    illustrate_function: typing.Callable | None = None,
    keep_site_comments: bool = False,
    keep_tags: bool = False,
    lilypond_flags: str = "--png",
    preview: bool = False,
    resolution: int | None = None,
    **illustrate_keywords,
):
    """
    Persists ``argument`` as PNG.

    Writes ``png_file_path`` to disk when ``argument`` generates only one
    page of notation.

    Writes multiple files to disk when ``argument`` generates more than one
    page of notation:

      * ``/path/to/file-page1.png``
      * ``/path/to/file-page2.png``
      * ``/path/to/file-page3.png``
      * etc

    Writes one ``.ly`` file in parent directory ``png_file_path``.

    ``png_file_path`` should initialize a ``pathlib.Path`` object.

    ``png_file_path`` should carry ``.png`` suffix.

    Passes ``lilypond_flags`` to ``abjad.io.run_lilypond()``.

    Passes ``illustrate_function`` to ``abjad.persist.as_ly()``

    Passes ``keep_tags`` to ``abjad.persist.as_ly()``.

    Adds ``-preview`` to ``lilypond_flags`` when ``preview`` is true.

    Adds ``-dresolution=resolution`` to ``lilypond_flags`` when resolution is an
    integer.

    Passes ``**illustrate_keywords`` to ``abjad.persist.as_ly()``.

    Returns 4-tuple:

      * tuple of output PNG file path(s)
      * Abjad format time in seconds (from ``abjad.persist.as_ly()``)
      * LilyPond render time in seconds (from ``abjad.io.run_lilypond()``)
      * exit code (from ``abjad.io.run_lilypond()``)

    """
    png_file_path = pathlib.Path(png_file_path)
    assert png_file_path.suffix == ".png", repr(png_file_path)
    assert png_file_path.parent.is_dir(), repr(png_file_path)
    if illustrate_function is not None:
        assert callable(illustrate_function), repr(illustrate_function)
    assert isinstance(keep_site_comments, bool), repr(keep_site_comments)
    assert isinstance(keep_tags, bool), repr(keep_tags)
    assert isinstance(lilypond_flags, str), repr(lilypond_flags)
    assert isinstance(preview, bool), repr(preview)
    assert isinstance(resolution, int | type(None)), repr(resolution)
    if "tags" in illustrate_keywords:
        raise Exception("change tags=False to keep_tags=False")
    ly_file_path = png_file_path.with_suffix(".ly")
    abjad_format_time = as_ly(
        argument,
        ly_file_path,
        illustrate_function=illustrate_function,
        keep_site_comments=keep_site_comments,
        keep_tags=keep_tags,
        **illustrate_keywords,
    )
    original_directory = ly_file_path.parent
    original_ly_file_path = ly_file_path
    temporary_directory = pathlib.Path(tempfile.mkdtemp())
    temporary_ly_file_path = temporary_directory / ly_file_path.name
    shutil.copy(original_ly_file_path, temporary_ly_file_path)
    if preview:
        lilypond_flags += " -dpreview"
    if resolution:
        lilypond_flags += f" -dresolution={resolution}"
    with _contextmanagers.Timer() as timer:
        exit_code = _io.run_lilypond(temporary_ly_file_path, flags=lilypond_flags)
    lilypond_render_time = timer.elapsed_time
    png_file_paths = []
    for file_name in os.listdir(temporary_directory):
        if not file_name.endswith(".png"):
            continue
        source_png_file_path = temporary_directory / file_name
        target_png_file_path = original_directory / file_name
        shutil.move(source_png_file_path, target_png_file_path)
        png_file_paths.append(target_png_file_path)
    shutil.rmtree(temporary_directory)
    if 1 < len(png_file_paths):
        _png_page_pattern = re.compile(r".+page(\d+)\.png")

        def _key(path):
            match = _png_page_pattern.match(str(path))
            assert match is not None
            group = match.groups()[0]
            return group

        png_file_paths.sort(key=_key)
    return (
        tuple(png_file_paths),
        abjad_format_time,
        lilypond_render_time,
        exit_code,
    )
