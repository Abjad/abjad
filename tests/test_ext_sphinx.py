import pathlib
import re
import shutil

import pytest
from uqbar.strings import normalize


@pytest.fixture
def rm_dirs(app):
    path = pathlib.Path(app.doctreedir)
    shutil.rmtree(path)
    yield


@pytest.mark.sphinx("html", testroot="ext-sphinx")
def test_ext_sphinx_01(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()
    images_path = pathlib.Path(app.outdir) / "_images"
    assert sorted(path.name for path in images_path.iterdir()) == [
        "lilypond-962a34d48cf88ba5fbae0978ded1d96422cab4c774de3d31f4e0efcd0043ebfa.cropped.svg",
        "lilypond-962a34d48cf88ba5fbae0978ded1d96422cab4c774de3d31f4e0efcd0043ebfa.ly",
        "lilypond-962a34d48cf88ba5fbae0978ded1d96422cab4c774de3d31f4e0efcd0043ebfa.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-1.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-2.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-3.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-4.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3.cropped.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3.ly",
    ]
    index_path = pathlib.Path(app.srcdir) / "_build" / "html" / "index.html"
    index_source = index_path.read_text()
    assert re.findall(r"lilypond-\w{64}(?:-\d+|.cropped)?\.svg", index_source) == [
        # default
        "lilypond-962a34d48cf88ba5fbae0978ded1d96422cab4c774de3d31f4e0efcd0043ebfa.cropped.svg",
        # :no-trim:
        "lilypond-962a34d48cf88ba5fbae0978ded1d96422cab4c774de3d31f4e0efcd0043ebfa.svg",
        # default
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3.cropped.svg",
        # :no-trim:
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-1.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-2.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-3.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-4.svg",
        # :pages: 2-3,1
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-2.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-3.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-1.svg",
        # :with-columns: 2 (image url appears twice)
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-1.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-1.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-2.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-2.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-3.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-3.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-4.svg",
        "lilypond-cfc32183cc179d7ad77c45f06c8db2fe17a46059a5d8d3b0e0291523c33578f3-4.svg",
    ]


@pytest.mark.sphinx("text", testroot="ext-sphinx")
def test_ext_sphinx_02(app, status, warning, rm_dirs):
    app.build()
    assert not warning.getvalue().strip()
    index_path = pathlib.Path(app.srcdir) / "_build" / "text" / "index.txt"
    assert normalize(index_path.read_text()) == normalize(
        r"""
        Fake Docs
        *********

        This will show the cropped version of the staff:

           >>> staff = abjad.Staff("c' d' e' f'")
           >>> abjad.show(staff)

           \version "2.19.83"  %! abjad.LilyPondFile._get_format_pieces()
           \language "english" %! abjad.LilyPondFile._get_format_pieces()

           #(ly:set-option 'relative-includes #t)

           \include "default.ily" %! abjad.LilyPondFile._get_formatted_includes()

           \score { %! abjad.LilyPondFile._get_formatted_blocks()
               \new Staff
               {
                   c'4
                   d'4
                   e'4
                   f'4
               }
           } %! abjad.LilyPondFile._get_formatted_blocks()

        This will show the uncropped version of the staff:

           >>> abjad.show(staff)

           \version "2.19.83"  %! abjad.LilyPondFile._get_format_pieces()
           \language "english" %! abjad.LilyPondFile._get_format_pieces()

           #(ly:set-option 'relative-includes #t)

           \include "default.ily" %! abjad.LilyPondFile._get_formatted_includes()

           \score { %! abjad.LilyPondFile._get_formatted_blocks()
               \new Staff
               {
                   c'4
                   d'4
                   e'4
                   f'4
               }
           } %! abjad.LilyPondFile._get_formatted_blocks()

        This will show the single-SVG cropped version of the 4-page staff:

           >>> multipage_staff = abjad.Staff("c'1 d'1 e'1 f'1")
           >>> for note in multipage_staff:
           ...     page_break = abjad.LilyPondLiteral(r"\pageBreak", format_slot="after")
           ...     abjad.attach(page_break, note)
           ...
           >>> abjad.show(multipage_staff)

           \version "2.19.83"  %! abjad.LilyPondFile._get_format_pieces()
           \language "english" %! abjad.LilyPondFile._get_format_pieces()

           #(ly:set-option 'relative-includes #t)

           \include "default.ily" %! abjad.LilyPondFile._get_formatted_includes()

           \score { %! abjad.LilyPondFile._get_formatted_blocks()
               \new Staff
               {
                   c'1
                   \pageBreak
                   d'1
                   \pageBreak
                   e'1
                   \pageBreak
                   f'1
                   \pageBreak
               }
           } %! abjad.LilyPondFile._get_formatted_blocks()

        This will show four individual pages, because there is no single SVG
        for uncropped output for the 4-page staff:

           >>> abjad.show(multipage_staff)

           \version "2.19.83"  %! abjad.LilyPondFile._get_format_pieces()
           \language "english" %! abjad.LilyPondFile._get_format_pieces()

           #(ly:set-option 'relative-includes #t)

           \include "default.ily" %! abjad.LilyPondFile._get_formatted_includes()

           \score { %! abjad.LilyPondFile._get_formatted_blocks()
               \new Staff
               {
                   c'1
                   \pageBreak
                   d'1
                   \pageBreak
                   e'1
                   \pageBreak
                   f'1
                   \pageBreak
               }
           } %! abjad.LilyPondFile._get_formatted_blocks()

        This will show pages 2, 3 and 1 of the 4-page staff:

           >>> abjad.show(multipage_staff)

           \version "2.19.83"  %! abjad.LilyPondFile._get_format_pieces()
           \language "english" %! abjad.LilyPondFile._get_format_pieces()

           #(ly:set-option 'relative-includes #t)

           \include "default.ily" %! abjad.LilyPondFile._get_formatted_includes()

           \score { %! abjad.LilyPondFile._get_formatted_blocks()
               \new Staff
               {
                   c'1
                   \pageBreak
                   d'1
                   \pageBreak
                   e'1
                   \pageBreak
                   f'1
                   \pageBreak
               }
           } %! abjad.LilyPondFile._get_formatted_blocks()

        This will show all four pages, in a 2x2 grid:

           >>> abjad.show(multipage_staff)

           \version "2.19.83"  %! abjad.LilyPondFile._get_format_pieces()
           \language "english" %! abjad.LilyPondFile._get_format_pieces()

           #(ly:set-option 'relative-includes #t)

           \include "default.ily" %! abjad.LilyPondFile._get_formatted_includes()

           \score { %! abjad.LilyPondFile._get_formatted_blocks()
               \new Staff
               {
                   c'1
                   \pageBreak
                   d'1
                   \pageBreak
                   e'1
                   \pageBreak
                   f'1
                   \pageBreak
               }
           } %! abjad.LilyPondFile._get_formatted_blocks()
        """
    )
